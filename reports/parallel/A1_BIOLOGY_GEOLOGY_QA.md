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


---

## SECOND_PASS_REVIEW — authoritative reconciliation

**Second-pass scope.** This section supersedes any first-pass implication that the branch-local renderer alone was build-effective, that stock boilerplate deletion was scientifically justified across all records, or that unresolved visible-stem text could be reconstructed. The review used the independent cross-review at commit [`55c19556fe8429548d1d7ae60939a61510bfa49e`][5], the exact frozen verified JSON, and the V6.1.4 build overlay. The frozen JSON download again matched SHA-256 `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d`, contained **1,216** records, and is the only source used for canonical stimulus text.[1] [5]

### Exact conflict reconciliation

The eight overlapping updates below occurred in both candidate Biology payloads with different analysis fields. The deterministic successor payload assigns all eight to the compact `biology-v6.1.5-analysis-safety` analysis after comparison with their original frozen stems/options and declared micro-skills. The final payload rejects duplicate IDs before any rendering; it never relies on application order.

| ID | Intended skill | Deterministic source | Disposition |
|---|---|---|---|
| `v3_bio_09_01` | Respiratory partial-pressure diffusion | Compact v6.1.5 | Kept as analysis-only update. |
| `v3_bio_10_01` | Glomerular filtration, reabsorption, and secretion | Compact v6.1.5 | Kept as analysis-only update. |
| `v3_bio_11_01` | Resting potential, synapse, and ATP–myosin separation | Compact v6.1.5 | Kept as analysis-only update. |
| `v3_bio_12_01` | Endocrine axis, hormone receptors, and insulin | Compact v6.1.5 | Kept as analysis-only update. |
| `v3_bio_13_01` | Innate versus adaptive immunity | Compact v6.1.5 | Kept as analysis-only update. |
| `v3_bio_14_01` | LH surge, ovulation, and embryo timing | Compact v6.1.5 | Kept as analysis-only update. |
| `v3_bio_15_01` | Xylem, phloem, and transpiration | Compact v6.1.5 | Kept as analysis-only update. |
| `v3_bio_16_01` | Natural selection and population-level change | Compact v6.1.5 | Kept as analysis-only update. |

The successor contains **142 unique analysis-only updates**: the compact payload’s 16 updates, including all eight reconciled conflicts, plus **126** non-conflicting W04 analysis updates. Every update is restricted to `correct_analysis`, `distractor_analyses`, and `short_lesson`; no update contains `stem`, `options`, `correct_index`, source metadata, access pool, or stable-ID edits. Frozen gzip, SQLite, and verified JSON bytes remain unmodified.[1] [5]

### Visible stems, raw labels, and generic-analysis disposition

The first-pass `ScienceText.kt` change was not sufficient because the V6.1.4 build overlay overwrites branch-local source. The second pass places the change in the actual V6.1.4 overlay and adds the renderer/model path used by both active test and Review. Internal labels are mapped to Persian learner-facing terms, but the prior global stock-boilerplate deletion is **not** carried into the build-effective source: deleting arbitrary sentences can suppress item-specific reasoning and is unsupported. This is a deliberate safety correction.

| Category | Exact IDs / count | Final disposition |
|---|---:|---|
| Canonical paired statements rendered from immutable fields | **6**: `v3_bio_10_11`, `v3_bio_11_07`, `v3_bio_12_07`, `v3_bio_14_10`, `v3_bio_15_15`, `v3_bio_16_10` | The model reads the original `stimulus.left_label`, `left`, `right_label`, and `right`; test and Review render those values below the original stem. No replacement stem is invented. |
| Other paired-statement records with canonical fields already present | **5**: `v3_bio_02_12`, `v3_bio_05_12`, `v3_bio_06_07`, `v3_bio_07_15`, `v3_bio_08_07` | Supported automatically by the same renderer path; no payload mutation. |
| Non-paired visible-text repairs without canonical `left`/`right` values | **5**: `v3_bio_11_24`, `v3_bio_13_15`, `v3_bio_14_20`, `v3_bio_15_24`, `v3_bio_16_16` | **Safely demoted** from fresh `TRAIN`, distinct-alternative, rescue-safe-count, and SIM selection. No text/options are guessed or overwritten. |
| Raw taxonomy tokens | **10 machine-detected classes; 18 aliases mapped** | Localized at rendering time, preserving the original analysis sentence. |
| Unsupported global generic-analysis rewrite | **1 prior UI strategy** | Rejected; not included in the build-effective overlay. Scientific item analyses remain visible rather than being erased by a broad pattern. |

