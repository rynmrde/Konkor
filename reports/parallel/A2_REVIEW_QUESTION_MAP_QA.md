# A2 Review and Question Map QA Handoff

## Worker identity and scope

| Field | Recorded value |
|---|---|
| Role | A2 Android Review UI + Question Map + presentation-state owner |
| Account label | Normal/Standard Manus 1.6 |
| Primary branch | `parallel/a2-review-question-map` |
| Primary remote commit | `ad25e780b115d2bc144d6d3218c8104f0fb5bae5` |
| Primary baseline | `origin/main` `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Second-pass integration baseline | `radiology1405_android_project_v6.1.4.zip`, release `radiology1405-apk-v6.1.4-20260817` |
| Full-source baseline SHA-256 | `b242c94b3af76b5bb76043699d281555d72092b8416b1be77be3b8d31ec4ab8e` |
| Rescue overlay baseline | `radiology_v614_rescue_patch/overlay.tar.xz` SHA-256 `d17bdd905def35a45caa32aa5a0b07b6196ecc78de493a340bf36fac0c0103c3` |
| Product package and version | `com.rynmrde.konkor`, versionName `6.1.4`, versionCode `165` |
| Immutable bank status | Unchanged: gzip `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`; expanded SQLite `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c` |

The original assigned branch contains a standalone contribution based on the then-visible scaffold. **It is not sufficient for product release integration.** This second pass corrects that conclusion by targeting the actual V6.1.4 application package, its Room/session model, its full Compose navigator, and the current rescue overlay. No `main` branch and no Release were modified.

## SECOND_PASS_REVIEW

### Defects found

| ID | Finding | Release impact | Disposition |
|---|---|---|---|
| SP-01 | The primary contribution was scoped to `com.example` scaffold code rather than the full `com.radiology1405.prep` V6.1.4 product source. | Product integration was unproven. | Corrected in the full source overlay. |
| SP-02 | The original map did not prove a full ordered block source for post-submit correct/wrong/blank states after reopening Review. | Review map could not be derived robustly from active persisted session data. | Corrected through `SessionSummary.questions`, resolved from durable `questionIdsJson`. No Room schema change is required. |
| SP-03 | The original branch did not demonstrate that all Review/Map text uses the app’s existing 90–140% typography mechanism. | Accessibility regression risk. | Corrected by using `MaterialTheme.typography` everywhere in new Review/Map content and extracting the existing scaling calculation to the deterministic `scaledTypography` helper. |
| SP-04 | The first fix only surfaced `stimulus.left/right` paired statements. It discarded canonical table, graph, and generic structured premise payloads. | The 21 pair records and Chemistry table/comparison records could be visually incomplete. | Replaced with schema-generic parser/presenter over the canonical immutable `stimulus` JSON. |
| SP-05 | Review metadata exposed raw `questionForm` and `teachingLevel` tokens. | Persian UI raw-enum leakage. | Corrected with complete Persian mappings for the current frozen-bank vocabularies. |

### Applied full-product corrections

The overlay changes only source and test files. `Models.kt` preserves the original immutable stimulus object as `stimulusJson`; it does not modify question JSON, IDs, source metadata, or bank storage. `StudyRepository.kt` resolves the entire active block into `SessionSummary.questions` from the durable ordered `questionIdsJson`, while the actual Room `ActiveSessionEntity` remains the owner of answers, flags, positions, elapsed time, confidence, and analysis state.

`RadiologyApp.kt` renders a full block Question Map in the real Study header. Before submission, each selectable cell derives **current**, **unanswered**, **answered**, or **flagged** from the persisted active session. In Review, each cell derives **correct**, **wrong**, or **blank** from the same persisted answer JSON and ordered session question list; the current review index is retained as an outline. Cell taps invoke the existing `StudyViewModel.goTo`, which persists `position` or `reviewPosition` through the repository’s active-session mutation path. This provides the product seam for navigation, background/foreground resume, process recreation, session resume, and reopening Review.

The full Review now independently shows the original stem; source crop when present; all four original option texts; user answer; correct answer; correct/wrong/blank result; confidence; question-specific correct reasoning; selected-wrong explanation; each distractor explanation; and concise microtopic/source/time metadata. The Review and Question Map use the existing `RadiologyTheme(settings.textScale)` and its Material typography at all new text sites. Map cells reserve a 64dp minimum height and a 216dp map viewport to avoid clipping at 140% scale. RTL remains provided by the app-level `LocalLayoutDirection.Rtl`; existing theme, density, reduced-motion, audio, and haptic behavior are retained.

The structured-stimulus presentation is schema-generic. The Test adapter and Review adapter call the same canonical parser before interactive options. It renders comparison `left/right` with the canonical labels; data-table headers and rows; graph caption, axes, series labels and points; and non-empty generic textual fields exposed by other supported structures. Existing `official_source_crop` questions keep the authoritative crop image path. No premise was copied into a rewritten stem and no bank change was made.

### Explicit second-pass status

| Required item | Status | Evidence |
|---|---|---|
| Full V6.1.4 product package integration | **PASS** | Overlay directly changes `com.radiology1405.prep` full source. `:app:compileDebugKotlin` and `:app:assembleDebug` pass. |
| Real Room/session/navigation persistence seam | **PASS (source and deterministic regression)** | Durable `questionIdsJson`, `answersJson`, `flagsJson`, `position`, and `reviewPosition` drive map state; Robolectric regression reconstructs Review session JSON and rechecks map/result states. Android API 35 physical process-kill remains a Foreman execution gate. |
| Existing 90–140% text-scale contract | **PASS** | `TypographyScaleTest` passes; new Review/Map strings use Material typography from `scaledTypography`, including 90% and 140% boundary coverage. |
| Persian RTL/themes/density/motion/audio/haptic preservation | **PASS (static integration)** | Existing app-level RTL/theme controller and `ExperienceController` paths are retained; map taps use existing select SFX/haptic; no setting schema changed. Device visual confirmation remains a Foreman gate. |
| Raw internal enum leakage in changed Review/Map presentation | **PASS** | Targeted source scan found no `condition_wrong`, `truth_partial`, raw `questionForm`, raw `teachingLevel`, or `ErrorType.name` presentation paths. |
| `VISIBLE_STIMULUS_21` | **PASS** | Executed real-bank Robolectric regression confirms all 21 specified comparison IDs expose canonical A/B content in Test, Review, and reconstructed Review session paths. |
| Chemistry structured-stimulus 16 witness | **PASS** | Executed real-bank Robolectric regression confirms all 13 `data_table` and 3 `comparison` Chemistry witness IDs expose non-empty canonical premise content in both adapters. |
| Exhaustive active TRAIN structured-stimulus regression | **PASS** | Executed regression enumerated **152** active TRAIN rows with a canonical stimulus payload. Textual stimuli render canonical blocks; authoritative source-crop stimuli retain a non-empty crop route. |

### Exact canonical witness sets

The original 21 comparison witnesses are `v3_bio_02_12`, `v3_bio_05_12`, `v3_bio_06_07`, `v3_bio_07_15`, `v3_bio_08_07`, `v3_bio_10_11`, `v3_bio_11_07`, `v3_bio_12_07`, `v3_bio_14_10`, `v3_bio_15_15`, `v3_bio_16_10`, `v3_chem_20_03`, `v3_chem_26_03`, `v3_chem_54_07`, `v3_geo_45_09`, `v3_geo_46_08`, `v3_geo_47_07`, `v3_geo_49_08`, `v3_phys_30_02`, `v3_phys_33_02`, and `v3_phys_34_03`.

The Chemistry 16 witness set is `v3_chem_19_11`, `v3_chem_19_12`, `v3_chem_19_13`, `v3_chem_20_18`, `v3_chem_20_19`, `v3_chem_20_20`, `v3_chem_26_10`, `v3_chem_26_11`, `v3_chem_26_12`, `v3_chem_26_13`, `v3_chem_54_11`, `v3_chem_54_12`, `v3_chem_54_13`, `v3_chem_20_03`, `v3_chem_26_03`, and `v3_chem_54_07`. The first 13 are canonical `data_table` payloads; the last 3 are canonical comparisons.

### Exact validation record

| Gate | Command or observed artifact | Result |
|---|---|---|
| Exhaustive structured stimulus regression | `:app:testDebugUnitTest --tests com.radiology1405.prep.ui.StructuredStimulusRobolectricTest` | **PASS**; two tests passed on local Robolectric API 34. |
| JVM test suite | `:app:testDebugUnitTest` | **PASS**. |
| Kotlin compile | `:app:compileDebugKotlin` | **PASS**. |
| Android instrumentation source compilation | `:app:compileDebugAndroidTestKotlin` | **PASS**; includes `QuestionMapPersistenceInstrumentedTest` and `VisibleStimulus21InstrumentedTest`. |
| Lint | `:app:lintDebug` | **PASS**; 0 errors, 20 warnings, 5 hints. Warnings are dependency/legacy/baseline items, not new blocking errors. |
| Debug APK | `:app:assembleDebug` | **PASS**; APK SHA-256 `f7e24adb0f29e6cf2de83ddf39e2f216b034ff2f937fb036e4e9bc6d4ffadaa2`. |
| Immutable bank | gzip + expanded SQLite SHA-256 | **PASS**; matches frozen hashes above. |
| Device inventory | `adb devices` | **No attached Android device.** |

### Remaining Foreman gates

The correction does **not** claim completed device-level release QA. An Android API 35 device/emulator must still execute the compiled instrumentation tests, install the signed candidate, perform open → answer → flag → map jump → submit → Review, inspect the 21 and Chemistry-16 stimuli visually at 90% and 140%, background and force-stop/recreate the process, resume the active session, and reopen Review. Signed release build, signing verification, migration/progress preservation on a pre-existing user database, and the full final-hours behavior gates remain Foreman responsibilities.

### Integrator artifact

The finalized second-pass full-source overlay is `overlay.tar.xz` with SHA-256 to be recorded after the final report commit. It contains only the V6.1.4 files required for the correction, its tests, and this report. It must be applied on top of the stated V6.1.4 rescue overlay; it is not a replacement for the immutable bank, a main-branch merge, or a Release.
