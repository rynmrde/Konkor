# A2 Physics Bank and Exam-Solution QA — V6.1.4

**Role:** `[KONKOR-A2-M1-PHYSICS]` Physics bank + exam-solution QA, standard worker.  
**Worker branch:** `parallel/a2-physics`.  
**Baseline pinned:** `origin/main` and release tag `radiology1405-apk-v6.1.4-20260817` both resolve to commit `72dc76e56b7ae625ad1904c76910eeaec5f90f58`.  
**Scope:** Reconstructed V6.1.4 release source and frozen bank, not the small GitHub scaffold alone. No `main` merge, force-push, or release publication was performed.

> **Release clearance: NO.** The frozen database is structurally valid and all reviewed scientific keys are correct, but release-critical learner-facing analysis defects remain: raw internal enum leakage in 168 Physics items, templated filler in analyses, comparison stimuli that the current UI does not render, and ID-only session selection that does not block demonstrated same-scenario variants.

## Provenance and Reconstruction

The attached Composio GitHub connection was active and a read-only repository request succeeded. The current main reference and the V6.1.4 tag were independently pinned to the same commit. The release overlay and its workflow were retrieved through the same approved route; the immutable V6.1 base archive was retrieved through the approved Drive connection and verified before the overlay was applied.

| Artifact | Observed SHA-256 | Result |
|---|---:|---|
| V6.1 base Android project ZIP | `1344aca90474ac96e27e94ba754ebafd42778e2ceaab91f9a5fb1be2e882d046` | Verified |
| V6.1.4 rescue overlay | `d17bdd905def35a45caa32aa5a0b07b6196ecc78de493a340bf36fac0c0103c3` | Verified |
| Frozen gzip bank | `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14` | Verified |
| Expanded SQLite bank | `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c` | Verified |
| Official verified-JSON baseline | `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d` | Reported by release validator |

The current syllabus anchor was also verified on the Ministry textbook portal: **Physics (3)**, book code **112244**, Experimental Sciences, grade 12, academic year **1404–1405**.[1]

## Complete Physics Machine Scan

All **187** Physics records in the frozen V6.1.4 database were scanned. Every Physics record is active; none is in `QUARANTINE`. The scan checked ID/option/key integrity, learner-facing analysis fields, raw enum leakage, full-payload duplicates, reordered-option duplicates, numeric reskins, review completeness, pools, source types, and final-hours scope.

| Measure | Exact result |
|---|---:|
| Physics records scanned | 187 |
| Active / quarantined | 187 / 0 |
| TRAIN / SIM1 / SIM2 / FINAL | 142 / 22 / 22 / 1 |
| Authored / official-stem training | 180 / 7 |
| Four-option and correct-index failures | 0 / 0 |
| Missing `review_default` payloads | 0 |
| Full-payload exact duplicates | 0 groups |
| Full-payload reordered-option duplicates | 0 groups |
| Full-payload numeric-reskin candidates | 0 groups |
| Stem-plus-options collisions requiring stimulus inspection | 1 group |
| Short `correct_analysis` records (<60 normalized characters) | 6 |
| Learner-facing raw-enum leaks | 168 items, 168 distractor-analysis occurrences |

The sole stem/options collision is **not** an exact duplicate after its full stimulus is included: `v3_phys_30_02` is a fluids comparison and `v3_phys_33_02` is a circuits comparison. The corresponding full-payload, option-reordered, and numeric-skeleton comparisons are all distinct.

The high-ROI/final-hours set comprises all nine selected Physics microtopics in this frozen rescue profile: kinematics; work, energy and power; fluids; current, resistance and circuits; dynamics, friction and momentum; heat and thermodynamics; oscillation/waves/sound; electrostatics/capacitance; and magnetism/induction. The profile uses 271 official 1398–1404 Physics records across 16 source files, applying higher planning weights to 1402–1404. Its recent weighted distribution is predominantly numerical single-stage (40.48%), graph/diagram interpretation (33.12%), and numerical multi-stage (7.46%); 47.94% of forms are numerical overall. These metadata support the required emphasis on formula, condition, unit, direction, and calculation checks.

## Deep Scientific Review

The deep-review cohort had **25** records: all seven available 1402–1404 official-stem Physics records, two top-priority authored records from each current final-hours Physics microtopic, six short-analysis records, and the full near-duplicate candidate set. Every reviewed key was independently recomputed or checked against the stated physical model. No reviewed correct index was scientifically false.

