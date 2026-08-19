#!/usr/bin/env python3
"""Read-only, schema-aware structural and quality scan for the frozen Chemistry bank."""
from __future__ import annotations

import json
import re
import sqlite3
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: scan_chemistry_bank.py DB_PATH OUTPUT_JSON")

db_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])

def normalize(value: str, mask_numbers: bool = False) -> str:
    value = unicodedata.normalize("NFKC", value or "")
    value = value.replace("ي", "ی").replace("ك", "ک")
    if mask_numbers:
        value = re.sub(r"(?<!\w)[+-]?(?:\d+(?:[.,/]\d+)?|[a-zA-Z])(?!(?:\w))", "#", value)
    value = re.sub(r"[^\w]+", " ", value.lower(), flags=re.UNICODE)
    return " ".join(value.split())

def normalize_option(value: str) -> str:
    """Normalize answer text while preserving mathematical and ionic charge signs."""
    value = unicodedata.normalize("NFKC", value or "")
    value = value.replace("ي", "ی").replace("ك", "ک").replace("−", "-").replace("–", "-")
    return re.sub(r"\s+", "", value).casefold()


def item_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("text", "label", "value", "content"):
            if isinstance(value.get(key), str):
                return value[key]
        return " ".join(item_text(v) for v in value.values())
    return str(value)

def answer_text(options: list[str], index: object) -> str:
    if isinstance(index, int) and 0 <= index < len(options):
        return options[index]
    return ""

conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
conn.row_factory = sqlite3.Row
integrity = conn.execute("PRAGMA quick_check").fetchone()[0]
columns = [r[1] for r in conn.execute("PRAGMA table_info(question)")]
rows = conn.execute("SELECT * FROM question WHERE subject=? ORDER BY priority DESC, id", ("شیمی",)).fetchall()

records: list[dict] = []
for row in rows:
    q = json.loads(row["full_json"])
    options = [item_text(x) for x in (q.get("options") or [])]
    distractors = q.get("distractor_analyses") or {}
    record = {
        "id": row["id"],
        "source_type": row["source_type"],
        "access_pool": row["access_pool"],
        "microtopic": row["microtopic"],
        "priority": row["priority"],
        "difficulty": row["difficulty"],
        "question_form": row["question_form"],
        "selected_scope": bool(row["selected_scope"]),
        "obsolete": bool(row["obsolete"]),
        "correct_index": q.get("correct_index", row["correct_index"]),
        "stem": q.get("stem") or "",
        "options": options,
        "correct_analysis": q.get("correct_analysis") or "",
        "distractor_analyses": {str(k): item_text(v) for k, v in distractors.items()},
        "review_default": q.get("review_default") or {},
        "short_lesson": q.get("short_lesson") or "",
        "fast_method": q.get("fast_method") or "",
        "start_method": q.get("start_method") or "",
        "calculation_required": bool(q.get("calculation_required")),
        "needs_human_review": bool(q.get("needs_human_review")),
        "eligible_for_safety_evidence": bool(q.get("eligible_for_safety_evidence")),
        "teaching_ladder_level": q.get("teaching_ladder_level"),
        "textbook_refs": q.get("textbook_refs") or [],
        "source_file": q.get("source_file"),
        "source_page": q.get("source_page"),
        "semantic_fingerprint": q.get("semantic_fingerprint"),
        "stem_template_id": q.get("stem_template_id"),
        "scenario_model": q.get("scenario_model"),
        "scenario_variant": q.get("scenario_variant"),
        "raw": q,
    }
    record["correct_option"] = answer_text(options, record["correct_index"])
    record["signature_exact"] = normalize(record["stem"]) + " || " + " | ".join(normalize(x) for x in options)
    record["signature_numeric_masked"] = normalize(record["stem"], True) + " || " + " | ".join(normalize(x, True) for x in options)
    records.append(record)

