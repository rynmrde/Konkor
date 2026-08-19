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

## SECOND_PASS_REVIEW

**Second-pass role:** A2 Mathematics / duplicate-session QA. **Bank evidence:** immutable V6.1 gzip SHA-256 `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`; no bank row, ID, key, option, source label, or progress record was modified in this pass.

### Canonical paired-statement disposition

The 21 previously blocked records are **not quarantined and not rewritten**. The checksum-verified frozen record for every ID contains a non-empty canonical `stimulus.left` and `stimulus.right`; the visible-stem defect is therefore an integration/UI rendering concern, not a bank-identity or selection defect. Stable question IDs remain unchanged, so historical `attempt.questionId`, mastery, due-credit, active-session, backup, and review references require **no mapping or Room migration**. The Review/UI owner must render these canonical structured fields in both test and review surfaces.

| Stable ID | Canonical left (A) | Canonical right (B) | Key | Disposition |
|---|---|---|---:|---|
| `v3_bio_02_12` | DNAپلیمراز رشتهٔ جدید را فقط در جهت ۵′ به ۳′ طویل می‌کند. | هر جهش الزاماً رخ‌نمود جاندار را تغییر می‌دهد. | 3 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_bio_05_12` | چرخهٔ کربس در مادهٔ زمینه‌ای راکیزه انجام می‌شود. | در خود قندکافت کربن‌دی‌اکسید آزاد می‌شود. | 3 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_bio_06_07` | اکسیژن آزادشده در فتوسنتز از شکستن آب به‌دست می‌آید. | گیاهان CAM معمولاً روزنه‌های خود را در روز باز می‌کنند. | 4 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_bio_07_15` | افزایش فشار هیدروستاتیک مویرگ خروج آب به مایع میان‌بافتی را تقویت می‌کند. | همهٔ سیاهرگ‌ها خون کم‌اکسیژن حمل می‌کنند. | 4 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_bio_08_07` | صفرا آنزیم گوارشی ندارد و با ریزکردن قطره‌های چربی سطح تماس را زیاد می‌کند. | پرزهای فراوان، ویژگی اصلی رودهٔ بزرگ برای جذب مواد غذایی‌اند. | 3 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_bio_10_11` | تراوش خون در کلافک و ورود مواد به کپسول بومن آغاز می‌شود. | آلدوسترون فقط و مستقیماً بازجذب آب را زیاد می‌کند. | 1 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_bio_11_07` | بازشدن کانال‌های ولتاژی سدیم، فاز سریع ناقطبی‌شدن را ایجاد می‌کند. | ناقل عصبی از یاختهٔ پس‌سیناپسی به فضای سیناپسی رها می‌شود. | 1 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_bio_12_07` | هورمون‌های تیروئیدی معمولاً سوخت‌وساز پایه را افزایش می‌دهند. | FSH و LH را هیپوتالاموس ترشح می‌کند. | 2 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_bio_14_10` | HCG در اوایل بارداری به حفظ جسم زرد کمک می‌کند. | لقاح معمولاً در حفرهٔ رحم انجام می‌شود. | 3 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_bio_15_15` | پس از لقاح مضاعف در نهاندانگان، تخم و یاختهٔ آغازین آندوسپرم تشکیل می‌شوند. | همهٔ عناصر رسانای آوند چوبی در بلوغ زنده‌اند. | 3 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_bio_16_10` | رانش ژنی در جمعیت‌های کوچک اثر نسبی بیشتری دارد. | صفات اکتسابی هر فرد الزاماً به نسل بعد منتقل می‌شوند. | 1 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_chem_20_03` | افزایش نیروهای بین‌مولکولی معمولاً نقطهٔ جوش را افزایش می‌دهد. | جفت‌الکترون ناپیوندی هیچ اثری بر شکل مولکول ندارد. | 4 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_chem_26_03` | ایزومرهای ساختاری فرمول مولکولی یکسان و اتصال اتمی متفاوت دارند. | فرمول عمومی آلکن زنجیری تک‌پیونددوگانه CₙH₂ₙ₊₂ است. | 3 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_chem_54_07` | خوردگی آهن یک فرایند اکسایش‌ـ‌کاهش است و حضور آب و اکسیژن آن را تسهیل می‌کند. | هر سنگ معدنی با عیار بیشتر، بدون توجه به هزینه‌ها، الزاماً اقتصادی‌تر است. | 3 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_phys_30_02` | نیروی شناوری برابر وزن شارهٔ جابه‌جا‌شده است. | در لولهٔ باریک‌تر، سرعت شارهٔ پایا کمتر است. | 3 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_phys_33_02` | در اتصال موازی، اختلاف پتانسیل دو سر شاخه‌ها یکسان است. | ولت‌سنج آرمانی مقاومت ناچیز دارد. | 3 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_phys_34_03` | جهت جریان القایی با تغییری که آن را ایجاد کرده مخالفت می‌کند. | سیم موازی میدان بیشترین نیروی مغناطیسی را می‌گیرد. | 4 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_geo_45_09` | در مرز واگرا پوستهٔ اقیانوسی جدید می‌تواند ساخته شود. | گسل امتدادلغز فقط جابه‌جایی قائم ایجاد می‌کند. | 3 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_geo_46_08` | سنگ دگرگونی بدون ذوب کامل و بر اثر دما/فشار تغییر می‌کند. | سختی موس مقدار مقاومت سنگ در برابر ضربه است. | 1 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_geo_47_07` | افزایش عیار معمولاً ارزش اقتصادی ذخیره را بیشتر می‌کند. | عیار هیچ ارتباطی با مقدار مادهٔ مفید ندارد. | 3 | **RETAIN**; canonical stimulus available; UI rendering required |
| `v3_geo_49_08` | خاک حاصل برهم‌کنش سنگ مادر، اقلیم، جانداران، پستی‌وبلندی و زمان است. | حذف پوشش گیاهی معمولاً فرسایش آبی را کم می‌کند. | 2 | **RETAIN**; canonical stimulus available; UI rendering required |

**Canonical-stimulus gate:** PASS — 21/21 IDs retained their stable identity; 21/21 have non-empty left/right structured fields; 0 exact IDs require quarantine or bank rewrite.

### Duplicate and numeric-variant cluster disposition

The selection layer treats an evidence family as a non-novel exposure by normalizing superficial number changes, reusable wrappers, option-method suffixes, and option order. Any group below is therefore blocked from appearing twice in one normal TRAIN block and a correct exact re-exposure has zero mastery delta. The independent five-exact/five-numeric finding did not supply member IDs; the deterministic cross-check is stronger operationally because it protects all detected family collisions, not only a fixed ten-group subset.

| Detector / disposition | Group count | Member IDs / handling |
|---|---:|---|
| Literal same prompt with reordered options | 4 | v3_chem_26_10, v3_chem_26_11, v3_chem_26_12, v3_chem_26_13; v3_chem_20_18, v3_chem_20_19, v3_chem_20_20; v3_chem_19_11, v3_chem_19_12, v3_chem_19_13; v3_chem_54_11, v3_chem_54_12, v3_chem_54_13 — **SUPPRESS** in same normal TRAIN block and do not count as unique evidence. |
| Template/direct-path same-problem families | 21 | v3_math_41_04, v3_math_41_08, v3_math_41_12; v3_chem_24_03, v3_chem_24_07; v3_math_40_03, v3_math_40_07; v3_math_40_04, v3_math_40_08, v3_math_40_12; v3_math_40_06, v3_math_40_10; v3_geo_44_08, v3_geo_44_12; v3_math_39_04, v3_math_39_08, v3_math_39_12; v3_chem_23_04, v3_chem_23_08; v3_chem_23_05, v3_chem_23_09; v3_phys_34_04, v3_phys_34_08; v3_phys_32_04, v3_phys_32_08, v3_phys_32_12; v3_phys_35_04, v3_phys_35_08; v3_geo_50_07, v3_geo_50_11; v3_chem_25_02, v3_chem_25_06, v3_chem_25_10; v3_phys_30_04, v3_phys_30_08; v3_phys_30_06, v3_phys_30_10; v3_chem_22_03, v3_chem_22_07; v3_math_36_06, v3_math_36_10; v3_geo_43_07, v3_geo_43_11; v3_geo_48_09, v3_geo_48_13; v3_chem_17_04, v3_chem_17_08 — **SUPPRESS** by `evidenceFamily`; distinct instructional shells are not fresh mastery evidence. |
| All evidence-family collisions after canonical stimulus expansion | 25 | **SUPPRESS** in same normal TRAIN block; the mass gate verifies no selected family repeats. |
| Strict digit-canonical prompt variants with changed literal prompt | 0 | None under this conservative prompt-only detector — any future detected case is already covered by digit-normalized evidence-family suppression. |

### Final-Hours composition and unique-mastery protection

The deterministic composed-source gate scopes `StudyRepository.startOrResume` through active-session construction and fails if a Final-Hours overlay adds the historical exact-repeat fallback. It requires the normal TRAIN invariant, `attempted + selected` exclusions, at least three evidence-family exclusions across the selection paths, and the `AdaptiveEngine` rule `val masteryDelta = if (exactRepeat && correct) 0.0 else delta`.

| Gate | Result | Observed output |
|---|---|---|
| Frozen IDs / four options / key range / option-analysis coverage | PASS | 1,216 records; every key in `0..3`; four options per record. |
| Canonical pair stable-ID/stimulus gate | PASS | 21/21 stable IDs; 21/21 non-empty left/right; SIM intersection 0. |
| Mass normal TRAIN generation | PASS | 2,000 generated blocks; duplicate ID 0; historical-repeat exposure 0; evidence-family repeat 0; adaptive short blocks 61. |
| SIM isolation | PASS | SIM1 117; SIM2 117; mutually disjoint; no normal TRAIN holdout leakage. |
| Final-Hours composed selection source gate | PASS | No `poolIds` repeat fallback in `startOrResume`; historical and evidence-family exclusions present. |
| Unique mastery | PASS | Correct exact re-exposure mastery delta remains zero. |

**Integration instruction:** apply the existing A2 duplicate/mastery overlay, then this second-pass test/report overlay, then the Review/UI canonical-stimulus renderer. Run `tests/verify_a2_duplicate_session.py` only after all overlays are composed; it is intentionally a final-composition regression gate.

### Second-pass references

- Frozen authoritative bank folder: `RADIOLOGY_1405_V6_1_FINAL_FREEZE_2026-08-12` (`1R2IovFE_e0O_vU4IBCSiJpqrwK4LecxK`).
- Frozen bank gzip SHA-256: `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`.
- A2 primary baseline: `72dc76e56b7ae625ad1904c76910eeaec5f90f58`; original A2 handoff commit: `77d55808293f7258a36de0e3f1e57166233c70a7`.


### Physics duplicate contract addendum

The frozen full-source records confirm that the following IDs differ in presentation shell but share an immutable `followup_group`. They are not independently novel within one normal TRAIN block. The composed selector now constructs a multi-key contract containing the existing evidence-family key plus `followup:<group>` and any present canonical-scenario key. Candidate filtering and the final block invariant both reject a collision on **any** such key.

| Pair | Frozen shared `followup_group` | Same-session disposition | Later exposure disposition |
|---|---|---|---|
| `v3_phys_30_04` / `v3_phys_30_08` | `فشار، چگالی و شاره‌ها::subskill_4` | **Suppress** the second member, even if IDs and UI scenario families differ. | Retain only as review evidence; set the existing `spacedRetrieval` marker; zero correct-answer mastery delta and no distinct-coverage increment. |
| `v3_phys_30_06` / `v3_phys_30_10` | `فشار، چگالی و شاره‌ها::subskill_2` | **Suppress** the second member, even if IDs and UI scenario families differ. | Retain only as review evidence; set the existing `spacedRetrieval` marker; zero correct-answer mastery delta and no distinct-coverage increment. |

The two exact pair regressions are part of the 2,000-block mass gate. The gate verifies their source group equality, proves the selector supplies a shared suppression key, and asserts neither pair co-occurs in any normal TRAIN block. The independent five exact and five numeric cluster finding is covered by the same evidence-family component of the multi-key contract; any cluster member collision is blocked before selection and rechecked at block construction.

**Post-addendum composed-gate result:** PASS — 1,216 frozen IDs; four-option/key coverage PASS; canonical paired stimulus 21/21; 2,000 normal blocks with no duplicate ID, evidence/follow-up/canonical collision, historical exact repeat, or SIM leakage; 169 adaptive short blocks rather than forced repetition; exact Physics follow-up regressions 2/2 PASS. The result is a test-only/code overlay handoff; no bank rows, stable IDs, Room schema, migration mapping, main branch, or release was changed.
