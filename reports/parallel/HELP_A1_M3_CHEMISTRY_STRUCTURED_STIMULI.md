# A1/M3 Helper Report — Chemistry Structured-Stimulus Rendering

**Role:** Chemistry structured-stimulus UI/resume helper  
**Account label:** A1/M3  
**Full V6.1.4 base inspected:** `validation_base/radiology1405_android_v6_1` from the checksum-verified V6.1 base project  
**Immutable bank:** gzip SHA-256 `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`; SQLite SHA-256 `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`

## Finding

The unmodified full V6.1.4 source parses and renders only `official_source_crop`. It discards `stimulus.type == "data_table"` and `stimulus.type == "comparison"` in `Question.fromJson`; both `TestQuestion` and `ReviewQuestion` therefore show only a generic stem and options. The session already persists question IDs and reloads them through `BankStore`, but the released parser loses structured payload after every reload. This is a genuine learner-facing blocker, not a duplicate-scanner artifact.

The source-layer fix preserves `TableStimulus` and `ComparisonStimulus` in `Question`, renders them before the full stem in both Test and Review, and keeps the content in the question object loaded by `activeSummary` and `startOrResume`. The same payload also participates in the duplicate signature, so distinct table/A–B questions are neither hidden nor falsely treated as one question.

## Exact Inventory

The prior “known 16” is incomplete. The immutable active non-obsolete Chemistry bank has **20** structured-stimulus records: **17** `data_table` records and **3** `comparison` records. Sixteen are TRAIN and four are SIM1. Every record has a complete structured payload, four distinct options, a valid correct index, a correct-answer analysis, and four option analyses.

| Type | Exact IDs |
|---|---|
| `data_table` | `v3_chem_19_10`, `v3_chem_19_11`, `v3_chem_19_12`, `v3_chem_19_13`, `v3_chem_20_18`, `v3_chem_20_19`, `v3_chem_20_20`, `v3_chem_26_10`, `v3_chem_26_11`, `v3_chem_26_12`, `v3_chem_26_13`, `v3_chem_54_11`, `v3_chem_54_12`, `v3_chem_54_13`, `v3_chem_55_14`, `v3_chem_55_15`, `v3_chem_55_16` |
| `comparison` | `v3_chem_20_03`, `v3_chem_26_03`, `v3_chem_54_07` |

## Test, Review, and Resume Contract

| Flow | Release V6.1.4 base | Patched overlay |
|---|---|---|
| JSON parsing | Fails: only source crops are retained. | Passes: table and comparison payloads are parsed into typed fields. |
| Test screen | Fails: no table/A–B data is rendered. | Passes: `QuestionStimulus(question)` renders caption, headers, rows, A and B content before the stem/options. |
| Review screen | Fails: no structured premise beside answer/key/reasoning. | Passes: the identical full stimulus appears before stem, answer status, correct analysis, and option explanations. |
| Resume/reopen | ID reload works, but parser loses structured fields. | Passes: `activeSummary` and `startOrResume` reload by stable ID through the fixed parser. |

## Deterministic Validation

| Command | Result |
|---|---|
| `python3 scripts/verify_chemistry_structured_stimuli.py` | PASS: all 20 exact IDs, complete payloads, four options, valid keys, answer/distractor reasoning, base gap, and patched parser/render/resume contract. |
| `python3 validation_project/tests/verify_chemistry_structured_stimuli.py` | PASS: portable fixture test against full V6.1.4 source plus overlay. |
| `python3 validation_project/tests/verify_rescue_v614.py` | PASS: frozen bank, prior compatibility gates, and the extended source assertions. |

The portable integration test is `tests/verify_chemistry_structured_stimuli.py`. It hard-fails if the structured-ID inventory changes, an option/key/reasoning field is incomplete, either renderer call disappears, either structured parser branch disappears, or ID-based resume stops reloading through `BankStore`.

## Scope and Integration

This helper is Chemistry/UI-only. It does not modify the frozen bank, schema, progress data, Physics data, `main`, or a Release. It should be integrated with the current Chemistry overlay source package, because `Models.kt` and `RadiologyApp.kt` are shared source files. The historical `MANIFEST.txt` is intentionally not rewritten.

**Remote publication status:** not yet confirmed. The connected service previously returned `permission_denied: 403 Forbidden`; this helper report and patch are staged locally for publication to `parallel/help-a1-m3-structured-stimulus` only once access is available.
