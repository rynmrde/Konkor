# Konkor Foreman Preflight

> **Phase:** A — preflight only. **Foreman role:** FINAL INTEGRATOR / RELEASE OWNER. **Account tier:** Normal/Standard. **Integration and release status:** prohibited until the exact `GO_INTEGRATE` instruction is received.

## Scope, Source of Truth, and Baseline

This report records a preflight rather than a release decision. The repository baseline was pinned through the existing project GitHub route at `72dc76e56b7ae625ad1904c76910eeaec5f90f58` on `main`; the verified historical release was `radiology1405-apk-v6.1.4-20260817`, published on 2026-08-17. The latest successful historical workflow observed for that baseline was run `32031100891`. These facts establish the starting point only and do **not** prove a future release.

| Baseline item | Recorded value | Preflight disposition |
|---|---|---|
| Default branch | `main` | Pinned at `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Historical release | `radiology1405-apk-v6.1.4-20260817` | Historical evidence only; never overwrite |
| Historical app version | `6.1.4` / versionCode `165` | Must not be silently downgraded |
| Historical successful workflow | `32031100891` | Historical evidence only; new work requires new outputs |
| Historical releases | 8 existing releases | The lite claim that GitHub had zero releases is **REJECTED as false** |
| Frozen source gzip SHA-256 | `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14` | Immutable reference |
| Frozen expanded SQLite SHA-256 | `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c` | Immutable reference |
| Frozen verified JSON SHA-256 | `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d` | Immutable reference |
| Historical base project ZIP SHA-256 | `1344aca90474ac96e27e94ba754ebafd42778e2ceaab91f9a5fb1be2e882d046` | Required materialization checksum |

The `main` repository tree is a bootstrap/workflow wrapper that carries the V6.1.4 rescue overlay rather than a directly merge-ready full application tree. The authoritative Phase A integration baseline must therefore be materialized from release asset `radiology1405_android_project_v6.1.4.zip`, verified against the recorded source-ZIP checksum, and then overlaid with the immutable V6.1.4 rescue overlay. No worker overlay is eligible for blind extraction into `main`.

## Connector and Materialization State

The configured project Composio connection was proven usable earlier in this preflight through a minimal read-only repository metadata request. Its task enablement subsequently reverted/was interrupted while attempting to save the existing connector activation. Consequently, this report is a **local working copy** pending publication to `parallel/foreman-preflight`; no standalone GitHub or Drive route was requested or used. Publication, live branch refresh, and release-asset materialization remain blocked until the existing project connection is active.

| Item | Current evidence | Status |
|---|---|---|
| Existing project Composio connection | Existing connector identified; enablement repeatedly interrupted before persistence | **BLOCKED** |
| Read-only GitHub access proof | Repository metadata returned for `rynmrde/Konkor` while connection was active | PASS, historical session evidence |
| V6.1.4 release source ZIP | Asset name identified; full asset not yet materialized in this sandbox | **BLOCKED** |
| V6.1.4 rescue overlay | Retrieved as immutable repository content; recorded workflow SHA `d17bdd905def35a45caa32aa5a0b07b6196ecc78de493a340bf36fac0c0103c3` | PASS, source layout still requires release ZIP |
| Full V6.1.4 integration baseline | Cannot yet be reconstructed and inspected locally | **BLOCKED** |

## Recovered A3 Persistence Candidate

The recovered A3 attachment is an XZ-compressed tar overlay with SHA-256 `42e691c266b97153176a3152c90ec13cf3d43a9e05bb7ae81e2059b52f91d706`, matching its supplied manifest. Its archive names were inspected for links before copying only declared source files for read-only review. It is an **app-only candidate**, not a release or an acceptance certificate.

| A3 assertion inspected | Directly observed in candidate | Disposition |
|---|---|---|
| Room migrations | Schema version `3`, explicit `MIGRATION_1_2` and `MIGRATION_2_3`, no destructive fallback string | Candidate evidence only; must run migration fixture on full baseline |
| Review map reconstruction | `attemptsForSession`, `reviewQuestionStates`, and session-scoped `currentOutcome` exist | Candidate evidence only; requires process recreation and Review reopening test |
| Persistent map UI | `FlowRow` map rendering exists | Candidate evidence only; needs all states, direct jump, accessibility, 90–140% scale, and API-35 confirmation |
| Backup/restore | Pre-restore snapshot logic and persisted review-map refresh paths exist | Candidate evidence only; needs actual restore and compatibility test |
| Unique mastery | Candidate test checks a repeated question does not inflate unique mastery | Candidate evidence only; must compose with A2 selection change |
| Atomic finish review | `finishReview` itself only mutates session phase; atomic composition with required outcome/map state is not proven | **FIX REQUIRED** |

The A3 candidate replaces `StudyRepository.kt`. The A2 duplicate-selection candidate also replaces `StudyRepository.kt` and `AdaptiveEngine.kt`. Neither overlay may be untarred over the other. A future integrator must three-way merge A2 no-repeat/evidence-family/adaptive-short-block behavior with A3 persisted review-map behavior and then rerun both static guards, migration tests, package-bank tests, JVM tests, lint, and API-35 instrumentation.

## Release-Blocking Findings

The following conditions are not waived by a worker report, a static scan, or historical artifacts.

| Blocker | Evidence state | Required disposition before integration/release |
|---|---|---|
| 21 active TRAIN paired-statement items lack visible A/B claims | Authoritative second-pass evidence states all 21 are authored and the exact claims exist in immutable `stimulus.left/right` | Implement canonical stimulus rendering in Test and Review; prove all 21 render, persist, resume, restore, map, and review correctly; preserve IDs/progress/bank bytes |
| A2/A3 persistence composition | Both candidates replace `StudyRepository.kt` | Deliberate three-way merge, atomic `finishReview` outcome/state handling if necessary, all A2/A3 regression and runtime tests |
| Full standalone Review requirement | Existing module is standalone and baseline host wiring was not proven | Show full stem/stimulus/figure/options/user answer/key/outcome/confidence/reasoning/distractor context in an actual session |
| Text scale | User-facing 90–140% behavior not evidenced end-to-end | API-35 UI verification at minimum, default, and maximum scale |
| Dynamic C-unlock | Missing live dynamic evidence | Demonstrate measured progress/ROI-based unlock behavior with actual Room fixtures; no quota substitute |
| Paired-statement render source | Existing generic renderer may omit canonical stimulus | All-21 exact source-to-visible-stem regression gate and post-submit Review gate |
| Physics analysis and duplicates | First pass finds 168 raw-enum displays, six short analyses, comparison stimuli, and two same-scenario pairs | Standard worker patch plus independent review; verify raw-enum elimination and safe distinct-session behavior |
| Biology patch collision | `v3_bio_09_01` through `v3_bio_16_01` conflict across candidate patches | Evidence-backed reconciliation, stable-ID decision and migration/progress analysis |
| Biology vague items | `v3_bio_12_08`, `v3_bio_15_11`, `v3_bio_16_13` remain flagged | Textbook-grounded repair or explicit safe exclusion with tests |
| Geology malformed record | `real_1401_in_geo_153` has malformed displayed options | Reconstruct only from authoritative source or keep quarantined/excluded; never silently rewrite frozen record |
| Quantitative analysis quality | Five exact active-TRAIN duplicate groups, five numeric-variant groups, 29 identical correct-analysis groups, and 40 calculation-required records lacking strict equation/numeric/unit evidence | Review-required candidates, not automatic defects; exact ID disposition, explanation-quality remediation or safe selection exclusion required |
| Real-exam provenance | 17 active records remain verified and 16 conflict records remain quarantined, but provenance must stay independently defensible | Retain source-year/session/question/booklet/page/key evidence; do not overstate verification or resolve conflicts without primary evidence |
| Packaged-bank validity | Historical package checks do not validate any future build | Re-run bank/schema/ID/key/holdout/SIM/duplicate validators against debug and signed release APKs |

## Branch and Report Matrix

The matrix below records a preflight disposition, not an integration order. `ACCEPT AS EVIDENCE` means only that the report is usable as an input; it does **not** accept code or a bank mutation. `PENDING` requires current-branch re-read, source/diff verification, and listed gates after `GO_INTEGRATE`. `REJECT FOR INTEGRATION` prohibits merging the branch as-is.

| Branch or evidence ref | Preflight disposition | Evidence summary and conditions |
|---|---|---|
| `parallel/a1-biology-geology` | PENDING | Renderer/test changes are potentially useful; bank findings include 107 near-duplicate candidates and malformed `real_1401_in_geo_153`. Do not mutate bank without primary source and versioned migration. |
| `parallel/a1-chemistry` | PENDING | App-level raw-enum localization and same-block signature guard are candidates; full Kotlin/API-35 gates were not completed locally. |
| `parallel/a1-official-real-exam` | ACCEPT AS EVIDENCE | Retains 17 verified active `real_exam` and 16 quarantined conflicts. Provenance caveat remains mandatory. |
| `parallel/a2-math-duplicates` | PENDING | No-repeat/evidence-family/short-block candidate conflicts with A3 repository change; needs combined composition and all-21 stimulus policy coverage. |
| `parallel/a2-review-question-map` | REJECT FOR INTEGRATION | Standalone `com.example` module was developed against a scaffold, not demonstrated host wiring. Concepts may be ported only after full baseline materialization. |
| `parallel/a2-physics` at `04b571947ab0c8c40b5025b121f8442a3e5911f2` | PENDING — SECOND PASS | Report-only audit of 187 records; raw enum, short-analysis, comparison-stimulus, and same-scenario findings require standard-worker remediation and independent review. |
| `parallel/a3-final-hours` | PENDING | New V6.1.5 overlay proposes scheduler/Room changes. Must reconcile version/schema/migration and dynamic C-unlock requirements. |
| Recovered A3 persistence overlay | PENDING — FIX REQUIRED | Manifest SHA matches. Must combine deliberately with A2 and prove atomic review finish, migration, resume, backup/restore, and all map states. |
| `parallel/bank-biology` | PENDING | Material bank/data candidate; requires evidence, stable IDs/mapping, migration and progress preservation. |
| `parallel/bank-chemistry` | PENDING | Material V6.2 candidate and retirement mapping; requires new asset/database identity, independent audit, and no fabricated mastery transfer. |
| `parallel/bio-a` | PENDING | Report/script evidence only; conflicts with Biology patch IDs require reconciliation. |
| `parallel/bio-b` | PENDING | Candidate Biology patch conflicts with other `_01` records; reconcile before acceptance. |
| `parallel/help-a1-m2-chemistry` | ACCEPT AS EVIDENCE | Support report only. |
| `parallel/help-a1-m3-math-duplicates` | PENDING | No-op at last observed head; no report. |
| `parallel/help-a1-m3-physics-fallback` | PENDING — NOT YET OBSERVED | Required fallback evidence branch must publish before Physics disposition can advance. |
| `parallel/help-a1-m4-final-hours-audit` | ACCEPT AS EVIDENCE | Audit input only; Final-Hours implementation remains pending. |
| `parallel/help-a2-m3-android-build-bootstrap` | PENDING | Build bootstrap changes require direct diff, source-integrity and reproducibility review. |
| `parallel/help-a2-visible-stem-qa` | ACCEPT AS EVIDENCE | Key all-21 visible-stem input; requires canonical implementation evidence. |
| `parallel/help-a3-persistence-validation` | ACCEPT AS EVIDENCE | Validation helper only; recovered overlay remains independently pending. |
| `parallel/help-a3-question-map-persistence` | PENDING | Depends on A3 Final-Hours overlay; requires exact predecessor SHA and deliberate merge. |
| `parallel/help-bank-chemistry-bank-biology` | ACCEPT AS EVIDENCE | Scan/report input only. |
| `parallel/help-chemistry-validation-w02` | ACCEPT AS EVIDENCE | Validation input only. |
| `parallel/help-duplicates-bio-a` | ACCEPT AS EVIDENCE | Candidate/group evidence only, not true-duplicate assertion. |
| `parallel/help-lite-a1-l2-analysis-patch-validator` | PENDING | Validator without a stable report at observed head. |
| `parallel/help-real-exam-bio-b` | ACCEPT AS EVIDENCE | Source-audit input only. |
| `parallel/help-real-exam-source-audit-bank-biology` | ACCEPT AS EVIDENCE | Source-audit input only. |
| `parallel/lite-a1-bio-geo-lint` | ACCEPT AS EVIDENCE | Lint findings only. |
| `parallel/lite-a1-official-support` | ACCEPT AS EVIDENCE | Official-source support only. |
| `parallel/lite-a3-room-migration-scan` | ACCEPT AS EVIDENCE | Migration-scan input only; no release gate waiver. |
| `parallel/real-exam-1402-1404` | ACCEPT AS EVIDENCE | Historical pattern/source evidence only. |
| `parallel/real-exam-source-audit` | ACCEPT AS EVIDENCE | Source-audit input only. |
| `parallel/help-lite-a1-independent-review-20260819` at `9dd1afe8e29a5559fdc45779af969198b0595f8f` | PENDING | Independent report must be re-read at commit; its 21 paired-statement blocker remains open until canonical rendering tests land. |
| `parallel/help-independent-quant-gates` at `8e29c59efc5caf94ed3f240e64d4480d5dab1e15` | PENDING | Structural/key/4-option claims are evidence; numeric/duplicate/analysis findings are review candidates requiring exact dispositions. |
| Official second-pass evidence at `72b21461fc357ee8600c71074db5bf5786735a91` | ACCEPT AS EVIDENCE | Supports app-layer canonical stimulus rendering and confirms all 21 are authored; does not itself implement or test the fix. |
| Independent Bio/Geo evidence at `55c19556fe8429548d1d7ae60939a61510bfa49e` | PENDING | Conflicting Biology IDs, vagueness, and Geo153 findings require reconciliation and primary evidence. |

## Anticipated Integration Order

The following order is only a conflict-resolution plan for Phase B. It is not authorization to apply changes.

1. Re-fetch `main`, releases, workflow runs, and all completed branches after `GO_INTEGRATE`.
2. Materialize and checksum the full V6.1.4 release source ZIP, apply and checksum the immutable V6.1.4 rescue overlay, and run baseline static/bank/build checks.
3. Reconcile the actual target package, version, signing configuration, Room schema, and canonical source layout before accepting any scaffold-oriented module.
4. Resolve the full-source/review/stimulus-rendering implementation first, including all-21 visible Claim A/Claim B tests.
5. Deliberately three-way merge A2 selection/unique-mastery and A3 persistence/review-map changes; implement atomic finish-review behavior if outcome, active session, and map state are otherwise non-atomic.
6. Reconcile Final-Hours scheduler with the composed persistence/selection layer, including live dynamic C-unlock and SIM decision logic.
7. Resolve only evidence-backed scientific/bank changes with explicit stable-ID or retirement/migration behavior. Preserve frozen V6.1 artifacts.
8. Apply Physics second-pass remediation and independent confirmation, then run full analysis-quality and raw-enum scans.
9. Execute the final gate sequence below. Any required failure blocks release.

## Required Final Gate Sequence

| Order | Gate | Evidence required |
|---|---|---|
| 1 | Fresh baseline | Latest `main` SHA, release inventory, branch heads, workflow status, V6.1.4 source ZIP checksum |
| 2 | Materialization | Full source ZIP checksum, V6.1.4 overlay checksum, exact source layout inventory |
| 3 | Bank static validation | Schema, IDs, four options, keys, source metadata, quarantine/obsolete, SIM disjointness, holdouts, exact/near duplicates |
| 4 | Scientific/content validation | All 21 stimulus rendering; Biology collision/vagueness and Geo153 disposition; Physics and quantitative analysis quality; raw-enum/generic-filler scans |
| 5 | Migration/progress | Explicit migrations, legacy fixture, Room progress, mastery, active session, Day Selector, backup/restore and incompatible-bank behavior |
| 6 | Selector/mastery | Normal-block no duplicate ID/evidence family, adaptive short blocks, intentional spaced repeat distinction, unique mastery preservation |
| 7 | Final-Hours | Tehran time, midnight, phases, ROI, live dynamic C unlock, SIM1/SIM2 decision and sleep/logistics rules |
| 8 | Static/build | Kotlin compile, JVM tests, lint, debug APK, packaged-bank inspection |
| 9 | Release/signing | Signed release APK, `apksigner`, package/version, signed APK bank/hash inspection |
| 10 | API-35 runtime | Instrumentation, signed install/launch, answer/navigation/flag/submit/review, Review completeness, map states/jump/persistence, process recreation, session resume, migration/progress preservation |
| 11 | Release documents | New tag/release only after PASS: APK/source hashes, bank hash, test summary, changelog, bank/duplicate/analysis audits, Final-Hours plan, migration report |

## Phase A Completion Condition

Phase A is complete only when this report is published unchanged or superseded at `reports/parallel/FOREMAN_PREFLIGHT.md` on `parallel/foreman-preflight`, the existing project connection enables a fresh GitHub verification, the V6.1.4 release source is materialized and inspected, every currently published worker/report is refreshed, and all blockers above have an explicit accept/reject/pending state. Phase A does not integrate, merge `main`, tag, sign, or publish.

## References

[1]: https://github.com/rynmrde/Konkor/commit/72dc76e56b7ae625ad1904c76910eeaec5f90f58 "Pinned historical baseline commit"
[2]: https://github.com/rynmrde/Konkor/releases/tag/radiology1405-apk-v6.1.4-20260817 "Historical V6.1.4 release"
[3]: https://github.com/rynmrde/Konkor/actions/runs/32031100891 "Historical successful workflow"
[4]: https://github.com/rynmrde/Konkor/tree/parallel/a2-math-duplicates "A2 duplicate-selection candidate"
[5]: https://github.com/rynmrde/Konkor/tree/parallel/a2-physics "Physics first-pass candidate"
[6]: https://github.com/rynmrde/Konkor/tree/parallel/help-independent-quant-gates "Independent quantitative gates"
[7]: https://github.com/rynmrde/Konkor/tree/parallel/help-lite-a1-independent-review-20260819 "Independent review evidence"

## Source-Baseline Reconciliation Addendum

A fresh connected-GitHub inventory at 2026-08-19T14:25Z confirmed eight releases and showed that historical release `radiology1405-apk-v6.1.4-20260817` targets `72dc76e56b7ae625ad1904c76910eeaec5f90f58`. Its public source asset `radiology1405_android_project_v6.1.4.zip` has SHA-256 `b242c94b3af76b5bb76043699d281555d72092b8416b1be77be3b8d31ec4ab8e`; the downloaded file matched its release-side `.sha256` file exactly. That value does **not** match the mandated historical frozen-project SHA-256 and cannot serve as the immutable integration baseline.

The authoritative Drive folder `1R2IovFE_e0O_vU4IBCSiJpqrwK4LecxK` contains `radiology1405_android_v6_1_project.zip` (file ID `14RbsAhiS1Cj3Y_JgPfR0pf1rmeXgxJUc`, Drive MD5 `625cb4477fb4d27c99eb3a11760b13bf`). A connected Drive download was ZIP-tested successfully and produced SHA-256 `1344aca90474ac96e27e94ba754ebafd42778e2ceaab91f9a5fb1be2e882d046`, matching the mandated frozen-project reference exactly. The disposable dry-composition baseline must use this Drive artifact, not the divergent release source asset.

| Source candidate | SHA-256 | Disposition |
|---|---|---|
| GitHub V6.1.4 release source asset | `b242c94b3af76b5bb76043699d281555d72092b8416b1be77be3b8d31ec4ab8e` | Historical release asset retained; **REJECTED as frozen dry-composition baseline** due mismatch |
| Authoritative Drive V6.1 project ZIP | `1344aca90474ac96e27e94ba754ebafd42778e2ceaab91f9a5fb1be2e882d046` | **ACCEPTED as immutable disposable baseline** |

[8]: https://github.com/rynmrde/Konkor/releases/tag/radiology1405-apk-v6.1.4-20260817 "Historical release asset inventory"
[9]: https://drive.google.com/file/d/14RbsAhiS1Cj3Y_JgPfR0pf1rmeXgxJUc/view?usp=drivesdk "Authoritative frozen V6.1 project archive"

## Physics Second-Pass Material-Bank Review Addendum

The live Physics branch was refreshed at commit `5ca5cf6c73762aa63b1d41558643fd122e3938f2`. Its report and compact overlay manifest claim a revised gzip bank SHA-256 of `ca4f3c63a88bf091d3ce464254048629f939a0f60b8b088e53ccd7bf206ffe2a`, expanded SQLite SHA-256 of `d6d93c2786b5900100bc348b06e740a47a94f1fb89932372a8a5ac0b68a13a5e`, and compact overlay SHA-256 of `25238d05278b94fcd8021515d7ee7ee53ac278c5e8d91fcab0ca24d20de0d0a5`. The overlay hash was independently reproduced. The archived frozen hashes remain `b5f47e…fe14` (gzip) and `d63219…63` (SQLite); they are retained as immutable historical references.

The compact Physics overlay contains **no regenerated `.db.gz` asset**. It instead ships a deterministic local rewrite script, `tools/apply_physics_second_pass.py`, which modifies only the `full_json` payloads of 18 named authored Physics IDs (`v3_phys_27_01`, `29_01`, `30_01`, `30_02`, `30_04`, `30_06`, `30_08`, `30_10`, `33_01`, `33_02`, `33_05`, `28_01`, `28_02`, `31_01`, `35_01`, `35_05`, `32_01`, and `34_03`). Its inspected behavior is local: decompress frozen asset to a temporary SQLite file, update learner-facing analysis/review fields, run `VACUUM` and `PRAGMA quick_check`, recompress deterministically, and assert the two claimed output hashes. It does not contain networking or subprocess calls. The accompanying validator reads the asset and source only.

> **Disposition: PENDING — MATERIAL BANK CHANGE.** The code and report plausibly support an explanation-only mutation, but it is not accepted until a disposable rebuild independently reproduces both hashes and a row-level audit proves: stable IDs, options, correct indices, pool/access fields, source metadata, SIM membership, quarantine, schema, and identity-bearing progress contracts are unchanged; only the stated learner-facing payload fields of the 18 audited authored records differ. A source-only renderer alternative has not yet been proved equivalent for these substantive content revisions. If the mutation remains necessary, integration must use a new audited bank/minor version with migration/progress and packaged-bank gates; old frozen artifacts must not be replaced.

## Dry-Composition Findings (Initial Candidate Set)

The authoritative Drive V6.1 project was unpacked and the historical V6.1.4 rescue overlay (`d17bdd…103c3`) was safely applied in a disposable workspace. The Chemistry candidate overlay hash matched `8f3ac3751a92534c7767afce31d36f880b1c0aaabac68e15bbe6be396c9609d2`; the duplicate second-pass overlay hash matched `64bfc1f47ac71462821be4e4d009e053c729619787d2db529d119237ec42e36c`. Archive path/link checks found no symlink or traversal issue in the inspected candidate layers.

A three-way dry merge was intentionally left unresolved. Both Chemistry and duplicate modify `BankStore.kt`, `Models.kt`, and `StudyRepository.kt`; Final-Hours also modifies `StudyRepository.kt` and `RadiologyApp.kt. The merge produced unresolved conflict markers in `BankStore.kt` and `StudyRepository.kt`; the Final-Hours UI file auto-merged structurally but remains unaccepted pending the dedicated UI second-pass review. The Geo153 exclusion patch dry-applies to a clean V6.1.4 rescue base but overlaps both selection/repository surfaces and therefore must be rebased after the final selection composition.

