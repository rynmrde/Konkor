# A2 Mathematics, Duplicate, Session-Selection, and Unique-Mastery QA

> **Role:** Mathematics scientific QA and duplicate/session-selection/unique-mastery owner  
> **Account label:** A2 / KONKOR-A2-M2-MATH-DUP  
> **Remote branch:** `parallel/a2-math-duplicates`  
> **Pinned baseline:** `72dc76e56b7ae625ad1904c76910eeaec5f90f58` (`main`, `ci: publish rescue directly without artifact quota`)  
> **Scope discipline:** No main merge, no force push, and no release publication. The historical V6.1.4 overlay and frozen bank were not modified.

## Executive finding

The frozen bank is structurally intact, but the existing normal TRAIN selector contains a direct contradiction of the Final-Hours rule: after fresh safe candidates are exhausted, it re-serves previously attempted question IDs as a “last resort.” The mastery engine also allowed a correct repeat of the same question to add mastery even though `distinctQuestions` did not increment. A separate evidence-family guard and adaptive short-block behavior are supplied in an **integration-only V6.1.5 candidate overlay**. This preserves intentional spaced retrieval as a different question while preventing exact and cosmetic variants from masquerading as new coverage.

The full Mathematics bank machine scan identified 166 Mathematics questions, with 137 active TRAIN records. However, only 28 active Mathematics TRAIN records meet the existing `safeOnly` predicate because 109 Mathematics records carry `needs_human_review=true`; this is a genuine availability constraint for the current selector, not evidence that the frozen bank was mutated. The patch intentionally converts depletion into a shorter adaptive block rather than repeating prior questions to force a fixed block size.

| Area | Result | Release implication |
|---|---:|---|
| Frozen gzip SHA-256 | `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14` | Unchanged and verified |
| Expanded SQLite SHA-256 | `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c` | Unchanged and verified |
| SQLite `quick_check` | `ok` | Pass |
| Question IDs | 1,216 total; 0 duplicate IDs | Pass |
| Exact normalized detector pairs | 149 | Mostly shared authored shells; requires semantic classification, not deletion by count |
| Same stem/reordered-options pairs | 412 | Mostly shared authored shells/options; selection protection added |
| Near-duplicate review candidates | 252; 80 Mathematics | Candidate queue, not all factual duplicates |
| Active Mathematics TRAIN records | 137 | Scan complete |
| Safe active Mathematics TRAIN records | 28 | Constrains normal-block fresh supply |
| Mass TRAIN-generation trials | 2,000 | Pass: no exact ID repeat, no evidence-family repeat, no SIM leakage |

## Mathematics scientific QA

The machine scan covered all 166 Mathematics records for four options, key range, non-empty stem, non-empty reasoning, duplicate option text, pool status, priority, scenario family, and active scope. No structural schema/content violation was found in this scan. The 28 safe active records reachable under the present `safeOnly` rule were then deep-reviewed for domain conditions, algebra/calculus validity, answer key, solution path, and fast method.

| Microtopic | Total Math | Active TRAIN | Safe active TRAIN | High-value review conclusion |
|---|---:|---:|---:|---|
| Function, domain, composition, inverse | 22 | 19 | 3 | The reviewed domain and composition condition items are correct; direct-domain clones require suppression. |
| Powers, radicals, logarithms | 22 | 16 | 1 | Condition item is correct; masked-number logarithm variants are low-transfer clone candidates. |
| Equations, inequalities, absolute value | 20 | 16 | 3 | Domain-exclusion and absolute-value logic items reviewed correct. |
| Trigonometry | 20 | 16 | 4 | Period and parity identities reviewed correct; three presentation variants of the same period item were found. |
| Limit and continuity | 20 | 17 | 10 | One-sided-limit, continuity condition, and factor-cancellation algorithms reviewed correct; several presentation variants were found. |
| Derivative and rate of change | 20 | 17 | 4 | Constant-derivative and tangent-slope items reviewed correct; duplicate presentation variants were found. |
| Probability and counting | 21 | 17 | 1 | Uniform-sample-space condition item reviewed correct. |
| Statistics | 21 | 19 | 2 | Translation-invariance and dispersion claims reviewed correct. |

