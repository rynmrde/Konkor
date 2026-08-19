# A3 Release-Critical Build Validation

> **Result: BLOCKED — do not release this composition yet.**

## Inputs and restoration

The supplied Foreman archive (`oN6VZQLRvKqDqPtMDS4o93.bin`, SHA-256 `31516e7b0f9c748412f84bd9f41191849e282a7d86522b6a7283a2cd9fa14f1d`) was unpacked into an isolated workspace. It did not contain the immutable bank or complete Gradle workspace, so it was layered onto the locally hash-verified V6.1.4 workspace. The frozen bank gzip SHA-256 matched the required value `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`.

A minimal compile compatibility restoration was necessary because the Foreman composition retained `RadiologyApp` calls to the existing `RescueUnlockState` contract while omitting the corresponding planner type, repository accessor, and view-model state. The fix restores only Room-derived UI state; it changes no entity, schema version, migration, stable ID, active-session JSON, backup format, mastery record, or progress data. The stale V6.1.4 `DaySelectionPolicyTest` was removed from the reconstructed workspace because its referenced dated-policy functions are intentionally absent from the submitted Final-Hours composition.

| Gate | Exact result | Evidence |
|---|---|---|
| Frozen bank gzip | **PASS** | SHA-256 matched historical immutable hash. |
| `validate_v6_1.py` bank/schema/SQLite gate | **PARTIAL PASS** | Bank/SQLite/count/pool-isolation section passed; chained V6.1.4 version assertion failed because supplied candidate is V6.1.5. |
| Final-Hours deterministic gate | **PASS** | `verify_final_hours_v615.py` passed. |
| No-reserve source scan | **PASS** | No non-zero protected sleep/logistics constant and no pre-exam REST decision were found. |
| Main Kotlin compile, before minimal fix | **FAIL** | Missing `RescueUnlockState`/`rescueUnlock` composition contract. |
| Main Kotlin compile, after minimal fix | **PASS** | Build advanced through main Kotlin compilation into unit-test execution. |
| JVM unit suite | **BLOCKED** | Stalled at `StructuredStimulusRobolectricTest` after 31 completed tests and a bounded 2m51s wait; process stopped. No pass is claimed. |
| Android-test Kotlin compile | **NOT COMPLETED** | KAPT phase started, but chained Gradle invocation was stopped because JVM suite stalled. |
| Lint/debug APK | **NOT COMPLETED** | Downstream tasks not reached after JVM stall. |
| Migration/progress/session preservation | **SOURCE-LEVEL PASS; runtime pending** | No migration/schema/session/backup/ID code was changed by the minimal fix; actual Android instrumentation/process-recreation gate remains pending. |
| API 35/install/launch/signed APK | **NOT RUN** | Not reached; no signed release artifact was produced. |

## Foreman action

Apply the helper overlay only to the same V6.1.5 Foreman composition. Re-run `:app:testDebugUnitTest` with diagnostics focused on `StructuredStimulusRobolectricTest`, then run Android-test compilation, lint, debug build, and required API 35 execution. Do not treat the V6.1.4-version assertion failure as a bank failure; the immutable bank gate itself passed. Do not release until the stalled JVM test and downstream gates pass.
