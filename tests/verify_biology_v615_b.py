#!/usr/bin/env python3
"""Validate the W04 Biology-B compact analysis overlay against the frozen V6.1 bank."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from pathlib import Path

BASE_SHA256 = "d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c"
EXPECTED_IDS = [
    "v3_bio_01_02", "v3_bio_04_02", "v3_bio_09_02", "v3_bio_07_02",
    "v3_bio_08_02", "v3_bio_12_02", "v3_bio_02_02", "v3_bio_16_02",
    "v3_bio_05_02", "v3_bio_15_02", "v3_bio_11_02", "v3_bio_10_02",
    "v3_bio_14_02", "v3_bio_03_02", "v3_bio_13_02", "v3_bio_06_02",
]
W03_IDS = {
    "v3_bio_01_01", "v3_bio_02_01", "v3_bio_03_01", "v3_bio_04_01",
    "v3_bio_05_01", "v3_bio_06_01", "v3_bio_07_01", "v3_bio_08_01",
    "v3_bio_09_01", "v3_bio_10_01", "v3_bio_11_01", "v3_bio_12_01",
    "v3_bio_13_01", "v3_bio_14_01", "v3_bio_15_01", "v3_bio_16_01",
}
FORBIDDEN = (
    "condition_wrong", "truth_partial", "wrong_condition", "partial_truth",
    "از کلیدواژه جواب نده", "روش کنترل:", "صورت را به بخش‌های مستقل",
    "صورت را به بخش هاي مستقل", "keyword", "trap/control",
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
    patch_path = Path(__file__).resolve().parents[1] / "app/src/main/assets/biology_v615_b_patch.json"
    if not database.is_file():
        fail(f"bank not found: {database}")
    if sha256(database) != BASE_SHA256:
        fail("frozen expanded-bank SHA-256 mismatch")
    patch = json.loads(patch_path.read_text(encoding="utf-8"))
    if patch.get("base_db_sha256") != BASE_SHA256:
        fail("patch base SHA-256 mismatch")
    updates = patch.get("updates")
    if not isinstance(updates, list) or len(updates) != len(EXPECTED_IDS):
        fail("update count is not exactly 16")
    update_ids = [update.get("id") for update in updates]
    if update_ids != EXPECTED_IDS or patch.get("rewritten_analysis_ids") != EXPECTED_IDS:
        fail("patch IDs/order do not equal the documented complementary set")
    if len(set(update_ids)) != len(update_ids):
        fail("duplicate patch ID")
    if set(update_ids) & W03_IDS:
        fail("overlap with W03 Biology-A rewritten IDs")

    conn = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    if conn.execute("PRAGMA quick_check").fetchone()[0] != "ok":
        fail("frozen base database quick_check failed")
    for update in updates:
        question_id = update["id"]
        row = conn.execute("SELECT * FROM question WHERE id=?", (question_id,)).fetchone()
        if row is None:
            fail(f"missing stable ID: {question_id}")
        source = json.loads(row["full_json"])
        if row["subject"] != "زیست" or row["source_type"] != "authored" or row["access_pool"] != "TRAIN":
            fail(f"non-authored Biology TRAIN target: {question_id}")
        if row["selected_scope"] != 1 or row["obsolete"] != 0:
            fail(f"out-of-scope or obsolete target: {question_id}")
        options = source.get("options")
        if not isinstance(options, list) or len(options) != 4 or any(not str(value).strip() for value in options):
            fail(f"invalid base options: {question_id}")
        if source.get("correct_index") not in range(4):
            fail(f"invalid base key: {question_id}")
        if update.get("source_type") != "authored":
            fail(f"source-type guard missing: {question_id}")
        fields = update.get("fields")
        if set(fields) != {"correct_analysis", "distractor_analyses", "short_lesson"}:
            fail(f"identity-bearing or unsupported field in overlay: {question_id}")
        analyses = fields["distractor_analyses"]
        if set(analyses) != {"0", "1", "2", "3"}:
            fail(f"not exactly four option analyses: {question_id}")
        texts = [fields["correct_analysis"], fields["short_lesson"], *analyses.values()]
        if any(not isinstance(text, str) or len(text.strip()) < 45 for text in texts):
            fail(f"missing or too-short scientific explanation: {question_id}")
        combined = " ".join(texts).casefold()
        if any(marker.casefold() in combined for marker in FORBIDDEN):
            fail(f"generic filler or raw enum leakage: {question_id}")
        # Each item must name its concrete biological content, not merely call a choice correct or wrong.
        if all(token not in combined for token in ("زیرا", "راکیزه", "فامتن", "هورمون", "آوند", "پادتن", "نفرون", "تیلاکوئید", "ریبوزوم", "دیافراگم", "سرخرگ", "آبکش")):
            fail(f"no concrete scientific reasoning token: {question_id}")
    conn.close()
    print("PASS: 16 disjoint Biology-B analysis-only updates validated against immutable V6.1 base")
    print(f"PATCH_SHA256={sha256(patch_path)}")


if __name__ == "__main__":
    main()