The frozen artifact establishes the six rendered pairs verbatim. For example, `v3_bio_10_11` contains the original glomerular-filtration and aldosterone claims; `v3_bio_15_15` contains the original double-fertilization and mature-xylem claims; and `v3_bio_16_10` contains the original genetic-drift and acquired-trait claims. The renderer uses those canonical fields rather than adding self-authored A/B wording.[1]

### Residual Biology review

The three residual vague/generic candidates were re-read against their frozen stem, four options, correct index, and the W04 scientific reasoning. All three are retained as **analysis-only** updates because the proposed reasoning directly addresses the actual option and does not alter question identity.

| ID | Frozen correct index | Second-pass result |
|---|---:|---|
| `v3_bio_12_08` | 3rd option (`2` zero-based) | Retained. The correct chain is final-hormone inhibition of upstream signals and therefore negative feedback in many endocrine axes; the analysis distinguishes intracellular receptors, negative feedback, and hypothalamic GnRH from anterior-pituitary FSH/LH. |
| `v3_bio_15_11` | 3rd option (`2` zero-based) | Retained. The incompatible statement is that all mature xylem conducting elements are alive; mature tracheids and vessel elements are dead. |
| `v3_bio_16_13` | 4th option (`3` zero-based) | Retained. Evolution is not a linear ladder toward perfection; selection changes heritable-trait frequencies in populations across generations, and genetic drift is relatively stronger in small populations. |

### Geology and remaining blockers

`real_1401_in_geo_153` remains **unresolved**. Its malformed displayed options are not reconstructed, re-keyed, or otherwise guessed. It stays outside this successor’s changes and requires an authoritative official-source reconstruction before any versioned bank repair.

The five safely demoted Biology visible-stem records are not equivalent to deletion: their immutable rows, stable IDs, historical attempts, and review references remain intact. The guard only stops them from being selected for new training, distinct alternatives, safe-count calculations, and simulations until authoritative presentation content is available.

### Second-pass implementation and tests

The build-effective V6.1.4 overlay now includes `biology_v621_second_pass_successor.json`, `PairedStimulus` parsing, one shared stem card used in both Test and Review, raw-taxonomy localization without generic text deletion, the safe selection exclusion list, and focused JVM-test source files.

| Validation | Result | Observed evidence |
|---|---|---|
| Successor update uniqueness and field contract | **PASS** | `BIOLOGY_SECOND_PASS_SUCCESSOR_OK 142 6`; 142 unique updates, exactly three analysis fields per update. |
| Immutable-bank contract | **PASS** | `SECOND_PASS_IMMUTABLE_BANK_OK 142 6 5`; verified JSON SHA matched, six canonical pairs were non-empty, five unresolved visible-stem rows were excluded from the successor. |
| Conflict ownership | **PASS** | All eight specified collision IDs resolve to `biology-v6.1.5-analysis-safety`; no duplicate successor ID remains. |
| Canonical renderer wiring | **PASS (static)** | `pairedStimulus` is parsed in `Models.kt`; `QuestionStemCard(question, compact)` is used in both Test and Review. |
| Safe demotion wiring | **PASS (static)** | All five unresolved visible-stem IDs are excluded in training candidates, alternatives, rescue-safe counts, and simulations. |
| Repacked build-effective overlay SHA-256 | **PASS** | `ed96733118d455b6bf1b3280eddea6096183c816cba7aeb86d92f46ece87d64c`. |
| Kotlin/JVM/Gradle, lint, Android API 35 instrumentation, signed APK | **NOT RUN** | Required Foreman/integrator gates on the fully integrated tree; no build pass is claimed here. |

> **Integration requirement.** The new overlay supersedes the prior branch-local renderer-only fix. Integrate the rebuilt overlay as one unit, run its static validator, then run Kotlin/JVM/lint, package inspection, migration/progress, Review/Question Map, API 35, and signed-release gates. Do not combine the predecessor Biology payloads directly or allow a last-applied patch to determine any of the eight conflicting IDs.

### Second-pass references

[5]: https://github.com/rynmrde/Konkor/blob/55c19556fe8429548d1d7ae60939a61510bfa49e/reports/parallel/INDEPENDENT_BIO_GEO_REVIEW.md "Independent Biology/Geology cross-review"
[6]: https://github.com/rynmrde/Konkor/tree/parallel/bank-biology "Compact Biology analysis candidate"
[7]: https://github.com/rynmrde/Konkor/tree/parallel/bio-b "Complementary Biology candidate"