| Item(s) | Model and verification result | Analysis-quality result |
|---|---|---|
| `real_1402_n2in_phys_070` | Work–energy theorem: \(\Delta K=W_g+W_{air}\); \(22.4-30=-7.6\,J\). Correct negative sign. | PASS |
| `real_1404_n2in_phys_075` | Latent heat only after boiling: \(Q=mL_v=9024\,kJ\), \(t=Q/P=4512\,s=75.2\,min\). | PASS |
| `real_1402_n2in_phys_073` | \(F=1.8C+32\) and \(F=5C\) give \(C=10\), then \(T=283\,K\). | PASS |
| `real_1402_n2in_phys_056` | \(\mu=\rho\pi r^2\), \(v=\sqrt{T/\mu}=100\,m/s\), \(\lambda=v/f=0.50\,m\), crest-to-next-trough \(=\lambda/2=25\,cm\). | PASS |
| `real_1403_n1in_phys_063` | Battery removed means fixed \(Q\); spacing ×1.5 makes \(C\to C/1.5\) and \(U=Q^2/(2C)\) ×1.5. Increase is \(2\,mJ\). | PASS |
| `real_1402_n2in_phys_075` | \(|F|=|q|vB\) at \(90^\circ\) gives \(B=0.5\,T\); south × east is upward for positive charge, so an electron force is downward. | PASS |
| `real_1403_n1in_phys_074` | Solenoid \(B=\mu_0NI/L=2.4\times10^{-3}\,T=24\,G\), with both cm→m and mA→A conversions correct. | PASS |
| `v3_phys_30_04`, `v3_phys_30_08` | Continuity gives \(A_1v_1=A_2v_2\Rightarrow v_2=9\,m/s\). | Key correct, but both should state the **steady incompressible-flow** condition; they are same-scenario variants in the same follow-up group. |
| `v3_phys_30_06`, `v3_phys_30_10` | Density gives \(\rho=m/V=4/0.002=2000\,kg/m^3\). | Key correct, but these are same-scenario variants in the same follow-up group and their analyses are too terse. |
| `v3_phys_33_05`, `v3_phys_35_05` | Ohm: \(I=V/R=2\,A\); wave: \(v=f\lambda=10\,m/s\). | Keys/units correct; condensed analyses need an explicit model → substitution → unit → answer path. |
| Conceptual authored cohort (`v3_phys_27_01`, `29_01`, `30_01`, `30_02`, `33_01`, `33_02`, `28_01`, `28_02`, `31_01`, `35_01`, `32_01`, `34_03`) | All reviewed correct claims, signs, directions, or conditions are physically correct. | FAIL presentation QA: generic template language and raw tokens occur in learner-visible distractor explanations; comparison records also depend on a stimulus that current UI does not render. |

The following short analyses require expansion despite having correct numerical answers: `v3_phys_30_04`, `v3_phys_30_06`, `v3_phys_30_08`, `v3_phys_30_10`, `v3_phys_33_05`, and `v3_phys_35_05`. Each needs the explicit model, relevant condition, substitution, unit check, and answer statement rather than an answer-only equation.

## Mandatory Defects Found

### 1. Raw internal enums leak into Persian review text

The second all-item pass found **168** Physics items with raw internal labels in `distractor_analyses`, including `wrong_condition`, `partial_truth`, `overgeneralization`, `calculation_trap`, and `unit_mistake`. The current review UI renders `question.optionAnalyses[original]` directly, so this is a user-visible breach of the no-enum rule.

| Filler or leakage signal | Occurrences | Affected Physics items |
|---|---:|---:|
| Raw enum labels in rendered distractor analyses | 168 | 168 |
| “این گزینه با همهٔ شرط‌ها سازگار است” | 1,360 | 170 |
| “منشأ دام این گزینه” | 1,020 | 170 |
| “نکتهٔ تثبیتی” | 873 | 170 |
| “از کلیدواژه جواب نده” | 533 | 21 |
| “این گزاره با کتاب سازگار است” | 180 | 23 |

This is not merely style debt. It makes post-submit explanation generic instead of question-specific and exposes implementation vocabulary to learners. The required repair is a bank-quality rewrite of every affected `distractor_analyses` and `review_default` payload using Persian, option-specific reasoning. A display-time translation layer alone would conceal tokens but would not cure the generic analysis defect.

### 2. Comparison stimuli are stored but not rendered

`v3_phys_30_02`, `v3_phys_33_02`, and `v3_phys_34_03` store their A/B claims in `stimulus.type == "comparison"`. The current `TestQuestion` and `ReviewQuestion` render source crops and stems, but not comparison stimuli. A learner sees only “دربارهٔ دو عبارت A و B…” and the answer combinations, without the two statements. This violates standalone review completeness and makes such questions unanswerable on the current UI.

**Required implementation fix:** render a comparison card with the actual `left_label`, `left`, `right_label`, and `right` directly after the stem in both test and review, and add an instrumentation test that verifies visibility after process recreation and on reopening review.

### 3. Normal-block selector excludes IDs only, not demonstrated scenario variants

