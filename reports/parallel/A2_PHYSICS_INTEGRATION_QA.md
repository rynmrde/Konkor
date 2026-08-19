# A2 Helper — Physics Integration QA

| Field | Value |
|---|---|
| Helper role | A2 post-completion Physics integration and validation support |
| Helper branch | `parallel/help-a2-m3-physics-integration-qa` |
| Physics owner branch reviewed | `parallel/a2-physics` at `5ca5cf6c73762aa63b1d41558643fd122e3938f2` |
| Evidence reviewed | `reports/parallel/A2_PHYSICS_QA.md` and `radiology_v614_rescue_patch/MANIFEST.txt` on the owner branch |
| Branches modified by this helper | None; this report is the only helper deliverable |

## Independent finding

**PHYSICS_INTEGRATION_BASELINE_MISMATCH = FAIL until reconciled by the Foreman.** The Physics owner report correctly presents its work as a full-source overlay rather than a main-branch integration. However, its published `radiology_v614_rescue_patch/MANIFEST.txt` identifies the base release/tag as `radiology1405-apk-v6.1.3-20260813` and labels the archive a V6.1.4 rescue overlay. The authoritative project target is the V6.1.4 release asset `radiology1405_android_project_v6.1.4.zip`. The numeric package version is still `6.1.4 (165)`, but the source-release provenance must be reconciled before applying the Physics overlay to any V6.1.4 candidate.

> A source overlay may not be merged merely because its runtime package version agrees. The exact source archive and rescue-overlay ancestry must be demonstrated, or the change must be replayed/rebased on the approved V6.1.4 full-source integration workspace.

## Positive findings

The owner report supplies useful evidence-backed Physics QA: it identifies 187 active Physics records, retains the four-option/key/pool/ID contracts, expands six short calculation analyses and 18 high-ROI authored analyses, and adds session-local follow-up exclusion. It also addresses raw learner-facing taxonomy leakage with a shared renderer and introduces canonical comparison-stimulus handling for three Physics records. Those corrections are compatible in intent with the A2 full-product Review work.

| Contract | Integration instruction |
|---|---|
| Shared Review UI | Do not take the Physics comparison-only renderer over the A2 schema-generic renderer. Retain the A2 `stimulusJson` parser and its shared Test/Review adapters, which already render the three Physics comparisons plus all other supported structured types. |
| Learner-facing raw tokens | Preserve the Physics shared sanitization mapping and merge it with A2’s Persian mappings for `questionForm` and `teachingLevel`; neither mapping should expose internal source tokens. |
| Session selection | Retain the Physics follow-up exclusion and zero-leak TRAIN assertions. A2’s map must reflect selected persisted IDs, not change the selection policy. |
| Room/session schema | Preserve the existing active-session fields. A2 derives map states from the durable ordered IDs, answers, flags, and navigation positions; no destructive schema reset is acceptable. |
| Bank assets | The Physics explanation-only bank revision has different bank hashes by design. The Foreman must package exactly the Physics revised bank with matching bank verification constants; the A2 overlay does not ship or alter any bank artifact. |

## Required reconciled validation sequence

The Foreman should reconstruct a clean V6.1.4 full-source workspace, apply the current rescue overlay, then replay/rebase the Physics change set and the A2 full-product Review/Map overlay in one integration workspace. A diff must confirm that the A2 schema-generic `visibleStructuredStimulus` path remains the only Test/Review structured-premise presenter and that the Physics comparison records still resolve through it.

| Gate | Minimum passing observation |
|---|---|
| Provenance | Exact V6.1.4 source-archive SHA and applied overlay SHA recorded; V6.1.3 manifest mismatch resolved or replacement overlay generated. |
| Bank integrity | Revised Physics gzip/SQLite hashes match the Physics workflow/runtime constants; all IDs, options, keys, pools, SIM disjointness, and quarantines validate. |
| Presentation | Physics comparison IDs `v3_phys_30_02`, `v3_phys_33_02`, and `v3_phys_34_03` show canonical A/B content before options in Test and Review, including reopen/resume. |
| Selection | Follow-up pair test, normal TRAIN zero-leak test, and unique-mastery accounting pass against the integrated bank. |
| Android gates | Kotlin compile, JVM tests, lint, debug APK, packaged-bank inspection, signed build, API 35 instrumentation, and real process-recreation/resume are observed on the integrated candidate. |

No Physics bank text, key, metadata, release, or owner-branch file was changed by this helper. This report is a coordination guard intended to prevent an unsafe source-overlay ancestry assumption during final integration.
