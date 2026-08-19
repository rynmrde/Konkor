#!/usr/bin/env python3
"""Independent validation for the v6.2 Chemistry QA bank candidate."""
from __future__ import annotations

import gzip
import hashlib
import json
import re
import shutil
import sqlite3
import sys
import tempfile
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

if len(sys.argv) != 5:
    raise SystemExit("usage: validate_v620_chemistry.py BASE_DB CANDIDATE_DB CANDIDATE_GZ AUDIT_DIR")

base, candidate, compressed, audit_dir = map(Path, sys.argv[1:])
results: list[dict[str, object]] = []

def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def record(name: str, ok: bool, evidence: object) -> None:
    results.append({"gate": name, "status": "PASS" if ok else "FAIL", "evidence": evidence})

def norm_option(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "")
    return re.sub(r"\s+", "", value.replace("ي", "ی").replace("ك", "ک").replace("−", "-")).casefold()

def exact_signature(q: dict) -> str:
    stem = unicodedata.normalize("NFKC", q.get("stem", ""))
    opts = [unicodedata.normalize("NFKC", str(v)) for v in q.get("options", [])]
    stimulus = q.get("stimulus") or {}
    return json.dumps([stimulus, stem, opts], ensure_ascii=False, sort_keys=True)

if not all(path.exists() for path in (base, candidate, compressed, audit_dir)):
    raise SystemExit("missing required candidate input")

with tempfile.NamedTemporaryFile(suffix=".db") as temporary:
    with gzip.open(compressed, "rb") as source:
        shutil.copyfileobj(source, temporary)
    temporary.flush()
    record("compressed v6.2 asset expands to candidate DB", sha(Path(temporary.name)) == sha(candidate), {"candidate_db_sha256": sha(candidate), "expanded_sha256": sha(Path(temporary.name))})

base_conn = sqlite3.connect(f"file:{base}?mode=ro", uri=True)
base_conn.row_factory = sqlite3.Row
candidate_conn = sqlite3.connect(f"file:{candidate}?mode=ro", uri=True)
candidate_conn.row_factory = sqlite3.Row
base_rows = {row["id"]: json.loads(row["full_json"]) for row in base_conn.execute("SELECT id,full_json FROM question")}
rows = list(candidate_conn.execute("SELECT * FROM question"))
questions = {row["id"]: json.loads(row["full_json"]) for row in rows}
record("candidate SQLite integrity", candidate_conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok", candidate_conn.execute("PRAGMA integrity_check").fetchone()[0])
record("candidate question IDs are unique", len(questions) == len(rows) == 1221, {"rows": len(rows), "unique": len(questions)})

chem_rows = [row for row in rows if row["subject"] == "شیمی"]
active_train = [row for row in chem_rows if row["access_pool"] == "TRAIN" and row["selected_scope"] and not row["obsolete"]]
record("v6.2 Chemistry counts and selected scope", len(chem_rows) == 272 and len(active_train) == 203, {"chemistry": len(chem_rows), "active_train": len(active_train)})

bad_options, bad_key, raw_enums, generic_template, missing_analysis = [], [], [], [], []
calculation_path = []
for row in chem_rows:
    q = questions[row["id"]]
    options = [str(value) for value in q.get("options", [])]
    analyses = q.get("distractor_analyses") or {}
    if len(options) != 4 or any(not value.strip() for value in options) or len({norm_option(value) for value in options}) != 4:
        bad_options.append(row["id"])
    if not isinstance(q.get("correct_index"), int) or q["correct_index"] not in range(4):
        bad_key.append(row["id"])
    if not str(q.get("correct_analysis", "")).strip() or any(not str(analyses.get(str(index), "")).strip() for index in range(4)):
        missing_analysis.append(row["id"])
    review_blob = json.dumps(q.get("review_default") or {}, ensure_ascii=False)
    if re.search(r"\b(condition_wrong|truth_partial|wrong_condition|partial_truth)\b", review_blob, re.I):
        raw_enums.append(row["id"])
    review_texts = " ".join(str(q.get(key, "")) for key in ("correct_analysis", "short_lesson", "fast_method", "start_method"))
    if any(marker in review_texts for marker in ("از کلیدواژه جواب نده", "روش کنترل:", "صورت را به بخش های مستقل", "صورت را به بخش‌های مستقل")):
        generic_template.append(row["id"])
    if q.get("calculation_required") and not any(token in review_texts for token in ("=", "مول", "mol", "M", "گرم", "L", "لیتر", "mL", "جرم")):
        calculation_path.append(row["id"])
record("all Chemistry records have valid choices, key, and option analyses", not bad_options and not bad_key and not missing_analysis, {"bad_options": bad_options, "bad_key": bad_key, "missing_analysis": missing_analysis})
record("no raw internal review enums or generic solution templates remain", not raw_enums and not generic_template, {"raw_enums": raw_enums, "generic_template": generic_template})
record("all declared Chemistry calculations have an explicit path or unit", not calculation_path, calculation_path)

active_signature_groups: defaultdict[str, list[str]] = defaultdict(list)
for row in active_train:
    active_signature_groups[exact_signature(questions[row["id"]])].append(row["id"])
active_duplicates = [group for group in active_signature_groups.values() if len(group) > 1]
record("no exact duplicate inside active Chemistry training including stimulus", not active_duplicates, active_duplicates)

mapping = json.loads((audit_dir / "CHEMISTRY-V6.2-MIGRATION-MAPPING.json").read_text(encoding="utf-8"))
retirements = mapping["retirements"]
mapping_ok = len(retirements) == 5
for entry in retirements:
    old_id, new_id = entry["retired_id"], entry["replacement_id"]
    old_row = candidate_conn.execute("SELECT selected_scope,obsolete FROM question WHERE id=?", (old_id,)).fetchone()
    new_row = candidate_conn.execute("SELECT selected_scope,obsolete,access_pool FROM question WHERE id=?", (new_id,)).fetchone()
    mapping_ok = mapping_ok and old_row is not None and new_row is not None and old_row["selected_scope"] == 0 and old_row["obsolete"] == 1 and new_row["selected_scope"] == 1 and new_row["obsolete"] == 0 and new_row["access_pool"] == "TRAIN"
record("retired cosmetic variants and new identity mapping", mapping_ok, retirements)

unchanged_ids = set(base_rows) - {entry["retired_id"] for entry in retirements}
key_changes = [qid for qid in unchanged_ids if questions[qid].get("correct_index") != base_rows[qid].get("correct_index")]
record("stable keys preserved for all unchanged identities", not key_changes, key_changes)

metadata_row = candidate_conn.execute("SELECT json FROM bank_root WHERE key='v6_2_chemistry_qa'").fetchone()
metadata = json.loads(metadata_row[0]) if metadata_row else {}
record("v6.2 metadata preserves source and progress-migration policy", bool(metadata_row) and metadata.get("baseline_db_sha256") == sha(base) and "No destructive Room migration" in metadata.get("progress_migration", ""), metadata)

candidate_conn.close()
base_conn.close()
summary = Counter(row["status"] for row in results)
payload = {"summary": dict(summary), "results": results}
(audit_dir / "CHEMISTRY-V6.2-VALIDATION.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for row in results:
    print(f"{row['status']:4} {row['gate']}")
print("SUMMARY", dict(summary))
if any(row["status"] == "FAIL" for row in results):
    raise SystemExit(1)
