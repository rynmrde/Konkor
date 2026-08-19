# A1 Chemistry Bank and Solution-Quality QA Handoff

**Role:** `KONKOR-A1-M3-CHEMISTRY` — Chemistry bank and solution-quality owner  
**Account label:** A1 / Standard 1.6  
**Branch:** `parallel/a1-chemistry`  
**Baseline recorded before work:** `72dc76e56b7ae625ad1904c76910eeaec5f90f58` on `origin/main`  
**Scope:** active Chemistry bank, solution-quality risk, raw-enum display, same-block duplicate prevention, and Final-Hours high-ROI Chemistry review. No `main` merge and no Release publication were performed.

## Executive Finding

The active immutable V6.1 Chemistry bank contains **267** records. Its structural/key/source invariants passed the full machine scan, but the scan confirmed widespread raw internal-enum text in user-visible analysis fields, substantial repeated authored-question forms, and repetitive/generic analysis prose. A source-only remedy was prepared because the archived bank must remain byte-identical unless a separately versioned, evidence-backed bank migration is approved.

The remedy localizes known raw internal trap tokens at parsing time and adds a canonical **same-block practice signature** to prevent repeated underlying question forms, including reordered-option variants represented by fixed generic stem wrappers. The implementation preserves IDs, Room data, progress, the archived bank gzip, and its expanded SQLite bytes. It does **not** relabel any item as official/real-exam, alter bank content, change holdouts, or affect SIM pools.

| Area | Result |
|---|---:|
| Active Chemistry records machine-audited | **267 / 267** |
| Four-option/key/identity/source integrity flags | **0** |
| Final-Hours selected records deep-reviewed | **60** |
| Underlying high-ROI problem clusters reviewed | **40** |
| Confirmed numerical/conceptual key defects in reviewed clusters | **0** |
| Bank records rewritten | **0** (frozen artifact deliberately preserved) |
| Source-layer raw-enum localization mappings | **12** |
| Raw-enum field occurrences addressed by parse-time display localization | **1,076** |
| Exact stem-and-option duplicate groups found | **5 groups / 19 records** |
| Reordered-option duplicate groups found | **2 groups / 20 records** |
| Numeric-skeleton clone candidates requiring human adjudication | **2 groups / 20 records** |
| Identical correct-analysis groups | **35 groups / 77 records** |

## Evidence and Calibration Material

The bank copy was read from the frozen V6.1 artifact and independently checked against both recorded immutable hashes: gzip `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14` and expanded SQLite `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`. The current Chemistry grade 10, 11, and 12 textbook PDFs and recent 1402–1404 Chemistry booklets were retrieved from the project Drive evidence folder and text-extracted locally. The full source inventory, IDs, links, and local SHA-256 values are recorded in `audit/EXTERNAL_EVIDENCE_SOURCES.md`.

The deep review checked every Final-Hours selected Chemistry record as a variant or underlying problem cluster. High-ROI calculations were chemically and arithmetically consistent: mole ratios and limiting reagents; gas molar volume at stated standard conditions; dilution and mass percent; solubility; isotope weighted averages; ionic charge/electron count; pH/pOH at 25 °C; strong-acid/base dilution; equilibrium quotients; enthalpy sign/stoichiometric scaling; and electrochemical charge. Representative verified paths include `KClO₃: 0.20 mol × 3/2 = 0.30 mol O₂ = 6.72 L`, `Q = It = 2 A × 30 s = 60 C`, and `pH = −log(2 × 10⁻³) ≈ 2.70`.

> No official-source metadata was invented. The reviewed records remain authored training items unless their complete year/session/question/booklet/page/stem/options/key evidence is separately established.

## Implemented Source-Only Remediation

The new overlay archive is `a1_chemistry_overlay.tar.xz`, SHA-256 `6890957e411156194a993ea5bb3531797a5b1e86dd88c9e26f7286deb9131679`.

| File | Change | Safety consequence |
|---|---|---|
| `app/src/main/java/com/radiology1405/prep/data/Models.kt` | Maps raw internal trap tokens such as `wrong_condition`, `partial_truth`, and `overgeneralization` to Persian learner-facing labels before review/cue rendering. | Removes raw enum leakage without touching stored bank data. |
| `Models.kt` | Builds a normalized core-stem practice signature after removing two known non-semantic authored wrapper frames; preserves numerical values and charge signs. | Detects same underlying form while avoiding automatic collapse of merely numeric reskins. |
| `app/src/main/java/com/radiology1405/prep/data/BankStore.kt` | Excludes signatures already selected in a normal training block in `trainingCandidates` and `distinctAlternative`; adds `uniquePoolIds`. | Prevents same question forms from entering one normal block. |
| `app/src/main/java/com/radiology1405/prep/data/StudyRepository.kt` | Routes the former fallback through `uniquePoolIds`. | Prevents fallback logic from reintroducing clone forms after normal selection is exhausted. |
| `tests/verify_rescue_v614.py` | Adds static regression gates for localized raw tokens and signature-guard wiring. | Makes integration failure visible before a release build. |

