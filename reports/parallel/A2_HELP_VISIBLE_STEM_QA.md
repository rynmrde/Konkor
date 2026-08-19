# A2 Helper — Visible Paired-Statement QA Gate

> **Helper branch:** `parallel/help-a2-visible-stem-qa`  
> **Baseline:** `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
> **Purpose:** Add a deterministic bank gate for A/B paired-statement questions that are unanswerable in the rendered app because their visible stem omits the required A and B claims.

## Confirmed result

The immutable frozen bank gzip was freshly downloaded from the authoritative Drive item `1r8IvfWT7R_ihzfLC6QyoGQNQiDFrvhZZ`; its SHA-256 matched the frozen baseline:

```text
b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14
```

`tests/verify_visible_stem_completeness.py` found **21 failing records**. All 21 are active TRAIN, selected in scope, eligible for safety evidence, and do **not** carry `needs_human_review`; they can therefore be shown by the normal safety selector.

| Subject | Failing safety-reachable TRAIN items |
|---|---:|
| Biology | 11 |
| Chemistry | 3 |
| Physics | 3 |
| Geology | 4 |
| **Total** | **21** |

Each failure has a visible stem equivalent to “about statements A and B, which option is correct?” and options such as “A true / B false,” but lacks an `A:` and `B:` claim in `Question.stem`. The runtime `Question` model renders the stem and options; it does not expose a separate pair-claim field. The learner therefore cannot determine the answer from the visible question.

## Affected IDs

```text
v3_bio_02_12, v3_bio_05_12, v3_bio_06_07, v3_bio_07_15, v3_bio_08_07,
v3_bio_10_11, v3_bio_11_07, v3_bio_12_07, v3_bio_14_10, v3_bio_15_15,
v3_bio_16_10, v3_chem_20_03, v3_chem_26_03, v3_chem_54_07,
v3_phys_30_02, v3_phys_33_02, v3_phys_34_03,
v3_geo_45_09, v3_geo_46_08, v3_geo_47_07, v3_geo_49_08
```

## Supplied guard

`tests/verify_visible_stem_completeness.py` is a fail-closed static validator. It verifies the frozen gzip hash, finds paired A/B-option structures, and requires both visible `A:` and `B:` statements in the stem. It emits a JSON summary and exits non-zero on any failure.

> **Release status:** This is a confirmed release blocker. The scientific/bank owner must restore the actual A/B claims in the visible stem, or quarantine every affected item with a non-destructive, progress-preserving bank migration. A runtime-only selector workaround is insufficient unless it reliably prevents all 21 items from all normal, review, resume, and backup-restored sessions.

No bank mutation, main merge, or release publication was performed on this helper branch.
