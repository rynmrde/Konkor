# REAL EXAM / OFFICIAL SOURCE / KEY / QUARANTINE AUDIT

**Worker:** `parallel/real-exam-source-audit`  
**Pinned baseline:** `72dc76e56b7ae625ad1904c76910eeaec5f90f58` (`main`, 2026-08-17)  
**Baseline workflow:** [successful Rescue V6.1.4 run 32031100891](https://github.com/rynmrde/Konkor/actions/runs/32031100891)  
**Branch commit:** The branch head produced by this report-and-validator commit; pin the returned branch SHA during integration.

## Scope and outcome

This audit examined the frozen V6.1 bank independently from the application overlay. It treated the 17 rows whose database and JSON `source_type` are both `real_exam` as the active verified-real-exam scope. The 71 rows typed `official_exam_stem_training` were not silently counted as `real_exam`; the 16 historical `quarantined_key_conflict` rows remained outside active training and outside the verified count.

| Required count | Result | Basis |
|---|---:|---|
| Active `real_exam` items verified | **17** | Every item’s hash-pinned source page, four options, key entry, and cited textbook anchor were checked. |
| Active `real_exam` items unverified | **0** | No active item required de-labeling. |
| Relabeled | **0** | The frozen bank is unchanged. |
| Historical key-conflict items quarantined | **16** | All remain in `QUARANTINE`; none was resolved without a directly recoverable authoritative booklet-code key. |
| Historical key conflicts resolved | **0** | The evidence threshold was not met. |
| Active real-exam items obsolete for 1405 | **0** | All 17 retained `obsolete_for_1405=false` and their cited textbook anchors were present in the supplied books. |
| Holdout items checked | **244** | `SIM1=117`, `SIM2=117`, `FINAL=10`; complete-identity and semantic-fingerprint checks found no cross-pool leakage. |

## Active real-exam evidence

All 17 active rows are **1403, first session, domestic Experimental Sciences**. The official Sanjesh notice explicitly identifies the relevant Biology booklet, Physics/Chemistry booklet, and combined Experimental Sciences key for that examination session.[1] The official file host returned HTTP 403 to direct retrieval from this environment, so the notice and its exact official URLs were retained as primary provenance while an independently downloaded key-table mirror was used solely to cross-check the one-based option entries. The mirror supplied all 195 entries; all 17 bank answers matched.

| Subject | Items | Source PDF hash check | Stem + 4-option page comparison | Key-table comparison | 1405 scope result |
|---|---:|---:|---:|---:|---:|
| Biology | 15 | 15/15 pass | 15/15 pass | 15/15 pass | 15/15 pass |
| Chemistry | 2 | 2/2 pass | 2/2 pass | 2/2 pass | 2/2 pass |
| **Total** | **17** | **17/17** | **17/17** | **17/17** | **17/17** |

The audited IDs are `real_1403_n1_bio_003`, `_010`, `_012`, `_014`, `_016`, `_019`, `_022`, `_024`, `_028`, `_029`, `_032`, `_033`, `_041`, `_042`, `_044`, `real_1403_n1_chem_102`, and `real_1403_n1_chem_109`. Their source bytes matched the frozen bank’s recorded SHA-256 values: Biology `6b080cda86b850cc61f040475fc4c03e7d62d11519f7f02ce1bf8cc1bc59edf8` and Chemistry `ce7fc7fb03eba06a56f9abce0ffce9a0e88166ba1cd66f9e3d711b367c0a6b85`.

The active-item scope review used the referenced official textbook copies in the supplied Biology and Chemistry folders, not filenames alone. The front matter identified the cited print years—Biology 1: 1402, Biology 2: 1403, Biology 3: 1404, Chemistry 1: 1402—and every cited section-token anchor passed the deterministic comparison. These are the books referenced by the bank’s own `textbook_refs` fields; this result confirms anchor presence, not a claim that an entire textbook was re-authored or re-audited.[2]

## Historical key-conflict quarantine

The 16 pre-existing historical conflicts remain **quarantined**. Twelve had source bytes available during this audit; all twelve source SHA-256 values, stems, and four option sets matched the frozen bank. Four 1401 domestic Chemistry records share a now-unavailable Drive source ID (`1HkkmucN0jwpIsryekXhDr0WeaW4xG8v`): Drive metadata search still listed it, but both Drive download and the web view failed. No substitute bytes were used.

| Conflict group | Count | Source-page result | Decision |
|---|---:|---|---|
| 1401 domestic Biology | 2 | Hash/text/options verified | Preserve quarantine |
| 1401 domestic Chemistry | 4 | Source file unavailable | Preserve quarantine; source recovery required |
| 1401 domestic Geology | 4 | Hash/text/options verified | Preserve quarantine |
| 1401 overseas Geology | 3 | Hash/text/options verified | Preserve quarantine |
| 1402 second-session domestic Biology | 1 | Hash/text/options verified | Preserve quarantine |
| 1403 first-session domestic Chemistry | 1 | Hash/text/options verified; stored option matches the 1403 key table but independent scientific candidate differs | Preserve quarantine |
| 1404 second-session domestic Geology | 1 | Hash/text/options verified | Preserve quarantine |
| **Total** | **16** | **12 checked; 4 source-unavailable** | **0 resolutions** |

The quarantine decision is deliberately conservative. Several records contain a Sanjesh-branded or archive-key claim, but the bank itself marks `official_booklet_code_key_recovered=false`, `needs_official_key_reconciliation=true`, `needs_human_review=true`, and `KEY_CONFLICT_QUARANTINE`. A non-official host, a generic result page, or an unresolved scientific candidate is **not** sufficient evidence to promote or rewrite any of these rows. This preserves the project’s explicit historical-key-conflict safety rule.

## Holdout integrity

The bank contains 1,216 questions with source-type counts `authored=1112`, `official_exam_stem_training=71`, `quarantined_key_conflict=16`, and `real_exam=17`. Pools are `TRAIN=956`, `SIM1=117`, `SIM2=117`, `FINAL=10`, and `QUARANTINE=16`.

Each holdout row is authored, has `eligible_for_safety_evidence=true`, and has `needs_human_review=false`. Blueprint IDs exactly equal the corresponding assigned pool and are pairwise disjoint. A stem-and-options-only diagnostic initially found generic “table row” prompt templates in more than one pool; that is not question identity because the rendered table/figure is carried in `stimulus`. The final check canonicalized **stem, four options, correct index, and stimulus**, and also checked `semantic_fingerprint`; it found **0** holdout-vs-training and **0** cross-holdout collisions. No holdout item is a real-exam or quarantined source type.

## Files changed

| File | Change |
|---|---|
| `tools/validate_real_exam_source_audit.py` | Added a portable deterministic validator for source-type counts, 17 active-real labels, 16 quarantine records, and complete-identity holdout isolation. |
| `reports/parallel/REAL_EXAM_SOURCE_AUDIT.md` | Added this evidence-led audit and integration handoff. |

No bank JSON, SQLite database, Room schema, migration, signing configuration, release metadata, or application source was changed. Therefore **no migration is required** and archived V6.1 bank bytes remain untouched.

## Validation

```text
python3 tools/validate_real_exam_source_audit.py \
  --bank /path/to/radiology1405_bank_v6_1.db
PASS: real-exam source labels, quarantine containment, and complete-identity holdout isolation
active_real_exam=17 quarantined=16 holdout=244
```

The local frozen artifacts independently matched the declared V6.1 SHA-256 values: verified JSON `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d` and SQLite `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`.[3]

## Integration instructions

Integrate only the two files above. Before merging, the integrator should extract or otherwise obtain the exact frozen V6.1 SQLite bank and run the validator command shown above. Do **not** use this report to promote any quarantined record, recreate unavailable source bytes, or change an answer key. The four 1401 domestic Chemistry quarantines require recovery of the exact original official booklet plus a booklet-code-specific official key before any resolution can be considered. The 1403 key-table cross-check should not by itself clear its unresolved scientific/key mismatch.

## References

[1] [Sanjesh: 1403 first-session question booklets and key notice](https://sanjesh.org/fa-IR/sanjesh/4936/news/view/14591/11277/Staging)  
[2] [Supplied Biology source folder](https://drive.google.com/drive/folders/1ml6rbR86DP0J8uzEbklj73YKmMDvr0qg) and [Chemistry source folder](https://drive.google.com/drive/folders/1HY_9LuGRtpqhpvSRyCdJH-Gce0j4Iacc)  
[3] [V6.1 final-freeze folder](https://drive.google.com/drive/folders/1R2IovFE_e0O_vU4IBCSiJpqrwK4LecxK)
