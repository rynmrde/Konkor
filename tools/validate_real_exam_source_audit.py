#!/usr/bin/env python3
"""Deterministic V6.1 real-exam, quarantine, and holdout contract validator.

Usage:
  python3 tools/validate_real_exam_source_audit.py --bank /path/to/radiology1405_bank_v6_1.db
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_SOURCE_TYPES = {
    "authored": 1112,
    "official_exam_stem_training": 71,
    "quarantined_key_conflict": 16,
    "real_exam": 17,
}
EXPECTED_POOLS = {"FINAL": 10, "QUARANTINE": 16, "SIM1": 117, "SIM2": 117, "TRAIN": 956}
HOLDOUTS = {"SIM1", "SIM2", "FINAL"}
DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
TRANSLATION = str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک", "ؤ": "و", "ۀ": "ه", "ة": "ه"})


def normalise(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).translate(TRANSLATION).translate(DIGITS)
    return re.sub(r"[\W_\u200c\u200d\u200e\u200f\ufeff]+", "", text)


def canonical(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, list):
        return [canonical(item) for item in value]
    if isinstance(value, str):
        return normalise(value)
    return value


def complete_identity(question: dict) -> str:
    payload = {
        "stem": question.get("stem"),
        "options": question.get("options"),
        "correct_index": question.get("correct_index"),
        "stimulus": question.get("stimulus"),
    }
    encoded = json.dumps(canonical(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", required=True, type=Path)
    args = parser.parse_args()
    require(args.bank.is_file(), f"bank does not exist: {args.bank}")

    db = sqlite3.connect(f"file:{args.bank}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    require(db.execute("PRAGMA quick_check").fetchone()[0] == "ok", "SQLite quick_check failed")
    rows = db.execute("SELECT id, source_type, access_pool, full_json FROM question ORDER BY id").fetchall()
    questions = []
    for row in rows:
        question = json.loads(row["full_json"])
        require(question.get("id") == row["id"], f"db/json id mismatch: {row['id']}")
        require(isinstance(question.get("options"), list) and len(question["options"]) == 4, f"not four options: {row['id']}")
        questions.append({"id": row["id"], "source_type": row["source_type"], "pool": row["access_pool"], "question": question})

    source_counts = dict(Counter(item["source_type"] for item in questions))
    pool_counts = dict(Counter(item["pool"] for item in questions))
    require(len(questions) == 1216, f"question count changed: {len(questions)}")
    require(source_counts == EXPECTED_SOURCE_TYPES, f"unexpected source-type counts: {source_counts}")
    require(pool_counts == EXPECTED_POOLS, f"unexpected pool counts: {pool_counts}")

    active_real = [item for item in questions if item["source_type"] == "real_exam"]
    require(len(active_real) == 17, "active real-exam count changed")
    required_real_fields = (
        "exam_year", "exam_session", "question_number", "source_file_id", "source_file_sha256",
        "source_page", "source_url", "official_answer_key_url", "official_origin",
        "text_verified_against_source_page", "obsolete_for_1405",
    )
    for item in active_real:
        question = item["question"]
        require(item["pool"] == "TRAIN", f"active real exam outside TRAIN: {item['id']}")
        require(question.get("source_type") == "real_exam", f"real-exam json label mismatch: {item['id']}")
        require(question.get("official_origin") is True, f"real exam lacks official-origin claim: {item['id']}")
        require(question.get("text_verified_against_source_page") is True, f"real exam lacks source-text verification: {item['id']}")
        require(question.get("obsolete_for_1405") is False, f"obsolete real exam active: {item['id']}")
        for field in required_real_fields:
            require(question.get(field) not in (None, ""), f"real exam missing {field}: {item['id']}")

    quarantined = [item for item in questions if item["source_type"] == "quarantined_key_conflict"]
    require(len(quarantined) == 16, "quarantine count changed")
    for item in quarantined:
        question = item["question"]
        require(item["pool"] == "QUARANTINE", f"quarantined item outside QUARANTINE: {item['id']}")
        require(question.get("needs_human_review") is True, f"quarantine review flag absent: {item['id']}")
        require(question.get("needs_official_key_reconciliation") is True, f"quarantine reconciliation flag absent: {item['id']}")
        require((question.get("v6_1_real_review") or {}).get("status") == "KEY_CONFLICT_QUARANTINE", f"quarantine status mismatch: {item['id']}")

    blueprints = json.loads(db.execute("SELECT json FROM bank_root WHERE key='simulation_blueprints'").fetchone()[0])
    pools = defaultdict(set)
    for item in questions:
        pools[item["pool"]].add(item["id"])
    for pool in HOLDOUTS:
        require(set(blueprints[pool]["question_ids"]) == pools[pool], f"blueprint/pool mismatch: {pool}")
    for left, right in (("SIM1", "SIM2"), ("SIM1", "FINAL"), ("SIM2", "FINAL")):
        require(not (pools[left] & pools[right]), f"holdout ID overlap: {left}/{right}")

    identity_index = defaultdict(list)
    fingerprint_index = defaultdict(list)
    for item in questions:
        identity_index[complete_identity(item["question"])].append(item)
        fingerprint_index[str(item["question"].get("semantic_fingerprint"))].append(item)
        if item["pool"] in HOLDOUTS:
            require(item["source_type"] == "authored", f"holdout non-authored: {item['id']}")
            require(item["question"].get("source_type") == "authored", f"holdout json non-authored: {item['id']}")
            require(item["question"].get("needs_human_review") is False, f"holdout needs review: {item['id']}")
            require(item["question"].get("eligible_for_safety_evidence") is True, f"holdout safety flag absent: {item['id']}")
    for name, index in (("complete identity", identity_index), ("semantic fingerprint", fingerprint_index)):
        for group in index.values():
            holdout = [item for item in group if item["pool"] in HOLDOUTS]
            training = [item for item in group if item["pool"] == "TRAIN"]
            holdout_pools = {item["pool"] for item in holdout}
            require(not (holdout and training), f"holdout/train {name} collision: {[item['id'] for item in group]}")
            require(len(holdout_pools) <= 1, f"cross-holdout {name} collision: {[item['id'] for item in group]}")

    db.close()
    print("PASS: real-exam source labels, quarantine containment, and complete-identity holdout isolation")
    print("active_real_exam=17 quarantined=16 holdout=244")


if __name__ == "__main__":
    main()
