# Biology-B Complementary QA Report — Deterministic W04 Cohort

## Baseline, scope correction, and branch boundary

This is the final factual handoff for `parallel/bio-b`. The GitHub default branch was pinned at [`72dc76e56b7ae625ad1904c76910eeaec5f90f58`](https://github.com/rynmrde/Konkor/commit/72dc76e56b7ae625ad1904c76910eeaec5f90f58) before Biology work. The task ran in the requested Normal/Standard project context; no Lite-tier marker was present. No main-branch change or release publication was performed.

The first 16-ID fragment on this branch was superseded and deleted when the published Biology-A handoff disclosed the exact W03/W04 boundary. The authoritative partition is **not** one `_01` versus one `_02` item per microtopic. It consists of 290 eligible active authored Biology TRAIN records, defined by `A_CORE_FULL` or `B_RAPID_EXPOSURE` scope and sorted lexicographically by stable ID. W03 owns positions 1–145, from `v3_bio_01_01` through `v3_bio_08_18`; W04 owns positions 146–290, from `v3_bio_08_19` through `v3_bio_16_23`. [1]

| Boundary control | Observed value |
|---|---:|
| Eligible authored Biology TRAIN population | 290 |
| W03 deterministic positions | 1–145 |
| W04 deterministic positions | 146–290 |
| W04 reviewed stable IDs | **145** |
| W03/W04 stable-ID intersection | **0** |
| W04 changes outside assigned IDs | **0** |
| Real-exam, official-stem training, SIM/FINAL, and quarantine records altered | **0** |

> **Correction record:** The early 16-item overlay would have overlapped W03. It is absent from the final branch tree and is explicitly superseded by `biology_v620_w04_patch.json`; the final verifier rejects any overlap with W03’s first 145 IDs.

## Sources and review method

The frozen V6.1 expanded SQLite bank and gzip were retrieved through the authorized project Drive connection and verified before review. The expanded SQLite SHA-256 is `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`; the gzip SHA-256 is `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`. SQLite returned `PRAGMA quick_check = ok`.

All 145 assigned records were inspected in structured five-item batches against their declared official Biology textbook section, with a second adjudication pass for conservative excerpt-matching flags. The first pass produced 88 flags when a text extractor returned an irrelevant nearby textbook section; a second constrained adjudication resolved 77 as scientifically supportable. The remaining 11 were inspected as actual production defects rather than silently retained. Ten referenced absent A/B statements or a table that was not stored in the question payload; one contained a reversed causal chain in an immunity option. These were repaired as self-contained items while preserving their stable IDs and answer positions. [2] [3] [4]

The resulting explanations are question-specific: they name the relevant anatomical structure, molecular process, direction of transport, timing, causal relation, or inheritance rule for the keyed option and for each original distractor. Generic trap/keyword/control filler and raw internal enum labels are absent from every W04 explanatory field.

| Review result | Count |
|---|---:|
| Assigned records with four rewritten option analyses, correct analysis, and short lesson | 145 |
| Analysis-only records | 134 |
| Explicit material-completeness repairs | 11 |
| Stem repairs for missing A/B statements or tables | 10 |
| Option repairs | 5 |
| Correct-key changes | 0 |
| Unresolved scientific flags left active | 0 |
| Raw enum or generic template markers in W04 overlay | 0 |

## Explicit production-defect repairs

| Stable ID | Defect identified | Repair and rationale |
|---|---|---|
| `v3_bio_10_11` | Stem named A/B but omitted both statements | Added self-contained renal secretion and ADH statements; retained option/key position and explained blood→tubule secretion versus reduced water reabsorption with lower ADH. |
| `v3_bio_11_07` | Stem named A/B but omitted both statements | Added sodium-channel depolarization and ATP-dependent myosin detachment statements. |
| `v3_bio_11_24` | Stem depended on an absent table | Replaced the absent-reference form with four meaningful nervous-system/muscle statements; key remains option 3. |
| `v3_bio_12_07` | Stem named A/B but omitted both statements | Added anterior-pituitary FSH/LH and intracellular-receptor distinctions. |
| `v3_bio_13_15` | Keyed causal chain reversed cause and effect | Rewrote option 4 in the correct direction: specific antibody binding can form precipitating antigen–antibody networks, which make removal easier. |
| `v3_bio_14_10` | Stem named A/B but omitted both statements | Added endometrial implantation and early embryonic hCG source/body-luteum target distinction. |
| `v3_bio_14_20` | Stem depended on an absent table | Replaced the absent-reference form with four self-contained embryonic-development statements; key remains option 1. |
| `v3_bio_15_15` | Stem named A/B but omitted both statements | Added phloem source-to-sink transport and xylem-versus-sucrose distinction. |
| `v3_bio_15_24` | Stem depended on an absent table | Replaced the absent-reference form with self-contained plant transport/double-fertilization statements; key remains option 3. |
| `v3_bio_16_10` | Stem named A/B but omitted both statements | Added homologous structure/common ancestry and random genetic-drift statements. |
| `v3_bio_16_16` | Stem depended on an absent table | Replaced the absent-reference form with self-contained evolution statements; key remains option 3. |

## Files, hashes, and migration safety

| File | Purpose |
|---|---|
| `app/src/main/assets/biology_v620_w04_patch.json` | Final 145-ID W04 overlay; SHA-256 `bfb28c508ffa56ea3d0f8df7d668c666fd8bd3ffc0cbfc3faee41eaf67502aff` |
| `tests/verify_biology_v615_b.py` | Deterministic frozen-base, exact-partition, four-option, identity, raw-filler, and completeness-repair verifier |
| `reports/parallel/BIOLOGY_B_QA.md` | This report |

The final overlay preserves stable ID, answer index, source type, access pool, scope, safety attributes, holdout membership, and historical-review status for every record. The eleven material repairs change only incomplete authored question text/options while preserving identity and answer position. No Room table may be reset. Existing attempts, confidence, flags, error history, mastery, due review state, and compatible active-session IDs can remain attached to the same questions.

This is a **material-bank successor fragment**, not a release-ready replacement. The integrator must merge this W04 overlay by stable question ID with Biology-A’s reconciled W03 candidate; resolve project-wide duplicate findings using authoritative evidence; build one explicitly versioned successor SQLite/gzip pair; recompute all runtime hashes; and exercise migration on first launch, process recreation, and active-session resume. Do not replace the immutable V6.1 asset in place or apply last-commit-wins across worker deltas. [1]

## Validation observed

| Validation | Observed result |
|---|---|
| Frozen expanded SQLite SHA-256 | **PASS** — equals `d63219…673c` |
| Frozen gzip SHA-256 and gzip stream test | **PASS** — equals `b5f47…e14` |
| Frozen SQLite `PRAGMA quick_check` | **PASS** |
| W04 exact cohort derivation | **PASS** — 290 eligible; positions 146–290 yield exactly 145 IDs, from `v3_bio_08_19` to `v3_bio_16_23` |
| W04 full overlay validator | **PASS** — exact 145/145 W04 IDs, zero W03 overlap, all authored active TRAIN, valid original keys, exactly four post-patch options, and four option analyses per record |
| Completeness and causal repair gate | **PASS** — ten absent A/B-or-table dependencies and one reversed immune causal chain repaired explicitly |
| Raw enum/generic-filler gate | **PASS** — no forbidden internal labels or generic trap/keyword/control markers in overlay explanations |
| Original V6.1 static asset validator | **PASS** — exact packaged archive, 1,216 unique IDs, option/key contracts, and holdout pool isolation |
| V6.1 rescue-engine static validator | **PASS** — A15/B21/C20/Q0 and 869 mandatory learning minutes |
| Aggregate native/UX static suite in rescue overlay | **Not runnable in this worker workspace** — the slim extracted overlay lacks `sfx_select.ogg` and `focus_ambient.ogg`; this is an asset-extraction limitation, not a passed release gate |
| Kotlin compile, lint, signed APK, API-35 instrumentation, Review/Map/process-recreation flow | **Not run in this scientific worker scope**; mandatory integration/release gates remain |

## Integration notes and remaining risks

The required integration order is to take the reconciled W03 Biology candidate named in Biology-A’s report, apply this disjoint W04 overlay by stable question ID, then compose it with other validated subject work. After the combined successor bank is materialized, rerun full bank, duplicate, analysis, migration, Android compilation, instrumentation, packaged-APK inspection, and signed-release gates. The known project-wide duplicate backlog and platform-flow validation are not resolved by this scientific worker; they remain explicit Foreman responsibilities.

No historical Biology quarantine key conflict was changed. No real-exam provenance claim was added or upgraded. The changes are textbook-grounded authored-item repairs only.

## References

[1]: [Biology-A deterministic boundary and integration report](https://github.com/rynmrde/Konkor/blob/parallel/bio-a/reports/parallel/BIOLOGY_A_QA.md)

[2]: [Official Biology grade 10 textbook, supplied Drive source](https://drive.google.com/file/d/1H6V7321-jC8n3MByS4dQ1V2qDHnbrS6f/view)

[3]: [Official Biology grade 11 textbook, supplied Drive source](https://drive.google.com/file/d/1Mjyb4dvdsQj51orLsYkvJoHKJBTw7Wjl/view)

[4]: [Official Biology grade 12 textbook, supplied Drive source](https://drive.google.com/file/d/1bj2hURks0yOZSEtXJBZRHlzUh4gHBJ-l/view)
