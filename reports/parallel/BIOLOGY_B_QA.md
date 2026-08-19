# Biology-B Complementary QA Report

## Scope, baseline, and coordination

This report records the **Biology-B** complementary scientific QA pass. The task began from the current GitHub `main` reference resolved through the authorized project connection: [`72dc76e56b7ae625ad1904c76910eeaec5f90f58`](https://github.com/rynmrde/Konkor/commit/72dc76e56b7ae625ad1904c76910eeaec5f90f58). The working branch is `parallel/bio-b`; no main-branch change or release publication was performed. Lite was not reported by the task environment; the task ran under the requested Normal/Standard project context.

The complementary boundary is deterministic. Biology-A (`parallel/bank-biology`) rewrote the authored TRAIN item ending in `_01` for each of the 16 active Biology microtopics. Biology-B reviewed the next untouched authored, selected-scope TRAIN ID in priority order for each same microtopic: the `_02` layer. The two sets are disjoint by stable question ID, so this branch neither redoes Biology-A’s 16 items nor changes their evidence or source status.

| Control | Biology-A | Biology-B |
|---|---:|---:|
| Stable IDs reviewed deeply | 16 `_01` IDs | 16 `_02` IDs |
| Identity-bearing fields changed | 0 | 0 |
| Stem, options, correct index, source type, pool, scope, or holdout changes | 0 | 0 |
| Analysis-only update records | 16 | 16 |
| Stable-ID overlap | — | **0** |

The immutable source bank was downloaded from the authoritative frozen V6.1 folder and verified before inspection. Its expanded SQLite SHA-256 is `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`; its gzip SHA-256 is `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`. The database returned `PRAGMA quick_check = ok` and contains 411 Biology records: 369 authored, 24 official-stem training, 15 `real_exam`, and 3 quarantined conflicts. No real-exam claim, key, or quarantine status was edited.

## Scientific review and evidence

All sixteen reviewed records are authored, active, selected-scope TRAIN questions. Their correct keys and four original options were retained after review. The previous explanations were not accepted as student-facing because they repeated generic template language and raw internal labels such as `wrong_condition` or `partial_truth`. The replacement text names the precise biological process, anatomical site, direction, causal relation, or inheritance rule for the keyed option and each distractor. It does not expose internal labels or tell the student to rely on a keyword.

The review was grounded in the supplied official grade 10–12 Biology textbooks. For example, the revised explanations distinguish codon from anticodon, homologous chromosomes from sister chromatids, pressure-driven inspiration, phloem source-to-sink transport, plasma-cell antibody secretion, and the temporal separation in CAM plants. These distinctions are curriculum concepts represented in the official books rather than claims inferred from non-official preparatory material. [1] [2] [3]

| ID | Microtopic | Concrete corrected reasoning focus |
|---|---|---|
| `v3_bio_01_02` | Gene expression | tRNA anticodon–mRNA codon pairing; no primer for RNA polymerase; stop codon mechanism |
| `v3_bio_04_02` | Cell cycle and division | Homolog pairing in prophase I; homolog versus sister-chromatid separation |
| `v3_bio_09_02` | Animal and human respiration | Diaphragm, thoracic volume, pulmonary pressure, ventilation, and countercurrent exchange |
| `v3_bio_07_02` | Circulation, heart, and capillaries | Directional definition of pulmonary artery; coronary return; lymphatic drainage |
| `v3_bio_08_02` | Digestion and absorption | Bile emulsification versus lipase action; small-intestinal villi; lymphatic lipid uptake |
| `v3_bio_12_02` | Endocrine regulation | Thyroid hormone effects; anterior pituitary versus hypothalamus; negative feedback |
| `v3_bio_02_02` | DNA replication and mutation | 3′-OH addition and 5′→3′ synthesis; ligase role; frameshift consequences |
| `v3_bio_16_02` | Evolution and animal diversity | Homology, non-ladder evolution, inherited variation, and random genetic drift |
| `v3_bio_05_02` | Cellular respiration | Krebs-cycle location; carbon-dioxide release; oxidative phosphorylation; proton direction |
| `v3_bio_15_02` | Plant transport, growth, and reproduction | Phloem source-to-sink transport; double fertilization |
| `v3_bio_11_02` | Nervous system, senses, and muscle | Voltage-gated sodium channels; synaptic release; ATP-dependent myosin detachment |
| `v3_bio_10_02` | Excretion and osmoregulation | Filtration, reabsorption, secretion, and ADH-dependent water reabsorption |
| `v3_bio_14_02` | Reproduction and embryonic development | Morula timing, endometrial implantation, and hCG source/target distinction |
| `v3_bio_03_02` | Mendelian and sex-linked inheritance | Paternal X/Y transmission; recessive genotype; X-linked recessive inheritance; ABO alleles |
| `v3_bio_13_02` | Innate and adaptive immunity | Plasma-cell antibody secretion versus phagocytosis, inflammation, and immune memory |
| `v3_bio_06_02` | C3/C4/CAM photosynthesis | Water as the O₂ source; C4 spatial versus CAM temporal separation; thylakoid location |

> **Scientific-change boundary:** The distractors were reviewed as meaningful, conceptually distinct statements. No option text was changed because each set already supports a specific correction about process, place, direction, time, causation, or biological role. Only the explanatory text was replaced.

## Files and migration safety

| File | Change |
|---|---|
| `app/src/main/assets/biology_v615_b_patch.json` | 16 disjoint, analysis-only update records; SHA-256 `d6bec46341de0232ab2bcaa27b1ea56edf8b4c3712e94fb17f3f92807a5702be` |
| `tests/verify_biology_v615_b.py` | Deterministic base-hash, SQLite integrity, stable-ID, exact-four-options, selected-TRAIN, disjointness, filler, and raw-enum checks |
| `reports/parallel/BIOLOGY_B_QA.md` | This factual coordination and scientific QA handoff |

The Biology-B overlay does **not** alter question ID, stem, options, correct index, priority, source type, access pool, scope, holdout assignment, or any Room progress key. It is therefore migration-safe in principle: attempts, mastery, confidence, due review state, error history, and active-session references continue to use the same IDs.

This file is an **integration fragment**, not a separately installable bank release. The integrator must merge its 16 disjoint `updates` into the reconciled Biology-A `biology-v6.1.5-analysis-safety` patch, apply the combined patch transactionally to a copy of the immutable V6.1 database, recompute the combined runtime SQLite SHA-256, update the expected patched hash in `BankStore`, and run the first-launch, process-recreation, and progress-preservation release gates. The frozen gzip and expanded SQLite artifacts remain byte-identical.

## Validation observed

| Validation | Observed result |
|---|---|
| Frozen expanded SQLite SHA-256 | **PASS** — equals required `d63219…673c` |
| Frozen gzip SHA-256 and gzip stream | **PASS** — equals required `b5f47…e14` |
| SQLite `PRAGMA quick_check` | **PASS** |
| Biology-B deterministic overlay validator | **PASS** — 16 expected IDs, 0 Biology-A overlap, all authored selected TRAIN, four option analyses per item, no prohibited generic filler or raw internal-enum terms in the overlay |
| Original V6.1 asset validator | **PASS** — exact packaged archive, counts, unique IDs, four options, valid SIM pool isolation |
| V6.1 rescue-engine static validator | **PASS** — A15/B21/C20/Q0, 869 mandatory learning minutes |
| Aggregate native/UX static suite | **Not runnable from the slim rescue overlay** — it lacks packaged `sfx_select.ogg` and `focus_ambient.ogg`; this is an extracted-overlay asset limitation, not a passed release gate |
| Android compilation, APK install, instrumentation, Review/Map/process-recreation flow | **Not run in this scientific worker scope**; required at integration/release time |

The residual duplicate work remains the project-wide semantic-adjudication backlog reported by Biology-A; this pass did not relabel any candidate as a duplicate or modify session/mastery logic. The new Biology-B analysis overlay itself has no repeated ID and does not add a question, so it cannot introduce duplicate question delivery or inflate unique mastery.

## Integration notes and blockers

The expected integration order is: first apply the reconciled Biology-A patch from commit [`8ca9768c10f00676b92767d1884d01d01f2f1f83`](https://github.com/rynmrde/Konkor/commit/8ca9768c10f00676b92767d1884d01d01f2f1f83), then merge the disjoint Biology-B records by question ID, recompute the combined patched-database hash, and validate the actual Android package. Do not merge Biology-A’s superseded declassification draft. No authority resolved a historical key conflict during this task; all three Biology conflicts remain quarantined.

The only blocker for complete release validation is that this branch is intentionally a compact scientific overlay and does not contain the full Android source/assets or a signing/instrumentation environment. This is not a waiver: the integrator must execute the required Kotlin, lint, signed APK, API 35, Review, Question Map, navigation, process-recreation, progress-preservation, duplicate-free block, and final-hours behavior gates after composing the combined patch.

## References

[1]: [Official Biology grade 10 textbook, supplied Drive source](https://drive.google.com/file/d/1H6V7321-jC8n3MByS4dQ1V2qDHnbrS6f/view)

[2]: [Official Biology grade 11 textbook, supplied Drive source](https://drive.google.com/file/d/1Mjyb4dvdsQj51orLsYkvJoHKJBTw7Wjl/view)

[3]: [Official Biology grade 12 textbook, supplied Drive source](https://drive.google.com/file/d/1bj2hURks0yOZSEtXJBZRHlzUh4gHBJ-l/view)

[4]: [Biology-A reconciled QA report](https://github.com/rynmrde/Konkor/blob/parallel/bank-biology/reports/parallel/BIOLOGY_QA.md)
