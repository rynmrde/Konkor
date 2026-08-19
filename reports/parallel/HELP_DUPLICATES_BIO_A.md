# Helper Duplicate Adjudication — Biology

## Scope

This helper branch, `parallel/help-duplicates-bio-a`, was created after the Biology-A primary scope completed. It addresses the highest-priority unresolved Biology-bank finding reported by `parallel/bank-biology`: the residual duplicate-candidate set.

| Field | Value |
|---|---|
| Baseline | `main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Bank inspected | Frozen V6.1 expanded SQLite, SHA-256 `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c` |
| Source population | Active, non-obsolete, non-quarantine Biology records |
| Mutation performed | None |

## Finding

The earlier 64 findings are correctly treated as **duplicate candidates**, not confirmed duplicate questions. A source-aware exact extractor was applied to normalized stimulus (while retaining semantic stimulus identity), stem, and all four options. It found **zero** groups that were safe to label as exact duplicates under that stronger definition.

> No Biology record was deleted, merged, re-keyed, quarantined, or otherwise changed on this helper branch. That is deliberate: lexical overlap or generic shared stems cannot justify a destructive question-bank mutation.

The helper adds two reproducible extractors. The broad extractor is intentionally over-inclusive and is suitable for triage; the exact-group extractor is conservative and shows that the current candidate count is not evidence of safe semantic identity.

## Integration Recommendation

The Foreman should retain the existing no-repeat normal-session enforcement and must perform candidate adjudication at the **session-generation layer** using a semantic fingerprint that includes stimulus identity, stem, options, and the intended concept. Exact wording alone must not remove questions or alter unique mastery. When a pair is later confirmed as semantically identical by authoritative evidence, preserve both stable IDs but prevent co-selection in a normal block; only intentional spaced retrieval may revisit an ID, and it must not inflate unique mastery.

## Changed Files

| File | Purpose |
|---|---|
| `tools/extract_biology_duplicate_candidates.py` | Produces transparent broad lexical duplicate candidates without mutating the bank. |
| `tools/extract_exact_biology_duplicate_groups.py` | Produces conservative exact candidate groups using stem, options, and stimulus identity. |
| `reports/parallel/HELP_DUPLICATES_BIO_A_CANDIDATES.json` | Broad candidate extractor output; not a deletion list. |
| `reports/parallel/HELP_DUPLICATES_BIO_A_EXACT_GROUPS.json` | Source-aware exact-group output: zero safe groups. |

## Tests

| Gate | Result |
|---|---|
| Frozen DB opened | PASS |
| Broad candidate extractor executed | PASS; confirms broad lexical approaches overflag generic prompts. |
| Source-aware exact-group extractor executed | PASS; `group_count = 0`, `member_count = 0`. |
| Bank mutation | PASS; none performed. |

## Blocker

A safe destructive duplicate merge requires explicit semantic and authoritative-source adjudication that is not present in the current bank metadata. The next practical owner is the Foreman/session-generation integrator: enforce no co-selection using a richer semantic identity policy while preserving IDs, progress, SIM disjointness, and intentional-review accounting.