The reviewed direct algorithms are mathematically sound: composition requires the output of the inner function to lie in the outer function’s domain; `1/(x−3)` excludes only `x=3`; `sin(2x)` has period `π`; `log_a(x)` requires `x>0`; `(x²−9)/(x−3)` tends to `6` at `x→3`; and continuity at `a` requires `lim f(x)=f(a)`. The reviewed real-exam anchors `real_1403_n1in_math_126` and `real_1404_n1in_math_133` also matched their supplied keys and calculation paths during manual review.

The bank-quality concern is **calibration and novelty**, not a documented key error in the reviewed safe subset. Examples include the same visible mathematical prompt presented as direct, “model-linked,” and “answer-with-method” variants: `v3_math_36_06/v3_math_36_10`; `v3_math_39_04/v3_math_39_08/v3_math_39_12`; `v3_math_40_03/v3_math_40_07/v3_math_40_11`; `v3_math_40_04/v3_math_40_08/v3_math_40_12`; `v3_math_40_06/v3_math_40_10`; and `v3_math_41_04/v3_math_41_08/v3_math_41_12`. These are **low-value near duplicates**, not distinct new evidence. No frozen-bank edit was made because it would require a material bank version and evidence-backed re-audit.

## Whole-bank duplicate classification

The initial lexical detector deliberately over-includes reusable stems such as “which statement is correct?” and paired-statement option shells. It was used only to form a review queue. The selection fix uses an evidence family limited to the same subject and microtopic, strips reusable presentation shells and option-method suffixes, and masks superficial number changes. It therefore suppresses the harmful case—same transferable reasoning presented cosmetically differently—without claiming that all lexical matches are identical knowledge claims.

| Detector class | Machine result | Classification | Handling |
|---|---:|---|---|
| Duplicate IDs | 0 | No true ID duplicates | No bank edit |
| Exact normalized stem/options pairs | 149 | Predominantly shared template shells; some are direct question replicas | Do not delete from frozen bank; block same evidence family in normal TRAIN selection |
| Same stem with reordered options | 412 | Presentation variants, frequently with different underlying claims in analysis metadata | Suppress same evidence family in normal TRAIN selection |
| Numeric-reskin pairs (strict full stem/options rule) | 0 | Detector too strict for shell-plus-number variants | Evidence-family masking catches the actual low-value numeric variants |
| Near-duplicate candidates | 252 | Candidate queue only; 80 Mathematics | Runtime suppression, not false assertion of factual identity |
| Intentional spaced retrieval | Supported | Different alternate question remains allowed across time | Keep; never treat it as new unique mastery unless question ID is new |
| Protected SIM holdouts | SIM1/SIM2 each 117 | Disjoint, safety-eligible, and absent from safe TRAIN candidates | Preserved and asserted in mass gate |

A cross-subject rendering blocker was also surfaced: 21 active TRAIN items in Biology (11), Geology (4), Chemistry (3), and Physics (3) display a generic “two statements A and B” stem with A/B answer-combination options but do not include the two statements in `Question.stem`. The `Question` runtime model does not expose a separate statement field, while the needed facts appear only inside solution metadata. These items are not Mathematics and were not edited on this branch, but they are **unanswerable as rendered** and should be assigned immediately to the scientific/UI bank owner before release. They also explain a large portion of the superficial duplicate detector output.

## Scoped implementation supplied

The Git repository stores native application changes as tar overlays. Accordingly, this branch adds a separate, non-release overlay rather than overwriting `radiology_v614_rescue_patch`.

