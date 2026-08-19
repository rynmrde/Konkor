#!/usr/bin/env python3
"""List non-standalone explanations in a proposed Biology QA revision set."""
from __future__ import annotations

import json
import re
from pathlib import Path

RAW_ENUMS = re.compile(r"\b(?:condition_wrong|wrong_condition|truth_partial|partial_truth|truth_false|false_truth|truth_true|true_truth|condition_true|true_condition|overgeneralization|unknown|not_reviewed)\b", re.I)
GENERIC = ("به دام گزینه", "کلمه کلیدی", "کنترل کنید", "دام سوال", "از کلیدواژه جواب نده", "شرح بالا")


def meaningful(value: object) -> bool:
    text = str(value or "").strip()
    return len(text) >= 24 and not RAW_ENUMS.search(text) and not any(marker in text for marker in GENERIC)


def main() -> None:
    root = Path("/home/ubuntu/Konkor-bio-a")
    review = json.loads((root / "reports/parallel/BIOLOGY_A_STRUCTURED_REVIEW.json").read_text(encoding="utf-8"))
    overrides = json.loads((root / "reports/parallel/BIOLOGY_A_MANUAL_OVERRIDES.json").read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in review["items"]}
    rows.update(overrides)
    failures = []
    for qid, row in sorted(rows.items()):
        if not meaningful(row.get("correct_analysis")):
            failures.append({"id": qid, "field": "correct_analysis", "value": row.get("correct_analysis")})
        for index in range(4):
            value = (row.get("distractor_analyses") or {}).get(str(index))
            if not meaningful(value):
                failures.append({"id": qid, "field": f"distractor_analyses.{index}", "value": value, "correct_index": row.get("correct_index"), "stem": row.get("stem"), "options": row.get("options")})
    out = root / "reports/parallel/BIOLOGY_A_PROPOSAL_QUALITY_FAILURES.json"
    out.write_text(json.dumps(failures, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"proposal explanation failures: {len(failures)}")


if __name__ == "__main__":
    main()
