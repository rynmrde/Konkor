# A1 Biology + Geology Scientific / Question-Bank QA

**Worker role:** `KONKOR-A1-M2-BIO-GEO` (Normal/Standard)  
**Branch:** `parallel/a1-biology-geology`  
**Baseline branch / SHA:** `origin/main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
**Baseline release observed:** `radiology1405-apk-v6.1.4-20260817`  
**Worker scope:** Biology and Geology bank QA, analysis-quality QA, and the narrowly related Persian review-text presentation fix. No merge to `main`, release, signing, or bank artifact overwrite was performed.

## Evidence and scope

The frozen source gzip and verified JSON were retrieved through the configured project storage route. Their SHA-256 values matched the immutable V6.1 references exactly: `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14` for the gzip bank and `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d` for the verified JSON. The expanded SQLite database also matched the pinned checksum `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`.[1]

The review was calibrated against the stored current Biology 10–12 and Geology textbook files, together with the stored 1403–1404 Biology and Geology examination materials. These files are source evidence for scientific review; authored records were not treated as historical-exam evidence.[2] [3] [4]

| Audit population | Count | Result |
|---|---:|---|
| All SQLite question records | 1,216 | Database hash and expected overall count matched. |
| Biology + Geology records | 596 | Includes inactive/quarantined records. |
| Active Biology + Geology records machine-scanned | **585** | 408 Biology and 177 Geology. |
| Final-Hours reachable `TRAIN` records | **474** | 280 in A-core task microtopics and 194 in B-rapid task microtopics. |
| Final-Hours Biology/Geology learning tasks | 27 | 16 A-core microtopics and 11 B-rapid microtopics. |
| Critical candidate packet extracted for deep review | **119** | Exact/reordered duplicates, duplicate-option records, vague-reference flags, and low-complexity generic-stem flags. |
| Representative high-risk records individually adjudicated | **4** | Included official-stem training and high-priority authored Biology/Geology examples. |

## Full machine-scan results

The structural scan found **no** JSON parse failures, missing stems, missing options, invalid answer indexes, or non-four-option active Biology/Geology records. The counts below are findings, not all necessarily bank changes: a near-duplicate candidate requires scientific/identity adjudication before any destructive action.

| Finding | Exact count | Interpretation / action |
|---|---:|---|
| Raw internal enum leakage in learner-facing analysis fields | **525** | Fixed in the UI text path on this branch; the frozen bank bytes remain unchanged. |
| Generic analysis boilerplate | **549** | Fixed in the UI text path by removing stock lead-ins while retaining the scientific statement/method that follows. |
| Low-complexity generic authored stem flags | **54** | Bank-review queue; requires a versioned, evidence-backed rewrite rather than a blind edit. |
| Duplicate option pairs within an item | **23** | Requires item-level source review before bank mutation. |
| Vague referent flags | **20** | Requires item-level wording review before bank mutation. |
| Exact duplicate clusters | **7 clusters / 21 distinct IDs** | Selection layer must prevent same-content repetitions; some clusters span separate microtopic IDs. |
| Reordered-option duplicate clusters | **3 clusters / 25 distinct IDs** | Candidate same-content variants; do not credit as unique mastery/coverage. |
| Near-duplicate candidate clusters | **107** | Machine candidates only; no destructive consolidation performed. |

> The scan is deliberately conservative: it flags content for review rather than inferring that a textual similarity is a scientific error. This preserves stable IDs and avoids silently changing frozen evidence.

## Scientific adjudication and decisions

The representative review confirmed that much of the visible defect is presentation-layer boilerplate rather than absence of a factual explanation. For example, Biology transcription/translation analyses contain the relevant scientific fact—such as the distinction between an mRNA codon and tRNA anticodon, or 5′→3′ RNA synthesis—but preface it with raw taxonomy keys and generic filler. The patch removes only those stock wrappers; it leaves the question-specific fact and any formula/method visible.

The following training record is an **unsafe bank-repair candidate**, not a safe in-place rewrite: `real_1401_in_geo_153` (Geology, *earthquakes and hazards*). Its displayed option strings are visibly malformed, while its analysis describes a valid amplitude relationship: a one-unit magnitude increase corresponds to ten-fold amplitude; the `31.6` factor belongs to energy, not amplitude. The original official source must be re-read and the four displayed options reconstructed from that source before a new bank version can correct or quarantine it. The item was **rejected for automatic modification** in this worker branch.[3]

| Decision class | Exact count | Notes |
|---|---:|---|
| Bank question rewrites applied | **0** | Frozen gzip/DB/JSON remain byte-identical. |
| Bank question rewrites rejected pending authoritative source reconstruction | **1** | `real_1401_in_geo_153`; malformed options require source-level repair and a versioned migration. |
| Bank analysis rewrites applied | **0** | No bank JSON was changed. |
| Learner-facing analysis presentation rewrites | **2 source files** | One renderer change plus one focused regression test. |
| Stable IDs changed | **0** | No identity or progress migration impact. |

## Implemented fix on this branch

The branch adds a presentation normalizer in `ScienceText.kt`. It maps every raw taxonomy key detected by the whole-bank scan—including `wrong_condition`, `partial_truth`, `calculation_trap`, `unit_error`, `direction_error`, and learning-error keys—to Persian learner-facing labels. It also strips only stock review lead-ins such as “source of trap,” “all conditions agree,” and “control method,” while retaining the question-specific biological/geological statement and calculation method.

| Commit | Purpose |
|---|---|
| `9082712696911995b14806a9d9a4ebba29da547a` | Initial Persian taxonomy rendering map. |
| `19a0b5dc8d7a74dae63e3f0abed37bfebcf76ed6` | Focused renderer test. |
| `d03627ff1496901bf1290825606ec11b1c28d31b` | Remove stock review boilerplate while preserving scientific reasoning. |
| `d515ceaf492627962fac709a3d3230caa7cb2170` | Regression test for boilerplate removal / reasoning preservation. |
| `a4392e55ec0ba5c13af6016a0749ba02f2413b39` | Add `unit_error`, the remaining machine-detected raw key, to the renderer map. |
| `07b9b4e16f2e61906bd02e2f002f9ea075c94aff` | Extend the regression test to cover `unit_error`. |

The new test file is `app/src/test/java/com/radiology1405/prep/ui/ScienceTextTest.kt`. It asserts that raw internal labels are absent from learner-facing text, Persian labels are shown, stock filler is removed, and the actual scientific reason is retained.

## Validation performed

| Gate | Result | Evidence |
|---|---|---|
| Frozen bank gzip / verified JSON / DB checksum | PASS | All three matched their pinned V6.1 SHA-256 values. |
| Bank count and question-table scan | PASS | 1,216 total; 585 active Biology/Geology records scanned. |
| Four options / valid key / JSON structural scan | PASS | No active Biology/Geology structural violations of these types. |
| Duplicate and near-duplicate scan | PASS as detection | Findings recorded above; no unsafe auto-merge or ID mutation. |
| Raw-enum and boilerplate scan | PASS as detection | 525 and 549 findings respectively; presentation path patched. |
| Committed branch content check | PASS | Renderer and test were retrieved from `parallel/a1-biology-geology` after commit. |
| Deterministic raw-label / filler safeguard check | PASS | All 10 machine-detected raw enum tokens are mapped; stock-filler removal and reasoning-preservation test assertions are present. |
| Kotlin / Gradle execution | NOT RUN | This worker did not claim a build pass; the Foreman must run the required compile/JVM/lint/instrumentation gates on the integrated tree. |

## Integration actions required

The integrator should cherry-pick or otherwise integrate the branch only after normal conflict review. The renderer fix is app-only and preserves bank hash, IDs, and Room schema. It should be followed by the new JVM test and the full required Android build gates.

A material bank follow-up remains necessary for `real_1401_in_geo_153` and the duplicate-option / duplicate-cluster queue. Such a change must create a new bank version, retain old artifacts, supply authoritative source metadata, map any identity changes, and demonstrate progress preservation. Do **not** edit the frozen V6.1 artifact in place.

### References

[1]: https://drive.google.com/drive/folders/1R2IovFE_e0O_vU4IBCSiJpqrwK4LecxK "RADIOLOGY_1405_V6_1_FINAL_FREEZE_2026-08-12"
[2]: https://drive.google.com/drive/folders/1ml6rbR86DP0J8uzEbklj73YKmMDvr0qg "Biology curriculum and examination sources"
[3]: https://drive.google.com/drive/folders/1lV90myeWo3jl5sBsbBbV2MU-InI3d2nL "Geology curriculum and examination sources"
[4]: https://github.com/rynmrde/Konkor/tree/parallel/a1-biology-geology "Assigned worker branch"
