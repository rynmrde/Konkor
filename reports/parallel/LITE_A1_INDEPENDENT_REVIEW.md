# Independent Cross-Review: Official Sources and 21 Visible-Stem Blocker

## Review target and scope

| Field | Value |
|---|---|
| Reviewer role | `KONKOR-A1-L1-OFFICIAL-SUPPORT` independent review pass |
| Baseline cited by reviewed workers | `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Standard source branch | [`parallel/real-exam-source-audit`](https://github.com/rynmrde/Konkor/tree/parallel/real-exam-source-audit) |
| Standard source report | [`REAL_EXAM_SOURCE_AUDIT.md`](https://github.com/rynmrde/Konkor/blob/parallel/real-exam-source-audit/reports/parallel/REAL_EXAM_SOURCE_AUDIT.md) |
| A1 source report | [`A1_OFFICIAL_REAL_EXAM.md`](https://github.com/rynmrde/Konkor/blob/parallel/a1-official-real-exam/reports/parallel/A1_OFFICIAL_REAL_EXAM.md) |
| Visible-stem branch | [`parallel/help-a2-visible-stem-qa`](https://github.com/rynmrde/Konkor/tree/parallel/help-a2-visible-stem-qa) |
| Visible-stem report | [`A2_HELP_VISIBLE_STEM_QA.md`](https://github.com/rynmrde/Konkor/blob/parallel/help-a2-visible-stem-qa/reports/parallel/A2_HELP_VISIBLE_STEM_QA.md) |
| Review method | Cross-report consistency and safety review; no whole-bank redo and no scientific answer edits |

## Major-claim decision ledger

| Major claim | Decision | Independent basis and exact issue |
|---|---|---|
| Current baseline is `72dc76e56b7ae625ad1904c76910eeaec5f90f58` | **PASS** | The standard report, A1 report, and visible-stem report all cite the same baseline. No contradiction found. |
| 17 active `real_exam` rows may remain verified | **PASS WITH EVIDENCE CAVEAT** | Both source reports agree on the same 17 IDs and 17/17 key comparisons. However, the standard report relies partly on an archive-hosted key mirror because direct Sanjesh retrieval returned 403; A1 correctly avoids claiming the mirror is official. Integration must retain the source/hash and provenance distinction. |
| The 16 historical key conflicts must remain quarantined | **PASS** | Both reports preserve all 16 and resolve zero. The reports differ in grouping and access narrative, but neither promotes or rewrites a conflict. The unresolved 1403 Chemistry conflict is explicitly retained in quarantine. No unsafe relabel was found. |
| All 33 active-plus-quarantined candidates are source-page/option structurally valid | **PASS WITH LIMITATION** | A1 reports 33/33 required fields and four options, with exact stem anchors for 32/33; `real_1401_in_chem_081` has only 0.815 fallback similarity and remains quarantined. This is safe, but the exact ID must remain an explicit residual rather than being summarized as a full exact-stem pass. |
| Holdout pools are disjoint and contain no real-exam/quarantine records | **PASS FOR CLAIMED CHECK** | Both reports state SIM1=117, SIM2=117, FINAL=10, total 244, authored-only and zero non-authored protected records. The standard report additionally describes complete-identity plus semantic-fingerprint checking. No holdout leak is evidenced in the reports. The release integrator must rerun the validator against the actual packaged bank. |
| 21 visible-stem failures are a release blocker | **PASS** | The A2 report identifies a fail-closed validator, immutable gzip hash `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`, and 21 active TRAIN, selected, safety-eligible, non-human-review records whose rendered stems omit the required A/B claims. The blocker is user-visible and cannot be waived by source verification. |
| The 21 items can be safely fixed by relabeling or selector filtering | **FAIL** | No deterministic source-backed replacement or complete selector proof is presented. The A2 report correctly says runtime-only filtering is insufficient unless it blocks normal, review, resume, and restored sessions. No relabel is justified. |
| The 21 items can be safely quarantined immediately | **FAIL AS AN IMMEDIATE PATCH** | Quarantine may be the safe fallback, but the reviewed evidence does not provide a migration, progress-preservation, pool-disjointness, or bank-hash-preserving patch. Quarantine without those gates would be destructive or incomplete. |
| Source metadata is release-ready for every claimed real-exam record | **FAIL / INCOMPLETE EVIDENCE** | The reports establish aggregate counts and strong evidence for the 17 active rows, but the standard report says some direct official endpoints were inaccessible and A1 retains archive-host provenance. The final report must distinguish official provenance, mirror cross-check, source file/page, and key identity per row; a blanket “verified” statement is too broad without the retained TSV/evidence artifacts. |

## Exact 21 visible-stem blocker IDs

The following IDs are the complete blocker list reported by A2 and should be treated as **active, safety-reachable, unanswerable until repaired or safely excluded**:

```text
v3_bio_02_12, v3_bio_05_12, v3_bio_06_07, v3_bio_07_15, v3_bio_08_07,
v3_bio_10_11, v3_bio_11_07, v3_bio_12_07, v3_bio_14_10, v3_bio_15_15,
v3_bio_16_10, v3_chem_20_03, v3_chem_26_03, v3_chem_54_07,
v3_phys_30_02, v3_phys_33_02, v3_phys_34_03,
v3_geo_45_09, v3_geo_46_08, v3_geo_47_07, v3_geo_49_08
```

The subject split is Biology 11, Chemistry 3, Physics 3, and Geology 4. The reports contain no evidence that any of these IDs are real-exam, quarantine, or SIM holdout records; their current status is active TRAIN. Therefore source-audit approval must **not** be interpreted as approval for their normal delivery.

## Contradictions and missing evidence

The principal contradiction is not a conflicting scientific decision but a **provenance-strength mismatch**. The standard report says every active real-exam item’s “hash-pinned source page, four options, key entry, and cited textbook anchor were checked,” while the same report states that direct official Sanjesh retrieval returned 403 and an independently downloaded key-table mirror was used for the 195 key entries. A1 is more precise: the key PDF was archive-hosted and the archive host is not being claimed as Sanjesh. The safe consolidated wording is: **the 17 rows pass exact comparison against the identified key-table artifact, but official-host retrieval/provenance remains partially unavailable and must not be overstated**.

The second issue is an evidence-packaging gap. The standard report names `tools/validate_real_exam_source_audit.py`, but the review target does not expose the validator output or the retained TSV/evidence logs in the report itself. This is not evidence of a failed check; it is a reproducibility gap. The integrator must require the actual validator, bank hash, and retained row-level evidence artifacts before treating the claim as a release gate pass.

The visible-stem report is internally consistent and stronger than the source reports on blocker status: it provides a hash, validator name, counts, subject split, and all 21 IDs. It does not provide the actual missing A/B claim text or a repair mapping. Consequently, a scientific rewrite cannot be approved from this report alone.

## Unsafe decisions not found

No reviewed branch relabeled a record, resolved a historical key conflict, moved a real-exam or quarantined record into a holdout, or altered an answer. The conservative decision to preserve all 16 quarantines is safe. The explicit refusal to treat a mirror as official-host evidence is also safe. No deterministic safe fix was obvious for the 21 visible-stem records because the missing claims require bank-owner reconstruction or a fully gated exclusion/migration.

## Required release actions

The integrator should block release until the 21 IDs are either repaired with the actual A/B claims and four-option semantics preserved, or excluded through a non-destructive, progress-preserving migration with tests covering normal selection, review, resume, and backup restore. The integrator should also preserve the row-level evidence distinction for the 17 active real-exam records and rerun the source, quarantine, holdout, and packaged-bank validators against the exact signed APK bank.

## Review disposition

**Independent review: CONDITIONAL PASS for quarantine/source-safety decisions; FAIL for release readiness until the 21 visible-stem blocker is repaired or safely excluded and row-level provenance artifacts are attached.** No helper patch was made because no deterministic safe fix was evident from the reviewed evidence.

## References

[1]: https://github.com/rynmrde/Konkor/blob/parallel/real-exam-source-audit/reports/parallel/REAL_EXAM_SOURCE_AUDIT.md "Standard real-exam/source audit report"

[2]: https://github.com/rynmrde/Konkor/blob/parallel/a1-official-real-exam/reports/parallel/A1_OFFICIAL_REAL_EXAM.md "A1 official-real-exam report"

[3]: https://github.com/rynmrde/Konkor/blob/parallel/help-a2-visible-stem-qa/reports/parallel/A2_HELP_VISIBLE_STEM_QA.md "A2 visible-stem QA report"
