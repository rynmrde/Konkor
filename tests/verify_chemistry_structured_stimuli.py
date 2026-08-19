#!/usr/bin/env python3
"""Portable V6.1.4 regression test for Chemistry table/comparison stimuli."""
from __future__ import annotations
import gzip
import hashlib
import json
import sqlite3
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'app'
ASSET = APP / 'src/main/assets/radiology1405_bank_v6_1.db.gz'
KOTLIN = APP / 'src/main/java/com/radiology1405/prep'
EXPECTED_GZIP = 'b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14'
EXPECTED_IDS = {
    'v3_chem_19_10', 'v3_chem_19_11', 'v3_chem_19_12', 'v3_chem_19_13',
    'v3_chem_20_03', 'v3_chem_20_18', 'v3_chem_20_19', 'v3_chem_20_20',
    'v3_chem_26_03', 'v3_chem_26_10', 'v3_chem_26_11', 'v3_chem_26_12', 'v3_chem_26_13',
    'v3_chem_54_07', 'v3_chem_54_11', 'v3_chem_54_12', 'v3_chem_54_13',
    'v3_chem_55_14', 'v3_chem_55_15', 'v3_chem_55_16',
}

assert hashlib.sha256(ASSET.read_bytes()).hexdigest() == EXPECTED_GZIP
with tempfile.NamedTemporaryFile(suffix='.db') as tmp:
    with gzip.open(ASSET, 'rb') as source:
        tmp.write(source.read())
    tmp.flush()
    db = sqlite3.connect(tmp.name)
    records = []
    for (raw,) in db.execute("SELECT full_json FROM question WHERE subject='شیمی' AND obsolete=0"):
        question = json.loads(raw)
        stimulus = question.get('stimulus') or {}
        if stimulus.get('type') not in {'data_table', 'comparison'}:
            continue
        assert len(question['options']) == 4 and len(set(question['options'])) == 4, question['id']
        assert question['correct_index'] in range(4), question['id']
        assert question['correct_analysis'].strip(), question['id']
        assert all((question.get('distractor_analyses') or {}).get(str(index), '').strip() for index in range(4)), question['id']
        if stimulus['type'] == 'data_table':
            headers, rows = stimulus.get('headers') or [], stimulus.get('rows') or []
            assert stimulus.get('caption', '').strip() and len(headers) >= 2 and rows, question['id']
            assert all(len(row) == len(headers) and all(str(cell).strip() for cell in row) for row in rows), question['id']
        else:
            assert stimulus.get('left', '').strip() and stimulus.get('right', '').strip(), question['id']
        records.append(question['id'])
    db.close()
assert set(records) == EXPECTED_IDS and len(records) == 20, sorted(set(records) ^ EXPECTED_IDS)

models = (KOTLIN / 'data/Models.kt').read_text(encoding='utf-8')
ui = (KOTLIN / 'ui/RadiologyApp.kt').read_text(encoding='utf-8')
repo = (KOTLIN / 'data/StudyRepository.kt').read_text(encoding='utf-8')
for token in ['TableStimulus', 'ComparisonStimulus', 'stimulus?.optString("type") == "data_table"', 'stimulus?.optString("type") == "comparison"', 'tableStimulus = table', 'comparisonStimulus = comparison']:
    assert token in models, token
assert 'private fun QuestionStimulus(question: Question)' in ui
start_test = ui.index('private fun TestQuestion')
start_review = ui.index('private fun ReviewQuestion')
test_body = ui[start_test:start_review]
review_body = ui[start_review:]
assert 'QuestionStimulus(question)' in test_body and 'QuestionStimulus(question)' in review_body
for token in ['table.headers.forEach', 'table.rows.forEach', 'comparison.left', 'comparison.right']:
    assert token in ui, token
# Resume is ID-based: both activeSummary and startOrResume reload the current question from BankStore.
assert repo.count('?.let(bank::question)') >= 2
assert 'suspend fun activeSummary()' in repo and 'suspend fun startOrResume' in repo
print('CHEMISTRY_STRUCTURED_STIMULI_PORTABLE=PASS count=20 test=complete review=complete resume=id_reload')
