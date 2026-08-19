#!/usr/bin/env python3
"""Export a deterministic Biology audit cohort from a SQLite bank."""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("db", type=Path)
    parser.add_argument("assignment", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    assignment = json.loads(args.assignment.read_text(encoding="utf-8"))
    ids = assignment["deterministic_assignment"]["w03_bio_a_ids"]
    con = sqlite3.connect(args.db)
    rows = {row[0]: json.loads(row[1]) for row in con.execute("SELECT id, full_json FROM question")}
    out = []
    for ordinal, qid in enumerate(ids, start=1):
        q = rows[qid]
        out.append({
            "ordinal": ordinal,
            "id": qid,
            "subject": q.get("subject"),
            "microtopic": q.get("microtopic"),
            "priority": q.get("priority"),
            "runtime_scope_status": q.get("runtime_scope_status"),
            "source_type": q.get("source_type"),
            "access_pool": q.get("access_pool"),
            "stem": q.get("stem"),
            "options": q.get("options"),
            "correct_index": q.get("correct_index"),
            "correct_analysis": q.get("correct_analysis"),
            "distractor_analyses": q.get("distractor_analyses"),
            "textbook_refs": q.get("textbook_refs"),
            "tags": q.get("tags"),
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"exported {len(out)} questions: {out[0]['id']}..{out[-1]['id']}")


if __name__ == "__main__":
    main()
