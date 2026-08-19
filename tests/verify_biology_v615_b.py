#!/usr/bin/env python3
"""Validate the deterministic W04 Biology overlay against the frozen V6.1 bank."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from pathlib import Path

BASE_SHA256 = "d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c"
PATCH_NAME = "biology_v620_w04_patch.json"
MANUAL_REPAIRS = {
    "v3_bio_10_11", "v3_bio_11_07", "v3_bio_11_24", "v3_bio_12_07", "v3_bio_13_15",
    "v3_bio_14_10", "v3_bio_14_20", "v3_bio_15_15", "v3_bio_15_24", "v3_bio_16_10", "v3_bio_16_16",
}
MISSING_REFERENCE_REPAIRS = MANUAL_REPAIRS - {"v3_bio_13_15"}
FORBIDDEN = (
    "condition_wrong", "truth_partial", "wrong_condition", "partial_truth", "overgeneralization",
    "calculation_trap", "unit_mistake", "keyword", "کلیدواژه", "دام مفهومی", "روش کنترل",
    "از کلیدواژه جواب نده", "این گزینه با همهٔ شرط‌ها سازگار است",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: verify_biology_v615_b.py /path/to/radiology1405_bank_v6_1.db")
    database = Path(sys.argv[1])
    patch_path = Path(__file__).resolve().parents[1] / "app/src/main/assets" / PATCH_NAME
    if not database.is_file():
        fail(f"bank not found: {database}")
    if sha256(database) != BASE_SHA256:
        fail("frozen expanded-bank SHA-256 mismatch")
    patch = json.loads(patch_path.read_text(encoding="utf-8"))
    if patch.get("base_db_sha256") != BASE_SHA256:
        fail("patch base SHA-256 mismatch")
    updates = patch.get("updates")
    if not isinstance(updates, list) or len(updates) != 145:
        fail("update count is not exactly 145")

    conn = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    if conn.execute("PRAGMA quick_check").fetchone()[0] != "ok":
        fail("frozen database quick_check failed")
    eligible = conn.execute(
        """
        SELECT * FROM question
        WHERE subject='زیست' AND source_type='authored' AND access_pool='TRAIN'
          AND obsolete=0 AND runtime_scope_status IN ('A_CORE_FULL', 'B_RAPID_EXPOSURE')
        ORDER BY id
        """
    ).fetchall()
    if len(eligible) != 290:
        fail(f"expected 290 deterministic Biology split candidates, found {len(eligible)}")
    w03_ids = [row["id"] for row in eligible[:145]]
    w04_ids = [row["id"] for row in eligible[145:]]
    update_ids = [update.get("id") for update in updates]
    if update_ids != w04_ids or patch.get("rewritten_analysis_ids") != w04_ids:
        fail("updates do not exactly equal lexicographic W04 positions 146..290")
    if set(update_ids) & set(w03_ids):
        fail("W04 overlap with W03 positions 1..145")
    if patch.get("manual_completeness_repairs") != sorted(MANUAL_REPAIRS):
        fail("manual completeness-repair manifest mismatch")

    row_by_id = {row["id"]: row for row in eligible}
    stem_repairs = set()
    option_repairs = set()
    for update in updates:
        question_id = update["id"]
        row = row_by_id[question_id]
        original = json.loads(row["full_json"])
        if update.get("source_type") != "authored":
            fail(f"source-type guard missing: {question_id}")
        fields = update.get("fields")
        allowed = {"stem", "options", "correct_analysis", "distractor_analyses", "short_lesson"}
        if not isinstance(fields, dict) or not set(fields) <= allowed:
            fail(f"unsupported identity-bearing field: {question_id}")
        if not {"correct_analysis", "distractor_analyses", "short_lesson"} <= set(fields):
            fail(f"missing required analysis field: {question_id}")
        if "stem" in fields:
            stem_repairs.add(question_id)
        if "options" in fields:
            option_repairs.add(question_id)
        if ("stem" in fields or "options" in fields) and question_id not in MANUAL_REPAIRS:
            fail(f"unapproved material-field change: {question_id}")
        options = fields.get("options", original.get("options"))
        if not isinstance(options, list) or len(options) != 4 or any(not str(value).strip() for value in options):
            fail(f"invalid post-patch options: {question_id}")
        if original.get("correct_index") not in range(4):
            fail(f"invalid immutable base key: {question_id}")
        analyses = fields["distractor_analyses"]
        if set(analyses) != {"0", "1", "2", "3"}:
            fail(f"not exactly four option analyses: {question_id}")
        texts = [fields["correct_analysis"], fields["short_lesson"], *analyses.values()]
        if any(not isinstance(text, str) or len(text.strip()) < 45 for text in texts):
            fail(f"missing or too-short scientific explanation: {question_id}")
        combined = " ".join(texts).casefold()
        if any(marker.casefold() in combined for marker in FORBIDDEN):
            fail(f"generic filler or raw enum leakage: {question_id}")
    if stem_repairs != MISSING_REFERENCE_REPAIRS:
        fail(f"unexpected stem-repair set: {sorted(stem_repairs)}")
    if option_repairs != {"v3_bio_11_24", "v3_bio_13_15", "v3_bio_14_20", "v3_bio_15_24", "v3_bio_16_16"}:
        fail(f"unexpected option-repair set: {sorted(option_repairs)}")

    update_by_id = {update["id"]: update for update in updates}
    for question_id in MISSING_REFERENCE_REPAIRS:
        stem = update_by_id[question_id]["fields"]["stem"]
        if "A و B" in stem or "جدول" in stem:
            fail(f"incomplete visual/statement reference remains active: {question_id}")
    if not update_by_id["v3_bio_13_15"]["fields"]["options"][3].startswith("پادتن با اتصال اختصاصی"):
        fail("immune causal-chain repair did not restore correct direction")
    conn.close()
    print("PASS: 145 disjoint W04 Biology updates validate against immutable V6.1 base")
    print("PASS: W03/W04 split is exactly 145/145 with no overlap")
    print("PASS: ten incomplete A/B-or-table references and one immune causal chain have explicit repairs")
    print(f"PATCH_SHA256={sha256(patch_path)}")


if __name__ == "__main__":
    main()
