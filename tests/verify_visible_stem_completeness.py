#!/usr/bin/env python3
"""Fail closed when a visible A/B paired-statement question omits either statement."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

EXPECTED_GZ = 'b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14'
PAIR_STEM = re.compile(r'دو\s+عبارت\s+A\s+و\s+B', re.I)
PAIR_OPTIONS = re.compile(r'A\s*(?:درست|نادرست).*?B\s*(?:درست|نادرست)', re.I | re.S)
A_CLAIM = re.compile(r'(?:^|\n)\s*(?:عبارت\s*)?A\s*[:=].{8,}', re.I)
B_CLAIM = re.compile(r'(?:^|\n)\s*(?:عبارت\s*)?B\s*[:=].{8,}', re.I)

parser = argparse.ArgumentParser()
parser.add_argument('--bank-gz', type=Path, required=True)
parser.add_argument('--report', type=Path)
args = parser.parse_args()
assert hashlib.sha256(args.bank_gz.read_bytes()).hexdigest() == EXPECTED_GZ, 'unexpected frozen bank gzip'
tmp = args.bank_gz.with_suffix('.a2-visible-stem.tmp.db')
with gzip.open(args.bank_gz, 'rb') as source, tmp.open('wb') as target:
    target.write(source.read())
conn = sqlite3.connect(f'file:{tmp}?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
missing = []
for row in conn.execute('SELECT id, subject, microtopic, access_pool, selected_scope, obsolete, full_json FROM question'):
    raw = json.loads(row['full_json'])
    stem = str(raw.get('stem', ''))
    options = '\n'.join(map(str, raw.get('options') or []))
    if PAIR_STEM.search(stem) and PAIR_OPTIONS.search(options) and not (A_CLAIM.search(stem) and B_CLAIM.search(stem)):
        missing.append({
            'id': row['id'], 'subject': row['subject'], 'microtopic': row['microtopic'],
            'access_pool': row['access_pool'], 'selected_scope': bool(row['selected_scope']), 'obsolete': bool(row['obsolete']),
            'needs_human_review': bool(raw.get('needs_human_review', False)),
            'eligible_for_safety_evidence': bool(raw.get('eligible_for_safety_evidence', True)),
            'visible_stem': stem, 'options': raw.get('options'),
        })
tmp.unlink(missing_ok=True)
active = [q for q in missing if q['access_pool'] == 'TRAIN' and q['selected_scope'] and not q['obsolete']]
safety_reachable = [q for q in active if q['eligible_for_safety_evidence'] and not q['needs_human_review']]
summary = {
    'status': 'FAIL' if missing else 'PASS',
    'missing_visible_pair_claims': len(missing),
    'active_train': len(active),
    'safety_reachable_train': len(safety_reachable),
    'by_subject': dict(sorted(Counter(q['subject'] for q in missing).items())),
    'ids': [q['id'] for q in missing],
}
if args.report:
    args.report.write_text(json.dumps({'summary': summary, 'items': missing}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False))
sys.exit(1 if missing else 0)
