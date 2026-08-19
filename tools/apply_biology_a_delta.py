#!/usr/bin/env python3
"""Compile an identity-preserving Biology QA delta onto a frozen SQLite bank."""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import re
import shutil
import sqlite3
from pathlib import Path

RAW_ENUMS = re.compile(r"\b(?:condition_wrong|wrong_condition|truth_partial|partial_truth|truth_false|false_truth|truth_true|true_truth|condition_true|true_condition|overgeneralization|unknown|not_reviewed)\b", re.I)
GENERIC = ("به دام گزینه", "کلمه کلیدی", "کنترل کنید", "دام سوال", "از کلیدواژه جواب نده", "شرح بالا")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def meaningful(value: object) -> bool:
    text = str(value or "").strip()
    return len(text) >= 24 and not RAW_ENUMS.search(text) and not any(marker in text for marker in GENERIC)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_db", type=Path)
    parser.add_argument("assignment", type=Path)
    parser.add_argument("review", type=Path)
    parser.add_argument("overrides", type=Path)
    parser.add_argument("output_db", type=Path)
    parser.add_argument("output_gz", type=Path)
    parser.add_argument("audit", type=Path)
    args = parser.parse_args()

    assignment = json.loads(args.assignment.read_text(encoding="utf-8"))
    assigned_ids = assignment["deterministic_assignment"]["w03_bio_a_ids"]
    review = json.loads(args.review.read_text(encoding="utf-8"))
    overrides = json.loads(args.overrides.read_text(encoding="utf-8"))
    proposed = {item["id"]: item for item in review["items"]}
    proposed.update(overrides)
    if set(proposed) != set(assigned_ids):
        missing = sorted(set(assigned_ids) - set(proposed))
        extra = sorted(set(proposed) - set(assigned_ids))
        raise SystemExit(f"proposal membership mismatch; missing={missing}, extra={extra}")

    args.output_db.parent.mkdir(parents=True, exist_ok=True)
    args.audit.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.base_db, args.output_db)
    con = sqlite3.connect(args.output_db)
    con.row_factory = sqlite3.Row
    base = {row["id"]: json.loads(row["full_json"]) for row in con.execute("SELECT id, full_json FROM question")}

    audit_rows = []
    for qid in assigned_ids:
        old = base[qid]
        row = proposed[qid]
        new = copy.deepcopy(old)
        for key in ("stem", "options", "correct_index", "correct_analysis", "distractor_analyses"):
            new[key] = row[key]
        # Every option analysis must stand alone. Replace legacy cross-reference wording for the keyed option.
        keyed = str(new["correct_index"])
        if "شرح بالا" in new["distractor_analyses"].get(keyed, ""):
            new["distractor_analyses"][keyed] = new["correct_analysis"]
        new["v6_2_bio_a_qa"] = {
            "status": "REVIEWED_REVISED" if row["decision"] != "KEEP" or any(old.get(k) != new.get(k) for k in ("stem", "options", "correct_analysis", "distractor_analyses")) else "REVIEWED_NO_CONTENT_CHANGE",
            "reviewer_decision": row["decision"],
            "scientific_confidence": row["confidence"],
            "issue_tags": row["issue_tags"],
            "audit_note": row["audit_note"],
            "textbook_alignment": row["textbook_alignment"],
            "source_basis": "Official 1405 Biology textbook folder and 1402–1404 official Biology booklet folder reviewed by W03-BIO-A.",
        }
        if new["id"] != qid or new["subject"] != "زیست":
            raise ValueError(f"identity/subject violation for {qid}")
        if not isinstance(new["options"], list) or len(new["options"]) != 4 or any(not str(x).strip() for x in new["options"]):
            raise ValueError(f"options contract violation for {qid}")
        if not isinstance(new["correct_index"], int) or new["correct_index"] not in range(4):
            raise ValueError(f"key contract violation for {qid}")
        if not meaningful(new["correct_analysis"]) or any(not meaningful(new["distractor_analyses"].get(str(i))) for i in range(4)):
            raise ValueError(f"non-meaningful analysis remains for {qid}")
        if RAW_ENUMS.search(" ".join([new["stem"], *new["options"], new["correct_analysis"], *new["distractor_analyses"].values()])):
            raise ValueError(f"raw internal enum remains for {qid}")
        con.execute("UPDATE question SET full_json=? WHERE id=?", (json.dumps(new, ensure_ascii=False, separators=(",", ":")), qid))
        fields_changed = [key for key in ("stem", "options", "correct_index", "correct_analysis", "distractor_analyses") if old.get(key) != new.get(key)]
        audit_rows.append({
            "id": qid,
            "changed_fields": fields_changed,
            "key_preserved": old.get("correct_index") == new.get("correct_index"),
            "decision": row["decision"],
            "confidence": row["confidence"],
            "issue_tags": row["issue_tags"],
            "audit_note": row["audit_note"],
            "textbook_alignment": row["textbook_alignment"],
        })
    con.commit()
    integrity = con.execute("PRAGMA integrity_check").fetchone()[0]
    ids = [row[0] for row in con.execute("SELECT id FROM question ORDER BY id")]
    con.close()
    if integrity != "ok" or len(ids) != len(set(ids)):
        raise SystemExit(f"candidate DB integrity/ID failure: integrity={integrity}, ids={len(ids)}, unique={len(set(ids))}")

    with args.output_db.open("rb") as source, gzip.GzipFile(filename="", mode="wb", fileobj=args.output_gz.open("wb"), mtime=0) as target:
        shutil.copyfileobj(source, target, length=1024 * 1024)
    output = {
        "base_db_sha256": sha256(args.base_db),
        "candidate_db_sha256": sha256(args.output_db),
        "candidate_gzip_sha256": sha256(args.output_gz),
        "identity": {"assigned_ids": assigned_ids, "count": len(assigned_ids), "stable_ids_preserved": True},
        "database_integrity": integrity,
        "summary": {
            "items_reviewed": len(audit_rows),
            "items_with_content_changes": sum(bool(row["changed_fields"]) for row in audit_rows),
            "stem_or_options_changed": sum(bool(set(row["changed_fields"]) & {"stem", "options"}) for row in audit_rows),
            "analysis_changed": sum(bool(set(row["changed_fields"]) & {"correct_analysis", "distractor_analyses"}) for row in audit_rows),
            "key_changes": sum(not row["key_preserved"] for row in audit_rows),
            "manual_completion_repairs": sorted(overrides),
        },
        "items": audit_rows,
        "migration_implication": "A material-bank successor version is required. IDs and the Room progress database remain unchanged; integration must introduce a compatible, non-destructive bank selection/migration path rather than reset learner progress.",
    }
    args.audit.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"integrity": integrity, **output["summary"], "candidate_db_sha256": output["candidate_db_sha256"], "candidate_gzip_sha256": output["candidate_gzip_sha256"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
