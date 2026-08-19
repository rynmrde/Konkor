# Independent Helper QA — Biology Bank

> **Helper branch:** `parallel/help-bank-chemistry-bank-biology`  
> **Target branch inspected:** `parallel/bank-biology` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
> **Scope:** Read-only structural and solution-quality QA. No Biology question, target branch, main branch, release, or holdout assignment was changed.

The target Biology branch was still at the frozen baseline, so it remains an unfinished scientific-bank bottleneck. The embedded bank passed `PRAGMA quick_check`. It contains 411 Biology records: 369 authored, 24 official-exam-stem training, 15 real-exam, and three quarantined key-conflict records. There are 329 active selected Biology TRAIN questions.

| QA gate | Result |
|---|---:|
| SQLite quick check | PASS (`ok`) |
| Four-option/key/analysis structural errors | 0 found by this scan |
| Exact duplicate groups including full stimulus | 0 |
| Semantic fingerprint duplicate groups | 0 |
| Authored records carrying generic review-template markers | 369 |
| Records exposing raw internal enum labels inside review payload | 296 |

The highest-priority active authored block begins at `v3_bio_01_01` and is particularly urgent because it covers the high-yield “بیان ژن: رونویسی، ترجمه و تنظیم” microtopic. For example, `v3_bio_01_01` correctly identifies RNA synthesis as 5′→3′ but then appends generic coaching text. `v3_bio_01_02` has a valid mRNA-codon/tRNA-anticodon distinction but repeats the same generic solution language. `v3_bio_01_10` has a valid `n−1` peptide-bond calculation but repeats its calculation path and contains raw internal review labels. These are presentation and learning-value defects rather than a basis to change the stored answer key.

The recommended safe remediation sequence is to preserve every existing ID, stem, options, key, source type, access pool, and holdout property; then rebuild `correct_analysis`, all four `distractor_analyses`, `fast_method`, `short_lesson`, and `review_default` from item-specific Biology relationships. Remove the raw enum tokens from all review-visible fields rather than translating enum names in place. Begin with the priority-55.9 gene-expression block, then proceed in priority order. For multi-step calculations such as peptide-bond count, include the exact relationship and arithmetic; for conceptual questions, state the precise biological distinction or process that rejects each distractor.

The helper scan source and raw JSON output are committed on this helper branch so the Biology worker can reproduce the counts and identify all flagged IDs without re-running discovery. A full Biology source-evidence pass against the supplied official textbooks is still necessary before asserting scientific correctness beyond these structural findings.
