# Lite A2 — Pre-Integration Final-Gate Dependency Matrix

**Review role:** Independent CI/build and integration-gate reviewer  
**Review date:** 2026-08-19 UTC  
**Repository:** [`rynmrde/Konkor`](https://github.com/rynmrde/Konkor)  
**Review branch to publish:** `parallel/help-lite-a2-preintegration-ci-20260819`  
**Baseline observed:** `main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
**Disposition:** **NO GO_INTEGRATE yet. No main branch, release, or tag was modified.**

## Refreshed worker heads

The current Composio-backed branch inventory was refreshed before this review. The requested short SHAs resolve as follows; full SHAs are recorded to avoid abbreviated-SHA ambiguity.

| Workstream | Branch | Current head | Lane | Review status |
|---|---|---|---|---|
| Chemistry | `parallel/a1-chemistry` | `4e9a2f2c90ae7cc1e0ee093f341083e3d4295cd7` | V6.1.4 rescue overlay replacement plus QA report | Pending final overlay/build validation |
| Duplicate second pass | `parallel/help-a2-second-pass-contract` | `b717f4c96209954e0e6f596ed015a85c2e6dfc6d` | V6.1.5 integration-only overlay | Pending composition and full final gates |
| Final-Hours | `parallel/a3-final-hours` | `ee706e9836bd499decae0a1d79ea643884ab4d1c` | V6.1.5 candidate overlay, version 6.1.5/code 166 | JVM/static evidence; APK/device gates not run |
| Official real-exam | `parallel/a1-official-real-exam` | `72b21461fc357ee8600c71074db5bf5786735a91` | Documentation/QA handoff only | No application overlay change observed |
| Geo153 | `parallel/help-a1-official-geo153` | `1a2bacd753d6884c1d09f8d8723959e2b8765252` | Patch/test/report for source exclusion | Pending validator execution in composed tree |
| Physics | `parallel/a2-physics` | `04b571947ab0c8c40b5025b121f8442a3e5911f2` | QA report only | No application overlay change observed |
| Review/Question Map | `parallel/a2-review-question-map` | `ad25e780b115d2bc144d6d3218c8104f0fb5bae5` | Standalone Compose module and tests | Host integration explicitly not proven |
| Persistence cross-review | `parallel/help-a3-independent-persistence-review` | `3c8dd0cba28e0d8718d34a1dbdd81140839a2e84` | V6.1.5 overlay delta | Must follow validated Final-Hours overlay |
| Persistence validation | `parallel/help-a3-persistence-validation` | `3f12c5a7feb4111be2b0c0cd04fd431afd1d4a06` | Static gate script only | Requires execution against final tree |
| Question Map persistence | `parallel/help-a3-question-map-persistence` | `c6360595b852bad956296b1f820ab9c69c952e28` | V6.1.5-on-V6.1.5 delta | Requires A3 predecessor; not standalone |
| Newer Biology/Geo | `parallel/a1-biology-geology` | `f4ee7395fcbce1904d0bdf98493b5c629571d4fb` | Bank/analysis workstream | Must be selected explicitly; not assumed integrated |
| Newer Biology helpers | `parallel/bio-a`, `parallel/bio-b` | `88deba771c9dcf4f65cd49948272797c05ed544b`, `9ee96431094a0f5fc970fc2f078fcb78d53a8786` | Bank/analysis helpers | Heads exist; integration and collision status not yet closed |
| Persistence QA | `parallel/a3-persistence-qa` | `72dc76e56b7ae625ad1904c76910eeaec5f90f58` | No change beyond baseline | No evidence contribution |

The requested duplicate second-pass SHA is **not** the older `parallel/a2-math-duplicates` branch; it is the newer `parallel/help-a2-second-pass-contract` head shown above. That distinction matters because only the latter carries `radiology_v615_a2_secondpass_patch/`.

## Exact overlay composition order

The order below is dependency-constrained, not a suggestion. Each archive must be checksum-verified and extracted into a fresh copy of the frozen V6.1 project. Never apply these archives to a previously mutated worktree.

| Order | Material | Required action | Dependency / collision rule |
|---:|---|---|---|
| 0 | Frozen V6.1 project ZIP | Download from the authoritative Drive asset and verify `1344aca90474ac96e27e94ba754ebafd42778e2ceaab91f9a5fb1be2e882d046` | This is the only valid source base. The generic root Gradle scaffold is not the release app. |
| 1 | Frozen V6.1 bank and source evidence | Verify gzip `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`, expanded DB `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`, and verified JSON hash `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d` | Bank remains immutable for this app-only composition. |
| 2 | V6.1.4 rescue overlay | Use the **current selected** `radiology_v614_rescue_patch/overlay.tar.xz` from Chemistry head `4e9a2f2c`; verify its actual SHA before extraction | Chemistry modifies the V6.1.4 archive path. Do not combine it with an older V6.1.4 overlay copy. |
| 3 | A2 duplicate second pass | Extract `radiology_v615_a2_secondpass_patch/overlay.tar.xz` from `b717f4c`, after confirming its manifest and declared SHA `64bfc1f47ac71462821be4e4d009e053c729619787d2db529d119237ec42e36c` | Manifest says base is V6.1.4 rescue plus A2 primary duplicate overlay. Inspect archive paths before extraction; do not assume non-overlap. |
| 4 | A3 Final-Hours | Extract `radiology_v615_final_hours_patch/overlay.tar.xz` from `ee706e`, after verifying the **current** manifest SHA `59a8ff9e5aa62bbe164fa8dffb6fc5056795eeb5ee82b511cc55fbff9281599d` | This changes the app lane to V6.1.5/code 166 and requires a new V6.1.5 workflow. It must not be treated as a V6.1.4 patch. |
| 5 | Persistence cross-review delta | Extract `radiology_v615_a3_independent_persistence_review/overlay-delta.tar.xz` from `3c8dd0c` only after A3, and inspect its archive manifest | This is V6.1.5-on-V6.1.5, not an independent overlay. |
| 6 | Question Map persistence delta | Extract `radiology_v615_question_map_persistence_delta/overlay-delta.tar.xz` from `c6360595` only after A3; verify `aa52bcdb5f93e516d49119f42b137c6e4a838d5da1c52906b7b1d7cc9b7e0361` | Manifest explicitly requires the validated A3 predecessor and related ReviewQuestionMap contract. |
| 7 | Geo153 patch and test | Apply `overlays/geo153/HELP_A1_OFFICIAL_GEO153_EXCLUSION.patch` and run `tests/verify_geo153_exclusion_overlay.py` in the composed tree | This is a source patch, not a tar overlay. Apply after the base/selected app overlays and inspect whether it touches bank-selection or validator files. |
| 8 | Review/Question Map module | Apply the selected `ReviewQuestionMap.kt` and tests from `ad25e78` only after resolving host package and navigation integration | A2 report states the baseline lacks the host architecture; a module PASS cannot certify product integration. |
| 9 | Static validators and reports | Add selected validator scripts/reports without allowing report-only branches to masquerade as app changes | Official and Physics heads are documentation-only based on changed-file metadata. |

**Version consequence:** Steps 3–8 are V6.1.5-lane changes or deltas. If any of them are accepted, the result cannot be released under the historical V6.1.4 version/tag. Either stop at an app-only V6.1.4 composition containing only compatible V6.1.4 changes, or create a new V6.1.5 release workflow/source asset/tag. Do not mix V6.1.5 code with V6.1.4 release metadata.

## Path-level collision and build-break risk matrix

The commit metadata shows no direct text-file collision between the named commits because most app changes are packed inside binary `overlay.tar.xz` or `overlay-delta.tar.xz` files. That is **not evidence of safety**: archive contents can overwrite the same extracted files. The following risks are therefore blockers until tar manifests are enumerated and compared.

| Risk | Paths / artifacts | Severity | Required check |
|---|---|---:|---|
| V6.1.4 archive replacement | `radiology_v614_rescue_patch/overlay.tar.xz` modified by Chemistry head | Critical | Hash and list archive contents from `4e9a2f2`; reject any stale V6.1.4 archive copied from another branch. |
| A2 vs A3 common engine/data files | A2 manifest declares `Models.kt`, `BankStore.kt`, `StudyRepository.kt`, `AdaptiveEngine.kt`, and `AdaptiveEngineTest.kt`; A3 manifest also changes `StudyRepository`, `AdaptiveEngine`, planner/presentation, and Room migration paths | Critical | Extract both archives to manifests and compute duplicate target paths. If a path is present in both, use a deliberate source merge or a verified last-writer rule; never silently overwrite. |
| A3 vs Question Map persistence | Question Map delta replaces V6.1.5 `StudyRepository` and adds `QuestionMapSessionProjection.kt`; A3 already owns the V6.1.5 repository/session surface | Critical | Apply A3 first, then inspect the delta patch against the A3 file version. Compile focused and full JVM tests after extraction. |
| A3 vs independent persistence delta | `radiology_v615_a3_independent_persistence_review/overlay-delta.tar.xz` is V6.1.5-on-V6.1.5 | High | Confirm its base SHA/manifest matches the exact A3 overlay; reject if the delta was built against an older A3 archive. |
| Review module package/host mismatch | `app/src/main/java/com/example/review/ReviewQuestionMap.kt` versus release package `com.radiology1405.prep` | Critical | Port or integrate explicitly; do not copy the `com.example` module unchanged into the release project. Run compile, lint, instrumentation and real host UI tests. |
| Room schema/migration collision | A3 adds schema v4 / `MIGRATION_3_4`; persistence deltas may touch session persistence; Question Map delta adds snapshot persistence | Critical | Inspect final Room version, migration registration, exported schemas, backup/restore, and migration tests. Reject destructive fallback and duplicate migration definitions. |
| Static validator path collision | `tests/verify_a2_duplicate_session.py`, `tests/verify_final_hours_v615.py`, `tests/verify_geo153_exclusion_overlay.py`, `tools/verify_persistence_overlay.sh` | Medium | Run each against the same final extracted tree and bank; record raw outputs. |
| Bank/holdout selection collision | A2 changes evidence-family/follow-up/scenario exclusion; A3 changes distinct TRAIN/session/SIM behavior | Critical | Run final composition gate once, including exact IDs, evidence family, follow-up group, scenario fingerprint, holdout disjointness, and unique-mastery counters. |
| Version/signing workflow collision | V6.1.4 workflow versus required new V6.1.5 workflow | Critical | Preserve V6.1.4 workflow/assets. Add a new V6.1.5 workflow with version 166 assertions and a new source asset. |
| Source ZIP provenance collision | Historical V6.1.4 ZIP versus final V6.1.5 source | Critical | Materialize the source ZIP from the exact final tree before integration/release; never reuse or relabel the historical asset. |

The **most likely build-breaking collision** is the shared `StudyRepository.kt` / `AdaptiveEngine.kt` / model-data surface between A2 and A3, followed by the explicit replacement of `StudyRepository.kt` by the Question Map persistence delta. Archive-level path manifests are mandatory before integration can be considered safe.

## Final-gate dependency matrix

| Gate | Depends on | Exact command or evidence | Current status | Blocks GO_INTEGRATE? |
|---|---|---|---|---|
| Baseline pin | Current `main` | `git fetch origin && git rev-parse origin/main` | Refreshed at `72dc76e...` | No, repeat immediately before integration |
| Archive/source hashes | Drive ZIP, bank, selected overlays | `sha256sum` for frozen ZIP, each archive, bank gzip/DB/JSON | Historical hashes known; current archive composition not independently rerun | **Yes** |
| Archive path collision scan | All selected tar/delta archives | `tar -tf overlay.tar.xz`; sorted intersection of target paths | Not observed | **Yes** |
| Chemistry static/QA | Chemistry overlay + frozen bank | Chemistry QA validator/report; raw-enum and duplicate scans | Report evidence exists; final composed run not observed | **Yes** |
| A2 duplicate/session gate | A2 overlay + all preceding overlays | `python3 tests/verify_a2_duplicate_session.py --bank-gz <verified-bank.gz>` | Required by manifest; not observed on final composition | **Yes** |
| Final-Hours static gate | A3 overlay | `python3 tests/verify_final_hours_v615.py` | A3 reports PASS on its own candidate; final composed run not observed | **Yes** |
| Geo153 exclusion gate | Geo153 patch | `python3 tests/verify_geo153_exclusion_overlay.py` | Not observed on final composition | **Yes** |
| Persistence static gate | A3 + persistence deltas | `bash tools/verify_persistence_overlay.sh` | Script exists; final run not observed | **Yes** |
| Schema and source validation | Final bank/source | `python tests/validate_v6_1.py` plus schema/ID/four-option/key/source/quarantine/holdout checks | Workflow command exists; final raw output not observed | **Yes** |
| Kotlin compilation | Fully composed extracted project | `gradle --no-daemon :app:compileDebugKotlin --stacktrace` | A3 focused/full JVM evidence only; final compile not observed | **Yes** |
| JVM tests | Fully composed project | `gradle --no-daemon :app:testDebugUnitTest --stacktrace` | A3 candidate reports second-pass JVM PASS; deltas/composition not run | **Yes** |
| Lint | Fully composed project | `gradle --no-daemon :app:lintDebug --stacktrace` | A3 manifest says NOT RUN | **Yes** |
| Debug APK | Fully composed project | `gradle --no-daemon :app:assembleDebug --stacktrace` | Not observed on final composition | **Yes** |
| Packaged bank | Debug APK | Extract `assets/radiology1405_bank_v6_1.db`; `sha256sum`; reject `.db.gz` packaging | Not observed | **Yes** |
| Release version/package | Final signed APK | `$ANDROID_HOME/build-tools/35.0.0/aapt dump badging "$APK"`; assert package/version 6.1.5/166 if A3 accepted | Not observed | **Yes** |
| Signing | Final APK and release key | `$ANDROID_HOME/build-tools/35.0.0/apksigner verify --verbose --print-certs "$APK"` | Not observed | **Yes** |
| API 35 instrumentation | Final debug APK/project | `gradle -p "$PROJECT" --no-daemon :app:connectedDebugAndroidTest --stacktrace` | A2 host device execution was previously blocked; A3 says NOT RUN | **Yes** |
| Migration/process persistence | Final schema and historical DB | API 35 migration, backup/restore, process recreation, active-session and Question Map snapshot tests | Not observed | **Yes** |
| Install/launch smoke | Final signed APK | `adb install "$APK"`; `adb shell monkey -p com.rynmrde.konkor -c android.intent.category.LAUNCHER 1`; PID/crash checks | Not observed | **Yes** |
| UI end-to-end | Final host app | Open → answer → navigate → flag → submit → review; full Review and Map persistence assertions | Standalone module evidence is not host evidence | **Yes** |
| Source asset | Final integrated tree | Create deterministic source ZIP, manifest and SHA-256 before release | Mandatory materialization not observed | **Yes** |

## Shortest reliable command sequence

Run from a fresh extracted project after the archive collision scan and before any release action:

```bash
python3 tests/verify_a2_duplicate_session.py --bank-gz "$BANK_GZ"
python3 tests/verify_final_hours_v615.py
python3 tests/verify_geo153_exclusion_overlay.py
bash tools/verify_persistence_overlay.sh
python3 tests/validate_v6_1.py | tee "$GITHUB_WORKSPACE/_out/static-validation.txt"
! grep -R 'fallbackToDestructiveMigration' app/src/main/java
! grep -q 'android.permission.INTERNET' app/src/main/AndroidManifest.xml
gradle --no-daemon :app:compileDebugKotlin :app:testDebugUnitTest :app:lintDebug :app:assembleDebug --stacktrace | tee "$GITHUB_WORKSPACE/_out/gradle-debug.txt"
# inspect the packaged bank from the debug APK and verify its SHA-256
# verify migration/progress/session/UI instrumentation on API 35
gradle -p "$PROJECT" --no-daemon :app:connectedDebugAndroidTest --stacktrace
gradle --no-daemon :app:assembleRelease --stacktrace | tee "$GITHUB_WORKSPACE/_out/gradle-release.txt"
$ANDROID_HOME/build-tools/35.0.0/apksigner verify --verbose --print-certs "$APK"
$ANDROID_HOME/build-tools/35.0.0/aapt dump badging "$APK"
adb install "$APK"
adb shell monkey -p com.rynmrde.konkor -c android.intent.category.LAUNCHER 1
adb shell pidof com.rynmrde.konkor | grep -Eq '[0-9]+'
! adb logcat -d -s AndroidRuntime:E | grep -q 'Process: com.rynmrde.konkor'
```

The APK version assertions must be selected consistently. If A3 or any V6.1.5 delta is included, assert `versionName 6.1.5` and `versionCode 166`, create a new V6.1.5 source ZIP and workflow, and do not touch V6.1.4 assets. If only V6.1.4-compatible app/source changes are retained, assert 6.1.4/165 and materialize a new source asset from the exact final V6.1.4 tree.

## GO_INTEGRATE decision

**GO_INTEGRATE: NO.** The current evidence is sufficient to plan composition but not to integrate safely. The blocking items are: archive-level path manifests and collision resolution; Chemistry’s current V6.1.4 overlay hash and content; A2/A3 shared `StudyRepository.kt` and `AdaptiveEngine.kt` resolution; A3 predecessor validation for both persistence deltas; package migration of the Review/Question Map module; final Room migration registration and preservation tests; final static/JVM/lint/debug/release outputs; API 35 instrumentation; signed APK/package/version/certificate verification; and a deterministic source ZIP materialized from the exact final tree.

Report-only heads for Official and Physics do not independently block the build, but their evidence must be attached to the final audit if their content is relied upon. The newer Biology heads are not included in the composition until Foreman names the exact selected branch, verifies bank/source compatibility, and reruns the full bank/session/duplicate gates.

## References

[1]: https://github.com/rynmrde/Konkor/commit/4e9a2f2c90ae7cc1e0ee093f341083e3d4295cd7 "Current Chemistry head"
[2]: https://github.com/rynmrde/Konkor/commit/b717f4c96209954e0e6f596ed015a85c2e6dfc6d "Current duplicate second-pass head"
[3]: https://github.com/rynmrde/Konkor/commit/ee706e9836bd499decae0a1d79ea643884ab4d1c "Current Final-Hours head"
[4]: https://github.com/rynmrde/Konkor/commit/72b21461fc357ee8600c71074db5bf5786735a91 "Current official real-exam head"
[5]: https://github.com/rynmrde/Konkor/commit/1a2bacd753d6884c1d09f8d8723959e2b8765252 "Current Geo153 helper head"
[6]: https://github.com/rynmrde/Konkor/commit/04b571947ab0c8c40b5025b121f8442a3e5911f2 "Current Physics head"
[7]: https://github.com/rynmrde/Konkor/commit/3c8dd0cba28e0d8718d34a1dbdd81140839a2e84 "Current persistence cross-review head"
[8]: https://github.com/rynmrde/Konkor/commit/c6360595b852bad956296b1f820ab9c69c952e28 "Current Question Map persistence head"
[9]: https://github.com/rynmrde/Konkor/blob/main/.github/workflows/radiology-v614-rescue.yml "Authoritative V6.1.4 rescue workflow"