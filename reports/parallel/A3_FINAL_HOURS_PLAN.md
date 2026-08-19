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
| Candidate overlay SHA-256 | `59a8ff9e5aa62bbe164fa8dffb6fc5056795eeb5ee82b511cc55fbff9281599d` |
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

The repository integration makes the Day Selector’s live card dynamic, uses the Final-Hours decision to choose the next session, preserves active sessions first, and allows the resulting TRAIN block to be the recommended diagnostic/retest/fallback size rather than a fixed 15-question session. The candidate mode string carries the recommendation kind for traceability without displaying raw internal enums to the learner.

## SECOND_PASS_REVIEW

> **Status: PASS for the Final-Hours source and JVM gates listed below; this is not a release approval.** The pass is limited to the V6.1.4-based source overlay and deterministic/JVM evidence. Android API 35 instrumentation, signed-build, packaged-bank, install/launch, migration-device, Review and Question Map release gates remain foreman work.

The second pass scanned the complete extracted V6.1.4 source baseline and then the live V6.1.5 overlay. The baseline contained the exact stale hazards reported by the independent worker: dated `dayPlans`, a day-3 `SIM2` branch, hard secondary/extra-C unlock conditions, and a dated UI contract. Those scheduler paths are now removed from `RescuePlanner`; the only retained A/B/C values are historical inventory labels, not eligibility gates. `BankStore.dayPlans()` remains an immutable bank-data reader with no live Final-Hours call site.

| Independent finding | V6.1.4 baseline defect | V6.1.5 second-pass correction | Evidence |
|---|---|---|---|
| Stale historical day logic | Fixed `2026-08-17` to `2026-08-19` plans and day-index stages | Deleted `dayPlans`, `RescueStage`, `nextStage`, DaySelectionPolicy helpers/tests, dated stage UI and three-day wording | Source gate forbids the deleted symbols; live plan derives only from `FinalHoursPlanner` and Tehran `now` |
| Unconditional SIM2 | Day 3 selected SIM2 whenever incomplete | SIM2 remains gated by reviewed SIM1, repaired weaknesses, pace/fatigue, protected time and marginal-value comparison | `reviewedButUnrepairedSim1ForcesTargetedRepairInsteadOfUnconditionalSim2` passes |
| Historical hard C threshold | Attempted-topic, ready-topic and correct-rate unlock constants plus both SIM passes | Deleted threshold unlock code; added `ExtraTimeCWitness` and `EXTRA_TIME_C` recommendation, derived from live Room evidence | Source gate forbids `secondaryUnlocked` and `extraUnlocked`; four extra-C fixtures pass |
| Missing live C support | C was only an historical label and could not be explicitly recommended | C is recommended only when its live marginal reliable-gain/minute beats unresolved A/B work, protected time remains, no open session exists, pace evidence is adequate, and SIM gates do not outrank it | `extraTimeCUnlocksOnlyWithLiveWitnessAndReturnsASeparateRecommendation` passes |
| Duplicate/unique-mastery conflict | Final TRAIN fallback could draw IDs without the prior-attempt exclusion | Removed exact-repeat fallback; selection now fails safely if distinct eligible TRAIN IDs are exhausted, and rejects both prior-attempt overlap and within-block duplicate IDs | Source gate requires the fail-safe and `ids.distinct()` guard; unique/repeat counter fixture passes |

The public `extraTimeCWitness(input)` is the explicit unlock witness requested by review. It records whether the route is eligible, C candidate, marginal reliable-gain/minute, any higher-priority A/B blocker, the minimum protected-time reservation and an explanatory Persian decision string. It does **not** contain a day number, topic-count target, historical correct-rate target or a forced threshold. `EXTRA_TIME_C` is a separate recommendation kind rather than a reinterpretation of simulation or review work.

| Extra-C witness gate | Required live evidence |
|---|---|
| Candidate | Historical C-labelled topic with safe available training content and non-reliable/non-low-ROI current state |
| Marginal ROI | No unresolved A/B topic with at least the candidate’s current reliable-gain/minute |
| Time and sleep | At least `max(45 minutes, 2 × minimum useful minutes)` remains **after** the fixed 420-minute sleep and 90-minute logistics reserve |
| Session safety | No uncompleted active session |
| Pace and fatigue | At least the existing reliable timing witness; adverse or absent timing blocks extra time |
| SIM ordering | SIM1 coverage gate, SIM1 review/repair gate, and a superior eligible SIM2 information value each block C |
| Duplicate safety | Recommended C question count is 3–5; repository selection uses only distinct, previously unattempted TRAIN IDs and fails safely instead of repeating |

