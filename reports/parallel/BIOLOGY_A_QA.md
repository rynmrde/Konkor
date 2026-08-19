# Biology A Scientific QA Report

## Worker Identity and Baseline

| Field | Observed value |
|---|---|
| Worker | `KONKOR-W03-BIO-A` |
| Branch | `parallel/bio-a` |
| Baseline default branch | `main` |
| Baseline SHA | `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Baseline commit | `ci: publish rescue directly without artifact quota` |
| Final branch commit | `cedd6d437c8d36d4be5a41d7abe8170550ae6f7e` (superseded by the report-amend commit below) |
| Execution tier check | The task was assigned `NORMAL/STANDARD 1.6`; no Lite-tier marker was present in the active environment. |

The current repository stores the deployable project as a pinned V6.1 source archive plus the V6.1.4 rescue overlay. The worker downloaded the exact workflow-pinned source archive and verified the immutable archive hash before inspecting the active bank. The active source gzip and expanded SQLite hashes matched the project’s frozen-reference values: `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14` and `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`, respectively.

## Scope and Deterministic W03/W04 Boundary

The complete active Biology population contains 411 records. The audit population was defined as **active, non-obsolete, authored Biology TRAIN records with `A_CORE_FULL` or `B_RAPID_EXPOSURE` scope**, excluding SIM/FINAL holdouts, official-stem-training items, real-exam records, and quarantine. This produced 290 eligible records. Lexicographic stable-ID ordering divided the population without overlap: W03 audited positions `1..145`; W04 owns positions `146..290`.

| Measure | Baseline | W03 result |
|---|---:|---:|
| Whole-bank question rows | 1,216 | 1,216 |
| Biology rows | 411 | 411 |
| W03 assigned authored TRAIN Biology IDs | — | 145 |
| W04 assigned IDs | — | 145 |
| W03/W04 overlap | — | 0 |
| SQLite integrity | `ok` | `ok` |
| W03 IDs changed in candidate | — | 145, exactly the assigned set |
| Unassigned records changed | — | 0 |

The immutable stable IDs, answer keys, source types, pools, scope flags, safety eligibility, review flags, and obsolete status were preserved. No real-exam claim was created or changed; no historical key-conflict record was touched.

## Evidence and Scientific Method

The deep review used the project-designated Biology textbook and recent official-booklet evidence. The review treated these files as authoritative project sources, not as a basis to relabel authored items as authentic exam questions. The 1402–1404 booklets were used to calibrate form, statement precision, and Konkur-style distractor quality; correctness was kept tied to the supplied textbook sections.

| Evidence role | Project-authoritative source |
|---|---|
| Grade 10 Biology text | [Zist 10 PDF][1] |
| Grade 11 Biology text | [Zist 11 PDF][2] |
| Grade 12 Biology text | [Zist 12 PDF][3] |
| 1402 Biology booklet | [Zist 402, second session][4] |
| 1403 Biology booklets | [Zist 403, first session][5]; [Zist 403, second session][6] |
| 1404 Biology booklets | [Zist 404, first session][7]; [Zist 404, second session][8] |

The whole active Biology bank was machine-scanned for database integrity, unique IDs, JSON/row identity, option-count/key contracts, analysis presence and specificity signals, raw enum leakage, real-exam provenance, obsolete/quarantine contracts, exact duplicates, and near-duplicate candidates. The assigned half then received structured scientific review in 29 five-item batches, followed by a stronger, targeted repair pass for the 24 explanations that were too terse, placeholder-like, or cross-referential.

> The review rule was intentionally conservative: an item’s stable identity and key remained unchanged unless authoritative correction required otherwise. This worker found no justified key change in the assigned authored TRAIN cohort.

## Changes Applied to the Candidate Successor Bank

All 145 assigned items received standalone explanation review. Eighty-five items also received a stem and/or option rewrite to repair ambiguity, incomplete wording, factual precision, weak distractors, triviality, or non-Konkur form. The 145-item analysis rewrite removed generic trap/keyword filler and unsupported internal-label text from the assigned cohort.

| Change category | Count |
|---|---:|
| Assigned items deeply audited | 145 |
| Assigned items with any content change | 145 |
| Stem and/or option changes | 85 |
| Correct and/or option-analysis changes | 145 |
| Correct-key changes | 0 |
| Explicitly completed formerly incomplete A/B items | 2 |
| Raw internal-enum leaks within W03 candidate | 0 |
| Non-meaningful explanation fields within W03 candidate | 0 |

The two incomplete active records were repaired rather than silently left active or reset: `v3_bio_02_12` became a self-contained DNA replication/silent-mutation item, and `v3_bio_08_07` became a self-contained bile/emulsification and intestinal-villus item. Both retained their existing answer position, stable ID, subject, source type, access pool, and progress identity.

## Candidate Artifacts

| Artifact | SHA-256 | Purpose |
|---|---|---|
| `artifacts/radiology1405_bank_v6_2_bio_a_candidate.db` | `4795f614ebbc710fe5df3aa0416329fd9034163eea1791cf52ce815c73f32ec5` | SQLite candidate containing only W03 Biology-A delta |
| `artifacts/radiology1405_bank_v6_2_bio_a_candidate.db.gz` | `21dc64b6ba53940daba36116057eed0f84d60980d083c2de71531977a4ca61f9` | Deterministically gzipped candidate artifact |
| `reports/parallel/BIOLOGY_A_DELTA_AUDIT.json` | Generated in branch | Per-question changed-field and scientific-audit ledger |
| `reports/parallel/BIOLOGY_A_DELTA_VALIDATION.json` | Generated in branch | Deterministic identity/migration-safe validation result |
| `reports/parallel/BIOLOGY_A_MACHINE_SCAN_BASELINE.json` | Generated in branch | Whole active Biology baseline scan and W03/W04 split |
| `reports/parallel/BIOLOGY_A_MACHINE_SCAN_CANDIDATE.json` | Generated in branch | Whole Biology candidate scan |

## Validation Executed

| Gate | Result | Observed evidence |
|---|---|---|
| Pinned source archive integrity | PASS | SHA-256 matched the workflow-pinned V6.1 archive hash. |
| Frozen active gzip and DB integrity | PASS | Both frozen reference hashes matched. |
| Whole active Biology machine scan | PASS with findings | 411 Biology records, 296 baseline raw-enum findings, 6 exact-duplicate groups, and 269 near-duplicate candidates. |
| Candidate SQLite integrity | PASS | `PRAGMA integrity_check = ok`. |
| Candidate ID count and uniqueness | PASS | 1,216 unchanged IDs. |
| W03 changed-ID boundary | PASS | Exactly 145 changed IDs; zero unassigned IDs changed. |
| W03/W04 non-overlap | PASS | 145/145 partition with intersection 0. |
| Four options and valid key in W03 | PASS | All assigned items validated. |
| Correct-key preservation | PASS | 0 changed keys. |
| Source/pool/scope/safety contract preservation | PASS | No assigned record changed these fields. |
| Meaningful, standalone explanations in W03 | PASS | 0 residual failures after the targeted repair pass. |
| Raw internal-enum leakage in W03 | PASS | 0 residual leaks. |

The complete candidate scan still reports 186 raw-enum findings and five exact-duplicate groups outside the W03 authored-TRAIN assignment. These are **not silent passes**: they are explicit integration backlog for W04 and the cross-worker bank integrator. The remaining exact groups are composed of unassigned official/training or W04 IDs; this worker did not alter them to avoid violating the deterministic W03/W04 boundary.

## Bank-ID, Migration, and Integration Notes

This is a **material-bank change**, so the integrator must create an explicitly versioned successor bank rather than overwrite the frozen V6.1 reference. The candidate name uses `v6_2` only as an integration placeholder; the Foreman must allocate the actual next bank/app version after resolving all scientific worker deltas.

No Room-progress data may be reset. Since every unchanged-identity question retained its stable ID and answer key, the compatible migration design is to preserve existing attempts, confidence, flags, error history, mastery, due review state, and active sessions. The app must select the successor bank non-destructively and retain a compatible read path for any active session that references the frozen-bank digest. The integrator must not simply replace the V6.1 asset under the old identity.

The candidate SQLite file is intentionally a **worker delta artifact**, not a release-ready replacement: it contains only W03 changes applied to the frozen base. Integrate by question ID and authoritative evidence with all other scientific deltas, then build one unified successor JSON/SQLite/gzip and update checksum/version/migration contracts once. Do not last-commit-win overlapping bank changes.

## Blockers and Handoff

No W03-specific scientific blocker remains. The unresolved global Biology backlog is explicit: W04 must deep-audit its non-overlapping 145 authored TRAIN records; the Foreman must reconcile the remaining duplicate and raw-enum findings across all subject workers; and the final unified material-bank version must receive migration, build, APK-package, signed-release, and device-flow gates.

The handoff files are committed on `parallel/bio-a`. They include the deterministic scanner, cohort exporter, structured-review ledger, strict explanation-repair ledger, delta compiler, delta validator, candidate DB/gzip, and this report. These deliverables permit the integration branch to reproduce the W03 delta exactly from the frozen base.

## References

[1]: https://drive.google.com/file/d/1H6V7321-jC8n3MByS4dQ1V2qDHnbrS6f/view "Zist 10 PDF"
[2]: https://drive.google.com/file/d/1Mjyb4dvdsQj51orLsYkvJoHKJBTw7Wjl/view "Zist 11 PDF"
[3]: https://drive.google.com/file/d/1bj2hURks0yOZSEtXJBZRHlzUh4gHBJ-l/view "Zist 12 PDF"
[4]: https://drive.google.com/file/d/17EErlZc19qpiGXZis8cmCWsGfCu3xHKQ/view "Zist 402, second session"
[5]: https://drive.google.com/file/d/1RLMr0QK1qYDfLduSzIwV2U_3UbYUH8Gm/view "Zist 403, first session"
[6]: https://drive.google.com/file/d/1YAcugEg28-mHnRKtyIFuFVj1KEZJ5utv/view "Zist 403, second session"
[7]: https://drive.google.com/file/d/1ISfKm_0F-JskE0Eih3A_hbLjgaHv46Zt/view "Zist 404, first session"
[8]: https://drive.google.com/file/d/13QoQKbp1j3vhCdby0tAvsqruXg9UpoKV/view "Zist 404, second session"
