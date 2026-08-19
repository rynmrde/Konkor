# Chemistry Bank and Solution-Quality QA — V6.2 Candidate

> **Worker:** W03 Chemistry Bank + Solution Quality  
> **Branch:** `parallel/bank-chemistry`  
> **Pinned baseline:** `main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
> **Worker candidate bundle commit (remote-reassembled and verified):** `b68754b96c1ab495a8ce86fc6e4d89b6d46c7c87`  
> **Release status:** No main change, release creation, tag, merge, or force-push was performed.

## Scope and Evidence

The active frozen V6.1 Chemistry database was machine-scanned directly, not inferred from filenames. It passed `PRAGMA quick_check` and contained **267 Chemistry records**: 238 authored, 22 official-exam-stem training, five quarantined key-conflict, and two real-exam records. The highest-priority selected training set contained 203 questions; its top `74.0` priority tier contained 17 stoichiometry/gas items.

The audit used the supplied official Chemistry sources. In particular, the Grade 10 Chemistry text states that one mole of gas at STP occupies **22.4 L**, which was used only for the affected STP calculation checks. The new questions are explicitly labelled as authored training, not official exam questions. Existing official-source provenance fields were preserved. [1] [2]

| Audit measure | Result |
|---|---:|
| Baseline Chemistry records machine-scanned | 267 |
| Deep-reviewed top-priority records | 17 |
| Deep-review records retained with bespoke solution rewrites | 12 |
| Cosmetic/accidental high-priority variants retired non-destructively | 5 |
| New distinct high-priority replacements | 5 |
| Additional active/holdout scan-flagged records manually repaired | 12 |
| Existing Chemistry records whose review-facing JSON changed | 267 |
| Candidate Chemistry records | 272 |
| Candidate active selected Chemistry TRAIN records | 203 |
| Candidate total bank records | 1,221 |

The all-record change count reflects systematic reconstruction of review-facing text: raw internal labels were removed from review payloads and generic template repetitions were stripped. The 24 listed deep or targeted repairs received question-specific correct-answer, distractor, short-lesson, fast-method, and review-default explanations. Five historical IDs were retained but marked obsolete, while five replacements have new identities; therefore no prior attempt, mastery, or error history is fabricated or transferred.

## Material Corrections

The priority `17` stoichiometry/gas subset contained five accidental or cosmetic repeats of already represented skills. IDs `v3_chem_17_06` through `v3_chem_17_10` are now obsolete only; replacements `v62_chem_17_06` through `v62_chem_17_10` use different calculation contexts: calcium carbonate with acid, aluminium with acid, combined gas-law change, solution molarity, and iron(III) oxide reduction. All have full unit-bearing solution paths and distinct scenario IDs.

The retained deep-review items were recalculated or re-reasoned from the displayed conditions. Their explanations now show the shortest valid formula path, units, assumptions, and why each distractor fails. Corrections cover stoichiometric ratios, limiting reagent, gas volume at STP, percent yield, purity, multi-stage mass-volume conversion, and lattice-energy ranking. Three official-exam-stem training records at lower priority were also expanded from terse answers into actual molecular-formula, calorific-value/purity, and redox-ordering solutions. Two existing simulation-pool questions had solution explanations strengthened only; their IDs, keys, access pools, and safety eligibility did not change.

The scan initially reported five groups with identical generic stem/options. A stimulus-aware inspection showed that they have different embedded data tables or paired statements and unique semantic fingerprints; they are therefore not duplicates when rendered in the application and remain active. No exact duplicate remains among active selected Chemistry training questions when the full stimulus, stem, and options are considered.

## Candidate Asset and Migration Contract

| Artifact | SHA-256 |
|---|---|
| Frozen V6.1 expanded bank (baseline) | `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c` |
| Candidate V6.2 expanded bank | `ed84693259455e6da488af23a7fa39c6548ea64e95bee6a93ba5cedf8f7656c6` |
| Candidate V6.2 gzip asset | `47ba0670e5c3b22e5823dfb577ade40267f530fd40f7d4a2b8c8119b9f67cbce` |
| V6.2 Chemistry overlay archive | `1e47e59d162b25407eeafd08cb2d251a385c84e4a60b56fb16186ac5004f9502` |

The candidate is delivered as a second immutable asset, `radiology1405_bank_v6_2.db.gz`, and a `BankStore.kt` override that opens a new verified `radiology1405_bank_v6_2.db` cache. The archive does **not** remove the V6.1 asset. The Room progress database remains separate and unchanged; no destructive migration is added. Retired IDs preserve historic attempts and the five new IDs receive no inherited mastery or attempt records.

## Tests Performed

| Gate | Result | Evidence |
|---|---|---|
| Frozen V6.1 Chemistry SQLite quick check | PASS | `ok` |
| Candidate SQLite integrity check | PASS | `ok` |
| Candidate gzip expands byte-for-byte to candidate DB | PASS | SHA-256 equality |
| Candidate IDs unique | PASS | 1,221 rows / 1,221 IDs |
| Chemistry count and active selected TRAIN count | PASS | 272 / 203 |
| Four valid options, valid key, and four option analyses | PASS | zero violations |
| Raw review enums and known generic-template markers | PASS | zero violations |
| Declared calculation paths contain formula/unit evidence | PASS | zero violations |
| Exact active TRAIN duplicate check including stimulus | PASS | zero groups |
| Retired→replacement mapping | PASS | five valid pairs; old obsolete, new active TRAIN |
| Unchanged IDs retain their answer key | PASS | zero key changes |
| Overlay static integration: V6.1 retained, V6.2 hash/loader, separate progress DB, no destructive migration | PASS | six checks |
| Remote branch overlay reconstruction | PASS | eight uploaded segments reassembled to SHA-256 `1e47e59d162b25407eeafd08cb2d251a385c84e4a60b56fb16186ac5004f9502`; archive contains required asset and loader |

The disposable frozen-project copy did not include a `gradlew` wrapper and no system Gradle executable was present. Therefore Kotlin compilation, JVM tests, lint, APK asset inspection, Android installation, and runtime persistence verification were **not run in this worker environment**. This is a release-authority gate, not a pass claim.

## Integration Instructions

The foreman must first run `bash radiology_v620_chemistry_patch/reassemble_overlay.sh`; it reconstructs and verifies `overlay.tar.xz` with SHA-256 `1e47e59d162b25407eeafd08cb2d251a385c84e4a60b56fb16186ac5004f9502`. The foreman must then apply `radiology_v620_chemistry_patch/overlay.tar.xz` **after** the existing V6.1.4 rescue overlay. Preserve the archived V6.1 asset and all V6.1 source-hash evidence. Update the release workflow and its static validators deliberately for the new V6.2 database/gzip names, SHA-256 values, and counts (`1,221` total; `1,117` authored; 17 real; 71 provisional; 16 quarantined). The AAPT packaging inspection must expect `assets/radiology1405_bank_v6_2.db`, while legacy V6.1 archival checks remain explicit rather than being deleted.

Before integration or release, the foreman must run the full required matrix: static/bank validation, Kotlin compile, JVM tests, lint, debug/release asset inspection, signing, Android API 35 instrumentation, install/launch, Review and Question Map flows, process recreation, progress preservation, duplicate-free session behavior, and SIM holdout checks. The provided candidate must be rejected or corrected if any required gate fails.

## Remaining Risks

The versioned loader creates a fresh local **bank cache** because the bank checksum changes. This does not destroy Room progress, but runtime testing must prove that historic records containing now-retired question IDs still render safely in Review and that backup/restore accepts both bank identities according to the existing compatibility policy. The new asset is deliberately a candidate until the designated integrator performs the release build and device gates.

## References

[1]: https://drive.google.com/file/d/1rmRyR509x-8bDAS0FG6WiP9R5DtXjfXH/view "Official supplied Chemistry 1 / Grade 10 textbook"
[2]: https://github.com/rynmrde/Konkor/blob/72dc76e56b7ae625ad1904c76910eeaec5f90f58/.github/workflows/radiology-v614-rescue.yml "Pinned active V6.1.4 rescue workflow"
