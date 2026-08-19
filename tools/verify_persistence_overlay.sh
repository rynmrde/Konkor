#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
overlay="$repo_root/radiology_v614_rescue_patch/overlay.tar.xz"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

[[ -f "$overlay" ]] || { echo "FAIL: rescue overlay missing: $overlay"; exit 1; }
tar -xJf "$overlay" -C "$work"
root="$work/app/src/main/java/com/radiology1405/prep"
db="$root/data/ProgressDatabase.kt"
repo="$root/data/StudyRepository.kt"
importer="$root/data/LegacyProgressImporter.kt"

for file in "$db" "$repo" "$importer"; do
  [[ -f "$file" ]] || { echo "FAIL: required persistence file missing: $file"; exit 1; }
done

grep -q 'version = 3' "$db" || { echo 'FAIL: Room schema version 3 not declared'; exit 1; }
grep -q 'Migration(1, 2)' "$db" || { echo 'FAIL: migration 1->2 missing'; exit 1; }
grep -q 'Migration(2, 3)' "$db" || { echo 'FAIL: migration 2->3 missing'; exit 1; }
! grep -q 'fallbackToDestructiveMigration' "$db" || { echo 'FAIL: destructive Room fallback present'; exit 1; }
grep -q 'Index(value = \["sessionName", "questionId"\], unique = true)' "$db" || { echo 'FAIL: per-session question uniqueness index missing'; exit 1; }
grep -q 'suspend fun persistSubmittedSession' "$db" || { echo 'FAIL: transactional submit persistence helper missing'; exit 1; }
grep -q 'database.withTransaction' "$repo" || { echo 'FAIL: repository transaction boundary missing'; exit 1; }
grep -q 'radiology1405_v6_1_progress' "$repo" || { echo 'FAIL: current backup kind missing'; exit 1; }
grep -q 'BankStore.EXPECTED_DB_SHA256' "$repo" || { echo 'FAIL: backup bank hash guard missing'; exit 1; }
grep -q 'dao.upsertSnapshot' "$repo" || { echo 'FAIL: recovery snapshot writes missing'; exit 1; }
grep -q 'Raw preservation happens before interpretation' "$importer" || { echo 'FAIL: legacy raw-preservation marker missing'; exit 1; }
grep -q 'bank.question(id)' "$importer" || { echo 'FAIL: legacy stable-ID existence check missing'; exit 1; }

echo 'PASS: persistence overlay static invariants verified'
echo "schema=3 migrations=1->2,2->3 destructive_fallback=absent unique_attempt_index=present transaction=present backup_hash_guard=present legacy_raw_preservation=present"