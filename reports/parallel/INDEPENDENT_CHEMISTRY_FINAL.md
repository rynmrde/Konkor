# Independent Chemistry Final Review

**Reviewed branch:** `parallel/a1-chemistry`  
**Reviewed commit:** [`4e9a2f2c90ae7cc1e0ee093f341083e3d4295cd7`](https://github.com/rynmrde/Konkor/commit/4e9a2f2c90ae7cc1e0ee093f341083e3d4295cd7)  
**Parent:** `1b050d79357739525ca810914332e885a62ff737`  
**Requested helper branch:** `parallel/help-independent-chemistry-final`  
**Scope:** independent bank, overlay, structured-stimulus, selection-signature, quantitative-analysis, duplicate-classification, and final active-TRAIN checks. No main, bank, release, or scientific content was modified.

## Executive decision

The corrected Chemistry source overlay is independently verified as the exact expected artifact, and the frozen bank remains byte-identical. The corrected implementation preserves the active 16 structured-stimulus cases through canonical `data_table`/`comparison` fields, renders them in Test and Review source paths, and includes the stimulus payload in `practiceSignature`. All 203 active TRAIN Chemistry records have four options and valid answer keys. The 19 named quantitative overrides are present and, on full text review with arithmetic/chemical recomputation, no wrong key, formula, or unit was found.

The result is **CONDITIONAL PASS for the requested Chemistry data/source gates**, not release approval. Android compilation, JVM tests, lint, signed APK, and runtime/instrumentation gates were not run in this sandbox. The exact historical claim of “29 repeated-analysis groups” is not reproducible as the current aggregate: the corrected report records 35 identical-analysis groups covering 77 records. The safe classification and source-only remediation are supported, but the exact number must not be presented as independently confirmed without the earlier scan artifact.

## Gate matrix

| Gate | Result | Exact independent evidence |
|---|---|---|
| Exact corrected commit | **PASS** | Commit `4e9a2f2c90ae7cc1e0ee093f341083e3d4295cd7`; parent is prior Chemistry tip `1b050d79357739525ca810914332e885a62ff737`. |
| Expected overlay SHA-256 | **PASS** | `radiology_v614_rescue_patch/overlay.tar.xz` hashes to `8f3ac3751a92534c7767afce31d36f880b1c0aaabac68e15bbe6be396c9609d2`. |
| Frozen bank untouched | **PASS** | Frozen gzip hash `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`; expanded DB hash `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`. The overlay contains source files only and no bank asset. |
| Chemistry record count | **PASS** | 267 Chemistry records in the frozen DB. |
| Active TRAIN count | **PASS** | 203 records satisfy `access_pool=TRAIN`, `selected_scope=1`, and `obsolete=0`. |
| Four options and valid keys for all active TRAIN | **PASS** | Independent SQLite/JSON checker found no bad active record. |
| Structured stimuli, total | **PASS** | 20 Chemistry records have `stimulus.type` equal to `data_table` or `comparison`. |
| Requested 16 structured cases | **PASS** | Exactly 16 of those 20 are active TRAIN; the other four are outside active TRAIN selection. The active IDs are recorded in the attached checker output and are preserved in the frozen bank. |
| Canonical stimulus parsing | **PASS** | `Models.kt` parses table caption/headers/rows and comparison labels/values into typed fields. |
| Selection-signature inclusion | **PASS** | `Question.practiceSignature` concatenates normalized core stem and `stimulusSignature`; `BankStore.kt` applies the signature in `trainingCandidates`, `uniquePoolIds`, and `distinctAlternative`. |
| Stimulus rendering path | **PASS at source level** | `RadiologyApp.kt` invokes `QuestionStimulus` in both question/test and review rendering paths and renders table rows and comparison fields. Device/UI execution remains open. |
| 19 quantitative overrides present | **PASS** | All 19 named IDs occur in `correctedChemistryAnalyses`; each has equation/formula or explicit calculation, numeric result evidence, and chemical/unit evidence. |
| 19 quantitative overrides scientific validity | **PASS, source/manual review** | Yield, limiting reagent, gas volume, solubility, isotope averages, pH/pOH dilution, reaction rates, and acidic redox were independently recomputed. No wrong key, formula, or unit was found. |
| Localization coverage | **PASS at source level** | The map contains 13 internal-token forms, including the previously missing `calculation_trap`; frozen raw strings remain untouched by design. |
| Earlier five exact duplicate groups | **PASS classification** | They are not bank deletions: the structured stimuli distinguish the underlying records, and stimulus-aware signatures produce zero duplicate groups in the 20 structured records. |
| Earlier five numeric candidate groups | **PASS classification** | Numeric values and charge signs remain in the canonical stem/signature. They are not automatically collapsed or rewritten; same-block exclusion remains deliberate. |
| Earlier 29 repeated-analysis groups | **NOT REPRODUCED as an exact count** | The corrected report’s current aggregate is 35 identical-analysis groups covering 77 records. The remediation is safe source-only localization/compaction plus 19 targeted overrides, but the historical “29” number is not independently confirmed here. |
| Final checker claim | **PASS for structural/data checks** | Independent checker: 203 active TRAIN; no four-option/key failures; all 19 overrides present with evidence. The supplied static rescue validator also passed after using the independently verified frozen DB. |
| Android/build/runtime gates | **OPEN / NOT RUN** | This review did not claim Kotlin compilation, JVM tests, lint, APK signing, API-35 instrumentation, installation, or UI interaction PASS. |

## Exact structured-stimulus evidence

The frozen bank contains 20 structured Chemistry records, not 16 in total. The requested 16-case figure is correct for the active TRAIN subset. The four structured records outside active TRAIN are `v3_chem_19_10`, `v3_chem_20_03`, `v3_chem_26_03`, and `v3_chem_54_07`; the active set contains the remaining 16 structured IDs. This distinction matters because a total-bank scan that reports 20 and an active-selection scan that reports 16 are both correct but answer different questions.

The implementation is structurally coherent. `Models.kt` reads `data_table` captions, headers, and rows, or `comparison` labels and values. `practiceSignature` normalizes and includes the complete stimulus representation. `RadiologyApp.kt` renders the same parsed fields in both test and review paths. `BankStore.kt` excludes used signatures in normal selection and fallback selection. The independent signature scan found no duplicate signatures among structured records.

## Quantitative override review

All 19 named overrides were read from the corrected `Models.kt`. The main scientific checks were as follows. The two yield records calculate \((30/40)\times100=75\%\). The limiting-reagent records use \(n/\text{coefficient}\) correctly and obtain 3 mol water from 3 mol hydrogen. The magnesium chain correctly applies 60% of 10 g, converts 6 g to 0.25 mol, and obtains 5.6 L hydrogen at 22.4 L·mol⁻¹. Solubility records scale grams of solute and water consistently. Isotope records correctly use weighted averages and atom counts. The pH/pOH records correctly apply tenfold or hundredfold dilution and the 25 °C relation \(pH+pOH=14\). Reaction-rate records correctly use concentration change over time and stoichiometric coefficients. The redox override supplies balanced acidic half-reactions, the net equation, coefficient sum 16, and oxidation-number comparison.

These are source-level scientific checks of the 19 override texts against the corresponding bank stems and keys. They are not a replacement for official-textbook adjudication, APK runtime review, or release QA.

## Duplicate and repeated-analysis classification

The old exact/numeric duplicate findings are safely classified without mutating the frozen bank. The old exact-looking cases carry distinct table or comparison stimuli that the previous `Question` model discarded. The corrected parser preserves them, and the signature includes them. Numeric variants retain values and signs, so the implementation does not incorrectly collapse legitimate calibration variants. Across-time spaced retrieval remains possible; only same-block selection is guarded.

The repeated-analysis issue is more nuanced. The current report states 35 identical-analysis groups covering 77 records, while the earlier independent review referenced 29 groups. Because the exact earlier scan artifact is not part of the specified commit, this review marks the exact 29 count **not reproduced**, not PASS. The safety decision is nevertheless sound: no bank rewrite was made, and the source-only changes remove raw internal labels and target 19 high-ROI calculation explanations. A future bank-versioned semantic rewrite is still needed for genuinely generic distractor explanations.

## Validation limitations and remaining gates

The supplied static validator initially could not run because the overlay intentionally excludes the bank asset; after placing the independently verified frozen DB in a disposable local workspace, it returned `V614_RESCUE_VALIDATION=PASS`. This does not prove a packaged APK contains the correct asset. Kotlin/JVM compilation, Android lint, signed build, apksigner verification, API-35 instrumentation, install/launch, and interactive Test/Review stimulus rendering remain release-owner responsibilities.

No speculative bank rewrite, key correction, ID mutation, migration change, or release action was performed.

## References

[1]: https://github.com/rynmrde/Konkor/commit/4e9a2f2c90ae7cc1e0ee093f341083e3d4295cd7 "Exact corrected Chemistry commit"
[2]: https://github.com/rynmrde/Konkor/tree/radiology1405-apk-v6.1.4-20260817 "V6.1.4 historical release source"
[3]: https://drive.google.com/drive/folders/1R2IovFE_e0O_vU4IBCSiJpqrwK4LecxK "Frozen V6.1 evidence folder"