The mapping is intentionally presentation-layer only. It does not claim an enum-label replacement is a sufficient scientific distractor analysis; it merely eliminates unacceptable raw developer text. A subsequent versioned bank rewrite should replace enum-only distractor explanations with question-specific explanations where the localized label still lacks the concrete chemical relation.

## Duplicate and Analysis-Quality Findings

The ordinary authored stem wrappers below were masking duplicate underlying problems:

> `داده‌های زیر را با مدل مناسب پیوند دهید…`  
> `برای حل مسئلهٔ زیر، کدام پاسخ نهایی با مسیر کنترل درست جفت شده است؟`

Examples confirmed in Final-Hours reachable Chemistry include yield (`v3_chem_17_03` / `v3_chem_17_07`), gas-law volume (`v3_chem_17_04` / `v3_chem_17_08`), atomic charge (`v3_chem_18_02` / `v3_chem_18_06` / `v3_chem_18_10`), isotope average (`v3_chem_18_03` / `v3_chem_18_07`), pH/pOH (`v3_chem_22_02` / `v3_chem_22_06` / `v3_chem_22_10`), and ten-fold strong-acid dilution (`v3_chem_22_03` / `v3_chem_22_07`). The guard is deliberately applied only to normal selection; it does not rewrite the frozen bank or change intended spaced retrieval across time.

The numerical reasoning in the reviewed items is substantively correct, but many analyses repeat templated filler such as “تیپ را تشخیص بده…” and duplicate the same result. This is a quality defect rather than a key defect. No bank rewrite was committed because the archive is frozen and a mass semantic cleanup must be versioned, source-reviewed, and migration-safe rather than silently replacing historical data under deadline pressure.

## Validation Evidence

| Gate | Result | Evidence |
|---|---|---|
| Frozen gzip/SQLite hashes | PASS | `scripts/verify_chemistry_patch.py` recomputed both expected hashes. |
| Chemistry row count / option-key integrity | PASS | 267 rows; all records have four options and a valid key. |
| Raw enum localization wiring | PASS | `audit/CHEMISTRY_PATCH_VALIDATION.json`. |
| Same-block duplicate guard wiring | PASS | `audit/CHEMISTRY_PATCH_VALIDATION.json`. |
| Full V6.1 static rescue/bank/coverage/SIM gate | PASS | `audit/chemistry_overlay_static_validation.txt`: `V614_RESCUE_VALIDATION=PASS`. |
| Local Kotlin/JVM compile | NOT RUN to completion | The sandbox initially lacked both a Gradle wrapper and Android SDK. Gradle 8.13 was provisioned, but configuration stopped before compile because no Android SDK was available. This is an environment prerequisite, not a PASS and not a release gate waiver. CI/foreman must run Kotlin compile, JVM tests, lint, debug build, signed build, and API-35 instrumentation. |
| Bank mutation | PASS — none | Immutable gzip and DB hashes remain exactly unchanged. |

## Handoff and Integration Instructions

The foreman should replace `radiology_v614_rescue_patch/overlay.tar.xz` with the archived source-only overlay and update the corresponding overlay SHA in the release workflow **only after rebasing this change onto the then-current `main` and incrementing the app version appropriately**. This worker does not alter workflow versioning, signed-release logic, package identity, or release metadata.

Integration must rerun the full required release matrix. In particular, the foreman must verify an actual normal TRAIN block cannot contain two records with the same `practiceSignature`, while SIM1/SIM2 disjointness and intentional due retrieval behavior remain unchanged. The UI flow must also confirm that Review displays Persian labels instead of raw strings such as `wrong_condition`.

### Residual Risks Requiring Follow-Up

The two numeric-skeleton clone clusters are **candidates**, not automatically excluded by this patch; numerical values and charge signs are retained in the practice signature to avoid suppressing legitimately distinct calibration questions. The 35 identical-analysis groups and enum-only distractor explanations need a controlled, source-backed bank version if time permits. None of these residuals justifies mutating the frozen V6.1 bank without a proper minor bank version, ID/mapping strategy, migration test, and fresh signed-bank verification.