Static baseline evidence: bank gzip SHA matched `b5f47e…fe14`; `tests/validate_v6_1.py`, `tests/verify_asset_v6_1.py`, and `tests/verify_rescue_v614.py` passed against the verified rescue base. `verify_native_experience_v61.py` failed in this dry workspace because the applied historical rescue overlay does not include `res/raw` audio assets while that validator expects them. This is a **baseline packaging/overlay-composition discrepancy**, not a pass; release gates must rerun it against the final actual assembled source.

[10]: https://github.com/rynmrde/Konkor/blob/5ca5cf6c73762aa63b1d41558643fd122e3938f2/reports/parallel/A2_PHYSICS_QA.md "Physics second-pass report"
[11]: https://github.com/rynmrde/Konkor/tree/5ca5cf6c73762aa63b1d41558643fd122e3938f2 "Physics second-pass source and compact overlay"

### Physics reproducibility result

The inspected rewrite was executed **only in the disposable workspace** against the verified frozen bank. It did enumerate the asserted 18 IDs, and the read-only Physics validator passed its targeted qualitative checks on the resulting bank. However, the required reproducibility assertion failed: actual rebuilt expanded SQLite hash was `52bf1b4ab3f39909ee2344acf9de6201d1176c6c9461f18d479cfcf89536e2c7` and actual gzip hash was `8070e76b3e519224da195fc6fae7f1f06060f92db96325ac8f080c05d3976286`, not the branch-claimed `d6d93c…3a5e` / `ca4f3c…fe2a`. The rebuild script therefore terminated non-zero at its own hash assertion. The ordinary frozen-bank validator also failed afterward, as expected, because the app’s pins still name the frozen bank.

