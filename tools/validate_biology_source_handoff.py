#!/usr/bin/env python3
"""Guard the audited Biology real-exam and quarantine source boundaries in a bank SQLite file."""
from __future__ import annotations

import argparse
import json
import sqlite3
from collections import Counter
from pathlib import Path

ACTIVE_BIOLOGY_IDS = {
    "real_1403_n1_bio_003", "real_1403_n1_bio_010", "real_1403_n1_bio_012",
    "real_1403_n1_bio_014", "real_1403_n1_bio_016", "real_1403_n1_bio_019",
    "real_1403_n1_bio_022", "real_1403_n1_bio_024", "real_1403_n1_bio_028",
    "real_1403_n1_bio_029", "real_1403_n1_bio_032", "real_1403_n1_bio_033",
    "real_1403_n1_bio_041", "real_1403_n1_bio_042", "real_1403_n1_bio_044",
}
QUARANTINED_BIOLOGY_IDS = {
    "real_1401_in_bio_017", "real_1401_in_bio_042", "real_1402_n2in_bio_041",
}
BIOLOGY_SOURCE_SHA256 = "6b080cda86b850cc61f040475fc4c03e7d62d11519f7f02ce1bf8cc1bc59edf8"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", required=True, type=Path)
    args = parser.parse_args()
    connection = sqlite3.connect(f"file:{args.bank}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    require(connection.execute("PRAGMA quick_check").fetchone()[0] == "ok", "SQLite quick_check failed")
    rows = connection.execute("SELECT id, source_type, access_pool, full_json FROM question ORDER BY id").fetchall()
    records = {row["id"]: {"source_type": row["source_type"], "pool": row["access_pool"], "question": json.loads(row["full_json"])} for row in rows}
    connection.close()

    require(ACTIVE_BIOLOGY_IDS <= records.keys(), "an audited active Biology real-exam ID is missing")
    require(QUARANTINED_BIOLOGY_IDS <= records.keys(), "an audited Biology quarantine ID is missing")
    for item_id in ACTIVE_BIOLOGY_IDS:
        item = records[item_id]
        question = item["question"]
        require(item["source_type"] == "real_exam" and question.get("source_type") == "real_exam", f"active source label changed: {item_id}")
        require(item["pool"] == "TRAIN", f"active real exam left training: {item_id}")
        require(question.get("source_file_sha256") == BIOLOGY_SOURCE_SHA256, f"unexpected Biology source SHA: {item_id}")
        require(question.get("official_origin") is True, f"official-origin claim absent: {item_id}")
        require(question.get("text_verified_against_source_page") is True, f"source-page verification absent: {item_id}")
        require(question.get("obsolete_for_1405") is False, f"audited active item marked obsolete: {item_id}")
        require(isinstance(question.get("options"), list) and len(question["options"]) == 4, f"option count invalid: {item_id}")
    for item_id in QUARANTINED_BIOLOGY_IDS:
        item = records[item_id]
        question = item["question"]
        require(item["source_type"] == "quarantined_key_conflict", f"quarantine label changed: {item_id}")
        require(item["pool"] == "QUARANTINE", f"quarantine pool changed: {item_id}")
        require(question.get("needs_official_key_reconciliation") is True, f"reconciliation flag lost: {item_id}")
        require(question.get("needs_human_review") is True, f"review flag lost: {item_id}")
        require((question.get("v6_1_real_review") or {}).get("status") == "KEY_CONFLICT_QUARANTINE", f"status changed: {item_id}")
    biology_counts = Counter(item["source_type"] for item in records.values() if item["question"].get("subject") == "زیست")
    print("PASS: audited Biology real-exam and quarantine boundaries preserved")
    print("active_real_exam=15 quarantined=3 source_type_counts=", dict(sorted(biology_counts.items())))


if __name__ == "__main__":
    main()
