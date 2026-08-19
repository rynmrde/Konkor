#!/usr/bin/env python3
"""Deterministic non-disclosing audit for the frozen V6.1 verified bank.

This worker-scoped checker intentionally prints counts and invariant failures only.
It never prints stems, options, crop data, or SIM/FINAL question identifiers.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BANK_PATH = ROOT / ".audit_evidence" / "konkur_testbank_v6_1_verified.json"
EXPECTED_SHA256 = "54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d"
EXPECTED_SOURCE_COUNTS = {
    "authored": 1112,
    "official_exam_stem_training": 71,
    "quarantined_key_conflict": 16,
    "real_exam": 17,
}
EXPECTED_POOL_COUNTS = {
    "FINAL": 10,
    "QUARANTINE": 16,
    "SIM1": 117,
    "SIM2": 117,
    "TRAIN": 956,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def pool_ids(questions: list[dict], pool: str) -> set[str]:
    return {question["id"] for question in questions if question.get("access_pool") == pool}


def main() -> None:
    require(BANK_PATH.is_file(), f"Frozen bank missing: {BANK_PATH}")
    require(digest(BANK_PATH) == EXPECTED_SHA256, "Frozen verified-bank SHA256 mismatch")
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    questions = bank["questions"]

    require(len(questions) == 1216, "Question-count mismatch")
    ids = [question.get("id") for question in questions]
    require(all(isinstance(question_id, str) and question_id for question_id in ids), "Blank question ID")
    require(len(ids) == len(set(ids)), "Duplicate question ID")

    for question in questions:
        options = question.get("options")
        require(isinstance(options, list) and len(options) == 4, "Question lacks exactly four options")
        correct = question.get("correct_index")
        require(isinstance(correct, int) and 0 <= correct <= 3, "Invalid correct-index")
        analysis = question.get("correct_analysis")
        require(isinstance(analysis, str) and analysis.strip(), "Missing correct analysis")

    source_counts = Counter(question.get("source_type") for question in questions)
    pool_counts = Counter(question.get("access_pool") for question in questions)
    require(dict(source_counts) == EXPECTED_SOURCE_COUNTS, "Source-type count mismatch")
    require(dict(pool_counts) == EXPECTED_POOL_COUNTS, "Access-pool count mismatch")

    real = [question for question in questions if question.get("source_type") == "real_exam"]
    require(len(real) == 17, "Active real-exam count mismatch")
    for question in real:
        require(question.get("access_pool") == "TRAIN", "Active real-exam item outside TRAIN")
        require(question.get("exam_year") is not None, "Active real-exam item has no year")
        require(bool(question.get("exam_session")), "Active real-exam item has no session")
        require(question.get("question_number") is not None, "Active real-exam item has no number")
        require(bool(question.get("source_url")), "Active real-exam item has no source URL")
        require(bool(question.get("official_answer_key_url")), "Active real-exam item has no key URL")
        require(question.get("official_origin") is True, "Active real-exam item lacks official-origin flag")
        require(question.get("answer_key_official_origin") is True, "Active real-exam item lacks official-key-origin flag")
        require(question.get("retrieved_from_archive") is False, "Active real-exam item unexpectedly marked archive retrieval")
        require(question.get("text_verified_against_source_page") is True, "Active real-exam source page not text verified")
    recent_real = [question for question in real if question.get("exam_year") in {1402, 1403, 1404}]
    require(len(recent_real) == 17, "Unexpected recent active real-exam count")
    require({(question["exam_year"], question["exam_session"]) for question in recent_real} == {(1403, "نوبت 1 - داخل کشور")}, "Unexpected recent real-exam session mix")

    quarantine = [question for question in questions if question.get("source_type") == "quarantined_key_conflict"]
    require(len(quarantine) == 16, "Quarantine count mismatch")
    for question in quarantine:
        require(question.get("access_pool") == "QUARANTINE", "Quarantine item leaked from QUARANTINE")
        require(question.get("needs_human_review") is True, "Quarantine item lacks human-review flag")
        require(question.get("eligible_for_safety_evidence") is False, "Quarantine item safety eligible")
        require(question.get("exam_year") is not None, "Quarantine item has no year")
        require(question.get("question_number") is not None, "Quarantine item has no number")
        require(bool(question.get("source_url")), "Quarantine item has no source URL")
        require(bool(question.get("official_answer_key_url")), "Quarantine item has no key URL")
    recent_quarantine = [question for question in quarantine if question.get("exam_year") in {1402, 1403, 1404}]
    require(len(recent_quarantine) == 3, "Unexpected recent quarantine count")
    require(
        {(question["exam_year"], question["exam_session"]) for question in recent_quarantine}
        == {(1402, "نوبت 2 - داخل کشور"), (1403, "نوبت 1 - داخل کشور"), (1404, "نوبت 2 - داخل کشور")},
        "Unexpected recent quarantine session mix",
    )

    sim1 = pool_ids(questions, "SIM1")
    sim2 = pool_ids(questions, "SIM2")
    final = pool_ids(questions, "FINAL")
    require(len(sim1) == 117 and len(sim2) == 117 and len(final) == 10, "Holdout size mismatch")
    require(not sim1 & sim2 and not sim1 & final and not sim2 & final, "Holdout pool overlap")
    for question in questions:
        if question.get("access_pool") in {"SIM1", "SIM2", "FINAL"}:
            require(question.get("source_type") == "authored", "Holdout includes non-authored item")
            require(question.get("eligible_for_safety_evidence") is True, "Holdout includes safety-ineligible item")
            require(question.get("needs_human_review") is False, "Holdout includes human-review item")
            require(question.get("obsolete_for_1405") is not True, "Holdout includes obsolete item")
    blueprint = bank["simulation_blueprints"]
    for name, expected in (("SIM1", sim1), ("SIM2", sim2)):
        listed = blueprint[name]["question_ids"]
        require(len(listed) == len(expected), f"{name} blueprint count mismatch")
        require(len(listed) == len(set(listed)), f"{name} blueprint duplicate")
        require(set(listed) == expected, f"{name} blueprint/pool mismatch")

    by_year = Counter(question["exam_year"] for question in quarantine)
    print("REAL_EXAM_1402_1404_AUDIT=PASS")
    print(f"frozen_json_sha256={EXPECTED_SHA256}")
    print(f"questions={len(questions)} source_counts={dict(sorted(source_counts.items()))}")
    print(f"pool_counts={dict(sorted(pool_counts.items()))}")
    print(f"active_real={len(real)} recent_active_real={len(recent_real)}")
    print(f"quarantine={len(quarantine)} recent_quarantine={len(recent_quarantine)} quarantine_by_year={dict(sorted(by_year.items()))}")
    print("holdout_integrity=SIM1_117_SIM2_117_FINAL_10_disjoint_blueprints_exact")


if __name__ == "__main__":
    main()
