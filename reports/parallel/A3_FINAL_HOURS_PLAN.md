# A3 Final-Hours Scheduler Handoff

| Field | Recorded value |
|---|---|
| Role | Final-Hours adaptive scheduler / ROI / SIM owner |
| Account label | `KONKOR-A3-M1-FINAL-HOURS` (Standard) |
| Upstream default branch | `main` |
| Baseline SHA | [`72dc76e56b7ae625ad1904c76910eeaec5f90f58`](https://github.com/rynmrde/Konkor/commit/72dc76e56b7ae625ad1904c76910eeaec5f90f58) |
| Worker branch | `parallel/a3-final-hours` |
| Candidate app version | `6.1.5` / `166` |
| Candidate overlay | `radiology_v615_final_hours_patch/overlay.tar.xz` |
| Candidate overlay SHA-256 | `e2b9f7752823a94c63295b1ce1baea328275520d16880dc4123d4042dcf4f156` |
| Historical V6.1.4 overlay | Preserved without modification |
| Latest baseline workflow | [32031100891](https://github.com/rynmrde/Konkor/actions/runs/32031100891), `success` |

## Baseline and delivery shape

The pinned baseline is `72dc76e56b7ae625ad1904c76910eeaec5f90f58`, the then-current `main` head. The repository stores its native application as a checksum-verified frozen V6.1 project plus a source overlay. Therefore, this handoff deliberately does **not** rewrite the historical V6.1.4 archive. It supplies a separately packaged V6.1.5 overlay and manifest for foreman-controlled integration. The frozen V6.1 ZIP was retrieved through the connected project Drive service and verified as `1344aca90474ac96e27e94ba754ebafd42778e2ceaab91f9a5fb1be2e882d046` before local validation.

| Preserved invariant | Handoff status |
|---|---|
| Bank archive, expanded SQLite, stable question IDs and holdouts | Unchanged |
| V6.1.4 overlay and historical release | Unchanged |
| Package identity | Remains `com.rynmrde.konkor` |
| Existing Room data | Preserved by explicit schema migration `3 → 4` |
| Existing active session | Resumed before a new recommendation is generated |
| SIM holdout leakage guard | Retained in session construction |

## Implemented Final-Hours behavior

The new `FinalHoursPlanner` is a deterministic reader of persisted evidence. It uses `Asia/Tehran`, sets the exam deadline to **2026-08-21 07:00 Iran time**, and never synthesizes a prior mastery value. Its input includes Room attempts, mastery rows, due credits, persisted simulations, the active session, confidence, timing and error history. It reports unique training questions, review repeats, simulation questions and total attempts independently, so review or simulation activity cannot inflate unique mastery coverage.

| Decision area | Implemented rule |
|---|---|
| Objective | Rank microtopics by expected reliable-correct gain per minute, incorporating official expected frequency, recent 1402–1404 signal, stability, error/blank/low-confidence evidence, spacing, prerequisite and calculation burden, safe-question quality, transfer evidence and minimum useful time. |
| Diagnostic | An unseen micro-skill receives **3–5 distinct questions**, not a daily quota. Mixed evidence yields a short lesson plus **2–4 different** retest questions. |
| Repeated failure | A recurring error becomes a prerequisite-repair candidate only when its projected marginal return beats the remaining alternatives. |
| Logical phases | The planner selects rapid high-ROI coverage, SIM1-and-repair, final consolidation, or protected sleep/logistics from evidence and remaining time rather than a literal calendar day. |
| Time protection | It reserves **420 minutes** for final sleep and **90 minutes** for meals, hygiene and logistics. With fewer than four study hours remaining, new prerequisite-heavy topics become low ROI for now. |
| SIM1 | Requires at least 60% evidence-backed viable-topic coverage and enough protected time; no fixed attempt count is used. |
| SIM2 | Requires a persisted review witness for SIM1, no unrepaired SIM1 weakness, adequate pace evidence without adverse fatigue, enough protected time and information value greater than targeted repair. |
| SIM2 fallback | If SIM2 is not justified and no targeted repair remains, the planner permits a **40–75 question** TRAIN-only mixed diagnostic, never Holdout. |

The repository integration makes the Day Selector’s live card dynamic, uses the Final-Hours decision to choose the next session, preserves active sessions first, keeps the existing distinct-question and holdout safeguards, and allows the resulting TRAIN block to be the recommended diagnostic/retest/fallback size rather than a fixed 15-question session. The candidate mode string carries the recommendation kind for traceability without displaying raw internal enums to the learner.

## Migration and persistence

`ProgressDatabase` moves from schema version `3` to `4` through `MIGRATION_3_4`. It adds nullable `simulation_result.reviewedEpochMs`; no table is dropped, no progress record is recreated, and destructive migration remains absent. Finishing review of SIM1 or SIM2 writes that witness explicitly. Backup exports now declare schema `4`, while restores continue to accept schema versions `1` through `4` and gracefully interpret legacy simulations without a review timestamp as **unreviewed**.

> A submitted SIM1 without `reviewedEpochMs` cannot unlock SIM2. This protects the required review-before-next-simulation gate across backgrounding, process recreation and restore.

## Added deterministic coverage

`FinalHoursPlannerTest` covers the Tehran conversion and midnight boundary, protected budget, adaptive 3–5 question diagnostics, ROI ordering, Room-shaped counter fixtures, SIM1 transition without calendar/attempt thresholds, SIM2 eligibility, non-holdout fallback, active-session priority and final sleep/logistics behavior. `tests/verify_final_hours_v615.py` is a structural guard for Tehran time, no `468` quota, the explicit Room migration, simulation-review persistence, repository integration and the required test cases.

| Validation step | Observed result |
|---|---|
| Frozen V6.1 source ZIP checksum | **PASS** |
| Packaged V6.1.5 overlay hash and re-extraction | **PASS** |
| V6.1.5 Final-Hours static source gate | **PASS** |
| Focused `FinalHoursPlannerTest` JVM run | **PASS** |
| Complete JVM unit-test suite | **PASS** — Gradle reported `BUILD SUCCESSFUL` |
| Kotlin compilation in the verified frozen project | **PASS** |
| Lint, debug APK, signed release, package/bank inspection | **NOT RUN** in this worker handoff |
| Android API 35 instrumentation, install/launch, UI, process recreation and migration instrumentation | **NOT RUN** in this worker handoff |

## Foreman integration instructions

The foreman should verify the candidate SHA, extract the overlay into the same checksum-verified frozen V6.1 source, add a new V6.1.5 workflow and update its version/package assertions. V6.1.4 workflow or release assets must not be overwritten. Before release, the foreman must run the static gate, full Kotlin/JVM/lint/debug/release gates, signed APK and bank checks, API 35 instrumentation, Review/Map persistence flow, progress migration checks and Final-Hours timezone/SIM behavior. This worker did not merge `main`, publish a release or claim any unrun gate as passed.

## Residual integration risk

The source-overlay packaging model requires a foreman workflow change before the candidate can enter CI. The unit suite verifies the engine and compilation but does not substitute for required signed-build, emulator or UI flow gates. The new schema migration is non-destructive by construction, but it still requires API 35 migration instrumentation against a v3 fixture before release.
