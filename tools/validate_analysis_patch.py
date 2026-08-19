#!/usr/bin/env python3
"""Validate compact analysis-only Biology/Geology patch contracts.

This validator intentionally does not infer or modify question options, keys,
stems, source metadata, IDs, holdout membership, or bank hashes. It checks only
that each update is explicitly keyed by a stable ID and contains complete,
question-specific analysis fields when those fields are supplied.
"""
import json
import re
import sys
from pathlib import Path

RAW_ENUM = re.compile(r"\b(?:condition_wrong|truth_partial|truth_correct|wrong_option|correct_option|wrong_condition|partial_truth|calculation_trap|unit_error|direction_error)\b")
VAGUE = re.compile(r"(?:این تعریف|این مورد|این فرایند|این حالت|این ویژگی|این بخش)")


def norm(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def main(path):
    data = json.loads(Path(path).read_text())
    assert isinstance(data, dict), "patch root must be an object"
    updates = data.get("updates")
    assert isinstance(updates, list) and updates, "patch must contain non-empty updates list"
    seen = set()
    failures = []
    analysis_records = 0
    for index, update in enumerate(updates):
        if not isinstance(update, dict):
            failures.append((index, "update is not an object"))
            continue
        qid = norm(update.get("id"))
        fields = update.get("fields")
        if not qid:
            failures.append((index, "missing stable id"))
        if qid in seen:
            failures.append((qid, "duplicate update id"))
        seen.add(qid)
        if not isinstance(fields, dict) or not fields:
            failures.append((qid, "missing fields object"))
            continue
        forbidden = set(fields) & {"stem", "options", "correct_index", "source_type", "access_pool", "official_key_verified", "needs_human_review", "eligible_for_safety_evidence"}
        if forbidden:
            failures.append((qid, f"non-analysis fields supplied: {sorted(forbidden)}"))
        if any(k in fields for k in ("correct_analysis", "distractor_analyses", "short_lesson", "fast_method", "main_trap")):
            analysis_records += 1
        ca = norm(fields.get("correct_analysis"))
        if "correct_analysis" in fields and len(ca) < 35:
            failures.append((qid, "correct_analysis shorter than 35 characters"))
        da = fields.get("distractor_analyses")
        if "distractor_analyses" in fields:
            if not isinstance(da, dict) or any(not norm(da.get(str(i))) for i in range(4)):
                failures.append((qid, "distractor_analyses must contain non-empty keys 0..3"))
        combined = " ".join(norm(fields.get(k)) for k in ("correct_analysis", "distractor_analyses", "short_lesson", "fast_method", "main_trap"))
        if RAW_ENUM.search(combined):
            failures.append((qid, "raw internal enum in learner-facing analysis"))
        if VAGUE.search(combined):
            failures.append((qid, "vague referent requires subject-level wording review"))
    print(json.dumps({"patch": str(path), "updates": len(updates), "analysis_records": analysis_records, "unique_ids": len(seen), "failures": failures}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