The Final-Hours/Rescue focused run contained **18 deterministic fixtures**: the requested Tehran/midnight/countdown, final-sleep, zero-progress diagnostic, active-session, ROI, dynamic A/B/C, SIM1/SIM2, fallback and unique-versus-repeat cases, plus four new extra-C state/interactions and retained bank-safe/teaching checks. It reported `BUILD SUCCESSFUL`. The full JVM suite also reported `BUILD SUCCESSFUL` after the removed legacy day-policy test was intentionally absent from the validation workspace.

### Publication status

The corrected local archive, manifest and this report are prepared for one atomic update of `parallel/a3-final-hours`. An earlier repository attempt first encountered a stale historical Composio account identifier and then an `OAuth authentication failed: Upstream MCP server error` before any write. The authorized retry uses the existing enabled Composio connector UUID `02a3aad0-b63d-4ce5-a6b5-f496edcdbc2e`; it does not enable or use a standalone GitHub connector. No main branch, release or other worker branch is in scope. The validated local artifact is `radiology_v615_final_hours_patch/overlay.tar.xz` at SHA-256 `59a8ff9e5aa62bbe164fa8dffb6fc5056795eeb5ee82b511cc55fbff9281599d`; the remote branch head and read-back must be verified immediately after the atomic write.

## Migration and persistence

`ProgressDatabase` moves from schema version `3` to `4` through `MIGRATION_3_4`. It adds nullable `simulation_result.reviewedEpochMs`; no table is dropped, no progress record is recreated, and destructive migration remains absent. Finishing review of SIM1 or SIM2 writes that witness explicitly. Backup exports now declare schema `4`, while restores continue to accept schema versions `1` through `4` and gracefully interpret legacy simulations without a review timestamp as **unreviewed**.

> A submitted SIM1 without `reviewedEpochMs` cannot unlock SIM2. This protects the required review-before-next-simulation gate across backgrounding, process recreation and restore.

## Added deterministic coverage

`FinalHoursPlannerTest` covers the Tehran conversion and midnight boundary, protected budget, adaptive 3–5 question diagnostics, ROI ordering, Room-shaped counter fixtures, SIM1 transition without calendar/attempt thresholds, SIM2 eligibility, non-holdout fallback, active-session priority, final sleep/logistics, a historical C label that does not suppress live ROI, reviewed-but-unrepaired SIM1, and four dynamic extra-C state/interactions. `tests/verify_final_hours_v615.py` is a structural guard for Tehran time, no `468` quota, the explicit Room migration, simulation-review persistence, the required extra-C witness, removed legacy day/SIM2/C symbols, no exact-repeat TRAIN fallback, repository uniqueness guards and the required test cases.

| Validation step | Observed result |
|---|---|
| Frozen V6.1 source ZIP checksum | **PASS** |
| Packaged V6.1.5 overlay hash and re-extraction | **PASS** — second-pass SHA-256 `59a8ff9e5aa62bbe164fa8dffb6fc5056795eeb5ee82b511cc55fbff9281599d` |
| V6.1.5 Final-Hours static source gate | **PASS** |
| Focused `FinalHoursPlannerTest` JVM run | **PASS** |
| Complete JVM unit-test suite | **PASS** — Gradle reported `BUILD SUCCESSFUL` in 21 seconds after second-pass fixes |
| Kotlin compilation in the verified frozen project | **PASS** |
| Lint, debug APK, signed release, package/bank inspection | **NOT RUN** in this worker handoff |
| Android API 35 instrumentation, install/launch, UI, process recreation and migration instrumentation | **NOT RUN** in this worker handoff |

## Foreman integration instructions

The foreman should verify the candidate SHA, extract the overlay into the same checksum-verified frozen V6.1 source, add a new V6.1.5 workflow and update its version/package assertions. V6.1.4 workflow or release assets must not be overwritten. Before release, the foreman must run the static gate, full Kotlin/JVM/lint/debug/release gates, signed APK and bank checks, API 35 instrumentation, Review/Map persistence flow, progress migration checks and Final-Hours timezone/SIM behavior. This worker did not merge `main`, publish a release or claim any unrun gate as passed.

## Residual integration risk

The source-overlay packaging model requires a foreman workflow change before the candidate can enter CI. The unit suite verifies the engine and compilation but does not substitute for required signed-build, emulator or UI flow gates. The new schema migration is non-destructive by construction, but it still requires API 35 migration instrumentation against a v3 fixture before release.
