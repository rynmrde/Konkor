# LITE A3 — Room / Migration / Persistence Scan

**Role:** Lite support worker — Room/migration scan  
**Account label:** Manus account A3  
**Worker branch:** `parallel/lite-a3-room-migration-scan`  
**Baseline source:** `origin/main` fetched locally and verified through the connected Composio GitHub route  
**Baseline commit:** `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
**Latest baseline subject:** `ci: publish rescue directly without artifact quota`  
**Scan date:** 2026-08-19 UTC  
**Scope:** Static audit of the latest rescue overlay (`radiology_v614_rescue_patch/overlay.tar.xz`) and its migration/persistence tests. No main branch, release, or bank artifact was modified.

## Executive assessment

The latest rescue overlay uses a **Room schema version 3** with explicit `1→2` and `2→3` migrations and no destructive fallback. Active sessions, attempts, mastery, due credits, settings, simulation results, legacy-import state, and recovery snapshots are represented in Room. Submitted-session persistence is transactionally grouped, and the existing Android tests cover a basic legacy import and answer/review/reopen/SIM1 resume path.

The principal integration risks are not missing migrations. They are **restore-input validation boundaries, transient Day Selector state, legacy duplicate/invalid-row handling, and test coverage gaps around process recreation, migration fixtures, and unique-question accounting**. These should be treated as release-gate risks for any incoming persistence or Room change.

> Static conclusion: the schema migration path is structurally safe for the declared V1–V3 history, but the release is not fully migration-gate-complete until malformed backup/session fixtures, duplicate legacy rows, process recreation, and Day Selector recovery are tested deterministically.

## Verified implementation map

| Area | Evidence in overlay | Assessment |
|---|---|---|
| Room schema | `ProgressDatabase.kt:253-304`; eight entities; `version = 3`; `exportSchema = true` | Explicit schema versioning is present. |
| Migration `1→2` | `ProgressDatabase.kt:272-281` | Adds `active_session.cueShown` and creates `simulation_result`. |
| Migration `2→3` | `ProgressDatabase.kt:285-293` | Adds four attempt evidence columns and `simulation_result.remediationJson`. |
| Active session | `ActiveSessionEntity`; JSON fields for IDs, position, answers, confidence, option orders, flags, elapsed time, analyses, error types | Process-resumable session state is stored in Room. |
| Attempt history | `AttemptEntity`; unique index on `(sessionName, questionId)` | Prevents the same question from being inserted twice in one session, but import input is not explicitly deduplicated before insert. |
| Mastery | `MasteryEntity.distinctQuestions`, attempts, exam attempts, error and due fields | Supports unique-mastery and adaptive planning, subject to engine correctness. |
| SIM results | `SimulationResultEntity`; pool is primary key; question IDs and leak count persisted | SIM result persistence exists; selection is expected to enforce disjointness in `BankStore`/repository. |
| Settings | `AppSettingsEntity` | Theme, study mode, motion, text scale, focus, breaks, and cadence persist. |
| Recovery snapshots | `ProgressSnapshotEntity` | Wipe, restart, incompatible-session isolation, export, and restore retain recovery material. |
| Legacy import | `LegacyProgressImporter.kt` | One-way V5 bridge; raw input is preserved before interpretation; only existing bank IDs are converted. |
| Backup/restore | `StudyRepository.kt:538-594` | JSON schema and bank hash are checked; data replacement occurs in a Room transaction after a pre-restore snapshot. |
| Day Selector | `StudyViewModel.kt:32-99,245-275` | Selected date is UI state only, not Room-persisted; a new ViewModel defaults selection to today. |

## Migration and persistence findings

### Schema migration safety

`MIGRATION_1_2` adds the `cueShown` column with a non-null default and creates `simulation_result`. `MIGRATION_2_3` adds all later non-null columns with defaults, including `remediationJson`. The builder registers both migrations and does not call `fallbackToDestructiveMigration()`. This is a strong baseline for non-destructive upgrade behavior.

The declared migration history is nevertheless only directly exercised by code inspection in this scan. The visible Android migration fixture is an **external V5 JSON import fixture**, not a Room 1→2 or 2→3 database fixture. A release gate should create a temporary database at each prior schema, insert representative rows, run the migration, and assert that old fields and newly defaulted fields survive.

### Stable IDs and duplicate accounting

`Question.id` is the identity used by attempts, active sessions, backup validation, and legacy conversion. `AttemptEntity` has a unique `(sessionName, questionId)` index, while `MasteryEntity.distinctQuestions` is maintained by the adaptive engine rather than constrained by Room. The repository excludes previously attempted IDs during ordinary TRAIN selection and rejects any previously attempted SIM question.

The unique index protects one session from duplicate insertions, but it is not a substitute for selection and import validation. A malformed or old export containing repeated rows for the same session can cause restore/import failure or an integrity exception. Deterministic fixtures must cover exact duplicates, reordered-option duplicates, and repeated IDs across separate sessions, verifying that repeats count as attempts but never inflate `distinctQuestions`.

### Active-session serialization and review resume

The full active session is serialized into Room, including test/review positions, answer and confidence maps, option orders, flags, elapsed time, analyses-seen state, error types, phase, timestamps, and cue state. `submit()` writes attempts, mastery, due credits, the review-phase session, and simulation result inside one Room transaction. Reopening the repository reads the active session from Room and reconstructs the current question from bank ID.

The current serialization contract does not validate all nested JSON values on restore. `sessionCompatible()` checks that each referenced question exists and is eligible for the session pool, but does not assert that IDs are unique, option-order arrays are permutations of `0..3`, answers/confidence/error keys belong to the session, or positions are within bounds. A malformed backup can therefore be accepted as compatible and fail later in UI or review code. This is a high-priority hardening target for the persistence worker.

### Backup and restore

The export identifies kind `radiology1405_v6_1_progress`, schema `3`, and `BankStore.EXPECTED_DB_SHA256`. Restore accepts schemas 1–3 and two bank hashes, checks every attempt question ID against the installed bank, snapshots current state, then clears and repopulates progress in a transaction. V5-shaped input is routed through the legacy importer and receives a pre-restore snapshot.

The restore boundary does not similarly validate every active-session question ID before parsing all session fields, every due-credit `sourceQuestionId`, mastery subject/microtopic consistency, simulation pool membership, simulation question uniqueness, or attempt status/confidence/error enum values. It also accepts the older hard-coded bank hash without a documented migration map in this code path. These are compatibility and data-integrity risks, not evidence that the current bank is wrong.

### Legacy import

The importer preserves the raw legacy payload before parsing and records a status. It converts only attempts whose question IDs still exist in the installed bank, rebuilds mastery from chronological imported attempts, clamps legacy display settings, and imports only TRAIN active rounds. After import, repository initialization calls incompatible-session isolation, which can snapshot and delete a session whose questions are no longer eligible or safe.

The importer maps legacy attempts using `sessionName = legacy-day-round`, so duplicate legacy rows with the same question ID in one round collide with the Room unique index. The conversion also accepts legacy `pool` strings into `AttemptEntity` without normalization. Fixtures should cover duplicate rows, unknown IDs, malformed answers, unsupported pools, and a mixed TRAIN/SIM active round. The expected behavior should be explicit: preserve raw input, avoid partial progress corruption, and report a stable non-crashing status.

### Day Selector and process recreation

The selected plan date is held in `StudyUiState.selectedPlanDate`. It is passed to `startOrResume`, but it is not stored in `AppSettingsEntity`, `ActiveSessionEntity`, or a separate Room table. `refreshAll()` falls back to the current plan when the ViewModel is recreated. This is acceptable only if the intended contract is “selection lasts for the current ViewModel”; it does not satisfy a stronger interpretation of persistent Day Selector selection across process death.

Active sessions themselves are persisted and are the stronger process-recreation path. A deterministic instrumentation test should kill/recreate the activity or process after selecting a non-today training day, after answering and flagging, during review, and after SIM1 start. The test should distinguish expected recovery of the active session from the currently transient selected-day choice.

## Risk matrix for incoming worker changes

| Risk | Evidence | Impact | Likelihood | Required guard before integration | Priority |
|---|---|---:|---:|---|---:|
| Room schema version changed without a complete migration | `ProgressDatabase.kt:253-301` | Data loss or app-open crash | Medium | Add old-schema fixtures and run `MigrationTestHelper` for every version edge | P0 |
| Destructive fallback introduced | Current builder has explicit migrations and no fallback | Permanent progress loss | Medium | Static grep gate rejecting `fallbackToDestructiveMigration` and runtime upgrade test | P0 |
| Active-session JSON accepted with duplicate IDs or invalid option order | `sessionCompatible()` validates bank/pool eligibility but not nested shape | Review crash or wrong answer mapping | High | Malformed restore/session fixtures; validate IDs, positions, answers, confidence, error keys, and option permutations | P0 |
| Legacy duplicate rows collide with unique attempt index | `AttemptEntity` unique `(sessionName, questionId)`; importer batches legacy rows | Import failure or inconsistent partial state | Medium | Duplicate legacy fixture; assert raw preservation and atomic/no-partial conversion behavior | P0 |
| Backup restores unsupported references | Restore checks attempt IDs only | Dangling due credits, SIM references, or later crash | Medium | Validate all question-bearing payloads and reject or quarantine invalid records | P1 |
| Accepted old bank hash lacks explicit mapping | `restoreBackup():571-574` | Semantically stale progress accepted silently | Medium | Record source bank identity and test old-hash restore against stable IDs/mapping policy | P1 |
| Day Selector choice lost after process recreation | `selectedPlanDate` is ViewModel-only | User starts wrong day or loses intended plan | High | Decide contract; persist selected date or document/reset behavior and test it | P1 |
| Repeated questions inflate mastery coverage | `distinctQuestions` is engine-maintained; attempts are repeatable across sessions | Misleading mastery and ROI planning | Medium | Cross-session repeated-ID fixture; assert attempts increase while unique count does not | P1 |
| Room singleton remains open after repository close | `StudyRepository.close()` closes bank only | Test contamination/resource pressure | Medium | Add lifecycle test and determine whether database lifetime is application-scoped by design | P2 |
| Malformed legacy field values leak raw enums or invalid pools | Importer copies some legacy strings directly | UI or planner state corruption | Medium | Enum/pool normalization fixture and UI-string leakage scan | P2 |

## Safe deterministic test plan

The following tests are safe to add or run without changing scientific bank content.

| Test | Fixture | Assertions |
|---|---|---|
| `migration_1_to_2_preservesRowsAndAddsDefaults` | Create schema-1 DB with active session and attempts; run `MIGRATION_1_2` | Existing rows remain; `cueShown=false`; `simulation_result` exists and is writable. |
| `migration_2_to_3_preservesRowsAndAddsEvidenceDefaults` | Create schema-2 DB with attempt and simulation rows; run `MIGRATION_2_3` | Existing data remains; difficulty `2`, scenario family empty, boolean evidence false, remediation `{}`. |
| `legacy_duplicateRows_doNotPartiallyCorruptProgress` | V5 export with two identical question rows in one day/round | Import returns a documented status, raw snapshot remains byte-for-byte equal, and no partial duplicate history is left. |
| `restore_rejectsMalformedActiveSession` | Valid backup plus duplicate session IDs, invalid position, invalid option order, and answer key outside session IDs | Restore returns false or quarantines the session; prior state remains recoverable; no later review crash. |
| `restore_validatesAllQuestionBearingPayloads` | Backup with valid attempts but unknown due-credit source, SIM ID, or active-session ID | Restore rejects or explicitly drops only invalid records according to documented policy; it never creates dangling references. |
| `repeatedQuestionAcrossSessions_doesNotIncreaseUniqueMastery` | Submit the same stable ID in two sessions, with a different session name | Attempt count increases by two; distinct-question count increases once; SIM disjointness remains enforced. |
| `activeSession_survivesReopenDuringTestAndReview` | Answer, confidence, flag, elapsed, navigate, submit; close/recreate repository | All serialized fields and the review position are identical after reopen. |
| `daySelector_recreationContract` | Select a non-today plan, recreate ViewModel/process before starting | Assert either persisted selected date or the intentionally documented reset-to-today behavior. |
| `restore_isAtomicOnMalformedRow` | Valid existing state; backup with one malformed attempt row | Existing state and pre-restore snapshot remain intact; no half-restored database. |
| `wipeProgress_preservesSettingsAndCreatesRecoverySnapshot` | Seed settings, attempts, mastery, and active session; call wipe | Attempts/mastery/session are cleared, settings remain, and a pre-wipe snapshot exists. |

## Recommended handoff to the persistence medium worker

The highest-value compatible work is **restore/session payload validation plus deterministic migration fixtures**, not a bank or UI refactor. The worker should first add a small validation boundary around imported active sessions and question-bearing backup records, then add Room `MigrationTestHelper` coverage for 1→2 and 2→3. Any behavior change must remain non-destructive, preserve raw rejected payloads, and be surfaced to the Foreman with before/after test output.

No persistence-medium worker branch or persistence-specific report was present in the fetched remote branch inventory at scan time. I therefore did not edit another worker’s branch or report. A helper branch can safely carry only deterministic validation/test scaffolding after the medium worker’s target branch is identified; no such patch was invented on this lite branch.

## Residual coverage and release-gate status

This is a static scan of the latest rescue overlay, not a release certification. I did not run Android instrumentation, a signed build, lint, packaged-bank inspection, or an emulator process-death test. The release owner must rerun those gates after integration. In particular, migration/progress preservation, active-session malformed-input behavior, Day Selector recreation semantics, unique mastery accounting, and signed-APK verification remain required observed outputs.

## References

[1]: https://github.com/rynmrde/Konkor/tree/72dc76e56b7ae625ad1904c76910eeaec5f90f58 "Konkor baseline commit 72dc76e56b7ae625ad1904c76910eeaec5f90f58"
[2]: https://github.com/rynmrde/Konkor/blob/72dc76e56b7ae625ad1904c76910eeaec5f90f58/radiology_v614_rescue_patch/MANIFEST.txt "Konkor V6.1.4 rescue patch manifest"