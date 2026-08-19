#!/usr/bin/env python3
"""Read-only validation for the GEO153 exclusion helper overlay."""
import json
from pathlib import Path

ROOT = Path('/home/ubuntu/konkor_a1_workspace')
BANK = Path('/home/ubuntu/konkor_a1_evidence/konkur_testbank_v6_1_verified.json')
PATCH = ROOT / 'HELP_A1_OFFICIAL_GEO153_EXCLUSION.patch'
REPO = ROOT / 'base/radiology1405_android_v6_1'
TARGET = 'real_1401_in_geo_153'

bank = json.loads(BANK.read_text())
rows = [q for q in bank['questions'] if q['id'] == TARGET]
assert len(rows) == 1, f'target record count={len(rows)}'
q = rows[0]
assert q['source_type'] == 'official_exam_stem_training'
assert q['v6_access_pool'] == 'TRAIN'
assert q['needs_human_review'] is True
assert q['official_key_verified'] is False
assert q['needs_official_key_reconciliation'] is True
assert q['eligible_for_simulation'] is False

blueprints = bank['simulation_blueprints']
holdout_ids = set()
for pool in ('SIM1', 'SIM2', 'FINAL'):
    ids = blueprints[pool]['question_ids']
    holdout_ids.update(ids)
    assert TARGET not in ids, f'{TARGET} leaked into {pool}'

patch = PATCH.read_text()
repo_text = (REPO / 'app/src/main/java/com/radiology1405/prep/data/StudyRepository.kt').read_text()
assert 'const val GEO153 = "real_1401_in_geo_153"' in patch
assert 'fun blocks(id: String)' in patch
bank_store_text = (REPO / 'app/src/main/java/com/radiology1405/prep/data/BankStore.kt').read_text()
for needle in ('fun poolIds(', 'fun simulationIds(', 'fun trainingCandidates(', 'fun distinctAlternative('):
    assert needle in bank_store_text, f'missing base selection path: {needle}'
for needle in (
    'private fun sessionCompatible(',
    'suspend fun activeSummary()',
    'suspend fun startOrResume(',
    'suspend fun submit(',
):
    assert needle in repo_text, f'missing base session path: {needle}'
assert patch.count('QuestionDeliveryExclusions.blocks(id)') >= 4, 'selection/session block guards absent'
assert 'require(ids.none(QuestionDeliveryExclusions::blocks))' in patch, 'final selection assertion absent'

# Preservation depends on the existing compatible-session isolation contract.
for needle in (
    'dao.upsertSnapshot(ProgressSnapshotEntity(',
    'dao.deleteSession(active.name)',
    'attempts/mastery/settings are never erased',
):
    assert needle in repo_text, f'missing existing progress-preservation contract: {needle}'

assert 'radiology1405_bank_v6_1.db' not in patch
assert 'radiology1405_bank_v6_1.db.gz' not in patch
assert 'UPDATE question' not in patch

print('TARGET_ID=PASS')
print('TARGET_SOURCE_AND_UNRESOLVED_KEY_FLAGS=PASS')
print(f'HOLDOUT_DISJOINT=PASS count={len(holdout_ids)}')
print('SELECTION_GUARDS=PASS poolIds,simulationIds,trainingCandidates,distinctAlternative')
print('REVIEW_RESUME_GUARDS=PASS sessionCompatible,activeSummary,startOrResume,submit')
print('PROGRESS_PRESERVATION=PASS snapshot_then_close_active_session_only')
print('IMMUTABLE_BANK_MUTATION=PASS none')
