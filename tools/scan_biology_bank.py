#!/usr/bin/env python3
"""Deterministic machine scan for the active Biology subset of a Konkur SQLite bank."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sqlite3
import unicodedata
from itertools import combinations
from pathlib import Path

PERSIAN_STOP = {
    "از", "به", "در", "با", "که", "را", "و", "یا", "برای", "است", "هست", "این", "آن", "یک", "شد", "می", "های",
}
GENERIC_PHRASES = (
    "به دام گزینه", "کلمه کلیدی", "کنترل کنید", "دام سوال", "با دقت بخوانید", "عبارت را بررسی کنید",
)
RAW_ENUMS = re.compile(r"\b(?:condition_wrong|wrong_condition|truth_partial|partial_truth|truth_false|false_truth|truth_true|true_truth|condition_true|true_condition|overgeneralization|unknown|not_reviewed)\b", re.I)
WHITESPACE = re.compile(r"\s+")
TOKEN = re.compile(r"[\u0600-\u06ffA-Za-z0-9]+")


def clean(value: object) -> str:
    raw = unicodedata.normalize("NFKC", str(value or "")).replace("ي", "ی").replace("ك", "ک")
    return WHITESPACE.sub(" ", raw).strip()


def normalized(value: object) -> str:
    return clean(value).casefold()


def tokens(value: object) -> set[str]:
    return {token for token in TOKEN.findall(normalized(value)) if len(token) > 1 and token not in PERSIAN_STOP}


def question_text(question: dict) -> str:
    return " ".join([clean(question.get("stem")), *(clean(x) for x in question.get("options", []))])


def ngrams(words: set[str]) -> set[str]:
    return words


def field(question: dict, name: str, default=None):
    return question.get(name, default)


def priority_key(question: dict) -> tuple:
    priority = question.get("priority", 0)
    try:
        priority = float(priority)
    except (TypeError, ValueError):
        priority = 0.0
    final_hours = 1 if question.get("runtime_scope_status") == "A_CORE_FULL" else 0
    safety = 1 if question.get("eligible_for_safety_evidence") is True else 0
    return (-final_hours, -safety, -priority, str(question.get("id", "")))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("db", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    con = sqlite3.connect(args.db)
    con.row_factory = sqlite3.Row
    integrity = con.execute("PRAGMA integrity_check").fetchone()[0]
    rows = list(con.execute("SELECT id, full_json FROM question ORDER BY id"))
    all_ids = [row["id"] for row in rows]
    questions = []
    invalid_json = []
    for row in rows:
        try:
            question = json.loads(row["full_json"])
            if question.get("id") != row["id"]:
                invalid_json.append({"row_id": row["id"], "json_id": question.get("id")})
            questions.append(question)
        except json.JSONDecodeError as exc:
            invalid_json.append({"row_id": row["id"], "error": str(exc)})
    biology = [q for q in questions if clean(q.get("subject")) == "زیست"]

    issues: dict[str, list] = collections.defaultdict(list)
    exact: dict[str, list[str]] = collections.defaultdict(list)
    quality_flags: dict[str, list[str]] = {}

    for question in biology:
        qid = question.get("id")
        opts = question.get("options")
        analyses = question.get("distractor_analyses") or {}
        flags: list[str] = []
        if not isinstance(opts, list) or len(opts) != 4 or any(not clean(opt) for opt in (opts or [])):
            issues["bad_options"].append(qid)
        if isinstance(opts, list) and len({normalized(x) for x in opts}) != len(opts):
            issues["duplicate_option_text"].append(qid)
        if not isinstance(question.get("correct_index"), int) or question.get("correct_index") not in range(4):
            issues["bad_correct_index"].append(qid)
        if not clean(question.get("stem")):
            issues["empty_stem"].append(qid)
        if not clean(question.get("correct_analysis")):
            issues["missing_correct_analysis"].append(qid)
        if any(not clean(analyses.get(str(idx))) for idx in range(4)):
            issues["missing_option_analysis"].append(qid)
        all_analysis = " ".join([clean(question.get("correct_analysis")), *(clean(analyses.get(str(i))) for i in range(4))])
        generic_matches = [phrase for phrase in GENERIC_PHRASES if phrase in all_analysis]
        if generic_matches:
            issues["generic_analysis_phrase"].append({"id": qid, "matches": generic_matches})
            flags.append("generic_analysis_phrase")
        if RAW_ENUMS.search(question_text(question) + " " + all_analysis):
            issues["raw_internal_enum"].append(qid)
            flags.append("raw_internal_enum")
        if len({normalized(analyses.get(str(i))) for i in range(4)}) < 4:
            issues["repeated_option_analysis"].append(qid)
            flags.append("repeated_option_analysis")
        if len(tokens(question.get("correct_analysis"))) < 8:
            issues["thin_correct_analysis"].append(qid)
            flags.append("thin_correct_analysis")
        if question.get("source_type") == "real_exam":
            needed = [question.get("official_origin") is True, bool(question.get("source_official_origin_evidence")), bool(question.get("exam_year")), bool(question.get("key_provenance")), bool(question.get("textbook_refs")), question.get("obsolete_for_1405") is False]
            if not all(needed):
                issues["real_exam_provenance_incomplete"].append(qid)
        if question.get("source_type") == "quarantined_key_conflict":
            if question.get("access_pool") != "QUARANTINE" or question.get("eligible_for_training") is not False:
                issues["quarantine_contract_failure"].append(qid)
        if question.get("obsolete_for_1405") and question.get("access_pool") != "QUARANTINE":
            issues["obsolete_active"].append(qid)
        fingerprint = hashlib.sha256((normalized(question.get("stem")) + "\x1f" + "\x1f".join(normalized(x) for x in opts or [])).encode("utf-8")).hexdigest()
        exact[fingerprint].append(qid)
        if flags:
            quality_flags[qid] = flags

    exact_duplicates = [sorted(ids) for ids in exact.values() if len(ids) > 1]

    near_candidates: list[dict] = []
    similarity_population = [q for q in biology if q.get("access_pool") != "QUARANTINE" and not q.get("obsolete_for_1405")]
    vectors = {q["id"]: tokens(question_text(q)) for q in similarity_population}
    for left, right in combinations(sorted(vectors), 2):
        a, b = vectors[left], vectors[right]
        if not a or not b:
            continue
        score = len(a & b) / len(a | b)
        if score >= 0.62:
            near_candidates.append({"left": left, "right": right, "jaccard": round(score, 4)})
    near_candidates.sort(key=lambda row: (-row["jaccard"], row["left"], row["right"]))

    active = [q for q in biology if q.get("access_pool") != "QUARANTINE" and not q.get("obsolete_for_1405")]
    audit_eligible = [
        q for q in active
        if q.get("access_pool") == "TRAIN" and q.get("source_type") == "authored" and q.get("runtime_scope_status") in {"A_CORE_FULL", "B_RAPID_EXPOSURE"}
    ]
    audit_by_priority = sorted(audit_eligible, key=priority_key)
    audit_by_stable_id = sorted(audit_eligible, key=lambda q: str(q.get("id", "")))
    split = (len(audit_by_stable_id) + 1) // 2

    payload = {
        "scanner": "scan_biology_bank.py",
        "database": str(args.db),
        "integrity_check": integrity,
        "whole_bank": {"rows": len(rows), "unique_row_ids": len(set(all_ids)), "invalid_json_or_id_mismatch": invalid_json},
        "biology": {
            "total": len(biology),
            "active_nonquarantine_nonobsolete": len(active),
            "by_source_type": dict(collections.Counter(q.get("source_type") for q in biology)),
            "by_access_pool": dict(collections.Counter(q.get("access_pool") for q in biology)),
            "by_scope": dict(collections.Counter(q.get("runtime_scope_status") for q in biology)),
            "machine_issue_counts": {name: len(values) for name, values in sorted(issues.items())},
            "machine_issue_examples": {name: values[:50] for name, values in sorted(issues.items())},
            "exact_duplicate_groups": exact_duplicates,
            "near_duplicate_candidates": near_candidates[:200],
            "quality_flagged_ids": quality_flags,
        },
        "deterministic_assignment": {
            "definition": "Active, non-obsolete, authored Biology TRAIN items with A_CORE_FULL or B_RAPID_EXPOSURE scope; SIM/FINAL holdouts and quarantine are excluded.",
            "eligible_count": len(audit_by_stable_id),
            "priority_preview": [q["id"] for q in audit_by_priority[:50]],
            "stable_order": [q["id"] for q in audit_by_stable_id],
            "split_rule": "Sort eligible IDs lexicographically; W03-BIO-A audits positions 1..ceil(n/2), W04 audits positions ceil(n/2)+1..n.",
            "w03_bio_a_ids": [q["id"] for q in audit_by_stable_id[:split]],
            "w04_bio_b_ids": [q["id"] for q in audit_by_stable_id[split:]],
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "integrity": integrity,
        "whole_rows": len(rows),
        "biology": len(biology),
        "eligible": len(audit_by_stable_id),
        "w03": len(payload["deterministic_assignment"]["w03_bio_a_ids"]),
        "w04": len(payload["deterministic_assignment"]["w04_bio_b_ids"]),
        "issues": payload["biology"]["machine_issue_counts"],
        "exact_duplicate_groups": len(exact_duplicates),
        "near_duplicate_candidates": len(near_candidates),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