`BankStore.trainingCandidates` and `distinctAlternative` use the `excluded` ID set only. They do not exclude `followup_group`, semantic family, or a canonical scenario signature. The demonstrable pairs below share a follow-up group and retain the same numeric setup but differ only by direct versus “solution-path” framing.

| Same follow-up group | Variant A | Variant B | Risk |
|---|---|---|---|
| `فشار، چگالی و شاره‌ها::subskill_4` | `v3_phys_30_04` direct continuity, 6→2 cm² and 3 m/s | `v3_phys_30_08` same numbers, answer-path framing | Both can be selected in one normal block. |
| `فشار، چگالی و شاره‌ها::subskill_2` | `v3_phys_30_06` density, 4 kg and 0.002 m³ | `v3_phys_30_10` same numbers, direct framing | Both can be selected in one normal block. |

**Required implementation fix:** retain intentional spaced retrieval across time, but exclude the active session’s `followup_group` and a canonical scenario fingerprint while selecting ordinary training blocks. Count a later intentional repeat as `review_repeats`, never as distinct mastery.

## Fix Status

No bank binary or source-overlay mutation was committed by this worker. That restraint is intentional: the V6.1.4 frozen gzip/SQLite hashes are release-pinned, and a material bank update needs a new bank/app version, non-destructive migration proof, a regenerated overlay, updated hash gates, packaged-bank validation, and full integration QA. A quick direct gzip edit would falsify the frozen identity and is not safe.

The branch contains this factual handoff report only. The foreman should treat the three defects above as **required fixes**, not as optional cleanup. The scientifically correct answer keys can be preserved while changing only explanation text and rendering/selection behavior, but the changed bank must receive a new provenance hash and migration evidence.

## Tests and Reproducible Evidence

| Gate | Result | Evidence |
|---|---|---|
| Frozen gzip / DB hash and SQLite integrity | PASS | `verify_asset_v6_1.py` |
| Bank counts, pools, IDs, keys, four options, SIM disjointness | PASS | `verify_asset_v6_1.py` and `verify_rescue_v614.py` |
| Release static validation after documented audio prerequisite | PASS | `V61_PROJECT_STATIC_VALIDATION=PASS` |
| Physics all-item structural scan | PASS with 6 short-analysis findings | `scan_physics_v614.py` |
| Full-payload exact/reordered/numeric duplicate scan | PASS, zero groups | `audit_physics_ui_duplicates.py` |
| Learner-facing raw-enum and generic-filler scan | FAIL | 168 rendered-enum items; counts above |
| Comparison-stimulus UI trace | FAIL | `RadiologyApp.kt` test/review code renders crop and stem but not comparison stimulus |
| Follow-up-group selection trace | FAIL | `BankStore.kt` candidate selectors only test ID membership in `excluded` |
| Kotlin compile/JVM/lint/instrumentation | Not run in this reconstructed QA sandbox | The immutable base ZIP exposes neither `gradlew` nor a `gradle` executable locally; this does **not** waive the release gate. |

The first static-validation invocation failed only because the release workflow’s documented offline-audio generation step had not yet run (`sfx_select.ogg` absent). After `tools/generate_audio.sh`, the same static suite passed its packaged-asset, native-experience, UX, day-selector, rescue-plan, bank, and pool checks.

## SECOND_PASS_REVIEW

**Second-pass result: FINDINGS CONFIRMED; RELEASE BLOCKED.** I reran the full-payload duplicate and learner-text scans after correcting the audit parser to use the actual `correct_analysis` field and sign-preserving option canonicalization. The revised scan confirmed zero true full-payload duplicates, zero reordered-option duplicates, zero numeric-reskin groups, one benign stem/options collision with distinct stimuli, six short analyses, and 168 user-visible raw-enum items. The 25-record scientific cohort was then rechecked against the physical model, formula, conditions, signs/directions, units, and calculations listed above; no key correction is requested, but the analysis/UI/selector repairs are required.

## Handoff Priority

The next compatible worker or foreman should first repair **comparison-stimulus rendering** and **normal-session semantic/follow-up exclusion**, then rewrite the **168** affected Physics distractor analyses from source-grounded content rather than template expansion. After any bank change, rerun the frozen/new-bank identity gates, duplicate/session-selection checks, review-flow instrumentation, persistence, packaged-bank inspection, and signed-release verification.

## References

[1]: http://chap.sch.ir/books/13332 "Ministry textbook portal — Physics (3), book code 112244, 1404–1405"
[2]: https://github.com/rynmrde/Konkor/tree/radiology1405-apk-v6.1.4-20260817 "Konkor V6.1.4 release tag"
[3]: https://github.com/rynmrde/Konkor/commit/72dc76e56b7ae625ad1904c76910eeaec5f90f58 "Pinned V6.1.4 / current-main commit"
