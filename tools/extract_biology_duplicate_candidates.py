#!/usr/bin/env python3
"""Extract explainable Biology duplicate candidates from a SQLite bank without changing the bank."""
from __future__ import annotations

import argparse
import collections
import itertools
import json
import re
import sqlite3
import unicodedata
from pathlib import Path

STOP = {"از", "به", "در", "با", "که", "را", "و", "یا", "برای", "است", "هست", "این", "آن", "یک", "شد", "های"}
TOKEN = re.compile(r"[\u0600-\u06ffA-Za-z0-9]+")
SPACE = re.compile(r"\s+")


def norm(value: object) -> str:
    return SPACE.sub(" ", unicodedata.normalize("NFKC", str(value or "")).replace("ي", "ی").replace("ك", "ک")).strip().casefold()


def words(value: object) -> set[str]:
    return {token for token in TOKEN.findall(norm(value)) if len(token) > 1 and token not in STOP}


def similarity(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left and right else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("db", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    con = sqlite3.connect(args.db)
    rows = []
    for qid, full_json in con.execute("SELECT id, full_json FROM question WHERE subject='زیست' ORDER BY id"):
        q = json.loads(full_json)
        if q.get("access_pool") == "QUARANTINE" or q.get("obsolete_for_1405"):
            continue
        rows.append(q)
    con.close()
    by_stem: dict[str, list[dict]] = collections.defaultdict(list)
    by_options: dict[str, list[dict]] = collections.defaultdict(list)
    for q in rows:
        by_stem[norm(q.get("stem"))].append(q)
        by_options["\x1f".join(norm(item) for item in q.get("options", []))].append(q)
    exact_stem = []
    same_options = []
    for grouping, label, target in ((by_stem, "EXACT_STEM", exact_stem), (by_options, "IDENTICAL_OPTION_SET", same_options)):
        for signature, members in grouping.items():
            if len(members) < 2:
                continue
            for left, right in itertools.combinations(members, 2):
                target.append({"kind": label, "left": left["id"], "right": right["id"], "signature": signature})
    exact_stem.sort(key=lambda row: (row["left"], row["right"]))
    same_options.sort(key=lambda row: (row["left"], row["right"]))
    # Cosmetic candidates require substantially similar stem and option wording, not a merely generic shared prompt.
    near = []
    vocab = {q["id"]: words(str(q.get("stem", "")) + " " + " ".join(q.get("options", []))) for q in rows}
    exact_pairs = {(r["left"], r["right"]) for r in exact_stem + same_options}
    for left, right in itertools.combinations(rows, 2):
        pair = (left["id"], right["id"])
        if pair in exact_pairs:
            continue
        stem_score = similarity(words(left.get("stem")), words(right.get("stem")))
        all_score = similarity(vocab[left["id"]], vocab[right["id"]])
        if stem_score >= 0.72 and all_score >= 0.65:
            near.append({"kind": "NEAR_OR_COSMETIC", "left": pair[0], "right": pair[1], "stem_jaccard": round(stem_score, 4), "content_jaccard": round(all_score, 4)})
    near.sort(key=lambda row: (-row["content_jaccard"], -row["stem_jaccard"], row["left"], row["right"]))
    data = {
        "method": "Exact normalized stem; exact normalized option set; and high-threshold lexical cosmetic candidate. Every candidate requires semantic adjudication; this extractor never deletes or merges questions.",
        "subject": "زیست",
        "population": len(rows),
        "counts": {"exact_stem_pairs": len(exact_stem), "identical_option_set_pairs": len(same_options), "near_or_cosmetic_pairs": len(near)},
        "exact_stem_pairs": exact_stem,
        "identical_option_set_pairs": same_options,
        "near_or_cosmetic_pairs": near,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
