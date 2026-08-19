# A3 Persistence, Migration, and Progress Preservation QA

> **Role:** Room, migration, progress preservation, and cross-system regression QA.  
> **Account label:** A3 / `KONKOR-A3-M2-PERSISTENCE-QA`.  
> **Assigned branch:** `parallel/a3-persistence-qa`.  
> **Original upstream baseline:** [`72dc76e56b7ae625ad1904c76910eeaec5f90f58`](https://github.com/rynmrde/Konkor/commit/72dc76e56b7ae625ad1904c76910eeaec5f90f58).  
> **Corrected Final-Hours composition commit:** [`ee706e9836bd499decae0a1d79ea643884ab4d1c`](https://github.com/rynmrde/Konkor/commit/ee706e9836bd499decae0a1d79ea643884ab4d1c).  
> **Prior local A3 commit:** `efb2f9172e75300ffeef64ab81ed650abd180f39` (`qa: add persistence migration and review map regression overlay`).

## SECOND_PASS_REVIEW

> **Local composition status: PASS for deterministic static guards, JVM tests, Kotlin compilation, and Android-test-source compilation. This is not release approval.** Android API 35 runtime instrumentation, signed build, APK installation, migration execution on device, Review/Map visual interaction, backup/restore runtime execution, packaged-bank inspection, and all release gates remain foreman work.

The independent review correctly identified that the first A3 overlay could not safely be overlaid wholesale with the Final-Hours and duplicate/session candidates because they each replaced `StudyRepository.kt`. This second pass reconstructed the full frozen V6.1 source, applied the V6.1.4 base overlay, hash-verified the corrected Final-Hours archive, and then used explicit three-way source composition. The resulting candidate does not restore the previously forbidden exact-repeat TRAIN fallback.

| Evidence item | Observed value | Result |
|---|---:|---|
| Frozen V6.1 project ZIP SHA-256 | `1344aca90474ac96e27e94ba754ebafd42778e2ceaab91f9a5fb1be2e882d046` | **PASS** |
| Frozen verified JSON SHA-256 | `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d` | **Preserved** |
| Frozen expanded SQLite SHA-256 | `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c` | **Preserved** |
| Corrected Final-Hours archive SHA-256 | `59a8ff9e5aa62bbe164fa8dffb6fc5056795eeb5ee82b511cc55fbff9281599d` | **PASS** |
| Revised A3 delta archive SHA-256 | `d012e645ea10eb3302442c9ad8e83312b05dc915332b7a1ae42f0a41b7cc7e84` | **PASS** |

## Composed persistence contract

The recomposed `StudyRepository.kt` retains the corrected Final-Hours selector’s dynamic recommendation and its **fail-safe error** when distinct eligible TRAIN content is exhausted. It also retains the duplicate/session candidate’s prior-attempt, within-block ID, and evidence-family suppression. Therefore, a normal TRAIN block cannot silently fall back to an exact repeat, cannot include duplicate stable IDs, and cannot treat cosmetic variants in the same evidence family as independent coverage.

| Requirement | Composed safeguard | Progress/identity effect |
|---|---|---|
| No exact-repeat TRAIN fallback | Selection fills only from distinct alternatives and family-filtered candidates, then throws a safe exhausted-content error rather than repeating. | Historical IDs remain stable; no new attempt is fabricated. |
| Evidence-family suppression | `BankStore` and the repository pass `excludedEvidenceFamilies` throughout due, weak, primary, and final candidate selection. | Cosmetic variants cannot inflate coverage. |
| Unique mastery | `AdaptiveEngine` preserves the maximum distinct question count; an exact correct repeat gets zero fresh mastery delta while wrong/blank repeats remain diagnostic evidence. | `total_attempts` and repeat evidence remain useful without inflating `unique_training_questions`. |
| Malformed active session | `ProgressPayloadValidator.session()` validates phase, pool, stable question IDs, pool eligibility, positions, JSON payload keys/types, option permutations, and internal enums before resume/navigation/completion. | Invalid session JSON is snapshotted and closed; attempts, mastery, settings, and bank identity remain intact. |
| Malformed V6/V6.1 backup | `ProgressPayloadValidator.backup()` validates payload kind/schema, question identity, attempt uniqueness/statuses, mastery bounds, credits, SIM rows, settings, and active session **before** any current Room row is cleared. | Invalid imports return `false`; existing progress is retained. |
| Legacy external backup | `LegacyProgressImporter.isValidExternalPayload()` rejects malformed external attempt/round data before destructive replacement, while preserving the pre-restore snapshot. | No malformed legacy payload may erase current progress. |
| Atomic SIM review completion | `finishReview()` executes `markSimulationReviewed()` and `activeSession.phase = done` inside one `database.withTransaction`. | A process stop cannot persist a reviewed witness without the matching session transition, or vice versa. |
| Review/Map persistence | The canonical `QuestionMapSessionProjection` plus A3 `persistedQuestionMap()` derive state from the active session and session-scoped attempt rows. | Correct/wrong/blank, answer, flag, current position, and direct jump survive resume, recreation, Review reopening, and a valid restore. |
| Room migration | Existing explicit `MIGRATION_1_2`, `MIGRATION_2_3`, and corrected Final-Hours `MIGRATION_3_4` are registered; no destructive migration fallback is introduced. | Existing Room rows and stable IDs stay on a documented forward path. |

## Revised overlay and integration order

The new artifact is `radiology_v615_a3_second_pass_patch/overlay.tar.xz`. It contains only the A3 delta relative to the corrected Final-Hours tree, including the composed repository, duplicate-suppression bank selector, persistence validator, durable Map wiring, and regression fixtures. It excludes the immutable bank, expanded SQLite asset, source gzip, generated audio, build outputs, package identity, signing material, tags, and release assets.

> Apply the corrected Final-Hours archive first, then this A3 archive. Remove the one stale test path listed in `REMOVED_PATHS.txt`. Do **not** blindly untar a later duplicate/UI overlay over `BankStore.kt`, `StudyRepository.kt`, `StudyViewModel.kt`, or `RadiologyApp.kt`; source-level merge is required because this A3 revision already contains the currently available duplicate/evidence-family semantics and the canonical corrected Question Map entry model.

| File group | Second-pass role |
|---|---|
| `StudyRepository.kt`, `BankStore.kt`, `AdaptiveEngine.kt` | Corrected Final-Hours + no-repeat/evidence-family + unique-mastery composition. |
| `ProgressDatabase.kt`, `LegacyProgressImporter.kt`, `ProgressPayloadValidator.kt` | Explicit migration, session-scoped attempts, pre-clear validation, raw/pre-restore protection. |
| `StudyViewModel.kt`, `RadiologyApp.kt` | Durable Question Map refresh and full tappable state rendering. |
| `ProgressPayloadValidatorTest.kt`, `AdaptiveEngineTest.kt`, `ProgressPersistenceTest.kt` | Malformed payload, distinct-mastery, transaction/recreation, and migration-registration coverage. |
| `tests/verify_a3_second_pass.py` | Deterministic structural regression guard for the composed contract. |

## Executed validation

| Gate | Observed result | Evidence |
|---|---|---|
| Corrected Final-Hours archive hash | **PASS** | SHA-256 matched `59a8ff…1599`. |
| A3 composed static guard | **PASS** | `tests/verify_a3_second_pass.py` passed Final-Hours decision, evidence-family filter, no historical TRAIN repeat/fallback, unique mastery, atomic witness, fail-closed backup/session, session query, map projection, and schema v4 checks. |
| Corrected Final-Hours static gate | **PASS** | `tests/verify_final_hours_v615.py` reported `PASS — V6.1.5 Final-Hours source gate`. |
| Duplicate/session deterministic selector gate | **PASS** | `tests/verify_a2_duplicate_session.py` reported 1,216 frozen IDs, 594 safe TRAIN candidates, two 117-question SIM pools, 2,000 normal-block trials, and 61 adaptive short-block cases without repeat. |
| JVM unit suite | **PASS** | `:app:testDebugUnitTest` completed within Gradle `BUILD SUCCESSFUL`; includes the new pure malformed-payload fixture and merged unique-mastery fixture. |
| Kotlin application compilation | **PASS** | `:app:compileDebugKotlin` completed within Gradle `BUILD SUCCESSFUL`. |
| Android-test Kotlin compilation | **PASS** | `:app:compileDebugAndroidTestKotlin` completed within Gradle `BUILD SUCCESSFUL`; `ProgressPersistenceTest` carries the atomic SIM review recreation assertion and all three migrations. |
| Exact publishable archive re-extraction | **PASS** | The archive was extracted onto a fresh corrected-Final-Hours tree; the A3 and Final-Hours static guards, staged duplicate guard, `:app:testDebugUnitTest`, `:app:compileDebugKotlin`, and `:app:compileDebugAndroidTestKotlin` all completed with `BUILD SUCCESSFUL` (42 Gradle tasks). |
| Historical V6.1 validator | **PARTIAL / version-inapplicable** | Its frozen-bank checks passed, then its `verify_native_experience_v61.py` asserted historical `6.1.4/165`; the corrected candidate intentionally reports `6.1.5/166`. It is not claimed as a full pass. |
| API 35 runtime instrumentation and migration execution | **NOT RUN** | Local VM lacks `/dev/kvm`; source compilation passed, but device execution remains required. |
| Lint, debug/release APK, signing, install/launch | **NOT RUN in this second pass** | Foreman gates. |

## Residual release gates

The foreman must execute Android API 35 instrumentation on a KVM-capable runner, including the explicit migration chain, malformed active-session isolation, malformed backup rollback, valid backup/restore during Review, and atomic SIM witness/session state after process recreation. The foreman must also verify a visible Review Map sequence—answer, flag, submit, direct jump, background/process recreation, reopen Review—and confirm correct/wrong/blank states. Signed release build, `apksigner` verification, package/version verification, signed APK bank verification, lint, debug APK inspection, install/launch, package identity, and all Final-Hours timezone/midnight/SIM gates remain mandatory before a release.

No main branch merge, tag, signed APK, or GitHub Release was created by A3.

## References

[1] [Original observed main baseline](https://github.com/rynmrde/Konkor/commit/72dc76e56b7ae625ad1904c76910eeaec5f90f58)  
[2] [Corrected Final-Hours composition commit](https://github.com/rynmrde/Konkor/commit/ee706e9836bd499decae0a1d79ea643884ab4d1c)  
[3] [Baseline successful workflow](https://github.com/rynmrde/Konkor/actions/runs/32031100891)
