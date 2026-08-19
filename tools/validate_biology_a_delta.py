#!/usr/bin/env python3
"""Validate the W03 Biology-A successor-bank delta against the frozen source bank."""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path

RAW_ENUMS = re.compile(r"\b(?:condition_wrong|wrong_condition|truth_partial|partial_truth|truth_false|false_truth|truth_true|true_truth|condition_true|true_condition|overgeneralization|unknown|not_reviewed)\b", re.I)
GENERIC = ("به دام گزینه", "کلمه کلیدی", "کنترل کنید", "دام سوال", "از کلیدواژه جواب نده", "شرح بالا")


def qmap(path: Path) -> tuple[str, dict[str, dict]]:
    con = sqlite3.connect(path)
    integrity = con.execute("PRAGMA integrity_check").fetchone()[0]
    rows = {row[0]: json.loads(row[1]) for row in con.execute("SELECT id, full_json FROM question")}
    con.close()
    return integrity, rows


def text(q: dict) -> str:
    return " ".join([str(q.get("stem", "")), *(str(x) for x in q.get("options", [])), str(q.get("correct_analysis", "")), *(str(x) for x in (q.get("distractor_analyses") or {}).values())])


def meaningful(value: object) -> bool:
    value = str(value or "").strip()
    return len(value) >= 24 and not RAW_ENUMS.search(value) and not any(token in value for token in GENERIC)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("assignment", type=Path)
    parser.add_argument("audit", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    baseline_integrity, baseline = qmap(args.base)
    candidate_integrity, candidate = qmap(args.candidate)
    assignment = json.loads(args.assignment.read_text(encoding="utf-8"))["deterministic_assignment"]
    assigned = set(assignment["w03_bio_a_ids"])
    w04 = set(assignment["w04_bio_b_ids"])
    audit = json.loads(args.audit.read_text(encoding="utf-8"))

    failures: dict[str, object] = {}
    if baseline_integrity != "ok" or candidate_integrity != "ok":
        failures["sqlite_integrity"] = {"baseline": baseline_integrity, "candidate": candidate_integrity}
    if set(baseline) != set(candidate) or len(candidate) != 1216:
        failures["id_set"] = {"baseline": len(baseline), "candidate": len(candidate), "intersection": len(set(baseline) & set(candidate))}
    changed = {qid for qid in baseline if baseline[qid] != candidate[qid]}
    if changed != assigned:
        failures["changed_id_boundary"] = {"changed_not_assigned": sorted(changed - assigned), "assigned_not_changed": sorted(assigned - changed)}
    key_changed = [qid for qid in assigned if baseline[qid].get("correct_index") != candidate[qid].get("correct_index")]
    if key_changed:
        failures["key_changes"] = key_changed
    structural = []
    leaked = []
    nonmeaningful = []
    source_contract = []
    for qid in assigned:
        q = candidate[qid]
        if q.get("id") != qid or q.get("subject") != "زیست" or not isinstance(q.get("options"), list) or len(q["options"]) != 4 or any(not str(x).strip() for x in q["options"]) or q.get("correct_index") not in range(4):
            structural.append(qid)
        if RAW_ENUMS.search(text(q)):
            leaked.append(qid)
        if not meaningful(q.get("correct_analysis")) or any(not meaningful((q.get("distractor_analyses") or {}).get(str(i))) for i in range(4)):
            nonmeaningful.append(qid)
        for key in ("source_type", "access_pool", "runtime_scope_status", "eligible_for_training", "eligible_for_safety_evidence", "needs_human_review", "obsolete_for_1405"):
            if baseline[qid].get(key) != q.get(key):
                source_contract.append({"id": qid, "field": key})
    if structural:
        failures["structure"] = structural
    if leaked:
        failures["raw_enum_leakage"] = leaked
    if nonmeaningful:
        failures["nonmeaningful_analysis"] = nonmeaningful
    if source_contract:
        failures["source_access_contract"] = source_contract
    if set(assigned) & w04 or len(assigned) != len(w04) or len(assigned | w04) != 290:
        failures["assignment_partition"] = {"w03": len(assigned), "w04": len(w04), "overlap": sorted(assigned & w04)}
    if audit["summary"]["key_changes"] != 0 or audit["summary"]["items_reviewed"] != 145:
        failures["audit_summary"] = audit["summary"]

    output = {
        "status": "PASS" if not failures else "FAIL",
        "baseline_integrity": baseline_integrity,
        "candidate_integrity": candidate_integrity,
        "total_ids": len(candidate),
        "assigned_ids": len(assigned),
        "changed_ids": len(changed),
        "unassigned_ids_byte_equivalent": len(changed - assigned) == 0,
        "key_changes": len(key_changed),
        "raw_enum_leaks_in_assigned": len(leaked),
        "nonmeaningful_analysis_in_assigned": len(nonmeaningful),
        "w03_w04_overlap": len(assigned & w04),
        "failures": failures,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
