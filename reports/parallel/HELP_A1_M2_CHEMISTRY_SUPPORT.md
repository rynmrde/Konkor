# Helper Support: Chemistry QA Scan

**Helper worker:** `KONKOR-A1-M2-BIO-GEO` after completion of the assigned Biology/Geology scope  
**Helper branch:** `parallel/help-a1-m2-chemistry`  
**Helper baseline:** `origin/main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
**Target stream inspected:** `parallel/a1-chemistry` (observed still at the baseline SHA when this helper branch was opened).  
**Scope:** Deterministic, non-destructive support scan of the frozen active Chemistry bank. No bank artifact, question ID, source label, or release was changed.

## Scan outcome

The frozen verified SQLite table contains 267 Chemistry records; **262 active non-quarantined items** were scanned. The population contains 238 authored records, 22 official-stem training records, and 2 `real_exam` records. This helper scan is a triage inventory: a duplicate candidate or short stem is not automatically a scientific defect and must be adjudicated from textbook/official evidence before a bank change.[1]

| Scan category | Exact count | Required primary-worker handling |
|---|---:|---|
| Active Chemistry records machine-scanned | **262** | Full active Chemistry population covered. |
| Raw internal enum in analysis text | **237** | Integrate the app-level learner-facing renderer fix from `parallel/a1-biology-geology`; it handles this display defect without mutating the frozen bank. |
| Generic analysis boilerplate | **237** | Same presentation-layer remedy preserves the following question-specific reasoning. |
| Duplicate-option items | **13** | Deep-review four choices and correct key/source before any versioned bank rewrite. |
| Low-complexity stem candidates | **14** | Review first in selected/high-ROI authored items; do not infer an error from length alone. |
| Exact duplicate clusters | **5** | Ensure selection excludes repeated content in one normal block and unique mastery is not inflated. |
| Reordered-option duplicate clusters | **2** | Treat as same-content candidates until scientifically resolved. |
| Flagged records, any category | **239** | Mostly the systematic analysis-presentation defect, not a reason for bulk bank mutation. |
| High-priority flagged records (`priority ≥ 50`) | **99** | Start with mole/stoichiometry/gases, solutions, periodic trends, atomic structure, and environmental chemistry. |

## Immediate high-value review queue

The 13 duplicate-option records are all authored and selected in scope. The priority-first entries are `v3_chem_18_06` and `v3_chem_18_10` (atomic structure, isotopes, electron configuration; priority 53.0). The rest are `v3_chem_22_09`, `v3_chem_24_03`, `v3_chem_24_04`, `v3_chem_24_07`, `v3_chem_24_09`, `v3_chem_24_18`, `v3_chem_24_19`, `v3_chem_25_03`, `v3_chem_25_07`, `v3_chem_25_15`, and `v3_chem_25_17`.

| Queue | IDs | Meaning |
|---|---|---|
| Exact duplicate cluster A | `v3_chem_19_10`, `v3_chem_20_19`, `v3_chem_26_11`, `v3_chem_54_11`, `v3_chem_55_15` | Do not schedule more than one in a normal block pending adjudication. |
| Exact duplicate cluster B | `v3_chem_19_11`, `v3_chem_20_20`, `v3_chem_26_12`, `v3_chem_54_12`, `v3_chem_55_16` | Same handling. |
| Exact duplicate cluster C | `v3_chem_19_12`, `v3_chem_26_13`, `v3_chem_54_13` | Same handling. |
| Exact duplicate cluster D | `v3_chem_19_13`, `v3_chem_20_18`, `v3_chem_26_10`, `v3_chem_55_14` | Same handling. |
| Exact duplicate cluster E | `v3_chem_26_03`, `v3_chem_54_07` | Same handling. |
| Reordered candidate 1 | 17 IDs across `19`, `20`, `26`, `54`, `55` as captured in the machine artifact | Similarity candidate; compare answer order and scientific identity. |
| Reordered candidate 2 | `v3_chem_20_03`, `v3_chem_26_03`, `v3_chem_54_07` | Similarity candidate; compare answer order and scientific identity. |

The short-stem screen identified selected authored candidates at the first item of each microtopic cluster, including high-ROI `v3_chem_17_01` (mole/stoichiometry/gases, priority 74.0), `v3_chem_21_01` (solutions, 55.8), `v3_chem_54_01` (environmental chemistry/materials, 54.8), `v3_chem_19_01` (periodic trends, 53.7), and `v3_chem_18_01` (atomic structure, 53.0). Two short official-stem training records were also flagged by length only—`real_1403_n1in_chem_089` and `real_1404_n1in_chem_086`; they must **not** be rewritten merely because a heuristic classified them short.

## Recommended next actions

The Chemistry owner should first manually inspect the 13 duplicate-option records and the five exact duplicate clusters against the cited official pattern/textbook evidence. Any actual correction must use a new material bank version, source metadata, stable-ID preservation or mapping, and progress migration validation. The app-level review renderer change already prepared on `parallel/a1-biology-geology` is the preferred fix for raw enum and boilerplate display across Chemistry as well; it does not alter the bank hash or identity.

> This helper report intentionally distinguishes **machine flags** from scientifically proven defects. It contains no claim that any flagged Chemistry question is wrong until authoritative evidence confirms it.

### Reference

[1]: https://github.com/rynmrde/Konkor/tree/parallel/help-a1-m2-chemistry "Isolated helper branch and support report"
