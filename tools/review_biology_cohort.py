#!/usr/bin/env python3
"""Run structured scientific QA over a deterministic Biology audit cohort."""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import os
import time
from pathlib import Path

from openai import OpenAI

SYSTEM = """You are a senior Iranian Konkur Biology item writer and scientific editor. Audit Persian Biology multiple-choice questions for the 1405 curriculum. The supplied questions are authored TRAIN items, not authentic-exam claims. Preserve the stable ID and the original intended concept. Use current official Iranian Biology textbooks (grades 10–12, 1404/1405 editions) as the correctness standard and the supplied textbook section as the reference locator; do not invent page numbers or citations. Evaluate each stem, all four options, the key, and all explanations. Correct only when necessary, but replace generic/template explanation language with concrete Biology reasoning for every choice. Eliminate vague pronouns, raw internal labels, keyword/trap filler, answer leakage, ambiguity, and trivially eliminable distractors. Keep the question single-best-answer, exactly four self-contained options, and appropriate Konkur difficulty. Preserve the correct index unless a factual correction unavoidably requires changing it; flag any key change clearly. Do not label a question as real exam, do not manufacture official frequency, and do not make claims beyond the textbook. Write all revised question content in polished Persian. Output only the requested JSON schema."""

RESULT_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "decision": {"type": "string", "enum": ["KEEP", "REVISE", "KEY_CHANGE_REVIEW", "QUARANTINE_RECOMMEND"]},
                    "confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                    "issue_tags": {"type": "array", "items": {"type": "string", "enum": ["generic_analysis", "vague_referent", "factual", "ambiguity", "triviality", "weak_distractor", "non_konkur_difficulty", "key_review", "none"]}},
                    "stem": {"type": "string"},
                    "options": {"type": "array", "items": {"type": "string"}, "minItems": 4, "maxItems": 4},
                    "correct_index": {"type": "integer", "minimum": 0, "maximum": 3},
                    "correct_analysis": {"type": "string"},
                    "distractor_analyses": {
                        "type": "object",
                        "properties": {"0": {"type": "string"}, "1": {"type": "string"}, "2": {"type": "string"}, "3": {"type": "string"}},
                        "required": ["0", "1", "2", "3"],
                        "additionalProperties": False,
                    },
                    "audit_note": {"type": "string"},
                    "textbook_alignment": {"type": "string"},
                },
                "required": ["id", "decision", "confidence", "issue_tags", "stem", "options", "correct_index", "correct_analysis", "distractor_analyses", "audit_note", "textbook_alignment"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["items"],
    "additionalProperties": False,
}


def review_batch(index: int, batch: list[dict], model: str) -> dict:
    client = OpenAI()
    payload = []
    for q in batch:
        payload.append({
            "id": q["id"],
            "microtopic": q.get("microtopic"),
            "priority": q.get("priority"),
            "scope": q.get("runtime_scope_status"),
            "textbook_refs": q.get("textbook_refs"),
            "stem": q.get("stem"),
            "options": q.get("options"),
            "correct_index": q.get("correct_index"),
            "correct_analysis": q.get("correct_analysis"),
            "distractor_analyses": q.get("distractor_analyses"),
        })
    user = "Review exactly the following %d items and return exactly one result for each input ID, in the same order.\n\n%s" % (len(payload), json.dumps(payload, ensure_ascii=False))
    last_error = None
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
                max_completion_tokens=10000,
                response_format={"type": "json_schema", "json_schema": {"name": "biology_item_audit", "strict": True, "schema": RESULT_SCHEMA}},
                extra_body={"reasoning": {"effort": "medium"}},
            )
            content = response.choices[0].message.content
            data = json.loads(content)
            output_ids = [row["id"] for row in data["items"]]
            input_ids = [row["id"] for row in batch]
            if output_ids != input_ids:
                raise ValueError(f"batch {index}: output IDs do not match input order: {output_ids} != {input_ids}")
            return {"batch": index, "items": data["items"], "usage": {"prompt_tokens": getattr(response.usage, "prompt_tokens", None), "completion_tokens": getattr(response.usage, "completion_tokens", None)}}
        except Exception as exc:  # retry network/temporary model responses only
            last_error = repr(exc)
            time.sleep(2 ** attempt)
    return {"batch": index, "items": [], "error": last_error}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--model", default="gpt-5-mini")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    cohort = json.loads(args.input.read_text(encoding="utf-8"))
    batches = [cohort[i:i + args.batch_size] for i in range(0, len(cohort), args.batch_size)]
    results: list[dict] = []
    with futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending = [pool.submit(review_batch, index, batch, args.model) for index, batch in enumerate(batches)]
        for pending_result in futures.as_completed(pending):
            result = pending_result.result()
            print(f"batch {result['batch'] + 1}/{len(batches)}: {len(result.get('items', []))} items" + (f" ERROR {result['error']}" if result.get("error") else ""), flush=True)
            results.append(result)
    results.sort(key=lambda row: row["batch"])
    all_items = [item for result in results for item in result.get("items", [])]
    payload = {
        "model": args.model,
        "cohort_count": len(cohort),
        "reviewed_count": len(all_items),
        "errors": [{"batch": row["batch"], "error": row["error"]} for row in results if row.get("error")],
        "usage": [row.get("usage", {}) for row in results],
        "items": all_items,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if payload["reviewed_count"] != len(cohort) or payload["errors"]:
        raise SystemExit("incomplete review output")


if __name__ == "__main__":
    main()