| Artifact | SHA-256 / status | Purpose |
|---|---|---|
| `radiology_v615_a2_duplicate_patch/overlay.tar.xz` | `6bcf6f86f692aba2bf7dc5756c4320a4cb5ced91331a150b447d5fd81289ac89` | Apply after V6.1.4 overlay only; no release action |
| `radiology_v615_a2_duplicate_patch/MANIFEST.txt` | Included | Baseline, immutability, and Foreman integration requirements |
| `BankStore.kt` in overlay | Added evidence-family filter | Masks numeric reskins and reusable rendering shells for TRAIN selection only |
| `StudyRepository.kt` in overlay | Removed repeat fallback | Forbids duplicate IDs, historical exact repeats, and same-family variants in normal TRAIN blocks; permits adaptive shorter blocks |
| `AdaptiveEngine.kt` in overlay | Correct exact-repeat handling | Correct re-exposure does not increase mastery; wrong/blank repeat remains diagnostic evidence |
| `AdaptiveEngineTest.kt` in overlay | Added regression test | Asserts exact correct repetition cannot inflate mastery or unique coverage |
| `tests/verify_a2_duplicate_session.py` | Added deterministic gate | Validates bank IDs, SIM isolation, source guards, and 2,000 mass normal-block selections |

The patch does **not** alter the bank, bank hash, schema, Room version, migration list, package name, version, active-session serialization, review history, backups, or SIM blueprint. It only changes selection/mastery behavior and adds tests. No destructive migration is needed.

## Validation evidence

| Gate | Observed result | Notes |
|---|---|---|
| Frozen gzip hash | Pass | Matches historical immutable hash |
| Expanded SQLite hash and `quick_check` | Pass | Matches historical immutable hash; `quick_check=ok` |
| Bank counts/pools | Pass | 1,216 records; 17 real, 1,112 authored, 71 official-stem training, 16 quarantined |
| Original bank static component | Pass | `validate_v6_1.py` reached and passed bank hashes, SQLite integrity, counts, and pool isolation |
| A2 mass session gate, overlay source | Pass | 2,000 trials; 594 safe TRAIN candidates; SIM1/SIM2 117 each; 61 adaptive short blocks with no repeat fallback |
| A2 mass session gate, clean overlay chain | Pass | Fresh base ZIP → V6.1.4 overlay → A2 overlay, with frozen bank hash unchanged |
| Source assertions | Pass | Repeat fallback absent; duplicate/family guards present; exact-repeat mastery test present |
| Full local static suite | Not run to completion | Existing suite stops before app code at absent generated `sfx_select.ogg`; run `tools/generate_audio.sh` first in CI/Foreman environment |
| Kotlin/JVM/lint/debug APK | Not run locally | Sandbox lacked Gradle, Android SDK, and Kotlin compiler; required Foreman CI gate remains mandatory |
| Instrumentation/signed APK | Not run locally | Must be run by Foreman after versioning/integration |

## Required Foreman actions

Apply `radiology_v614_rescue_patch/overlay.tar.xz`, then `radiology_v615_a2_duplicate_patch/overlay.tar.xz`, on a fresh copy of the frozen V6.1 project. Treat the integration as an **app-only patch** and issue the appropriate new patch version only after all gates pass. Add `python tests/verify_a2_duplicate_session.py` to the final static CI gate; do not alter or re-run the V6.1.4 historical release workflow as a release publisher.

The Foreman must run generated-audio setup, Kotlin compilation, JVM tests, lint, debug/release assembly, packaged-bank verification, signed-APK verification, API 35 instrumentation, the complete answer/review/map/persistence flow, migration/progress preservation, Final-Hours timing checks, and the A2 mass gate. The 21 missing paired-statement stems are a **separate release blocker** unless a rendering or content fix proves that the A/B claims are visible to the user.

## Known limitations and residual risks

The detector is intentionally conservative. It prevents evidence reuse at runtime but does not rewrite the frozen authored content or assert that every near-duplicate pair is scientifically identical. The safe-question supply is low for Mathematics under existing `needs_human_review` flags, so Final-Hours volume must remain adaptive. The 61 short blocks seen in the conservative Monte Carlo are correct behavior under a no-repeat rule, not a failure to meet an obsolete quota.

The report is evidence for handoff, not release certification. No signed APK, Android instrumentation pass, or release asset was produced on this branch.
