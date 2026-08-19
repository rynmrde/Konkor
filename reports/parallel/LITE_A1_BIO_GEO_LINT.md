# Lite A1 Biology/Geology Structural and Heuristic Lint

**Worker role:** `KONKOR-A1-L2-BIO-GEO-LINT` (Lite support)  
**Account label:** Manus AI  
**Assigned branch:** `parallel/lite-a1-bio-geo-lint`  
**Baseline:** `origin/main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
**Baseline commit:** `ci: publish rescue directly without artifact quota` (2026-08-17 16:11:17 +0330)  
**Report status:** audit-only on the assigned branch; no bank, app, release, or `main` mutation.

## Connector and repository precheck

The existing project Composio connector was explicitly enabled for this task. A read-only GitHub access proof succeeded through Composio using the active GitHub account `github_senam-unware`: `GITHUB_GET_A_REPOSITORY` returned `rynmrde/Konkor`, default branch `main`, repository URL [github.com/rynmrde/Konkor](https://github.com/rynmrde/Konkor), and the repository’s current push timestamp. No standalone GitHub or Drive connector was used.

The local repository was freshly cloned or fetched, `origin/main` was pinned before inspection, and the assigned branch was created at the exact baseline SHA above. The current main tree is a scaffold plus tracked rescue patch archives; the packaged V6.1 bank is contained in the rescue overlay workflow rather than as a directly checked-out asset on the baseline tree. Consequently, the frozen-bank population counts below are reported from the completed subject-worker evidence, while the compact Biology analysis patches were extracted directly from their completed branches and linted locally.

## Scope and method

The scan covered the current rescue source paths, the completed Biology/Geology worker report, completed Biology analysis patches, duplicate helper evidence, and learner-facing UI text paths. The local patch scan examined **161 analysis updates**: 16 from `biology_v615_patch.json` and 145 from `biology_v620_w04_patch.json`. It checked stable IDs, analysis completeness, raw internal enums, vague referents, generic/short analysis heuristics, answer leakage where full options were present, and exact/reordered/near-duplicate candidates. Because these are compact analysis patches, absent `options`, `stem`, and `correct_index` fields are not treated as malformed full question records.

| Population or evidence set | Result |
|---|---:|
| Biology patch v6.1.5 updates | 16 |
| Biology patch v6.2 W04 updates | 145 |
| Total compact analysis updates locally linted | **161** |
| Duplicate IDs in compact patches | **0** |
| Exact cross-patch stem duplicate groups | **0** |
| Reordered-option duplicate groups in compact patches | **0** |
| Near-duplicate candidates in compact patches | **1** |
| Raw enum findings in compact patches | **0** |
| Vague-referent findings in compact patches | **3** |
| Full frozen active Biology/Geology records scanned by completed A1 worker | **585** |
| Final-Hours reachable Biology/Geology TRAIN records in completed A1 evidence | **474** |

## Findings from completed full-bank evidence

The completed `parallel/a1-biology-geology` report records a full machine scan of 585 active Biology/Geology records, comprising 408 Biology and 177 Geology items. It reports no JSON parse failures, missing stems, missing options, invalid answer indexes, or non-four-option active records. Its heuristic findings were **525 raw internal-enum occurrences**, **549 generic-analysis boilerplate flags**, **54 low-complexity generic authored-stem flags**, **23 duplicate-option pairs**, **20 vague-referent flags**, **7 exact duplicate clusters covering 21 IDs**, **3 reordered-option clusters covering 25 IDs**, and **107 near-duplicate candidate clusters**. These are candidate findings rather than automatic rewrite instructions.

The highest-risk scientific finding is `real_1401_in_geo_153`, a Geology earthquakes/hazards item whose displayed options were reported as malformed while the analysis distinguishes the ten-fold amplitude relation from the approximately 31.6-fold energy relation. The completed worker correctly rejected automatic mutation: the exact official source must be reconstructed before any versioned bank repair or quarantine decision. This item remains a medium-worker/Foreman review blocker.

The completed A1 worker also implemented a learner-facing renderer fix on its own branch, including mapping raw taxonomy labels and removing stock review lead-ins while preserving the question-specific scientific statement. The current baseline rescue overlay does **not** contain that `ScienceText.kt` normalizer; integration of that existing branch remains the appropriate action, followed by the required JVM, lint, instrumentation, and release gates. This Lite worker did not duplicate or cherry-pick that change.

## Compact patch lint findings

Both compact patches have unique stable update IDs and complete supplied analysis fields. The 16-record v6.1.5 patch produced no local lint findings. The 145-record W04 patch produced three vague-referent flags: `v3_bio_12_08`, `v3_bio_15_11`, and `v3_bio_16_13`. They require subject-level wording review; no automatic rewrite was made.

The W04 patch also supplies `stem` and/or `options` fields for a small subset of updates. These fields are outside a strict analysis-only patch contract and should be explicitly reconciled by the bank integrator against the immutable base before integration. The helper validator reported the following IDs: `v3_bio_10_11`, `v3_bio_11_07`, `v3_bio_11_24`, `v3_bio_12_07`, `v3_bio_13_15`, `v3_bio_14_10`, `v3_bio_14_20`, `v3_bio_15_11`, `v3_bio_15_15`, `v3_bio_15_24`, `v3_bio_16_10`, and `v3_bio_16_16`. This is a reconciliation warning, not proof that the supplied stem or options are scientifically wrong.

No raw enum was detected in the compact patch analyses. The full-bank raw-enum count remains the completed A1 worker’s 525-record finding and is addressed by that worker’s renderer patch, not by changing frozen bank bytes in this Lite branch. The compact patch scan found no duplicate IDs and no exact or reordered duplicate groups; this does not supersede the full-bank duplicate evidence above.

## UI-facing analysis and review checks

The baseline source contains the stand-alone review renderer with the original question stem, four options, user answer state, correct answer, confidence, error type, correct analysis, distractor analyses, short lesson, fast method, and trap sections. The baseline also contains review-state and Question Map-related paths. Focused source scanning found no direct raw enum tokens such as `condition_wrong`, `truth_partial`, `wrong_option`, or the Final-Hours state enum names in the baseline learner-facing source. However, the completed A1 full-bank evidence demonstrates that raw taxonomy labels can enter analysis content at runtime, so the completed renderer normalizer must be integrated and tested rather than relying on source-string absence alone.

The baseline UI still contains user-facing labels such as “دام” and a generic fallback “دام ثبت‌شده‌ای ندارد.” These are not, by themselves, proof of defective scientific analysis; they should be retained only where the underlying question-specific trap is present. Generic filler and vague referents remain a content-review queue, especially for the three W04 IDs listed above and the 20 full-bank vague-reference candidates in the completed A1 report.

## Safe helper handoff

After the primary scan, I inspected the completed subject and helper branches. The highest-priority compatible safe QA gap was a reusable validator that distinguishes compact analysis patches from full question records and prevents false malformed-option/key alarms. A separate helper branch was created as required:

| Helper branch | Commit | Change |
|---|---|---|
| `parallel/help-lite-a1-l2-analysis-patch-validator` | `e5cf891beb4cd6db71329b271b9f5f93c6caecc4` | Added `tools/validate_analysis_patch.py`, a non-mutating validator for stable IDs, analysis completeness, raw enums, vague referents, and forbidden full-record fields. |

The helper validator reproduced the clean v6.1.5 result and surfaced the three W04 vague-referent IDs plus the W04 full-record-field reconciliation warnings. It did not alter any question payload, key, source metadata, holdout membership, stable ID, or bank hash.

## Required handoff actions

The Foreman should integrate the completed A1 renderer fix only after normal conflict review, then run the full required compile, JVM tests, lint, debug/release signing, packaged-bank, Android API 35, install/launch, Review, Question Map, process-recreation, migration, and Final-Hours behavior gates. The Foreman should route `real_1401_in_geo_153`, the 23 duplicate-option pairs, the 7 exact duplicate clusters, the 3 reordered-option clusters, and the three W04 vague-referent IDs to medium/standard scientific review. No frozen bank artifact should be modified in place.

This Lite worker found no safe evidence-backed bank rewrite to apply. The remaining content findings require authoritative textbook or official-exam source review, explicit identity/migration handling, and a new bank version if any material correction is eventually accepted.

## References

[1]: [Konkor baseline repository](https://github.com/rynmrde/Konkor/tree/72dc76e56b7ae625ad1904c76910eeaec5f90f58)  
[2]: [Completed Biology/Geology QA branch](https://github.com/rynmrde/Konkor/tree/parallel/a1-biology-geology)  
[3]: [Completed Biology bank QA branch](https://github.com/rynmrde/Konkor/tree/parallel/bank-biology)  
[4]: [Biology duplicate helper branch](https://github.com/rynmrde/Konkor/tree/parallel/help-duplicates-bio-a)  
[5]: [Lite helper validator branch](https://github.com/rynmrde/Konkor/tree/parallel/help-lite-a1-l2-analysis-patch-validator)
