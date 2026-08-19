#!/usr/bin/env python3
"""Non-disclosing comparator for candidate versus frozen real/quarantine records."""
from __future__ import annotations

import gzip
import json
import sqlite3
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT / ".audit_evidence" / "konkur_testbank_v6_1_verified.json"
CANDIDATE = ROOT / ".helper_chemistry" / "extracted" / "app/src/main/assets/radiology1405_bank_v6_2.db.gz"
OUTPUT = ROOT / ".helper_chemistry" / "immutable_record_differences.json"
EXCLUDED_FIELDS = {"stem", "options", "stimulus", "correct_analysis", "distractor_analyses", "short_lesson", "fast_method"}


def main() -> None:
    frozen = {row["id"]: row for row in json.loads(FROZEN.read_text(encoding="utf-8"))["questions"]}
    with tempfile.NamedTemporaryFile(suffix=".db") as temporary:
        with gzip.open(CANDIDATE, "rb") as compressed:
            for block in iter(lambda: compressed.read(1024 * 1024), b""):
                temporary.write(block)
        temporary.flush()
        conn = sqlite3.connect(temporary.name)
        candidate = {identifier: json.loads(raw) for identifier, raw in conn.execute("SELECT id, full_json FROM question")}
        conn.close()
    differences = []
    for identifier, original in frozen.items():
        if original.get("source_type") not in {"real_exam", "quarantined_key_conflict"}:
            continue
        revised = candidate.get(identifier)
        if revised is None:
            differences.append({"id": identifier, "status": "missing_in_candidate", "fields": []})
            continue
        changed = sorted(
            key
            for key in set(original) | set(revised)
            if key not in EXCLUDED_FIELDS and original.get(key) != revised.get(key)
        )
        content_changed = any(original.get(key) != revised.get(key) for key in EXCLUDED_FIELDS)
        if changed or content_changed:
            differences.append({"id": identifier, "status": "different", "fields": changed, "content_fields_differ": content_changed})
    OUTPUT.write_text(json.dumps(differences, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"immutable_records_checked={sum(row.get('source_type') in {'real_exam','quarantined_key_conflict'} for row in frozen.values())}")
    print(f"immutable_records_different={len(differences)}")
    print(f"difference_report={OUTPUT}")


if __name__ == "__main__":
    main()
