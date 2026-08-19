# Helper Report — Biology Source-Audit Handoff

**Helper branch:** `parallel/help-real-exam-source-audit-bank-biology`  
**Target worker branch inspected:** `parallel/bank-biology`  
**Target status at inspection:** still at baseline `72dc76e56b7ae625ad1904c76910eeaec5f90f58`; no worker report or source patch was present.  
**Helper baseline:** `72dc76e56b7ae625ad1904c76910eeaec5f90f58`

## What was checked

This helper does not modify the target worker’s branch. It performs an independent source-boundary check derived from the frozen V6.1 bank and the supplied official Biology materials. The biology inventory is 411 records: 369 authored, 24 `official_exam_stem_training`, 15 active `real_exam`, and 3 `quarantined_key_conflict`.

| Boundary | Count | Result |
|---|---:|---|
| Active `real_exam` Biology rows | 15 | All retained `TRAIN`, `real_exam`, official-origin, source-page verification, four options, and `obsolete_for_1405=false`. |
| Active source PDF | 1 | Every active row pins to Biology 1403 first-session source SHA-256 `6b080cda86b850cc61f040475fc4c03e7d62d11519f7f02ce1bf8cc1bc59edf8`. |
| Biology quarantines | 3 | `real_1401_in_bio_017`, `real_1401_in_bio_042`, and `real_1402_n2in_bio_041` remain in `QUARANTINE` with reconciliation and human-review flags. |
| Official exam stem training rows | 24 | Kept distinct from the 15 rows actually labeled `real_exam`; they must not be promoted by inference. |

The 15 active items were independently compared with the supplied Biology 1403 first-session source pages and the session key table during the real-exam audit. Every source hash, stem, option set, key entry, and cited 1405-scope textbook anchor passed. The project’s official Sanjesh notice is the primary provenance for the session booklet and answer-key links.[1]

## Helper deliverable

`tools/validate_biology_source_handoff.py` guards the exact biology source boundary in any candidate SQLite bank. It fails if an audited active real-exam ID disappears, leaves `TRAIN`, changes labels or the verified source SHA, loses source/text verification, becomes obsolete, or if any of the three biology conflicts leaves `QUARANTINE` without the required reconciliation/review state.

```text
python3 tools/validate_biology_source_handoff.py \
  --bank /path/to/radiology1405_bank_v6_1.db
PASS: audited Biology real-exam and quarantine boundaries preserved
active_real_exam=15 quarantined=3 source_type_counts=
{'authored': 369, 'official_exam_stem_training': 24,
 'quarantined_key_conflict': 3, 'real_exam': 15}
```

## Integration instructions for the Biology worker or foreman

Apply only this helper validator and report if the candidate bank remains byte-identical in the guarded source metadata. If a Biology content patch must change any real-exam source field, first create a new audited bank version, preserve stable IDs where identity remains the same, provide an explicit mapping and non-destructive migration, and rerun this guard after deliberately updating its contract. Do not resolve the three quarantined Biology records on the basis of an archive claim or secondary key mirror; direct authoritative booklet-code evidence remains required.

## References

[1] [Sanjesh 1403 first-session question-booklet and key notice](https://sanjesh.org/fa-IR/sanjesh/4936/news/view/14591/11277/Staging)
