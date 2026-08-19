# A1 Official-Source / Real-Exam / Key / Quarantine Audit

**Worker role:** Official-source / real-exam / key / quarantine authority  
**Account label:** `KONKOR-A1-M1-OFFICIAL`  
**Branch:** `parallel/a1-official-real-exam`  
**Baseline:** `origin/main` commit `72dc76e56b7ae625ad1904c76910eeaec5f90f58` (recorded before this audit).  
**Baseline release context:** tag `radiology1405-apk-v6.1.4-20260817`, version `6.1.4` / versionCode `165`, and workflow `32031100891` were recorded as the current baseline context. No merge to `main` and no release publication were performed.

> **Decision:** The 17 active `real_exam` records remain verified. All 16 historical key-conflict records remain quarantined. No question is relabeled, resolved, marked obsolete, moved into a simulation, or otherwise changed in this worker branch.

## Result ledger

| Status | Exact count | Audit result |
|---|---:|---|
| Active verified `real_exam` records | 17 | Retained after exact answer-key, source, option-count, and 1405-scope checks. |
| Key-unverified historical candidates | 16 | The 16 pre-existing `quarantined_key_conflict` records remain unverified for release purposes. |
| Relabeled records | 0 | No evidence supported changing a source type. |
| Quarantined records | 16 | Preserved without key or pool changes. |
| Resolved historical key conflicts | 0 | No record was resolved without readable authoritative primary-key access. |
| Obsolete for 1405 | 0 | All 33 audited candidates store `obsolete_for_1405=false`; no contrary textbook evidence was located in scope. |
| Protected holdout records | 244 | 117 in SIM1, 117 in SIM2, and 10 in FINAL. |
| Holdout leak | 0 | Every protected record is `authored`; no real-exam or quarantined ID occurs in SIM1, SIM2, or FINAL. |

## Active 1403 first-session records

The active set contains 15 Biology and 2 Chemistry records from the 1403 first-session domestic experimental-science examination. Each has four options, an in-range zero-based key index, a retained source-booklet reference and source page, a declared official origin, `access_pool=TRAIN`, and `obsolete_for_1405=false`.

The internally opened key PDF visibly identifies itself as **«کلید سؤالات آزمون اختصاصی (سراسری) سال ۱۴۰۳ ـ نوبت اول»** for the experimental-science group. Its independent option rows were transcribed and deterministically compared with all 17 stored keys: **17/17 matched**. The locally acquired key PDF digest is `898ad1ae6d582f1225c02ce30c46f986898010b994173ec8e1e2e32ff1c7df66`. The source booklets and key copy are archive-hosted copies, not represented as official-host downloads; the retained classification depends on the identity-bearing key table plus exact option-row comparison, not a fabricated claim that the archive host is Sanjesh.[1]

| Subject | Active records | Key-row check | Four-option check | Current-1405 scope flag |
|---|---:|---:|---:|---:|
| Biology | 15 | 15/15 matched | 15/15 | 15/15 not obsolete |
| Chemistry | 2 | 2/2 matched | 2/2 | 2/2 not obsolete |
| **Total** | **17** | **17/17 matched** | **17/17** | **17/17 not obsolete** |

## Whole-candidate structural and booklet audit

The frozen verified JSON was downloaded through the configured Drive connection and its immutable SHA-256 matched `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d`. It contains 1,216 records: 17 `real_exam`, 16 `quarantined_key_conflict`, 71 `official_exam_stem_training`, and 1,112 `authored`.[2]

All eight unique booklet PDFs referenced by the 33 active real-exam and quarantined candidates were acquired through the configured Drive connection and processed read-only. The deterministic audit found all 33 stored source-page values within the corresponding extracted PDF page count; all 33 candidates have four options and in-range answer indices; and all 33 have the required stored year, session, number, source-file, source-URL, and subject fields. Exact normalized stem anchors were found for 32/33. The remaining candidate, `real_1401_in_chem_081`, is already quarantined; its PDF extraction produced an 0.815 fallback similarity rather than an exact normalized anchor, so it is explicitly **not** promoted or otherwise relied upon.

## Quarantine authority finding

The 16 historical conflict IDs are preserved exactly as supplied:

| Year / session group | IDs | Disposition |
|---|---:|---|
| 1401 domestic Biology and Chemistry | 6 | Remain `QUARANTINE`; direct result/key endpoint could not be read in the internal browser. |
| 1401 domestic and foreign Geology | 7 | Remain `QUARANTINE`; no readable primary key was obtained. |
| 1402 second-session domestic Biology | 1 | Remains `QUARANTINE`; the official 1402 key was identified by a contemporaneous publication, but the direct Sanjesh file returned a 403 access block from this environment. |
| 1403 first-session domestic Chemistry | 1 | Remains `QUARANTINE`; no authoritative conflict-resolution evidence was collected. |
| 1404 second-session domestic Geology | 1 | Remains `QUARANTINE`; no authoritative conflict-resolution evidence was collected. |
| **Total** | **16** | **0 resolved; 16 preserved** |

The primary Sanjesh routes were not silently substituted with reasoning, mirrors, or the frozen internal scientific-resolution report. The direct 1402 key URL returned Sanjesh’s 403 access block; the 1401 result/key endpoint closed the connection, after which the internal browser became unavailable. These are access limitations, not evidence for either key choice. A contemporaneous report documents the official 1402 experimental-science key URL, but it is not a substitute for reading that key.[3]

## Holdout integrity

The deterministic pool check returned 244 protected IDs: SIM1=117, SIM2=117, and FINAL=10. All are `source_type=authored`; the query for non-authored protected IDs returned zero rows. The frozen blueprint declarations also state `verified_real_count=0` in each protected pool. No active or quarantined historical item was found in SIM1, SIM2, or FINAL.

## Implementation and migration decision

No bank artifact, Room schema, migration, question ID, source metadata, key, access pool, holdout assignment, or packaged-bank hash was changed. This is intentional: the active records’ stored keys matched the inspected 1403 table, while the 16 historical conflicts lacked the required readable primary-key evidence for resolution. Therefore a bank mutation would add migration and release risk without evidence-backed benefit. Stable IDs and all existing user progress remain unaffected.

## Reproduction artifacts

The worker retained the following read-only audit artifacts outside the repository checkout: `primary_evidence_log.md`, `record_booklet_audit.tsv`, `record_booklet_audit_summary.md`, `active_1403_key_comparison.tsv`, and `active_1403_key_comparison.md`. The local scripts are audit-only and do not alter the frozen archive.

## Residual limitation and handoff

The current environment could not read direct official Sanjesh key endpoints because of documented access blocks/connection failure. Future resolution of any of the 16 quarantined records requires a readable official Sanjesh key or notice that identifies the exact year, session, booklet, question number, and option. Until then, their quarantine is mandatory. No release gate is waived by this report.

## References

[1]: https://dl.konkur.in/2024/04/tajrobi1403-key-%5Bkonkur.in%5D1.pdf "Archive-hosted 1403 first-session experimental-science key PDF inspected through the internal browser"
[2]: https://drive.google.com/drive/folders/1R2IovFE_e0O_vU4IBCSiJpqrwK4LecxK "Frozen V6.1 archive folder"
[3]: https://farsnews.ir/University_and_Seminary/1689401626000085045 "Contemporaneous publication linking the 1402 official Sanjesh experimental-science answer key"
