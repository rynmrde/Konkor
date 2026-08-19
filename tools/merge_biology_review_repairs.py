#!/usr/bin/env python3
"""Merge strict explanation repair rows into a complete structured Biology review."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("review", type=Path)
    parser.add_argument("repairs", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    review = json.loads(args.review.read_text(encoding="utf-8"))
    repairs = json.loads(args.repairs.read_text(encoding="utf-8"))
    mapping = {row["id"]: row for row in repairs["items"]}
    updated = 0
    for row in review["items"]:
        repair = mapping.get(row["id"])
        if repair:
            row["correct_analysis"] = repair["correct_analysis"]
            row["distractor_analyses"] = repair["distractor_analyses"]
            updated += 1
    if updated != len(mapping):
        raise SystemExit(f"merged {updated} of {len(mapping)} repair rows")
    review["analysis_repair_pass"] = {"model": "gpt-5", "repaired_item_count": updated, "purpose": "Replace terse, placeholder, or cross-referential option analyses with standalone scientific reasoning."}
    args.output.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"merged repairs for {updated} items")


if __name__ == "__main__":
    main()