> **Physics disposition remains PENDING / NOT ACCEPTED.** The candidate may contain valuable source/UI/selection work, but its material bank artifact is currently non-reproducible from the verified baseline under the shipped deterministic tool. It must supply a corrected deterministic rebuild or a verifiable revised bank artifact plus exact row-level audit and new-version/migration plan. It cannot enter the release composition as a material bank change in its present form.

## Superseding Live-Connection and Current-Head Addendum

The earlier connector-blocked wording is superseded. The existing project connection was subsequently used for fresh read-only GitHub and Drive verification, immutable Drive-baseline materialization, release/branch refreshes, and the local disposable checks recorded above. No standalone GitHub or Drive connection was requested. The authoritative Drive project ZIP, not the divergent public GitHub release source ZIP, is the accepted immutable dry-composition baseline.

| Current workstream | Exact observed head or artifact | Phase A disposition | Mandatory condition before Phase B integration |
|---|---|---|---|
| Official/source evidence | `72b21461fc357ee8600c71074db5bf5786735a91` | **ACCEPT AS EVIDENCE** | Keep the 17 verified active real-exam records and 16 quarantined conflicts; use canonical immutable `stimulus.left/right` rather than bank-rewriting the all-21 paired claims. |
| Chemistry second pass | `parallel/a1-chemistry` `4e9a2f2c90ae7cc1e0ee093f341083e3d4295cd7`; overlay `8f3ac375…609d2` | **ACCEPT-CANDIDATE** | Independent Chemistry review supports source/data gates and reports 35 identical-analysis groups covering 77 records, not the earlier unconfirmed 29 groups. Must pass composed build/runtime gates. |
| Duplicate/session second pass | `b717f4c96209954e0e6f596ed015a85c2e6dfc6d`; overlay `64bfc1…e36c` | **PENDING COMPOSITION** | Resolve `BankStore.kt`, `Models.kt`, `StudyRepository.kt`, `AdaptiveEngine.kt`, and tests with Final-Hours/A3 rather than last-overlay-wins. |
| Final-Hours corrected candidate | `ee706e9836bd499decae0a1d79ea643884ab4d1c` | **PENDING COMPOSITION** | Preserve actual-now/time-zone/ROI/SIM behavior and merge shared repository/UI layers with A3 and the eventual build-effective UI solution. |
| Persistence second pass | final report `b78daecaa26ccc5c2a397cf71b043baae10fc9d6`; overlay `d012e645ea10eb3302442c9ad8e83312b05dc915332b7a1ae42f0a41b7cc7e84` | **ACCEPT-CANDIDATE (SOURCE COMPOSITION)** | Overlay SHA independently reproduced and contains no bank asset. Independent persistence review confirms source-level composition PASS, but requires API-35 migration/restore/process/Review-Map runtime, lint, signed build, install, and visual gates. |
| Biology/Geology successor | `parallel/a1-biology-geology` `bf12b03dbeb5478d109b23f51f43f99c3af0196d` | **PENDING** | Integrate only its deterministic successor, not competing predecessor payloads; preserve frozen bank, render canonical stimuli, safely demote unresolved visible-text records, and retain Geo153 exclusion/reconstruction blocker. |
| Geo153 delivery exclusion | `1a2bacd753d6884c1d09f8d8723959e2b8765252` | **PENDING REBASE** | Patch dry-applies on clean rescue base, but touches `BankStore.kt`/`StudyRepository.kt`; rebase after final selection composition and execute source-backed exclusion/resume tests. |
| Physics material-bank second pass | `parallel/a2-physics` `5ca5cf6c73762aa63b1d41558643fd122e3938f2`; overlay `25238d…0d0a5` | **REJECT FOR CURRENT INTEGRATION** | Actual disposable output hashes `52bf1b…e2c7` / `8070e7…6286` do not reproduce claimed `d6d93c…3a5e` / `ca4f3c…fe2a`; correct reproducibility, row-level diff, audit/version/migration plan, and final source/build evidence are required. |
| Legacy standalone Review/Map | `parallel/a2-review-question-map` `ad25e780b115d2bc144d6d3218c8104f0fb5bae5` | **REJECT FOR INTEGRATION** | It is not demonstrated as a host-package implementation. Only portable concepts may inform the real V6.1.4 UI merge. |
| Independent Physics review | `21c37357a388f43c7d6a4d63b8f47f7b610cb3c7` | **ACCEPT AS HISTORICAL EVIDENCE** | It reviewed the obsolete first-pass commit, confirms that review is stale for current Physics, and does not cure the failed current material-bank reproduction. |
| Independent persistence final review | `e6d3f685340cd2b7075b82232a5309af65e7946e` | **ACCEPT AS EVIDENCE** | Confirms A3 source-composition result and explicitly withholds release certification pending runtime/signing/visual gates. |
| Preintegration CI review | `d5d797047f737c6b1ca7ce5a0b788168d3412ad6` | **ACCEPT AS BLOCKING EVIDENCE** | Its `NO GO_INTEGRATE` judgment remains directionally valid but its Physics inventory is stale; it cannot replace refreshed branch evidence. |
| Selection-composition helper | `parallel/help-a2-selection-composition-final` | **PENDING — NOT PUBLISHED AT REFRESH** | Independently diff and retest only when a branch/report/artifact appears. |
| UI fallback helper | `parallel/help-a2-ui-fallback-final` | **PENDING — NOT PUBLISHED AT REFRESH** | Independently compare with the primary UI second pass and prove full Test/Review, all-21 stimuli, Map, and 90–140% host behavior. |

