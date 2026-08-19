# A3 Final Independent Persistence Review

**Role:** Independent post-completion persistence reviewer  
**Account label:** Manus A3 Lite  
**Review date:** 2026-08-19 UTC  
**No main/release:** This review creates no main commit, tag, APK, or release.

## Verdict

> **Source-composition verdict: PASS. Release-certification verdict: FAIL/PENDING because required Android API 35 runtime, migration execution, install/launch, signed-build, and visual Review/Map gates remain unrun.**

The completed standard persistence worker now resolves the prior source-level blockers. The final artifact is pinned to report commit `b78daecaa26ccc5c2a397cf71b043baae10fc9d6`, artifact commit `78f1a5a9c2ae1f3eb2ad4763626cf7b025c15442`, and overlay SHA-256 `d012e645ea10eb3302442c9ad8e83312b05dc915332b7a1ae42f0a41b7cc7e84`. The local extraction independently reproduced the expected hash, and `tests/verify_a3_second_pass.py` passed all twelve deterministic assertions.

## Pinned artifact verification

| Item | Observed value | Result |
|---|---|---|
| Final report commit | `b78daecaa26ccc5c2a397cf71b043baae10fc9d6` | **PASS**; parent is artifact commit `78f1a5a9c2ae1f3eb2ad4763626cf7b025c15442` |
| Artifact commit | `78f1a5a9c2ae1f3eb2ad4763626cf7b025c15442` | **PASS**; contains manifest, removed-path list, overlay, and report |
| Remote branch head | `b78daecaa26ccc5c2a397cf71b043baae10fc9d6` | **PASS**; matches requested final report commit |
| Second-pass overlay SHA-256 | `d012e645ea10eb3302442c9ad8e83312b05dc915332b7a1ae42f0a41b7cc7e84` | **PASS**; independently recomputed after extraction |
| Corrected Final-Hours source SHA | `ee706e9836bd499decae0a1d79ea643884ab4d1c` | **Recorded** in the final manifest; required predecessor |
| Frozen project/bank identity | ZIP `1344aca9…d046`; SQLite `d63219dd…673c` | **Preserved** by manifest and composition contract |

## Independent gate results

| Gate | Final result | Independent evidence and limitation |
|---|---|---|
| No exact-repeat TRAIN fallback after Final-Hours composition | **PASS** | Final `StudyRepository.kt` uses excluded IDs and evidence families throughout candidate selection, throws when distinct eligible TRAIN content is exhausted, and has no `poolIds("TRAIN")` fallback. Static verifier passed `no historical train repeat` and `no repeat fallback`. |
| Evidence-family suppression | **PASS** | Final `BankStore.kt` fingerprints subject, microtopic, normalized stem/options, masks numeric reskins and reusable shells, and receives `excludedEvidenceFamilies` in due, weak, primary, and final selection paths. |
| Follow-up/scenario suppression | **PASS with scope note** | Scenario-family metadata remains in `Question`/`AttemptEntity` and is preserved through submit/mastery; evidence-family suppression survives the composed repository. The final artifact does not introduce a separate named `followup` database field, so any follow-up suppression is represented through the composed evidence-family/scenario metadata rather than a standalone follow-up table. |
| Unique mastery semantics | **PASS** | Final `AdaptiveEngine` keeps distinct-question count based on unique IDs and gives exact correct repeats zero fresh mastery delta while retaining attempt/spacing/negative diagnostic evidence. The regression fixture asserts mastery unchanged, distinct count `1`, and attempts `2`. |
| Fail-closed malformed active session | **PASS at source/JVM level** | `ProgressPayloadValidator.session()` validates pool/phase/date/timestamps, non-empty unique IDs, bank eligibility, positions, JSON key membership/types, four-option orders, flags, elapsed values, analysis booleans, and error enums. Resume/navigation/completion call the validator; malformed state is snapshotted and closed. Device execution remains pending. |
| Fail-closed backup payload | **PASS at source/JVM level** | `ProgressPayloadValidator.backup()` runs before any Room rows are cleared and validates payload kind/schema, attempt uniqueness/identity/status/enum/bounds, mastery ranges, credit sources, simulation rows, active session, and settings. Legacy external restore is separately prevalidated and wrapped in rollback transaction. Runtime malformed-restore execution remains pending. |
| Atomic SIM `finishReview()` witness + done transition | **PASS at source level; runtime pending** | Final `finishReview()` validates the active session and wraps `markSimulationReviewed()` plus the `phase = done` upsert in one `database.withTransaction`. The Android fixture verifies both values survive database close/reopen, but it performs the transaction directly through the DAO rather than invoking the repository method on a device. |
| Persisted Review Map | **PASS at source/JVM level** | Repository reconstructs entries from active-session IDs, answers, flags, and session-scoped attempts; `QuestionMapSessionProjection` derives correct/wrong/blank and persisted test/review positions; ViewModel refreshes the map on resume, submit, finish-review, navigation, and restore. Visual/device flow remains pending. |
| Process recreation | **PARTIAL PASS** | Room close/reopen fixture preserves active session and reviewed SIM witness/done state. Full Android process-death flow through the app, ViewModel, Review Map, and restore UI was not run because API 35 runtime instrumentation was unavailable. |
| Stable IDs and progress preservation | **PASS at composition/static level** | Attempt/session/mastery identity remains question-ID based; unique `(sessionName, questionId)` index is retained; backup snapshots are retained before restore/wipe; frozen bank hashes are unchanged. Runtime migration and restore execution remain pending. |
| Non-destructive Room migration registration | **PASS at source level; runtime pending** | Database version is `4`; explicit `MIGRATION_1_2`, `MIGRATION_2_3`, and `MIGRATION_3_4` are registered; `3→4` only adds nullable `reviewedEpochMs`; no destructive migration fallback exists. Device migration fixture execution remains pending. |
| Backup/restore | **PASS at source level; runtime pending** | Export writes schema 4 and reviewed-SIM timestamps; restore validates before clearing, preserves pre-restore snapshots, reconstructs all entities, and transactionally applies valid payloads. API 35 valid/invalid restore execution remains pending. |

