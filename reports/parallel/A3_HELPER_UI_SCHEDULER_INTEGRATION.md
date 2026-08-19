# A3 Helper: UI/Question-Map and Scheduler Integration Check

> **Status:** **FAIL — unsafe overlay composition; no release candidate.**  
> **Helper scope:** newest Review/Question-Map overlay plus user-authorized removal of scheduler sleep/logistics reserves.  
> **No main, tag, signed APK, or release was created.**

## Inputs and override

The Review/Question-Map candidate was commit `335333159d4fc5a2ec9d988d9a26e753d9e32a0d`; its full-source archive was independently downloaded and SHA-256 verified as `a6cb639111058858b374f9b744157f91a51f4d240c9decba6828bb55a7d73e6d`. The persistence composition base was the published A3 artifact at `b78daecaa26ccc5c2a397cf71b043baae10fc9d6`, and the scheduler base was corrected Final-Hours commit `ee706e9836bd499decae0a1d79ea643884ab4d1c`.

The user-authorized override was implemented only in `FinalHoursPlanner.kt`: protected sleep and logistics output values are zero, `availableStudyMinutes()` now runs through `EXAM_INSTANT`, and the pre-exam `REST` decision branch was removed. No Room entity, database migration, active-session JSON field, stable question ID, backup record, progress attempt, mastery record, or text-scale setting was modified by this scheduler-only patch.

| Gate | Result | Evidence |
|---|---|---|
| Newest UI archive hash | **PASS** | Downloaded archive SHA-256 matched `a6cb639…73e6d`. |
| Scheduler reserve removal scan | **PASS** | No protected-start subtraction and no pre-exam `RecommendationKind.REST` decision remain; remaining time ends only at the exam instant. |
| Non-destructive Room migration | **NOT EXECUTED** | The UI overlay caused compilation failure before migration fixtures could run. |
| Active-session, process recreation, backup/restore, Question-Map, text-scale, unique mastery | **NOT EXECUTED** | These gates cannot be truthfully passed on a non-compiling composition. |
| A3 persistence composition static guard | **FAIL** | The V6.1.4 UI overlay wholesale-replaced `StudyRepository.kt` and removed Final-Hours decision integration, evidence-family suppression, no-repeat protection, atomic SIM review, malformed payload validation, and durable A3 Map projection. |
| Kotlin compilation | **FAIL** | `:app:compileDebugKotlin` failed with unresolved `RescueStage`, `dayPlans`, `rescueUnlock`, `RescueUnlockState`, and related V6.1.4/V6.1.5 model contract mismatches. |

## Safe integration fix

> **Do not extract the V6.1.4 UI archive over Final-Hours/A3 composition.** It replaces `Models.kt`, `BankStore.kt`, `StudyRepository.kt`, and `RadiologyApp.kt` as a whole and is therefore incompatible with the V6.1.5 scheduler/session contracts.

The safe next step is a source-level three-way merge using the V6.1.5 Final-Hours/A3 composed versions as the authoritative data/repository base and importing only the UI overlay's Review presentation, structured-stimulus renderer, typography helper, text-scale tests, and Question-Map composables. The resulting source must retain `ProgressPayloadValidator`, `finishReview()` transaction, evidence-family filtering, no-repeat TRAIN selector, and canonical `QuestionMapSessionProjection`. Only after that merge compiles may the requested migration, backup/restore, recreation, 90–140% text-scale, Map persistence, and unique-mastery gates be re-run.

The packaged helper scheduler file is intentionally separate and applies cleanly to the corrected Final-Hours source. It is not a claim that the combined UI/scheduler release candidate passes.