### Confirmed dry-composition collision map

The initial evidence-backed dry composition is intentionally **not a merge candidate**. Chemistry and A2 duplicate second-pass both modify `BankStore.kt`, `Models.kt`, and `StudyRepository.kt`; Final-Hours also modifies `StudyRepository.kt` and `RadiologyApp.kt`; A3 modifies `StudyViewModel.kt`, `BankStore.kt`, `ProgressDatabase.kt`, `StudyRepository.kt`, `AdaptiveEngine.kt`, and `RadiologyApp.kt`. The disposable three-way merge emitted unresolved conflict markers in `BankStore.kt` and `StudyRepository.kt`. The final owner must use semantic source merging, preserve no-repeat/evidence-family behavior, and rerun the relevant selectors, persistence, Review/Map, and Final-Hours tests on the single composed tree.

### Phase A conclusion

**Phase A preflight is complete and publication-ready with `NO GO_INTEGRATE` status.** It identifies a checksum-matched immutable baseline, rejects an unsafe public-source baseline mismatch, enumerates active candidates and conflicts, preserves historical bank references, records the reproducibility failure for the only current material-bank mutation, and states concrete entry conditions for every candidate. It does **not** authorize integration, merge to `main`, tag creation, signing, artifact upload, or release publication. The foreman will wait for the exact `GO_INTEGRATE` message and will re-fetch `main` plus all accepted candidates immediately before Phase B.

[12]: https://github.com/rynmrde/Konkor/commit/b78daecaa26ccc5c2a397cf71b043baae10fc9d6 "A3 final persistence report commit"
[13]: https://github.com/rynmrde/Konkor/commit/e6d3f685340cd2b7075b82232a5309af65e7946e "Independent A3 final persistence review"
[14]: https://github.com/rynmrde/Konkor/commit/600fd3db6bec7fb8f45c21e5d45e2c0e9656ff6e "Independent Chemistry final review"
