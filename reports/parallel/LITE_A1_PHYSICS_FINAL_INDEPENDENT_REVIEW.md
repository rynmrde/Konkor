# A1 Independent Physics Final Review — Second Pass

## Pinned target

| Field | Result |
|---|---|
| Reviewed branch | `parallel/a2-physics` |
| Exact second-pass commit | `5ca5cf6c73762aa63b1d41558643fd122e3938f2` |
| Source baseline cited by worker | `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Review scope | Second-pass report, manifest, exact source-tree paths, and declared rebuilt-bank gates; no main/release edits |

## Claim ledger

| Claim | Decision | Independent review finding |
|---|---|---|
| Physics scope contains 187 records | **PASS WITH REPRODUCTION REQUIREMENT** | The report states 142 TRAIN + 22 SIM1 + 22 SIM2 + 1 FINAL = 187, with 180 authored and 7 official-stem records. The claim is internally consistent, but this review did not receive an exposed row-level bank artifact or executable validator output, so the integrator must rerun the count on the rebuilt bank. |
| 18 high-ROI analysis rewrites were made | **PASS AS REPORTED; BANK-AUDIT REQUIRED** | The report gives exactly 18 IDs and states only learner-facing analysis fields changed. The exact field set is `correct_analysis`, all four `distractor_analyses`, `short_lesson`, `fast_method`, `start_method`, `main_trap`, and `review_default`. A row-level before/after diff is still required for release evidence. |
| All six required terse IDs were rewritten | **PASS AS REPORTED** | Exact IDs: `v3_phys_30_04`, `v3_phys_30_06`, `v3_phys_30_08`, `v3_phys_30_10`, `v3_phys_33_05`, `v3_phys_35_05`. The report supplies formula, substitution, unit, and condition paths for each. |
| No raw learner-facing enum tokens remain in the actual shared renderer path | **PASS STATIC CLAIM; RUNTIME GATE REQUIRED** | The report identifies `ScienceText.kt` and shared `sanitizeLearnerFacingText` before formula-direction isolation, and reports 1,471 raw occurrences in stored fields versus 0 after sanitation. This is the correct safety boundary, but compile/JVM/instrumentation were not run locally and the exact source file was not independently decoded here; CI must verify the packaged renderer and Review/lesson paths. |
| Canonical comparison stimulus is used for all 3 Physics IDs in Test and Review | **PASS AS REPORTED; TEST EXECUTION REQUIRED** | Exact IDs: `v3_phys_30_02`, `v3_phys_33_02`, `v3_phys_34_03`. The report states `Models.kt` parses `stimulus.type == "comparison"` and `RadiologyApp.kt` uses one shared `ComparisonStimulusCard` in `TestQuestion` and `ReviewQuestion`; `ComparisonStimulusRenderTest` loads the packaged bank. The source-tree path exists, but the test was not executed in this independent environment. |
| Same-session follow-up exclusions cover both exact pairs | **PASS STATIC CONTRACT; EXECUTION REQUIRED** | Exact pairs and groups: `v3_phys_30_04`/`v3_phys_30_08` in `فشار، چگالی و شاره‌ها::subskill_4`; `v3_phys_30_06`/`v3_phys_30_10` in `فشار، چگالی و شاره‌ها::subskill_2`. The report states exclusion applies to due, weak, topic, and fallback paths and `followupLeak` must be zero for TRAIN. `FollowupGroupSelectionTest` is named, but no real test output was supplied. |
| Rewritten formulas, units, signs, and keys are scientifically correct | **CONDITIONAL PASS** | The report provides coherent checks: continuity `A₁v₁=A₂v₂`, density `ρ=m/V`, Ohm `I=V/R`, and wave `v=fλ`, with units and substitutions; the seven listed official records also have plausible model/sign/unit paths. However, no source pages, rendered analyses, or executable scientific validator output were attached to this review. Do not convert this into an unconditional release PASS without row-level evidence. |
| No unsupported item changes occurred | **PASS AS DECLARED; EXACT DIFF REQUIRED** | The report and manifest state IDs, option sets, keys, pools, source metadata, schema, filename, and Room-progress contracts are unchanged; only the 18 authored Physics explanation payloads changed. This is safe in principle, but the release gate must compare old/new question IDs, option arrays, correct indices, source fields, `access_pool`, and progress identity, failing on any non-explanation delta. |

## Exact 18-record mutation scope

The reported changed IDs are:

```text
v3_phys_27_01, v3_phys_29_01, v3_phys_30_01, v3_phys_30_02,
v3_phys_30_04, v3_phys_30_06, v3_phys_30_08, v3_phys_30_10,
v3_phys_33_01, v3_phys_33_02, v3_phys_33_05, v3_phys_28_01,
v3_phys_28_02, v3_phys_31_01, v3_phys_35_01, v3_phys_35_05,
v3_phys_32_01, v3_phys_34_03
```

The stated mutation is **explanation-only** across the eight learner-facing fields named above. The report says the rebuilt bank preserves all 1,216 IDs, four-option structures, correct indices, source-type counts, pool counts, quarantine count, SIM disjointness, option sets, source metadata, schema, filename, and Room-progress contracts. Those are necessary assertions, not yet independent PASS evidence, because the binary/row-level before-and-after diff was not exposed in the review payload.

## Why the bank hashes changed

The bank change is explained by deliberate edits to learner-facing analysis payloads for the 18 authored Physics IDs, not by a source/runtime override. The historical references remain `gzip b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14` and `SQLite d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`; the second-pass values are `gzip ca4f3c63a88bf091d3ce464254048629f939a0f60b8b088e53ccd7bf206ffe2a` and `SQLite d6d93c2786b5900100bc348b06e740a47a94f1fb89932372a8a5ac0b68a13a5e`. The report also records deterministic overlay hash `25238d05278b94fcd8021515d7ee7ee53ac278c5e8d91fcab0ca24d20de0d0a5` and workflow hash `96068ec72af543b0fdb07f683e8a635951547b180918538be802156556ec4067`.

This is a **material bank mutation**, even if semantically narrow. It is not safe to ship under unchanged V6.1.4 bank identity merely because IDs and progress keys are stable. The final integrator must issue an explicit new bank/minor version, attach a bank audit and old/new row diff, verify signed packaged-bank hashes, and document non-destructive migration/progress preservation. If the product owner instead chooses a runtime/source override, that would not explain the changed bank hashes and would not satisfy the reported analysis-rewrite claim.

## Release disposition

**Independent outcome: CONDITIONAL FAIL for release clearance.** The second-pass design is internally coherent and the reported safety contracts are directionally correct. Release remains blocked until CI provides actual compile, JVM, lint, instrumentation, packaged-bank, signed-APK, and process/progress checks, and until a deterministic old/new bank diff proves that only the 18 IDs and the eight named analysis fields changed. No safe helper patch was obvious from the available evidence, so this review makes no source or bank changes.

## References

[1]: https://github.com/rynmrde/Konkor/commit/5ca5cf6c73762aa63b1d41558643fd122e3938f2 "Pinned Physics second-pass commit"

[2]: https://github.com/rynmrde/Konkor/blob/5ca5cf6c73762aa63b1d41558643fd122e3938f2/reports/parallel/A2_PHYSICS_QA.md "Physics second-pass QA report"

[3]: https://github.com/rynmrde/Konkor/blob/5ca5cf6c73762aa63b1d41558643fd122e3938f2/radiology_v614_rescue_patch/MANIFEST.txt "Second-pass rescue manifest"
