# Lite A3 Idle Reassignment — Persistence + UI + Revised Final-Hours Review

**Role:** Independent persistence/UI/scheduler seam reviewer  
**Account label:** Manus A3 Lite  
**Review date:** 2026-08-19 UTC  
**No main/release:** No main branch, release, bank, or other worker branch was modified.

## Overall verdict

> **FAIL for the requested composition.**

The newest Persistence and UI/Review Map contracts pass the requested static checks, and the persistence verifier reports twelve PASS assertions. The revised Final-Hours scheduler does **not** satisfy the explicit reassignment requirement: mandatory sleep/final-sleep/meals/hygiene/logistics reserves remain encoded as scheduler constants, available-time cutoffs, a `SLEEP_AND_LOGISTICS` phase, a `REST` recommendation, extra-C minimum-reserve logic, and user-facing details. Therefore the composition is not PASS under the instruction that those reserves are revoked and must not survive as scheduler or migration gates.

The migration/persistence source itself contains no revoked-reserve terms and remains structurally clean. The failure is specifically in the Final-Hours scheduler seam, not in Room schema or backup migration registration.

## Reviewed newest artifacts

| Area | Reviewed branch / commit | Artifact status |
|---|---|---|
| Persistence | `parallel/a3-persistence-qa` / `b78daecaa26ccc5c2a397cf71b043baae10fc9d6` | Final second-pass report and `radiology_v615_a3_second_pass_patch/overlay.tar.xz` |
| UI / Review Map | `parallel/a2-review-question-map` / `e484fbc25a2c966566756eaca5c3515bdfcba84e` | Second-pass full-product Review/Map overlay and report |
| Revised Final-Hours | `parallel/a3-final-hours` / `ee706e9836bd499decae0a1d79ea643884ab4d1c` | Corrected Final-Hours overlay and report |
| Related post-completion review | `parallel/help-a2-postcompletion-independent-review` / `d1ea97d6b1478e4ce8a66d3ba7529ed82597f956` | Duplicate/mastery and post-completion review evidence |

## Observed checks

| Contract | Result | Evidence |
|---|---|---|
| Active-session compatibility | **PASS** | `ProgressPayloadValidator.session` is wired into the composed repository and validates pool/phase/date/timestamps, unique IDs, bank eligibility, positions, JSON keys/types, option orders, flags, elapsed values, analysis booleans, and error enums. |
| Backup/restore fail-closed behavior | **PASS at static/source level** | `ProgressPayloadValidator.backup` runs before Room clearing; pre-restore snapshots and transactional valid/legacy restore paths remain present. Runtime device restore remains a release-owner gate. |
| Process-recreation persistence seam | **PASS at static/source level; runtime pending** | Active session, session-scoped attempts, Review Map state, and atomic SIM witness/session transaction are present. No API 35 device execution was performed in this lite review. |
| Progress preservation | **PASS at static/source level** | Stable question IDs, unique session/question indexing, explicit snapshots, and non-destructive migration paths remain present. |
| Room migration registration | **PASS** | `MIGRATION_1_2`, `MIGRATION_2_3`, and `MIGRATION_3_4` remain registered; no destructive fallback was found. |
| UI Review/Map persistence seam | **PASS at static/source level** | UI overlay uses durable `questionIdsJson`, `answersJson`, `flagsJson`, `position`, and `reviewPosition`; persisted map refresh/navigation symbols are present. Device visual flow remains pending. |
| No exact-repeat TRAIN fallback | **PASS** | Persistence second-pass verifier passed `no historical train repeat` and `no repeat fallback`; composed repository throws when distinct eligible content is exhausted. |
| Evidence-family/unique mastery | **PASS** | Persistence verifier passed evidence-family filtering and unique mastery repeat semantics; UI overlay does not alter bank identity. |
| Revoked reserve-free scheduler seam | **FAIL** | Final-Hours source still defines `PROTECTED_SLEEP_MINUTES = 7 * 60`, `PROTECTED_LOGISTICS_MINUTES = 90`, `SLEEP_AND_LOGISTICS`, `REST`, `minimumReservedMinutes`, `protectedStart`, and returns zero available study minutes before the protected window. |
| Migration contamination by revoked reserves | **PASS** | Direct scan of `ProgressDatabase.kt` and `ProgressPayloadValidator.kt` found no sleep, final-sleep, meals, hygiene, logistics, or reserve scheduler terms. |

## Deterministic outputs

The extracted Persistence second-pass verifier produced:

```text
PASS: final-hours decision
PASS: evidence-family bank filter
PASS: no historical train repeat
PASS: no repeat fallback
PASS: unique mastery repeat semantics
PASS: atomic sim finish
PASS: review witness
PASS: fail closed session
PASS: fail closed restore
PASS: session attempts query
PASS: review map projection
PASS: schema v4 migration
```

The revised Final-Hours worker’s own static verifier also reports PASS, but that verifier treats the protected sleep/logistics behavior as an intended requirement. Under this reassignment, that behavior is revoked, so the independent reserve scan correctly changes the scheduler verdict to FAIL.

The explicit reserve scan found the following surviving scheduler seams:

| Source location | Surviving revoked behavior |
|---|---|
| `FinalHoursPlanner.kt:25–26` | Seven-hour sleep and 90-minute logistics constants |
| `FinalHoursPlanner.kt:35, 51` | `SLEEP_AND_LOGISTICS` phase and `REST` recommendation |
| `FinalHoursPlanner.kt:134, 171–185` | Available-time zero gate and rest recommendation before the protected window |
| `FinalHoursPlanner.kt:336–371` | Extra-C minimum reserve and sleep/logistics explanations |
| `FinalHoursPlanner.kt:375–377` | `protectedStart` subtracting sleep plus logistics from study time |
| `FinalHoursPlanner.kt:554–555` | Decision output continues exposing protected reserve fields |

## Required disposition

The Foreman must remove the revoked reserve contract from the Final-Hours planner and its tests before claiming composition PASS. `availableStudyMinutes` must no longer subtract mandatory sleep/logistics windows; `SLEEP_AND_LOGISTICS`, `REST`, `PROTECTED_SLEEP_MINUTES`, `PROTECTED_LOGISTICS_MINUTES`, `minimumReservedMinutes`, and protected-start logic must be removed or replaced with a non-reserve scheduler contract. Migration and persistence code must remain unchanged unless a direct dependency on those removed planner fields requires a compile-safe adjustment. Afterward, rerun the Final-Hours static/JVM suite, the persistence verifier, UI/Review Map tests, and all required device/release gates.

No safe helper source fix was applied in this lite review because removing the reserve behavior changes the scheduler contract and requires the standard Final-Hours owner or Foreman to make the evidence-backed composition change.

## References

[1]: https://github.com/rynmrde/Konkor/commit/b78daecaa26ccc5c2a397cf71b043baae10fc9d6 "Final Persistence second-pass branch"
[2]: https://github.com/rynmrde/Konkor/commit/e484fbc25a2c966566756eaca5c3515bdfcba84e "Review/Question Map second-pass branch"
[3]: https://github.com/rynmrde/Konkor/commit/ee706e9836bd499decae0a1d79ea643884ab4d1c "Revised Final-Hours branch"
[4]: https://github.com/rynmrde/Konkor/commit/d1ea97d6b1478e4ce8a66d3ba7529ed82597f956 "Post-completion duplicate/mastery review branch"