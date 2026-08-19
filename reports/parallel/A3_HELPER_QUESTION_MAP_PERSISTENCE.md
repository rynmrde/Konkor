# A3 Helper — Question Map Session Persistence Bridge

| Field | Value |
|---|---|
| Helper role | Selection/session/persistence support for the Question Map owner |
| Helper branch | `parallel/help-a3-question-map-persistence` |
| Direct base | `main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Required predecessor | A3 V6.1.5 Final-Hours overlay, SHA-256 `e2b9f7752823a94c63295b1ce1baea328275520d16880dc4123d4042dcf4f156` |
| Related UI contract | A2 `parallel/a2-review-question-map`, `ReviewQuestionMap.kt` |
| Scope | Room-backed session-map projection and direct navigation bridge; no bank, question wording, release, or main changes |

## Purpose

The A2 Question Map module correctly models selected answer, flag, result and selected-question state, but its handoff identifies the missing host persistence boundary. The V6.1.5 active session already contains the authoritative data needed to close that gap: question IDs, test/review positions, answers, flags, phase, and Room attempts. This helper delta exposes those existing facts as a UI-neutral snapshot rather than adding a duplicate map table or fabricating state.

| Existing persisted field | Question Map projection |
|---|---|
| `questionIdsJson` | Ordered, unique Question Map entries and direct-jump index |
| `position` / `reviewPosition` | Current selected map question before submit / during review and reopening |
| `answersJson` | Original option selected per question |
| `flagsJson` | Learner flag state, excluding cue-only metadata keys |
| `active_session.phase` | Pre-submit versus post-submit state |
| `attempt` rows for the active session key | Correct, wrong or blank result after submit and in reopened Review |

## Delta contents

`QuestionMapSessionProjection.kt` supplies `PersistedQuestionMapSnapshot` and `QuestionMapSessionProjection`. The projection keeps question wording and options out of the persistence adapter, ensuring that the bank and A2 presentation model remain their sources of truth. It filters review outcomes by the active session key, rejects empty or duplicate ID sets, retains the phase-specific selected index, and maps only stored grades to correct/wrong/blank presentation facts.

`StudyRepository.questionMapSnapshot()` reconstructs this snapshot from Room whenever the map opens, the app returns from background, a process is recreated, a session resumes, or Review is reopened. `StudyRepository.goToQuestion(questionId)` resolves the question against the active persisted session and atomically updates either the test position or review position under the repository mutex. A UI integration can map each projected entry into A2’s `QuestionMapEntry`, call `goToQuestion` from the A2 tap callback, and rebuild from `questionMapSnapshot()` after each repository mutation.

The delta adds a JVM JSON implementation only to the unit-test classpath; it does not change the Android runtime JSON implementation. `QuestionMapSessionProjectionTest` verifies pre-submit answer/flag/current restoration, post-submit correct/wrong/blank states filtered to the active session, and a completed Review reopening at its persisted review position.

## Validation and remaining gate

| Validation gate | Result |
|---|---|
| Focused `QuestionMapSessionProjectionTest` | **PASS** |
| Full V6.1.5 JVM suite with helper bridge | **PASS** — Gradle reported `BUILD SUCCESSFUL` |
| Kotlin compilation | **PASS** as part of the JVM task graph |
| Android API 35 instrumentation and real Review/Map UI flow | **Not run**; foreman integration gate remains required |

The helper delta must be applied only after the V6.1.5 Final-Hours overlay because it replaces the V6.1.5 `StudyRepository.kt`. It does not merge A2’s presentation package automatically, because A2’s branch is intentionally independent and imports a different package namespace. The foreman must reconcile both overlays in the verified frozen project, wire the presentation adapter, and execute device-level Review/Map/navigation/process-recreation tests.