## Previous blocker comparison

| Prior blocker from the previous independent review | Status | Resolution evidence |
|---|---|---|
| Overlay conflict could reintroduce the exact-repeat TRAIN fallback | **RESOLVED at source composition** | The second-pass overlay is explicitly composed after corrected Final-Hours and includes the duplicate/evidence-family path. Final source throws on exhaustion rather than repeating; static gate passed. |
| SIM review witness and active-session `done` transition were separate writes | **RESOLVED at source composition** | Final `finishReview()` places both writes in one Room transaction and validates the active session first. Android fixture confirms durable paired values after close/reopen; repository-level device invocation is still pending. |
| Restore/session validation was too permissive | **RESOLVED at source/JVM level** | New `ProgressPayloadValidator` rejects malformed session and backup payloads before destructive clearing; tests cover duplicate IDs, foreign keys, duplicate attempts, and validator wiring. Runtime malformed-payload rollback remains pending. |
| Standard persistence worker had not advanced | **RESOLVED** | `parallel/a3-persistence-qa` advanced through artifact commit `78f1a5a9…` and final report commit `b78daeca…`; remote head matches the requested final report SHA. |

## Remaining release blockers

The prior code blockers are resolved, but the final release gate is not yet PASS. The worker’s own report states that API 35 runtime instrumentation and migration execution, signed/debug/release APK work, lint, install/launch, and visual Review/Map interaction were not run. Those omissions matter specifically for process recreation, actual Room upgrade execution, valid and malformed backup/restore behavior on device, and the complete answer → flag → submit → direct-jump → Review flow. No release should be published until those observed gates pass.

A minor semantic review note remains: `ProgressPayloadValidator.backup()` validates attempt pool membership but does not explicitly require every attempt’s pool to equal the referenced question’s `accessPool`; it does validate question subject, microtopic, and correct key. This did not invalidate the requested structural fail-closed checks, but it is a safe follow-up hardening candidate if the integrator wants stronger semantic payload validation.

## Deterministic evidence observed

The independently rerun `tests/verify_a3_second_pass.py` produced twelve PASS results: Final-Hours decision wiring; evidence-family bank filter; no historical TRAIN repeat; no repeat fallback; unique mastery repeat semantics; atomic SIM finish; review witness; fail-closed session; fail-closed restore; session attempts query; Review Map projection; and schema-v4 migration. The artifact hash independently matched the expected `d012e645…7e84` value.

## Required final-owner actions

The foreman must apply the corrected Final-Hours predecessor and this second-pass overlay in the documented order, then run API 35 migration, malformed and valid restore, process recreation, Review/Map visual flow, Kotlin/JVM, lint, debug/release signing, install/launch, packaged-bank, and all final-hours gates. This review provides independent source-level PASS evidence only; it does not certify a release.

## References

[1]: https://github.com/rynmrde/Konkor/commit/b78daecaa26ccc5c2a397cf71b043baae10fc9d6 "Final persistence report commit"
[2]: https://github.com/rynmrde/Konkor/commit/78f1a5a9c2ae1f3eb2ad4763626cf7b025c15442 "Final persistence artifact commit"
[3]: https://github.com/rynmrde/Konkor/commit/ee706e9836bd499decae0a1d79ea643884ab4d1c "Corrected Final-Hours composition commit"
[4]: https://github.com/rynmrde/Konkor/commit/72dc76e56b7ae625ad1904c76910eeaec5f90f58 "Original observed main baseline"