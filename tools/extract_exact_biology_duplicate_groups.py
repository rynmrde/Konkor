#!/usr/bin/env python3
"""Export exact Biology duplicate groups for semantic adjudication; does not mutate the bank."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sqlite3
import unicodedata
from pathlib import Path

SPACE = re.compile(r"\s+")


def norm(value: object) -> str:
    return SPACE.sub(" ", unicodedata.normalize("NFKC", str(value or "")).replace("ي", "ی").replace("ك", "ک")).strip().casefold()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("db", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    con = sqlite3.connect(args.db)
    groups: dict[str, list[dict]] = collections.defaultdict(list)
    for qid, full_json in con.execute("SELECT id, full_json FROM question WHERE subject='زیست' ORDER BY id"):
        q = json.loads(full_json)
        if q.get("access_pool") == "QUARANTINE" or q.get("obsolete_for_1405"):
            continue
        stimulus = dict(q.get("stimulus") or {})
        for key in ("source_crop_data_uri", "source_crop_sha256", "source_crop_asset", "crop_metadata", "source_file", "source_page", "display_contract", "alt_text"):
            stimulus.pop(key, None)
        material = {"stimulus": stimulus, "stem": norm(q.get("stem")), "options": [norm(x) for x in q.get("options", [])]}
        fingerprint = hashlib.sha256(json.dumps(material, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        groups[fingerprint].append(q)
    con.close()
    selected = []
    for fingerprint, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        selected.append({
            "fingerprint": fingerprint,
            "member_count": len(members),
            "members": [{
                "id": q["id"], "microtopic": q.get("microtopic"), "priority": q.get("priority"), "source_type": q.get("source_type"), "access_pool": q.get("access_pool"), "runtime_scope_status": q.get("runtime_scope_status"), "correct_index": q.get("correct_index"), "stem": q.get("stem"), "options": q.get("options"), "correct_analysis": q.get("correct_analysis"), "textbook_refs": q.get("textbook_refs"), "stimulus_type": (q.get("stimulus") or {}).get("type"),
            } for q in members],
        })
    data = {"definition": "Exact normalized stimulus (excluding source-crop transport metadata), stem, and options; every group still requires semantic and session-policy adjudication.", "group_count": len(selected), "member_count": sum(g["member_count"] for g in selected), "groups": selected}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"group_count": data["group_count"], "member_count": data["member_count"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