## References

[1]: https://drive.google.com/file/d/1rmRyR509x-8bDAS0FG6WiP9R5DtXjfXH/view?usp=drivesdk "Chemistry Grade 10"
[2]: https://drive.google.com/file/d/15JZUrFMTgbTuWI0TkfpzUVfGCXhqIL1q/view?usp=drivesdk "Chemistry Grade 11"
[3]: https://drive.google.com/file/d/1G_aP6CYOsuGmkqdtcwMBvJXc6g4UorkF/view?usp=drivesdk "Chemistry Grade 12"
[4]: https://drive.google.com/file/d/1W_UFLtworR9k5cKESoyqgMzfqWiL1NTn/view?usp=drivesdk "1404 Chemistry Booklet, Session 1"
[5]: https://drive.google.com/file/d/1xGCDyu_20UlEyLWqDeymrnT1TT_DB70C/view?usp=drivesdk "1404 Chemistry Booklet, Session 2"
[6]: https://drive.google.com/file/d/1rJU59jwXiEivi8N9hUdBlXfb3_7GyA7X/view?usp=drivesdk "1403 Chemistry Booklet, Session 1"
[7]: https://drive.google.com/file/d/1r2WtLKZC54ZSzSWRORtr1QEu-DG-1NJ0/view?usp=drivesdk "1403 Chemistry Booklet, Session 2"
[8]: https://drive.google.com/file/d/1PsUqwtYRbLnkVMn10Ne0KQdyDnk8bfMn/view?usp=drivesdk "1402 Chemistry Booklet, Session 2"

## Confirmed Branch State and Secondary Assistance

