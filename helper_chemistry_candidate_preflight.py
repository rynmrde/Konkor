#!/usr/bin/env python3
"""Independent non-disclosing preflight for the chemistry V6.2 candidate overlay."""
from __future__ import annotations

import gzip
import hashlib
import json
import sqlite3
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANDIDATE_GZIP = ROOT / ".helper_chemistry" / "extracted" / "app/src/main/assets/radiology1405_bank_v6_2.db.gz"
CANDIDATE_STORE = ROOT / ".helper_chemistry" / "extracted" / "app/src/main/java/com/radiology1405/prep/data/BankStore.kt"
FROZEN_JSON = ROOT / ".audit_evidence" / "konkur_testbank_v6_1_verified.json"
EXPECTED_GZIP = "47ba0670e5c3b22e5823dfb577ade40267f530fd40f7d4a2b8c8119b9f67cbce"
EXPECTED_DB = "ed84693259455e6da488af23a7fa39c6548ea64e95bee6a93ba5cedf8f7656c6"
EXPECTED_SOURCES = {
    "authored": 1117,
    "official_exam_stem_training": 71,
    "quarantined_key_conflict": 16,
    "real_exam": 17,
}
EXPECTED_POOLS = {"FINAL": 10, "QUARANTINE": 16, "SIM1": 117, "SIM2": 117, "TRAIN": 961}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise AssertionError(message)


def ids_for(records: dict[str, dict], pool: str) -> set[str]:
    return {key for key, record in records.items() if record.get("access_pool") == pool}


def main() -> None:
    if not CANDIDATE_GZIP.is_file() or not CANDIDATE_STORE.is_file() or not FROZEN_JSON.is_file():
        fail("Required candidate or frozen evidence file is missing")
    if sha256(CANDIDATE_GZIP) != EXPECTED_GZIP:
        fail("Candidate gzip SHA-256 mismatch")
    store_text = CANDIDATE_STORE.read_text(encoding="utf-8")
    for token in (
        'PACKAGED_ASSET = "radiology1405_bank_v6_2.db"',
        'SOURCE_GZIP_ASSET = "radiology1405_bank_v6_2.db.gz"',
        'DB_NAME = "radiology1405_bank_v6_2.db"',
        EXPECTED_DB,
        EXPECTED_GZIP,
        "EXPECTED_QUESTIONS = 1221",
        "EXPECTED_VERIFIED_REAL = 17",
        "EXPECTED_AUTHORED = 1117",
        "EXPECTED_PROVISIONAL_STEMS = 71",
        "EXPECTED_QUARANTINED = 16",
    ):
        if token not in store_text:
            fail(f"BankStore candidate contract missing: {token}")

    frozen = json.loads(FROZEN_JSON.read_text(encoding="utf-8"))
    frozen_records = {record["id"]: record for record in frozen["questions"]}
    with tempfile.NamedTemporaryFile(suffix=".db") as temporary:
        with gzip.open(CANDIDATE_GZIP, "rb") as compressed:
            for block in iter(lambda: compressed.read(1024 * 1024), b""):
                temporary.write(block)
        temporary.flush()
        db_path = Path(temporary.name)
        if sha256(db_path) != EXPECTED_DB:
            fail("Candidate expanded DB SHA-256 mismatch")
        database = sqlite3.connect(db_path)
        if database.execute("PRAGMA quick_check").fetchone()[0] != "ok":
            fail("Candidate SQLite quick_check failed")
        rows = database.execute("SELECT id, full_json FROM question").fetchall()
        if len(rows) != 1221:
            fail("Candidate question-count mismatch")
        candidate_records: dict[str, dict] = {}
        for row_id, raw in rows:
            record = json.loads(raw)
            if row_id != record.get("id") or row_id in candidate_records:
                fail("Candidate question ID mismatch or duplicate")
            options = record.get("options")
            if not isinstance(options, list) or len(options) != 4:
                fail("Candidate record has invalid option count")
            if record.get("correct_index") not in range(4):
                fail("Candidate record has invalid answer key")
            if not isinstance(record.get("correct_analysis"), str) or not record["correct_analysis"].strip():
                fail("Candidate record lacks correct-answer reasoning")
            candidate_records[row_id] = record
        sources = Counter(record.get("source_type") for record in candidate_records.values())
        pools = Counter(record.get("access_pool") for record in candidate_records.values())
        if dict(sources) != EXPECTED_SOURCES:
            fail(f"Candidate source counts mismatch: {dict(sources)}")
        if dict(pools) != EXPECTED_POOLS:
            fail(f"Candidate pool counts mismatch: {dict(pools)}")

        # Real-exam and quarantine identity, source, key, options, and explanations
        # must remain unchanged. A chemistry-specific `review_default` preference may
        # change without activating or altering a protected item.
        immutable_checked = 0
        review_default_only_changes = 0
        for frozen_id, frozen_record in frozen_records.items():
            if frozen_record.get("source_type") in {"real_exam", "quarantined_key_conflict"}:
                immutable_checked += 1
                candidate = candidate_records.get(frozen_id)
                if candidate is None:
                    fail("Candidate removed a frozen real-exam or quarantine record")
                changed_fields = {
                    field
                    for field in set(frozen_record) | set(candidate)
                    if frozen_record.get(field) != candidate.get(field)
                }
                if changed_fields - {"review_default"}:
                    fail("Candidate changed protected real-exam or quarantine content/metadata")
                if changed_fields == {"review_default"}:
                    review_default_only_changes += 1

        sim1 = ids_for(candidate_records, "SIM1")
        sim2 = ids_for(candidate_records, "SIM2")
        final = ids_for(candidate_records, "FINAL")
        if len(sim1) != 117 or len(sim2) != 117 or len(final) != 10:
            fail("Candidate holdout-size mismatch")
        if sim1 & sim2 or sim1 & final or sim2 & final:
            fail("Candidate holdout-overlap")
        for record in candidate_records.values():
            if record.get("access_pool") in {"SIM1", "SIM2", "FINAL"}:
                if record.get("source_type") != "authored" or record.get("eligible_for_safety_evidence") is not True or record.get("needs_human_review") is not False:
                    fail("Candidate holdout safety violation")
        blueprint = json.loads(database.execute("SELECT json FROM bank_root WHERE key='simulation_blueprints'").fetchone()[0])
        if set(blueprint["SIM1"]["question_ids"]) != sim1 or set(blueprint["SIM2"]["question_ids"]) != sim2:
            fail("Candidate simulation blueprint mismatch")
        database.close()

    print("CHEMISTRY_V62_HELPER_PREFLIGHT=PASS")
    print("candidate_questions=1221 authored=1117 training_stems=71 real=17 quarantine=16")
    print("candidate_pools=TRAIN961 SIM1=117 SIM2=117 FINAL=10 QUARANTINE=16")
    print(f"real_quarantine_immutable_fields=PASS checked={immutable_checked} review_default_only_changes={review_default_only_changes}")
    print("holdout_isolation=PASS blueprint_membership=PASS")


if __name__ == "__main__":
    main()
