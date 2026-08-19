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
