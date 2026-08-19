# KONKOR A3 Lite — No-Reserve Recheck

| Field | Recorded value |
|---|---|
| Role | Lite helper / independent Final-Hours recheck |
| Account label | `KONKOR-A3-LITE-NO-RESERVE-RECHECK` |
| Repository | [`rynmrde/Konkor`](https://github.com/rynmrde/Konkor) |
| Baseline branch inspected | `parallel/a3-final-hours` |
| Baseline SHA | [`ee706e9836bd499decae0a1d79ea643884ab4d1c`](https://github.com/rynmrde/Konkor/commit/ee706e9836bd499decae0a1d79ea643884ab4d1c) |
| Baseline commit time | 2026-08-19 14:21:56 UTC |
| Helper branch | `parallel/help-a3-lite-no-reserve-recheck-20260819` |
| Scope | Static source/archive/test audit only; no main merge and no release |

## Verdict

> **OVERALL: FAIL — do not treat this helper report as release approval.**

The requested fixed sleep/final-sleep/meals/hygiene/logistics reserve is **still present** in the newest revised Final-Hours branch. The branch therefore fails the specific no-reserve recheck even though the remaining requested constraints have direct supporting evidence.

## Gate matrix

| Gate | Result | Exact evidence and interpretation |
|---|---|---|
| Fixed reserve removed | **FAIL** | `FinalHoursPlanner.kt` declares `PROTECTED_SLEEP_MINUTES = 7 * 60` and `PROTECTED_LOGISTICS_MINUTES = 90`; it also declares `SLEEP_AND_LOGISTICS` and returns that phase before the exam cutoff. The pinned `radiology_v615_final_hours_patch/MANIFEST.txt` independently states that the planner reserves 420 minutes for final sleep and 90 minutes for meals, hygiene, and logistics. This is the direct blocker. |
| Exam cutoff | **PASS (static)** | `FinalHoursPlanner.kt` defines `IRAN_ZONE = ZoneId.of("Asia/Tehran")`, defines `EXAM_INSTANT` from `2026-08-21 07:00` in that zone, and checks `now >= EXAM_INSTANT` to select `EXAM_STARTED`. No calendar-day shortcut was found in the pinned planner excerpt. |
| Tehran time | **PASS (static)** | The cutoff is constructed from `Asia/Tehran`, not the device default zone. The manifest and plan identify the same Iran exam timestamp. |
| Active-session safety | **PASS (static; execution not rerun)** | `StudyRepository.kt` reads `dao.activeSession()`, validates compatibility before recommendations, preserves an active non-done session, and uses a mutex for session mutation. `RescueSessionFlowTest.kt` covers answer/review/reopen/resume and SIM1 start. The required Android/instrumentation execution was not rerun by this lite worker. |
| ROI / adaptive volume | **PASS (static)** | `FinalHoursPlanner.kt` ranks evidence and computes availability, coverage, targeted repair, marginal information per minute, and conditional simulation eligibility. `StudyRepository.kt` consumes due credits and selects distinct alternatives rather than enforcing a fixed daily attempt count. |
| SIM1 / SIM2 / holdout | **PASS (static; execution not rerun)** | SIM1 requires coverage and available minutes; SIM2 requires persisted SIM1 existence, reviewed SIM1, no unresolved SIM1 topics, acceptable fatigue evidence, sufficient time, and information value beating targeted repair. `StudyRepository.kt` selects SIM pools separately, and `BankStore.kt` checks holdout membership/pool. The manifest records 18 deterministic planner fixtures covering SIM1/SIM2 and holdout behavior, but this helper did not execute the JVM suite. |
| Unique versus repeat accounting | **PASS (static)** | `StudyRepository.kt` excludes attempted/selected/source IDs, requires zero overlap with prior attempts, and fails safely when no distinct eligible TRAIN questions remain. `AdaptiveEngine.kt` separately derives distinct-question and exam-attempt counters; review and simulation activity cannot inflate unique mastery coverage. |

## Reproduction evidence

The archive [`radiology_v615_final_hours_patch/overlay.tar.xz`](https://github.com/rynmrde/Konkor/blob/ee706e9836bd499decae0a1d79ea643884ab4d1c/radiology_v615_final_hours_patch/overlay.tar.xz) was fetched through the connected collaboration service, decoded, and scanned deterministically. The decisive source matches were:

```text
app/src/main/java/com/radiology1405/prep/engine/FinalHoursPlanner.kt:25  const val PROTECTED_SLEEP_MINUTES = 7 * 60
app/src/main/java/com/radiology1405/prep/engine/FinalHoursPlanner.kt:26  const val PROTECTED_LOGISTICS_MINUTES = 90
app/src/main/java/com/radiology1405/prep/engine/FinalHoursPlanner.kt:35  SLEEP_AND_LOGISTICS("خواب و آمادگی آزمون")
app/src/main/java/com/radiology1405/prep/engine/FinalHoursPlanner.kt:154  if (now >= EXAM_INSTANT) { ... EXAM_STARTED ... }
app/src/main/java/com/radiology1405/prep/data/StudyRepository.kt:288  No distinct eligible TRAIN questions remain ... reduce the recommendation rather than repeat a question.
app/src/main/java/com/radiology1405/prep/data/StudyRepository.kt:321  require(overlap == 0) { "$pool session repeats a previously attempted question: $overlap" }
```

The existing branch manifest also records a claimed static/JVM pass, but that is **not** substituted for an independent build or test run. No Kotlin compile, lint, APK, instrumentation, install/launch, migration-device, or UI flow gate was run by this lite worker; those remain Foreman gates.

## Required handoff

The primary A3 worker or Foreman must remove the fixed reserve from the planner implementation and its tests, then rerun the complete Final-Hours test matrix. The exam cutoff, Tehran-zone conversion, active-session preservation, adaptive ROI, SIM/holdout disjointness, and unique-versus-repeat protections must remain intact. This helper created no app patch and made no release action.

## References

[1]: https://github.com/rynmrde/Konkor/commit/ee706e9836bd499decae0a1d79ea643884ab4d1c "Pinned newest revised Final-Hours commit"
[2]: https://github.com/rynmrde/Konkor/blob/ee706e9836bd499decae0a1d79ea643884ab4d1c/radiology_v615_final_hours_patch/MANIFEST.txt "Pinned Final-Hours patch manifest"
[3]: https://github.com/rynmrde/Konkor/blob/ee706e9836bd499decae0a1d79ea643884ab4d1c/radiology_v615_final_hours_patch/overlay.tar.xz "Pinned Final-Hours source overlay archive"

Author: **Manus AI**
Date: 2026-08-19 UTC
