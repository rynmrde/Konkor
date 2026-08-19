# A2 Physics Bank and Exam-Solution QA — Implemented Second Pass

**Role:** `[KONKOR-A2-M1-PHYSICS]` Physics bank and exam-solution QA, standard worker.  
**Worker branch:** `parallel/a2-physics`.  
**Source baseline:** `origin/main` and `radiology1405-apk-v6.1.4-20260817` both resolved to `72dc76e56b7ae625ad1904c76910eeaec5f90f58`.  
**Initial report commit:** `04b571947ab0c8c40b5025b121f8442a3e5911f2`.  
**Scope:** Full reconstructed V6.1.4 source and bank, using the verified base archive plus release overlay. No `main` merge, force-push, release publication, or release-tag update was performed.

> **Second-pass implementation status: source fixes complete; release clearance remains pending foreman integration gates.** The prior Physics findings were converted into a shared renderer fix, canonical comparison-stimulus rendering, audited bank revisions, normal-session follow-up exclusion, deterministic validation, and instrumentation test contracts. A fresh version/versionCode and full signed build/instrumentation run remain mandatory before release.

## Provenance and Integrity

The approved GitHub/Drive connection was used to reconstruct the V6.1.4 release source. The base ZIP was verified before applying the rescue overlay. The current syllabus reference is the Ministry’s **Physics (3)**, code **112244**, grade 12 Experimental Sciences, school year **1404–1405**.[1]

| Artifact | Historical or revised SHA-256 | Status |
|---|---:|---|
| Frozen V6.1 base Android ZIP | `1344aca90474ac96e27e94ba754ebafd42778e2ceaab91f9a5fb1be2e882d046` | Verified historical base |
| Historical frozen gzip bank | `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14` | Preserved historical reference |
| Historical frozen expanded SQLite bank | `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c` | Preserved historical reference |
| Historical verified-JSON reference | `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d` | Preserved historical reference |
| **Physics second-pass gzip bank** | `ca4f3c63a88bf091d3ce464254048629f939a0f60b8b088e53ccd7bf206ffe2a` | Runtime and static gates now pin this value |
| **Physics second-pass expanded SQLite bank** | `d6d93c2786b5900100bc348b06e740a47a94f1fb89932372a8a5ac0b68a13a5e` | Runtime and static gates now pin this value |
| **Physics second-pass deterministic overlay** | `25238d05278b94fcd8021515d7ee7ee53ac278c5e8d91fcab0ca24d20de0d0a5` | Rebuilt from changed source/test/asset inputs |
| **Physics second-pass workflow** | `96068ec72af543b0fdb07f683e8a635951547b180918538be802156556ec4067` | Bank/overlay pins updated; obsolete publish step disabled |

The revised bank preserves **1,216** question IDs, all four-option structures, correct indices, source-type counts, pool counts, quarantine count, SIM1/SIM2 disjointness, option sets, source metadata, schema, filename, and Room-progress contracts. The only database content edits are learner-facing analysis fields for 18 authored high-ROI Physics records.

## Initial Complete Scan and Scientific Review

The original scan covered **all 187 active Physics records**: 142 TRAIN, 22 SIM1, 22 SIM2, 1 FINAL; 180 authored and 7 official-stem training. It found zero invalid four-option records, zero incorrect key indices, zero full-payload exact duplicates, zero reordered-option duplicates, and zero full-payload numeric-reskin groups. A stem/options collision between `v3_phys_30_02` and `v3_phys_33_02` was inspected and found benign because their canonical comparison stimuli differ.

The scientific deep-review cohort contained all seven available 1402–1404 official-stem Physics records plus representative final-hours authored items, all six terse analyses, and both near-duplicate pairs. The keys were independently checked against model, formula, conditions, sign/direction, units, substitution, and answer. No retained key was changed. The official-pattern profile in the frozen bank comprises 271 official 1398–1404 Physics records from 16 source files and places the greatest recent weight on numerical single-stage and graph/diagram forms; this supports the final-hours focus on explicit calculation paths and conditions.[2]

