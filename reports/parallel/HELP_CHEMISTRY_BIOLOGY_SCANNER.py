#!/usr/bin/env python3
"""Read-only Biology helper QA scan for the frozen active bank."""
from __future__ import annotations
import json
import re
import sqlite3
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit('usage: scan_biology_helper.py DB_PATH OUTPUT_JSON')

def normalize(value: str) -> str:
    value=unicodedata.normalize('NFKC',value or '').replace('ي','ی').replace('ك','ک')
    return ' '.join(re.sub(r'[^\w]+',' ',value.casefold(),flags=re.UNICODE).split())

def option_norm(value: str) -> str:
    value=unicodedata.normalize('NFKC',value or '').replace('ي','ی').replace('ك','ک').replace('−','-')
    return re.sub(r'\s+','',value).casefold()

con=sqlite3.connect(f'file:{Path(sys.argv[1])}?mode=ro',uri=True); con.row_factory=sqlite3.Row
integrity=con.execute('PRAGMA quick_check').fetchone()[0]
rows=con.execute("SELECT * FROM question WHERE subject='زیست' ORDER BY priority DESC,id").fetchall()
issues=defaultdict(list); exact=defaultdict(list); semantic=defaultdict(list); active=[]
for row in rows:
    q=json.loads(row['full_json']); qid=row['id']; options=[str(x) for x in q.get('options') or []]
    analyses=q.get('distractor_analyses') or {}; review=json.dumps(q.get('review_default') or {},ensure_ascii=False)
    texts=' '.join(str(q.get(k,'')) for k in ('correct_analysis','short_lesson','fast_method','start_method'))+' '+' '.join(str(v) for v in analyses.values())
    if len(options)!=4 or any(not x.strip() for x in options): issues['not_four_or_blank_options'].append(qid)
    if len({option_norm(x) for x in options})!=len(options): issues['duplicate_options'].append(qid)
    if not isinstance(q.get('correct_index'),int) or q['correct_index'] not in range(4): issues['invalid_correct_index'].append(qid)
    if not str(q.get('correct_analysis','')).strip() or any(not str(analyses.get(str(i),'')).strip() for i in range(4)): issues['missing_option_specific_analysis'].append(qid)
    if re.search(r'\b(condition_wrong|truth_partial|wrong_condition|partial_truth)\b',review,re.I): issues['raw_internal_enum_in_review'].append(qid)
    if any(marker in texts for marker in ('از کلیدواژه جواب نده','روش کنترل:','صورت را به بخش‌های مستقل','صورت را به بخش های مستقل')): issues['generic_template_marker'].append(qid)
    if len(str(q.get('correct_analysis','')).strip())<70: issues['short_correct_analysis'].append(qid)
    exact[json.dumps([q.get('stimulus') or {},q.get('stem'),options],ensure_ascii=False,sort_keys=True)].append(qid)
    if q.get('semantic_fingerprint'): semantic[q['semantic_fingerprint']].append(qid)
    if row['access_pool']=='TRAIN' and row['selected_scope'] and not row['obsolete']:
        active.append({'id':qid,'priority':row['priority'],'microtopic':row['microtopic'],'stem':q.get('stem'),'options':options,'correct_index':q.get('correct_index'),'correct_analysis':q.get('correct_analysis'),'issues':[]})
for item in active:
    item['issues']=[kind for kind,ids in issues.items() if item['id'] in ids]
active.sort(key=lambda x:(-float(x['priority']),x['id']))
result={'integrity':integrity,'biology_total':len(rows),'active_train_selected':len(active),'source_counts':dict(Counter(r['source_type'] for r in rows)),'issue_counts':{k:len(v) for k,v in sorted(issues.items())},'issues':{k:sorted(v) for k,v in sorted(issues.items())},'exact_duplicate_groups':[v for v in exact.values() if len(v)>1],'semantic_duplicate_groups':[v for v in semantic.values() if len(v)>1],'highest_priority_active':active[:30]}
Path(sys.argv[2]).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'integrity':integrity,'biology_total':len(rows),'active_train_selected':len(active),'issue_counts':result['issue_counts'],'exact_duplicate_groups':len(result['exact_duplicate_groups']),'semantic_duplicate_groups':len(result['semantic_duplicate_groups'])},ensure_ascii=False,indent=2))
