# A2 Review + Question Map QA Handoff

| Field | Value |
|---|---|
| Role | Android Review UI + Question Map + presentation-state owner |
| Account label | A2-M3; Normal/Standard Manus 1.6 |
| Working branch | `parallel/a2-review-question-map` |
| Verified baseline | `origin/main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Baseline commit message | `ci: publish rescue directly without artifact quota` |
| Scope status | **Scoped module implemented and validated; full product integration blocked by the actual baseline architecture.** |

## Baseline Audit Finding

The verified `main` baseline is a 61-file Android Compose scaffold rather than the described Konkor application. It contains eight Kotlin files in total, only one production activity (`MainActivity.kt`), and no question bank, Room schema, active-session model, Review screen, Question Map, Day Selector, migration layer, scheduler, progress store, or existing review tests. Its application identity is `com.example`, version `1.0` / code `1`, rather than the historical reference version described in project instructions.

> The requested end-to-end review and session persistence wiring cannot truthfully be claimed against this baseline because the required app/domain architecture does not exist. This report therefore distinguishes a tested, mergeable presentation/state module from the unimplemented host integration.

## Delivered Scoped Module

`app/src/main/java/com/example/review/ReviewQuestionMap.kt` provides the following reusable Compose and presentation-state contracts.

| Requirement | Delivered behavior |
|---|---|
| Standalone Review | `StandaloneReview` renders original stem, optional figure resource, all four original options, learner answer, correct answer, outcome, confidence, solution, selected-wrong reasoning, distractor explanations, and concise microtopic/source/error information. |
| Four-option fidelity | `ReviewQuestion` rejects any record without exactly four original options and validates selected/correct indices. |
| Persian RTL presentation | The module uses RTL composition and learner-facing Persian labels for status, answer, confidence, error type, and map state. |
| Internal-enum safety | Presentation enums map to Persian labels; the UI never renders persistence-style raw values. |
| Tappable full-block map | `QuestionMap` renders a full lazy grid, map legend, accessible content descriptions, and direct selection callbacks. |
| Pre-submit states | Current, unanswered, answered, and flagged are represented. |
| Post-submit states | Correct, wrong, and blank are represented. |
| Process recreation | `rememberQuestionMapState` uses a bundle-safe `Saver` for selected question, answers, flags, and outcomes. |
| Session/review reopening | `QuestionMapSnapshot`, `snapshot`, and `restore` provide a Room-compatible persistence boundary; the future session repository must persist this snapshot. |
| Themes, scale, density, motion, audio, haptics | The module is Material-theme based and does not override app text-scale/density or mutate motion/audio/haptic settings. |

## Added Tests

| Test file | Coverage |
|---|---|
| `app/src/test/java/com/example/review/QuestionMapStateTest.kt` | Pre-submit visual states, post-submit correct/wrong/blank states, snapshot/restore preservation, and four-option contract. |
| `app/src/androidTest/java/com/example/review/ReviewQuestionMapInstrumentedTest.kt` | Tappable Persian map navigation plus standalone Review evidence rendering. The instrumentation source compiles. |

## Validation Evidence

| Gate | Result | Evidence / limitation |
|---|---|---|
| Kotlin production compile | PASS | `:app:compileDebugKotlin` completed successfully. |
| Focused JVM tests | PASS | `:app:testDebugUnitTest` completed successfully after the environment Java compiler was installed. |
| Instrumentation test compilation | PASS | `:app:compileDebugAndroidTestKotlin` completed successfully. |
| Lint | PASS with baseline warnings | `:app:lintDebug` reported **0 errors, 45 warnings**. Warnings are existing manifest/dependency/resource/icon concerns, not new Review/Map errors. |
| Debug APK | PASS | `:app:assembleDebug` produced `app-debug.apk`, SHA-256 `c5bed16aa15bc2048298f20a8b5245964eb3d17b761bbe735ab83852ba217ba1`. |
| Raw internal-enum / generic-filler scan | PASS | Scoped Review/Map source and test directories had no matches for the checked prohibited raw/filler phrases. |
| Device instrumentation execution | BLOCKED | `adb devices` returned no connected device or emulator; tests were compiled but not executed on API 35. |
| End-to-end Review/Map/session resume flow | BLOCKED | The verified baseline lacks question/session/repository/navigation infrastructure. |

The local build environment required a local Android SDK, a Java compiler, Gradle 9.3.1 (the project plugin minimum), and an ignored debug keystore because the baseline omitted both a Gradle wrapper and the keystore referenced by its debug signing configuration. None of those environment-only artifacts are part of the proposed branch change.

## Integrator Instructions and Residual Risk

The foreman should merge the module only after reconciling the missing host architecture. The integration must inject actual bank records into `ReviewQuestion`, persist `QuestionMapSnapshot` alongside the active session in Room, invoke `restore` on session resume and Review reopening, route `onQuestionSelected` through the existing question navigator, and then execute the required API 35 install/launch/process-recreation test flow. A real figure loader may pass `figurePainter` when figures are backed by files or URIs rather than drawable resources.

This branch does **not** modify bank data, question IDs, migrations, package identity, release signing, main, or any release. It must not be treated as evidence that the full Konkor product requirements are met.