| Official item | Independent check | Result |
|---|---|---|
| `real_1402_n2in_phys_070` | \(\Delta K=W_g+W_{air}\), so \(22.4-30=-7.6\,J\) | Correct, including negative resistance-air work |
| `real_1404_n2in_phys_075` | \(t=mL_v/P=9024\,kJ/(2\,kJ/s)=75.2\,min\) | Correct |
| `real_1402_n2in_phys_073` | \(5C=1.8C+32\Rightarrow C=10\Rightarrow283\,K\) | Correct |
| `real_1402_n2in_phys_056` | \(\mu=\rho\pi r^2\), \(v=100\,m/s\), crest-to-next-trough \(=\lambda/2=25\,cm\) | Correct |
| `real_1403_n1in_phys_063` | Battery removed means fixed \(Q\); energy rises from 4 to 6 mJ | Correct, increase \(2\,mJ\) |
| `real_1402_n2in_phys_075` | \(|F|=|q|vB\), electron direction reverses \(v\times B\) | Correct, \(0.5\,T\) east |
| `real_1403_n1in_phys_074` | \(B=\mu_0NI/L=2.4\times10^{-3}\,T=24\,G\) | Correct |

## Implemented Fixes

### Shared learner-facing enum safety

`ScienceText.kt` now applies `sanitizeLearnerFacingText` before formula-direction isolation. It maps all audited internal taxonomy keys—such as `wrong_condition`, `partial_truth`, `calculation_trap`, `unit_mistake`, and `overgeneralization`—to Persian learner-facing descriptions. This is a **shared renderer** used across the application, not a Physics-only branch. It prevents raw internal labels from reaching Review option analyses, full correct analyses, lessons, traps, or any other content passed through the scientific text renderer.

### Canonical comparison stimulus in test and review

`Models.kt` now parses `stimulus.type == "comparison"` into `ComparisonStimulus(leftLabel, left, rightLabel, right)` while preserving source crops. `RadiologyApp.kt` renders one shared `ComparisonStimulusCard` in both `TestQuestion` and `ReviewQuestion`, immediately alongside the existing canonical stem/crop flow. No A/B content was duplicated into stems.

The new `ComparisonStimulusRenderTest` loads the **packaged bank** and verifies that the canonical left/right labels and statements for `v3_phys_30_02`, `v3_phys_33_02`, and `v3_phys_34_03` render through that shared component. This is deliberately not a fixture-only assertion.

### Six short Physics analyses expanded

The following analyses now explicitly state the physical model, condition, formula, substitution, unit/sign check, and answer: `v3_phys_30_04`, `v3_phys_30_06`, `v3_phys_30_08`, `v3_phys_30_10`, `v3_phys_33_05`, and `v3_phys_35_05`.

| ID | Added reasoning path |
|---|---|
| `v3_phys_30_04` | Steady incompressible condition → \(A_1v_1=A_2v_2\) → \(v_2=9\,m/s\) |
| `v3_phys_30_06` | \(\rho=m/V\) → \(4/0.002=2000\,kg/m^3\) |
| `v3_phys_30_08` | Same continuity model with condition, substitution, inverse-area rationale, and unit retention |
| `v3_phys_30_10` | Density model, division path, and kg/m³ unit check |
| `v3_phys_33_05` | \(I=V/R=12/6=2\,A\) plus \(V/\Omega=A\) |
| `v3_phys_35_05` | \(v=f\lambda=5\times2=10\,m/s\) plus \(Hz\times m=m/s\) |

### Final-hours high-ROI generic-analysis rewrite

A substantive 18-record high-ROI authored Physics cohort was rewritten. All correct keys and option sets are preserved. The cohort includes the six short analyses plus final-hours conceptual, fluids, circuits, mechanics, thermal, waves, electrostatics, and magnetism items: `v3_phys_27_01`, `29_01`, `30_01`, `30_02`, `30_04`, `30_06`, `30_08`, `30_10`, `33_01`, `33_02`, `33_05`, `28_01`, `28_02`, `31_01`, `35_01`, `35_05`, `32_01`, and `34_03`.