The required Chemistry handoff report was committed to `parallel/a1-chemistry` at [`966d2e854a98fe68dfa968ca0c5e092845d9f9af`](https://github.com/rynmrde/Konkor/commit/966d2e854a98fe68dfa968ca0c5e092845d9f9af). The packaged overlay replacement was subsequently committed at [`1b050d79357739525ca810914332e885a62ff737`](https://github.com/rynmrde/Konkor/commit/1b050d79357739525ca810914332e885a62ff737), which is the confirmed current Chemistry branch tip. Neither commit targets `main` or publishes a release.

After the primary handoff, the branch inventory showed `parallel/a2-math-duplicates` still at the main baseline. A new helper branch, `parallel/help-a1-m3-math-duplicates`, was created from `72dc76e56b7ae625ad1904c76910eeaec5f90f58`. A read-only Mathematics duplicate scan found 247 records, zero literal normalized stem-and-option groups, and 33 wrapper-normalized same-underlying-problem candidate groups covering 90 records. The local helper report is `reports/parallel/HELP_A1_M3_MATH_DUPLICATES.md`.

The helper report commit itself was **not confirmed**: the connected GitHub service began returning TLS/connector timeouts after the helper branch creation. No unverified helper commit is claimed. The local report and `audit/MATH_DUPLICATE_HELPER.json` are preserved for the Mathematics owner or foreman to commit when the service is available.

> The local compile gate remains **not passed** because this sandbox lacks an Android SDK. The immutable-base plus overlay static validator passed. The foreman must run the required CI/Android SDK compile, test, lint, build, signing, and instrumentation gates before integration or release.

## SECOND_PASS_REVIEW — V6.1.4 Release-Source Validation

This second pass compared the original V6.1.4 rescue overlay (`overlay.tar.xz`) byte-for-byte at the source-file level with the proposed Chemistry overlay. The release-overlay diff confirmed that the earlier Chemistry proposal changed only `Models.kt`, `BankStore.kt`, `StudyRepository.kt`, and `tests/verify_rescue_v614.py`; no frozen-bank file, migration, package identity, simulation blueprint, or signing input was changed. The immutable V6.1.4 bank gzip still hashes to `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`.

| Second-pass finding | Decision | Evidence |
|---|---|---|
| Visible raw enum coverage was incomplete. | **Corrected.** Added `calculation_trap → دام محاسباتی`; all 13 visible raw-token forms are now covered. | `scripts/visible_chemistry_tokens.py` found 229 visible occurrences of exactly `wrong_condition`, `partial_truth`, `correct_reasoning`, and `calculation_trap`; `SECOND_PASS_DISPLAY_VALIDATION=PASS`. |
| The earlier count of 1,076 did not mean 1,076 user-visible enum leaks. | **Corrected report interpretation.** That count included raw metadata and review-derived scan paths; the second-pass visible-field count is 229. | `audit/SECOND_PASS_VISIBLE_CHEMISTRY_TOKENS.json`. |
| Generic authored explanation filler persisted in learner-facing fields. | **Corrected at parse/display layer.** Three exact templates are compacted without modifying the immutable bank. | The three templates occurred 63, 63, and 50 times respectively; after compaction no template remains in any rendered Chemistry field. |
| `v3_chem_23_13` lacked an explicit numerical calculation path. | **Corrected.** The learner-facing analysis now states coefficient ratio, substitution, rate units, and both results: `0.060 M·s⁻¹` and `0.015 M·s⁻¹`. | Verified against `2N₂O₅→4NO₂+O₂`: `4/2×0.030` and `1/2×0.030`. |
| `real_1404_n1in_chem_105` used an abbreviated, non-self-standing balanced-equation note. | **Corrected.** The analysis now provides both acidic half-reactions, the net balanced equation, coefficient sum, and oxidation-number comparison. | Net equation: `3MnO₂+4H⁺+2NO→3Mn²⁺+2H₂O+2NO₃⁻`; coefficient sum 16; Mn sum +6 versus N sum +7. |
| Duplicate answer options within a question. | **No defect found.** | All 267 Chemistry records retain four normalized-distinct option texts. |
| Other eight initial quantitative heuristic flags. | **Rejected as false positives or non-numerical conceptual items.** | Item-level review covered `v3_chem_23_13`, `v3_chem_25_05`, `v3_chem_25_09`, `real_1401_in_chem_105`, `real_1402_n2in_chem_097`, `real_1402_n2in_chem_103`, `real_1404_n1in_chem_079`, and `real_1404_n1in_chem_105`. |

The duplicate-selection guard was retained after review. Its canonical signature removes only the two proven generic authored framing sentences, preserves all numbers and signs in the underlying stem, and is restricted to same-block normal training selection. It does not mutate the bank, erase intentional across-time retrieval, or automatically suppress numeric-reskin candidates.

### Exact Second-Pass Tests

| Test | Result |
|---|---|
| `python3 scripts/second_pass_chemistry_validator.py` | PASS: 267 Chemistry rows; 0 normalized duplicate-option records; 63/63/50 generic-template instances inventoried; 8 heuristic calculation candidates enumerated for manual adjudication. |
| `python3 scripts/visible_chemistry_tokens.py` | PASS: 229 visible raw-token occurrences across exactly four forms, including the previously unmapped `calculation_trap`. |
| `python3 scripts/verify_second_pass_chemistry_display.py` | PASS: gzip hash preserved; 13 localized token mappings; three generic fillers compacted; two exact quantitative overrides present; zero remaining visible raw tokens, generic fillers, or duplicate-option records. |
| `python3 validation_project/tests/verify_rescue_v614.py` | PASS: V6.1.4 frozen-bank, coverage, quarantine, simulation, and second-pass static source assertions. |

> This remains a source-only overlay update. It does not convert generic distractor labels into fabricated scientific reasoning, relabel official provenance, or alter the archived bank. Detailed item-specific distractor rewrites require a separately versioned, source-backed bank migration.

**Second-pass overlay archive:** `a1_chemistry_second_pass_overlay.tar.xz`  
**SHA-256:** `e3bde3838b7241c95444a43fa52ecdde035d6ffbc31e0cdd57768c9f5c4cbeee`

**Second-pass branch publication status:** The local overlay and this updated report are ready, but their commit to `parallel/a1-chemistry` was **not completed**. At 2026-08-19 13:xx UTC, the connected GitHub service returned `permission_denied: 403 Forbidden` while creating the branch-scoped update. The earlier confirmed branch tip therefore remains `1b050d79357739525ca810914332e885a62ff737`. The staged payload is retained at `staging/github_commit_second_pass_chemistry.json` for a foreman to submit after connector restoration.

## INDEPENDENT_BLOCKER_REVIEW — Quantitative, Duplicate, and Renderer Reconciliation

This review rechecked the immutable V6.1.4 Chemistry bank against the proposed source overlay rather than accepting aggregate heuristics as defects. The frozen gzip remains `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`; no bank row, stable ID, option, key, provenance field, migration, or simulation blueprint was modified.

| Reported signal | Independent finding | Resolution |
|---|---|---|
| Five exact active-TRAIN duplicate groups | The generic stem and reordered `ردیف`/A–B answer labels alone are identical, but all 16 examined items contain distinct authored `data_table` or `comparison` stimuli in frozen JSON. The release `Question` model discarded these stimuli, so the UI did not render the premise and the old signature falsely collapsed them. | **Confirmed renderer/identity blocker fixed.** `Question` now parses table/comparison stimuli; both Test and Review render them; duplicate identity includes the stimulus payload. The 16 records now yield 16 distinct signatures. |
| Five numeric-variant groups | Values and signs remain part of the normalized core stem. Same-problem variants are intentionally collapsed in a normal block, while different numeric stems remain distinct. | **No bank rewrite.** The existing same-block guard remains; the new contract explicitly proves a numeric change is preserved. |
| 29 identical `correct_analysis` groups | This is not independently sufficient evidence of a bad answer: most groups are the same underlying authored problem in ordinary, paired-method, and data-table presentation forms. | **No mechanical rewrite.** Same-block signature selection prevents repeated underlying problems; display-layer filler compaction and targeted calculation overrides address the actual learner-facing quality defect. |
| Strict calculation checker (reported 40; broad local heuristic 61) | A formula/operator+number+unit regex falsely flags conceptual questions, count outputs, pH, percentages, and fully supported official comparison questions. However, it correctly identified high-ROI authored calculations whose displayed reasoning needed a shorter explicit path. | **Confirmed quality fixes applied.** Nineteen source-only correct-analysis overrides now provide actual formula/equation, substitution, condition, result, and a relevant unit where dimensional. |

### Confirmed Quantitative Analysis Overrides

The reviewed overrides cover `v3_chem_17_03`, `v3_chem_17_05`, `v3_chem_17_07`, `v3_chem_17_09`, `v3_chem_17_16`, `v3_chem_17_17`, `v3_chem_21_15`, `v3_chem_21_19`, `real_1404_n1in_chem_079`, `v3_chem_18_14`, `v3_chem_18_17`, `v3_chem_18_20`, `v3_chem_22_17`, `v3_chem_22_18`, `v3_chem_23_02`, `v3_chem_23_06`, `v3_chem_23_10`, `v3_chem_23_13`, and `real_1404_n1in_chem_105`. Examples include `22.4 L·mol⁻¹` for the Mg-to-H₂ chain, `0.030 M·s⁻¹` for average rate, `10⁻⁴ M` for acid dilution, weighted-isotope equations with `amu`, and the complete acidic redox balance. Questions whose requested result is intrinsically unitless or conceptual were not padded with fake units merely to satisfy the regex.

### Exact Independent Validation

| Test | Result |
|---|---|
| `python3 scripts/independent_chemistry_quant_review.py` | PASS as a conservative inventory: 203 active TRAIN Chemistry records; it surfaced broader heuristic groups for manual adjudication, not automatically accepted defects. |
| `python3 scripts/inspect_placeholder_stimuli.py` | PASS: all 16 generic-stem records have complete frozen `data_table` or `comparison` payloads. |
| `python3 scripts/verify_stimulus_duplicate_contract.py` | PASS: 16/16 former generic-stem records have unique stimulus-aware signatures; numeric variants remain distinct. |
| `python3 scripts/validate_independent_chemistry_fixes.py` | PASS: immutable gzip hash preserved; 203 active TRAIN records have four options and valid keys; all 19 checked quantitative overrides contain their expected formula/result/unit evidence. |
| `python3 validation_project/tests/verify_rescue_v614.py` | PASS: frozen bank, coverage, holdout, prior localization, duplicate guard, new stimulus parser/renderer, and quantitative override static assertions. |

> **No Physics bank work was performed in this pass.** The previously started fallback is superseded by the now-existing `parallel/a2-physics` full audit. This patch shares only the generic renderer/duplicate contract and does not modify Physics records.

**Final independent Chemistry overlay:** `a1_chemistry_independent_final_overlay.tar.xz`  
**SHA-256:** `8f3ac3751a92534c7767afce31d36f880b1c0aaabac68e15bbe6be396c9609d2`

**Final publication status:** The final independent overlay and report are staged in `staging/github_commit_final_chemistry.json` (payload SHA-256 `434a9f1ca450ed821d80ab0f9b63d500f44643a1174fdf0fa3e623c30a013584`) but are **not confirmed committed**. The connected GitHub service failed first with `unavailable: net/http: TLS handshake timeout`; a follow-up service-health check returned the same error. The previously confirmed remote branch tip remains `1b050d79357739525ca810914332e885a62ff737`. No main merge, Release, or Physics branch edit was attempted.