issues: dict[str, list[str]] = defaultdict(list)
for r in records:
    texts = [r["correct_analysis"], r["short_lesson"], r["fast_method"], r["start_method"]] + list(r["distractor_analyses"].values())
    review_text = json.dumps(r["review_default"], ensure_ascii=False)
    if len(r["options"]) != 4:
        issues["not_four_options"].append(r["id"])
    if any(not option.strip() for option in r["options"]):
        issues["blank_option"].append(r["id"])
    if len({normalize_option(option) for option in r["options"]}) != len(r["options"]):
        issues["duplicate_options"].append(r["id"])
    if not isinstance(r["correct_index"], int) or not 0 <= r["correct_index"] < len(r["options"]):
        issues["invalid_correct_index"].append(r["id"])
    if len(r["correct_analysis"].strip()) < 70:
        issues["short_correct_analysis"].append(r["id"])
    if any(len(t.strip()) < 30 for t in r["distractor_analyses"].values()):
        issues["short_distractor_analysis"].append(r["id"])
    if re.search(r"\b(condition_wrong|truth_partial|wrong_condition|partial_truth)\b", review_text, re.I):
        issues["raw_internal_enum_in_review"].append(r["id"])
    generic_markers = ("از کلیدواژه جواب نده", "روش کنترل:", "صورت را به بخش های مستقل", "صورت را به بخش‌های مستقل")
    if any(marker in text for marker in generic_markers for text in texts):
        issues["generic_solution_template_marker"].append(r["id"])
    if r["calculation_required"] and not any(token in (r["correct_analysis"] + " " + r["fast_method"]) for token in ("=", "مول", "mol", "M", "گرم", "L", "لیتر", "mL", "جرم")):
        issues["calculation_without_explicit_path_or_unit"].append(r["id"])

by_exact: dict[str, list[str]] = defaultdict(list)
by_masked: dict[str, list[str]] = defaultdict(list)
by_fingerprint: dict[str, list[str]] = defaultdict(list)
for r in records:
    by_exact[r["signature_exact"]].append(r["id"])
    by_masked[r["signature_numeric_masked"]].append(r["id"])
    if r["semantic_fingerprint"]:
        by_fingerprint[r["semantic_fingerprint"]].append(r["id"])

def groups(mapping: dict[str, list[str]]) -> list[dict]:
    return [
        {"ids": ids, "example_stem": next(x["stem"] for x in records if x["id"] == ids[0])}
        for _, ids in sorted(mapping.items()) if len(ids) > 1
    ]

high_roi = [r for r in records if r["access_pool"] == "TRAIN" and r["selected_scope"] and not r["obsolete"]]
high_roi.sort(key=lambda r: (-float(r["priority"]), r["microtopic"], r["id"]))
record_fields = (
    "id", "source_type", "access_pool", "microtopic", "priority", "difficulty", "question_form", "correct_index", "stem", "options", "correct_option", "correct_analysis", "distractor_analyses", "review_default", "short_lesson", "fast_method", "start_method", "calculation_required", "needs_human_review", "eligible_for_safety_evidence", "teaching_ladder_level", "textbook_refs", "source_file", "source_page", "stem_template_id", "scenario_model", "scenario_variant",
)
report = {
    "database": str(db_path),
    "quick_check": integrity,
    "question_columns": columns,
    "chemistry_total": len(records),
    "counts": {
        "source_type": dict(sorted(Counter(r["source_type"] for r in records).items())),
        "microtopic": dict(sorted(Counter(r["microtopic"] for r in records).items())),
        "access_pool": dict(sorted(Counter(r["access_pool"] for r in records).items())),
        "high_roi_train_selected": len(high_roi),
        "calculation_required": sum(r["calculation_required"] for r in records),
        "needs_human_review": sum(r["needs_human_review"] for r in records),
    },
    "issues": {k: sorted(v) for k, v in sorted(issues.items())},
    "exact_question_duplicate_groups": groups(by_exact),
    "numeric_variant_candidate_groups": groups(by_masked),
    "semantic_fingerprint_duplicate_groups": groups(by_fingerprint),
    "high_roi_questions": [{k: r[k] for k in record_fields} for r in high_roi],
}
out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({
    "quick_check": integrity,
    "chemistry_total": len(records),
    "high_roi_train_selected": len(high_roi),
    "calculation_required": report["counts"]["calculation_required"],
    "needs_human_review": report["counts"]["needs_human_review"],
    "issue_counts": {k: len(v) for k, v in sorted(issues.items())},
    "exact_duplicate_groups": len(report["exact_question_duplicate_groups"]),
    "numeric_variant_candidate_groups": len(report["numeric_variant_candidate_groups"]),
    "semantic_fingerprint_duplicate_groups": len(report["semantic_fingerprint_duplicate_groups"]),
}, ensure_ascii=False, indent=2))
