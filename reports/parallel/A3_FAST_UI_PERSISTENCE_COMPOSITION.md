# A3 Fast UI/Persistence Composition Handoff

> **Compile-ready core candidate:** source-level interface composition only; no main or release changes.

| Gate | Result | Evidence |
|---|---|---|
| Kotlin main compile | **PASS** | `:app:compileDebugKotlin` completed successfully after aligning the A3 session guard with the no-reserve scheduler. |
| Targeted JVM persistence/Final-Hours tests | **PASS** | `FinalHoursPlannerTest`, `AdaptiveEngineTest`, and `QuestionMapSessionProjectionTest` passed. |
| A3 persistence contracts retained | **PASS (source)** | Candidate retains `ProgressPayloadValidator`, atomic `finishReview()`, `attemptsForSession`, durable map projection, evidence-family filtering, and no-repeat TRAIN selection. |
| No-reserve scheduler | **PASS (source)** | The composed `FinalHoursPlanner` retains zero sleep/logistics reserves and no pre-exam REST branch. |
| Immutable bank/stable IDs/migration | **UNCHANGED** | The helper does not carry bank assets or alter `Question` IDs, Room identity, schema version, or migration semantics. |
| Full final-UI presentation tests | **EXCLUDED FROM THIS 15-MIN HELPER** | Two tests (`StructuredStimulusRobolectricTest`, `TypographyScaleTest`) target APIs from the unmerged wholesale V6.1.4 UI overlay and were excluded from this core candidate; the source merge keeps the accepted durable Review/Map UI boundary instead of accepting that unsafe wholesale replacement. |

## Publisher application rule

Apply the source files from this helper over the Foreman V6.1.5 composition. Do not wholesale-replace `Models.kt`, `StudyRepository.kt`, `BankStore.kt`, or `RadiologyApp.kt` with the older UI archive. The helper deliberately selects the A3-composed interfaces for those collision points and keeps the no-reserve scheduler. Run the full UI presentation suite only after the remaining presentation-only merge is completed.
