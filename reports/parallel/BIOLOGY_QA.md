# Biology Question-Bank and Analysis Quality Report

## Baseline, scope, and evidence

This worker audited **Biology only** from the newest repository baseline, `main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58` (V6.1.4 Three-Day Rescue). The immutable base bank has not been replaced: expanded SQLite SHA-256 is `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`, and gzip SHA-256 is `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`.

The scientific review used the supplied official Biology textbooks for grades 10–12 after title-page confirmation. It also inspected the supplied 1403 first-session Biology booklet, which contains the audited question text for `real_1403_n1_bio_016`. An independent real-exam source-audit worker then supplied the decisive reconciliation evidence: all fifteen active Biology `real_exam` records passed source-PDF hash, stem-plus-four-options, and 1403 key-table comparisons, with the official Sanjesh notice retained as the primary provenance. The fifteen labels therefore remain unchanged. [1] [2] [3] [4] [5]

| Baseline item | Verified value |
|---|---|
| Repository / baseline branch | `rynmrde/Konkor` / `main` |
| Baseline commit | `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Baseline release | `radiology1405-apk-v6.1.4-20260817` |
| Biology inventory | 411 total: 369 authored, 24 official-stem training, 15 `real_exam`, 3 quarantined conflicts |
| Worker branch | `parallel/bank-biology` |
| Source-audit peer report | `parallel/real-exam-source-audit`, `REAL_EXAM_SOURCE_AUDIT.md` |

## Audit method and required counts

The deterministic scan covered every active Biology record for malformed option structure, invalid keys, missing or generic analysis, raw UI/internal labels, source-label safety, implausibly short distractors, and exact/near duplicate candidates. The deep-review pack included one highest-priority authored TRAIN item for every Biology microtopic plus every unique high-priority generic-analysis or short-option candidate. This connects the review to the rescue engine, which uses safe alternatives from the active TRAIN pool.

| Required count | Result | Interpretation |
|---|---:|---|
| Machine-scanned | 408 | All active Biology records; 3 quarantined conflicts excluded. |
| Deep-reviewed | 44 | Rescue-priority or machine-flagged authored TRAIN questions. |
| Rewritten | 16 | Stable-ID authored questions received question-specific analysis rewrites. |
| Replaced | 0 | No question identity changed. |
| Analysis-rewritten | 16 | Correct analysis, all four option analyses, and short lesson rewritten. |
| Rejected | 0 | No question or real-exam label was rejected after source-audit reconciliation. |
| Duplicates flagged | 64 | 15 exact-stem, 15 identical-option-set, 34 near/cosmetic candidates. |
| Raw UI/internal enum findings | 0 | No `condition_wrong`, `truth_partial`, or analogous UI leakage. |

The 64 duplicate findings are deliberately **candidates**, not an unsupported claim that all are accidental repeats. Generic stems do not establish duplicated learning content where options, rendered stimulus, source crop, or semantic fingerprint differ. They require individual semantic adjudication before any removal, merge, or mastery-counting change.

## Biology improvements

The sixteen modified items preserve their IDs, stems, option text/order, correct index, source type, access pool, scope flag, and holdout status. The change is limited to question-specific explanatory text. Every modified option explanation states the concrete biological reason for correctness or failure and removes generic phrases such as “this definition,” “keyword,” or abstract “trap/control” filler.

| Question IDs | Scientific focus |
|---|---|
| `v3_bio_01_01`, `04_01`, `09_01`, `07_01`, `08_01`, `12_01` | Tier-A rescue concepts: transcription direction, S phase/mitosis, gas exchange, SA-node pacing, pepsin/bile/absorption, and insulin action. |
| `v3_bio_02_01`, `16_01`, `05_01`, `15_01`, `11_01` | Semiconservative replication, evolution, cellular respiration, plant transport, and neurophysiology. |
| `v3_bio_10_01`, `14_01`, `03_01`, `13_01`, `06_01` | Nephron transport, reproductive timing, ABO/X-linked inheritance, innate immunity, and photosynthesis. |

The all-item candidate re-scan reduced generic-filler findings from **115 to 110** while preserving zero raw UI/internal-enum findings. The remaining generic findings need continued review; the 16 current rewrites were limited to the highest-return rescue-visible subset rather than risking a broad unverified rewrite.

## Compact runtime patch, safety, and migration

The final patch is **analysis-only**. It keeps the V6.1 gzip bank immutable in the APK. On first open—or when the app-private database does not match the expected patched SHA—`BankStore` copies and verifies the immutable base, applies the compact JSON patch transactionally to the private database, verifies the patched SHA, and opens the result read-only. The compact patch JSON SHA-256 is `3943af9a9d83872c846c7458fae330184be44b7b1aead7502f1c2620c99ebb5d`; the patched runtime SQLite SHA-256 is `00f881e78e26326532b8b771134970052ddb296fc0e556ab30a980c95656ef14`.

> **No Room migration is required.** Every question ID and all identity-bearing fields remain stable, so attempts, mastery, review history, spaced-retrieval credits, and active-session references remain valid. The archived V6.1 bank remains byte-identical and hash-gated.

The adversarial peer check found a conflict in an earlier draft that conservatively proposed declassifying the fifteen 1403-N1 Biology `real_exam` records because their JSON did not carry a direct key flag. The independent source audit resolved that concern: `15/15` Biology records matched the supplied source bytes, page text/options, and key-table entries. The final patch **does not declassify** any `real_exam` record and preserves global counts `real_exam=17`, `official_exam_stem_training=71`, and `quarantined_key_conflict=16`.

## Validation

| Validation | Result |
|---|---|
| Compact patch reconstruction, transaction simulation, patched-hash verification | **PASS** |
| SQLite `PRAGMA quick_check` after applying patch | **PASS** |
| Original V6.1 static validation suite on compact staging tree | **PASS** |
| Base gzip and SQLite hash gates | **PASS** |
| Rescue triage A15/B21/C20/Q0 and mandatory 869-minute guard | **PASS** |
| Holdout isolation checks in existing suite | **PASS** |
| Active real-exam count after patch | **17** |
| Quarantine count after patch | **16** |

No Android SDK/Gradle wrapper was present in the extracted source bundle, so this worker could not perform a local APK compilation or instrumentation run. The integrator must execute the required Android build, signing, installation, Review/Question Map, process-recreation, and first-launch patch-installation gates before release.

## Files and integration instructions

| File | Change |
|---|---|
| `app/src/main/assets/biology_v615_patch.json` | Compact 16-question Biology analysis patch; no question identity edits. |
| `app/src/main/java/com/radiology1405/prep/data/BankStore.kt` | Immutable-base verification, transactional compact patch installation, patched-hash/count gates. |
| `tests/verify_biology_v615.py` | Deterministic base-to-patched reconstruction and exact-hash verifier. |
| `reports/parallel/BIOLOGY_QA.md` | This audit, evidence, counts, reconciliation, and integration handoff. |

> **Integration instruction:** Integrate the reconciled compact patch, not the superseded pre-reconciliation draft. Run `python3 tests/verify_biology_v615.py`, then `python3 tests/validate_v6_1.py`. On a real Android environment, first launch must begin with no private bank database so that the immutable-base-to-patched installation path is exercised; then perform process recreation and a Biology rescue session before any release decision.

| Commit record | Value |
|---|---|
| Baseline | `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Superseded implementation | `09ab5fc6ee77cd8b06af2a744b543836795320bc` — do **not** integrate; it contained the pre-reconciliation declassification draft. |
| Reconciled implementation | [`8ca9768c10f00676b92767d1884d01d01f2f1f83`](https://github.com/rynmrde/Konkor/commit/8ca9768c10f00676b92767d1884d01d01f2f1f83) |

## Unresolved risks

The residual 64 duplicate candidates require explicit semantic adjudication. The remaining 110 generic-filler findings should be addressed in priority order among rescue-safe authored TRAIN items. The existing 16 historical key conflicts remain quarantined; no quarantine record was promoted or rewritten.

## References

[1]: https://drive.google.com/file/d/1H6V7321-jC8n3MByS4dQ1V2qDHnbrS6f/view "زیست‌شناسی (1), grade 10 official textbook"
[2]: https://drive.google.com/file/d/1Mjyb4dvdsQj51orLsYkvJoHKJBTw7Wjl/view "زیست‌شناسی (2), grade 11 official textbook"
[3]: https://drive.google.com/file/d/1bj2hURks0yOZSEtXJBZRHlzUh4gHBJ-l/view "زیست‌شناسی (3), grade 12 official textbook"
[4]: https://drive.google.com/file/d/1RLMr0QK1qYDfLduSzIwV2U_3UbYUH8Gm/view "1403 first-session Biology source booklet"
[5]: https://github.com/rynmrde/Konkor/blob/parallel/real-exam-source-audit/reports/parallel/REAL_EXAM_SOURCE_AUDIT.md "Independent 1403 real-exam source audit"