For each revised record, `correct_analysis`, all four `distractor_analyses`, `short_lesson`, `fast_method`, `start_method`, `main_trap`, and `review_default` were rewritten to use question-specific Persian reasoning. The previously templated filler strings are absent from this target cohort.

### Scenario/follow-up session contract

`Question` now exposes its canonical `followup_group`. `BankStore` accepts an `excludedFollowupGroups` set for both `distinctAlternative` and `trainingCandidates`; bulk fallback selection grows this set as items are chosen. `StudyRepository` applies the set in due, weak, topic, and fallback selection paths, records `followupLeak` in session mode, and requires it to be zero for TRAIN sessions.

The pair contracts are explicitly covered by `FollowupGroupSelectionTest`:

| Pair | Shared group | Required contract |
|---|---|---|
| `v3_phys_30_04` / `v3_phys_30_08` | `فشار، چگالی و شاره‌ها::subskill_4` | The second variant cannot enter a normal TRAIN block after the first. |
| `v3_phys_30_06` / `v3_phys_30_10` | `فشار، چگالی و شاره‌ها::subskill_2` | The second variant cannot enter a normal TRAIN block after the first. |

Intentional later spaced retrieval remains possible because this exclusion is session-local; a repeat is not treated as a new distinct scenario within a normal block.

## SECOND_PASS_REVIEW — Exact Results

| Gate | Result |
|---|---:|
| Physics records scanned | 187 |
| High-ROI authored records rewritten | 18 |
| Required short analyses expanded | 6 / 6 |
| Raw enum occurrences stored in all Physics user fields before shared display sanitation | 1,471 |
| **Raw enum occurrences after shared renderer sanitation** | **0** |
| Raw enum occurrences in rewritten 18-record cohort | 0 |
| Generic-filler occurrences in rewritten 18-record cohort | 0 |
| Short-analysis failures after rewrite | 0 |
| Comparison IDs using canonical stimulus fields | 3 / 3 |
| Documented scenario-pair contracts | 2 / 2 |
| Four-option/key/pool/ID/SIM integrity | PASS |
| V6.1 static validation after changes | PASS |

The full static suite ended with `V61_PROJECT_STATIC_VALIDATION=PASS` in a **fresh reconstruction**: the verified base ZIP was unpacked, the compact overlay was applied, `tools/apply_physics_second_pass.py` rebuilt the bank to the two revised hashes above, required audio was regenerated, and all static gates passed. The compact overlay carries source and the deterministic rewrite tool rather than an opaque regenerated bank binary. The new `verify_physics_second_pass.py` gate checks the counts above, renderer mapping, comparison parser and dual test/review call sites, packaged-bank comparison instrumentation test source, and the two follow-up selection contracts.

## Required Remaining Release Gates

This branch deliberately does **not** claim a release-ready APK. The reconstructed local source has no Gradle wrapper or installed Gradle/Kotlin compiler, so Kotlin compile, JVM tests, Android instrumentation, lint, debug/release assembly, signed APK validation, and device flow verification were **not run locally**. The branch workflow’s obsolete V6.1.4 publication step is disabled. The foreman must assign a new patch/minor version and versionCode, then perform the required complete CI and signed-release gates after integrating all workers.

The historical frozen hashes remain recorded; the revised gzip/SQLite hashes are intentionally distinct because 18 bank explanation payloads changed. Any integrated release must ship the revised bank only with the matching runtime constants, workflow pins, new bank audit, migration/progress checks, packaged-bank inspection, and versioned release artifacts.

## References

[1]: http://chap.sch.ir/books/13332 "Ministry textbook portal — Physics (3), code 112244, 1404–1405"
[2]: https://github.com/rynmrde/Konkor/tree/radiology1405-apk-v6.1.4-20260817 "Pinned V6.1.4 source and frozen official-pattern profile"
[3]: https://github.com/rynmrde/Konkor/commit/72dc76e56b7ae625ad1904c76910eeaec5f90f58 "Pinned current-main/V6.1.4 baseline"
