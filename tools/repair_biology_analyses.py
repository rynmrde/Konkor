#!/usr/bin/env python3
"""Repair residual non-standalone Biology explanation fields in strict structured batches."""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import time
from pathlib import Path

from openai import OpenAI

SYSTEM = """You are a senior Iranian Konkur Biology scientific editor. For each Persian authored Biology TRAIN item, write a standalone correct-answer explanation and four standalone option analyses that conform to the current official Iranian Biology textbooks. Do not change the stem, options, or answer key. Every option analysis must explicitly state why that exact option is correct or incorrect, using the concept in that option. Never write a placeholder, dash, 'توضیح بالا', 'شرح بالا', 'درست' alone, a pronoun without a named referent, raw internal labels, generic test-taking advice, or a reference to another field. Remain concise but specific, accurate, and at appropriate Konkur level. Output only valid JSON matching the requested schema."""

SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "correct_analysis": {"type": "string", "minLength": 24},
                    "distractor_analyses": {
                        "type": "object",
                        "properties": {"0": {"type": "string", "minLength": 24}, "1": {"type": "string", "minLength": 24}, "2": {"type": "string", "minLength": 24}, "3": {"type": "string", "minLength": 24}},
                        "required": ["0", "1", "2", "3"],
                        "additionalProperties": False,
                    },
                },
                "required": ["id", "correct_analysis", "distractor_analyses"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["items"],
    "additionalProperties": False,
}


def one_batch(index: int, batch: list[dict], model: str) -> dict:
    client = OpenAI()
    compact = [{key: q.get(key) for key in ("id", "microtopic", "textbook_refs", "stem", "options", "correct_index", "correct_analysis", "distractor_analyses")} for q in batch]
    last_error = None
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": "Repair exactly these item explanations in their supplied order:\n" + json.dumps(compact, ensure_ascii=False)}],
                max_completion_tokens=7000,
                response_format={"type": "json_schema", "json_schema": {"name": "biology_analysis_repair", "strict": True, "schema": SCHEMA}},
                extra_body={"reasoning": {"effort": "high"}},
            )
            data = json.loads(response.choices[0].message.content)
            if [x["id"] for x in data["items"]] != [x["id"] for x in batch]:
                raise ValueError("item identity/order mismatch")
            return {"batch": index, "items": data["items"]}
        except Exception as exc:
            last_error = repr(exc)
            time.sleep(2 ** attempt)
    return {"batch": index, "items": [], "error": last_error}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cohort", type=Path)
    parser.add_argument("proposal", type=Path)
    parser.add_argument("overrides", type=Path)
    parser.add_argument("failures", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--model", default="gpt-5")
    args = parser.parse_args()
    cohort = {q["id"]: q for q in json.loads(args.cohort.read_text(encoding="utf-8"))}
    proposal = {q["id"]: q for q in json.loads(args.proposal.read_text(encoding="utf-8"))["items"]}
    proposal.update(json.loads(args.overrides.read_text(encoding="utf-8")))
    failed_ids = []
    for row in json.loads(args.failures.read_text(encoding="utf-8")):
        if row["id"] not in failed_ids:
            failed_ids.append(row["id"])
    inputs = []
    for qid in failed_ids:
        q = dict(cohort[qid])
        q["correct_analysis"] = proposal[qid]["correct_analysis"]
        q["distractor_analyses"] = proposal[qid]["distractor_analyses"]
        inputs.append(q)
    batches = [inputs[i:i + 4] for i in range(0, len(inputs), 4)]
    results = []
    with futures.ThreadPoolExecutor(max_workers=3) as pool:
        submitted = [pool.submit(one_batch, index, batch, args.model) for index, batch in enumerate(batches)]
        for pending in futures.as_completed(submitted):
            result = pending.result()
            print(f"batch {result['batch'] + 1}/{len(batches)}: {len(result.get('items', []))}" + (f" ERROR {result['error']}" if result.get("error") else ""), flush=True)
            results.append(result)
    results.sort(key=lambda row: row["batch"])
    repaired = [row for result in results for row in result.get("items", [])]
    output = {"requested_ids": failed_ids, "repaired_count": len(repaired), "errors": [row for row in results if row.get("error")], "items": repaired}
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if output["errors"] or output["repaired_count"] != len(failed_ids):
        raise SystemExit("analysis repairs incomplete")


if __name__ == "__main__":
    main()
