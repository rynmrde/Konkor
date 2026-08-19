# A1 Helper Audit — Final-Hours Planner Blockers

**Helper branch:** `parallel/help-a1-m4-final-hours-audit`  
**Baseline examined:** `72dc76e56b7ae625ad1904c76910eeaec5f90f58` plus the current V6.1.4 overlay.  
**Scope:** Read-only implementation and test audit. No code, bank, migration, release, or main-branch change is included in this helper handoff.

> **Finding:** The current planner implements a fixed three-day historical schedule, rather than an actual-now, exam-datetime, local-progress Final-Hours engine. The present implementation should not be release-certified against the project’s Final-Hours gates until the listed tests pass.

## Blocking discrepancies

| Severity | Current implementation evidence | Required behaviour | Exact release-risk consequence |
|---|---|---|---|
| Blocker | `RescuePlanner.nextStage(day, trainingAttempts, completedSimulations, extraUnlocked)` selects stages from literal `day` values 1, 2, and 3. | Derive phase from actual now, exam datetime, timezone, intended sleep, and persisted local progress; logical phases must not be hard-coded calendar days. | Midnight/timezone drift can route a study session into an invalid phase and violate the final-sleep protection. |
| Blocker | On day 3, `nextStage` returns `SIM2` whenever SIM2 is incomplete. | SIM2 is conditional: it must be offered only after SIM1 review and targeted repair, with enough time and acceptable fatigue, and only when it beats targeted repair. | The app can mandate SIM2 despite a higher-value wrong/blank repair block. |
| Blocker | `dayPlans()` emits fixed dates `2026-08-17`, `2026-08-18`, and `2026-08-19`, including a fixed third-day SIM2 plan. | Plans must recalculate from current time and the configured exam datetime, retaining logical phases instead of stale dates. | Re-opening on exam eve or after midnight can surface obsolete historical dates and wrong workload. |
| High | `unlockState()` defines C unlock using `ready >= 12`, a hard-coded threshold unrelated to the actual mandatory topic count. | Extra/C eligibility must be based on the live active mandatory set and actual progress, not a fixed historical count. | The app can make C unreachable for smaller mandatory sets or prematurely measurable under larger ones. |
| High | Existing `threeDayStagesPreserveBothIndependentSimulations` test asserts unconditional day-3 SIM2 behavior. | Test expectations must enforce conditional SIM2 decision criteria, including the selected alternative when SIM2 is not justified. | The test suite currently protects the behaviour that conflicts with the Final-Hours specification. |

## Required executable test matrix

| Test case | Inputs | Expected result |
|---|---|---|
| Iran timezone near midnight | `Asia/Tehran`; now immediately before and after local midnight; same persisted progress | Logical phase and sleep deadline remain correct; no historical day-number reset. |
| Final sleep guard | Time remaining before intended sleep less than four hours | No new prerequisite-heavy topic; show targeted repair, formula/textbook-sensitive retrieval, or sleep preparation. |
| SIM1 repair gate | SIM1 complete with wrong/blank/low-confidence records not repaired | SIM2 is not selected; next block is review and targeted repair. |
| SIM2 marginal-value gate | SIM1 repaired, fatigue/time poor, targeted repair score higher | SIM2 is not selected; return the selected repair/diagnostic alternative with reason. |
| SIM2 eligible case | SIM1 reviewed and repaired, adequate time/fatigue, SIM2 value higher | SIM2 becomes available, but remains an explicit conditional recommendation rather than a compulsory day-3 stage. |
| Mandatory-set scaling | Mandatory sets smaller and larger than 12 | C unlock derives from the actual mandatory-set completion and confidence evidence. |
| Reopen/resume | Persisted Room attempts, SIM results, and due states; app recreation | Phase, conditional SIM state, and next action are identical after resume. |

## Minimal design direction for A3

Introduce a time-aware planner input containing instant, `ZoneId.of("Asia/Tehran")`, exam instant, intended sleep interval, live topic evidence, due states, SIM1 remediation status, fatigue/time estimate, and comparable marginal values for SIM2 versus repair. The output should name the selected action and the policy reason. Preserve existing compatible sessions by deriving the new state from stored attempts and simulation records; do not convert historical progress to a fixed calendar-day index.

## Handoff

This audit is intentionally report-only to avoid conflicting with the primary Final-Hours worker. The Foreman/A3 owner should implement the planner change, replace the unconditional-SIM2 test, and add the above timezone/midnight/sleep/ROI/SIM regression matrix before calling the Final-Hours gate passed.
