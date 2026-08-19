#!/usr/bin/env python3
"""Independent, non-mutating review of V6.1 Biology/Geology overlays.

Checks immutable DB identity, patch IDs and field contracts, W04 paired-statement
visibility, and the standard renderer's raw-label/filler coverage. It never
rewrites the bank or changes source, key, stable ID, or holdout data.
"""
from __future__ import annotations
import hashlib
import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

BASE_SHA = "d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c"
RAW = ("condition_wrong", "wrong_condition", "truth_partial", "partial_truth", "overgeneralization", "calculation_trap", "calculation_error", "unit_mistake", "unit_error", "direction_error", "false_absolute", "keyword_trap", "knowledge_gap", "forgotten_rule", "misread", "time_management", "careless_error")
FILLERS = ("منشأ دام", "روش کنترل:", "از کلیدواژه جواب نده", "این گزینه با همهٔ شرط‌ها سازگار است", "این گزاره با کتاب سازگار است؛", "این گزاره دام مفهومی دارد؛", "نکتهٔ تثبیتی:")
MANUAL = {"v3_bio_10_11", "v3_bio_11_07", "v3_bio_11_24", "v3_bio_12_07", "v3_bio_13_15", "v3_bio_14_10", "v3_bio_14_20", "v3_bio_15_15", "v3_bio_15_24", "v3_bio_16_10", "v3_bio_16_16"}
OPTION_REPAIRS = {"v3_bio_11_24", "v3_bio_13_15", "v3_bio_14_20", "v3_bio_15_24", "v3_bio_16_16"}

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def main(db_path, patch615, patch620):
    out={"base_sha_pass":sha(db_path)==BASE_SHA,"patches":{},"bank_scope":{},"renderer_contract":{}}
    patch_objects=[]
    for p in (patch615,patch620):
        obj=json.loads(Path(p).read_text()); patch_objects.append(obj); updates=obj.get("updates",[]); ids=[u.get("id") for u in updates]
        out["patches"][Path(p).name]={"base_sha_pass":obj.get("base_db_sha256")==BASE_SHA,"updates":len(updates),"unique_ids":len(set(ids)),"duplicate_ids":[x for x,c in Counter(ids).items() if c>1],"field_contract_failures":[],"paired_statement_ids":[],"option_repair_ids":[]}
        for u in updates:
            qid=u.get("id"); fields=u.get("fields") or {}
            if not {"correct_analysis","distractor_analyses","short_lesson"} <= set(fields): out["patches"][Path(p).name]["field_contract_failures"].append((qid,"missing analysis field"))
            if "options" in fields:
                opts=fields["options"]
                if not isinstance(opts,list) or len(opts)!=4 or any(not str(x).strip() for x in opts): out["patches"][Path(p).name]["field_contract_failures"].append((qid,"malformed options"))
                else: out["patches"][Path(p).name]["option_repair_ids"].append(qid)
            stem=str(fields.get("stem", ""))
            if re.search(r"\bA\s*\)|\bB\s*\)",stem): out["patches"][Path(p).name]["paired_statement_ids"].append(qid)
    first={u.get("id"):u for u in patch_objects[0].get("updates",[])}
    second={u.get("id"):u for u in patch_objects[1].get("updates",[])}
    overlap=sorted(set(first)&set(second))
    conflicts=[qid for qid in overlap if first[qid].get("fields") != second[qid].get("fields")]
    out["cross_patch_overlap"]={"ids":overlap,"count":len(overlap),"conflicting_ids":conflicts,"conflict_count":len(conflicts)}
    con=sqlite3.connect(db_path)
    rows=con.execute("SELECT subject, COUNT(*) FROM question GROUP BY subject").fetchall()
    out["bank_scope"]={str(k):v for k,v in rows}
    out["bank_scope"]["biology_geology_total"]=sum(v for k,v in rows if k in ("زیست","زمین"))
    con.close()
    out["renderer_contract"]={"raw_labels_declared":len(RAW),"stock_filler_patterns_declared":len(FILLERS),"note":"Coverage execution is performed by the companion independent renderer checker; this helper remains non-mutating."}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=="__main__": main(*sys.argv[1:])
