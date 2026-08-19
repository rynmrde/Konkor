# A3 Independent Persistence Cross-Review

**Role:** Independent persistence reviewer  
**Account label:** Manus A3 Lite  
**Review date:** 2026-08-19 UTC  
**Pinned baseline:** `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
**No main/release:** No main branch, historical release, frozen bank, or other worker branch was modified.

## Executive verdict

> **Overall integration verdict: FAIL — do not release the current overlay chain yet.**

The individual persistence and product overlays contain several strong, independently supported PASS properties: Room migrations are explicit and non-destructive; stable question IDs remain the identity across attempts, sessions, mastery, and backup; the Final-Hours schema-4 field is serialized and restored; the Question Map projection reconstructs pre-submit and review states from the existing active session; and the duplicate/mastery overlay removes normal TRAIN repeat fallback and prevents correct exact repeats from increasing mastery.

The chain is nevertheless **not integration-safe as currently represented**. The Final-Hours `StudyRepository.kt` still contains an exact-repeat fallback, while the duplicate overlay’s replacement `StudyRepository.kt` removes it and adds evidence-family exclusion. Both overlays replace the same repository file and are based on V6.1.4, so applying them sequentially without a deliberate three-way merge can either reintroduce repeats or lose Final-Hours integration. In addition, Final-Hours `finishReview()` writes the SIM reviewed witness and marks the active session done in two separate DAO operations; a process death between them can unlock the next simulation before the session is durably completed. A safe helper delta below closes that transaction boundary.

## Cross-reviewed branches and evidence

| Area | Branch / artifact | Review status |
|---|---|---|
| Standard persistence | `parallel/a3-persistence-qa` | **FAIL / not advanced:** remote tip remains the baseline SHA and contains no persistence implementation delta beyond main. The prior persistence scan remains the applicable audit. |
| Review and Question Map | `parallel/a2-review-question-map` | **PASS as isolated module; FAIL for product integration:** presentation module and tests pass, but host repository/session wiring is absent from baseline. |
| Duplicate/mastery | `parallel/a2-math-duplicates` | **PASS in isolated overlay:** no-repeat and evidence-family guards plus exact-repeat mastery regression are present; full application gates remain outstanding. |
| Final-Hours | `parallel/a3-final-hours` | **PASS for isolated planner/static/JVM claims; FAIL for integration chain:** schema 4 and scheduler logic are present, but repository overlap and atomic review-witness gap remain. |
| Question Map persistence helper | `parallel/help-a3-question-map-persistence` | **PASS as projection helper:** stable IDs, phase-specific position, answers, flags, and active-session attempt outcomes are projected without a second map table. Device-level integration remains unrun. |

## Gate results

| Required review gate | Verdict | Factual basis |
|---|---|---|
| Non-destructive Room migrations | **PASS, with release test gap** | Final-Hours declares schema 4 and `MIGRATION_3_4` adds nullable `simulation_result.reviewedEpochMs`; migrations 1→2, 2→3, and 3→4 are registered; no destructive fallback is present. API 35 migration instrumentation against a v3 fixture was not run. |
| Stable question IDs | **PASS** | `Question.id` remains the attempt/session/bank lookup identity; duplicate QA reports zero duplicate IDs and preserves the frozen bank hashes. |
| Active-session compatibility | **FAIL / insufficient validation** | `sessionCompatible()` checks bank existence, pool, safety eligibility, and human-review status, but not duplicate IDs, positions, option-order permutations, answer-key bounds, or map payload key membership. The Map projection rejects duplicate IDs but trusts the remaining JSON shape. |
| Backup/restore | **FAIL / insufficient validation** | Schema 4 simulation timestamps are serialized/restored correctly, but restore validates attempt question IDs only. Active-session, due-credit, simulation, nested JSON, enum, and duplicate-attempt payloads are not comprehensively validated before replacement. |
| Process recreation and session resume | **PARTIAL PASS** | Active session fields and Map projection support resume/reopen; JVM helper tests pass. API 35 process recreation and install/launch were not run. Separate `finishReview()` operations create a SIM unlock race under process death. |
| Progress preservation | **PASS for migration shape; FAIL for release proof** | Migrations preserve rows, backups retain pre-restore/pre-wipe snapshots, and stable IDs are retained. No observed Android migration fixture, malformed-restore atomicity test, or signed-APK progress-preservation run was supplied. |
| Review full-stem/options/answers/reasoning | **PASS as isolated module; BLOCKED end-to-end** | Review module renders the required evidence and rejects non-four-option records; baseline lacks the host bank/session/repository integration needed to prove real flow. |
| Question Map states/jump/persistence | **PASS as isolated projection; BLOCKED device flow** | Pre-submit and post-submit states, direct selection contract, and persisted position are covered by JVM tests. The presentation adapter and host repository wiring still require integration; API 35 UI/process tests were not run. |
| Duplicate/session selection | **PASS in duplicate overlay; FAIL in Final-Hours overlay alone** | Duplicate overlay removes repeat fallback and checks evidence families. Final-Hours overlay retains lines 294–299 that re-serve unattempted-in-current-list but historically attempted TRAIN IDs. The two repository replacements must be merged deliberately. |
| Unique mastery | **PASS in duplicate overlay; integration pending** | Exact-repeat correct answers set mastery delta to zero while attempts and spacing evidence remain; regression test asserts unique count remains one. Final-Hours must retain this engine change after merge. |
| Final-Hours timezone/ROI/SIM logic | **PASS for isolated planner/static/JVM claims; integration pending** | Tehran clock, 2026-08-21 07:00 deadline, separated counters, adaptive diagnostics, protected sleep/logistics, SIM1/SIM2 review gates, and non-holdout fallback are covered by the worker’s static/JVM evidence. Device and release gates remain unrun. |

## Critical findings

### 1. Overlay conflict can reintroduce prohibited repeats — FAIL

The Final-Hours repository still has a comment and fallback that fills a TRAIN block from `bank.poolIds("TRAIN", allowedTopics, safeOnly = true)` after distinct candidates are exhausted. The duplicate overlay replaces that selection path with evidence-family exclusion, no historical repeats, and shorter adaptive blocks. Both files are named `StudyRepository.kt` and target the same V6.1.4-derived source. A blind overlay order is unsafe: applying Final-Hours after duplicate can restore the repeat fallback; applying duplicate after Final-Hours can discard Final-Hours decision wiring, Tehran planning, adaptive block size, SIM review witness, and schema-4 integration.

**Required disposition:** Foreman must perform a source-level three-way merge, then run both `verify_final_hours_v615.py` and `verify_a2_duplicate_session.py` plus a mass selection gate. The merged repository must contain Final-Hours decision input and the duplicate overlay’s evidence-family/no-repeat selection path.

### 2. SIM review witness is not atomically coupled to session completion — FAIL, safe helper supplied

Final-Hours `finishReview()` first calls `dao.markSimulationReviewed()` and then separately calls `dao.upsertSession(active.copy(phase = "done"))`. If the process dies after the first write, `reviewedEpochMs` can unlock SIM2 while the active session remains in `review`. This violates the requirement that the user must complete review before the next simulation is eligible.

**Safe helper fix:** `parallel/help-a3-independent-persistence-review` supplies a one-file delta that wraps both operations in `database.withTransaction { ... }`. It changes no schema, bank, IDs, selection, or UI behavior.

### 3. Restore/session validation boundary remains too permissive — FAIL / follow-up required

The restore path checks the installed bank for attempt IDs and checks active-session question eligibility, but it does not fully validate active-session JSON shape, option order, positions, duplicate IDs, answer bounds, confidence/error values, due-credit source IDs, simulation question IDs, or duplicate attempt rows before replacing progress. The Question Map helper correctly rejects empty/duplicate ID lists, but that rejection occurs when projecting the state, after the payload has already entered Room.

**Required disposition:** Add a pre-restore validator that rejects or quarantines malformed payloads before clearing existing state, and add malformed-session, malformed-credit, duplicate-attempt, and rollback fixtures. Preserve the existing pre-restore snapshot behavior.

### 4. Standard persistence branch has not advanced — FAIL / coordination status

At review time, `parallel/a3-persistence-qa` still pointed at the baseline SHA `72dc76e56b7ae625ad1904c76910eeaec5f90f58`. Therefore, there was no advanced standard persistence implementation to certify. The review above certifies only the separately supplied overlay code and reports, not an integrated persistence worker branch.

## Safe helper delta

| Artifact | Purpose | SHA / status |
|---|---|---|
| `radiology_v615_a3_independent_persistence_review/overlay-delta.tar.xz` | Atomic `finishReview()` transaction around SIM reviewed witness plus active-session `done` transition | Generated from the Final-Hours overlay; SHA recorded in the handoff commit |
| `reports/parallel/A3_INDEPENDENT_PERSISTENCE_CROSS_REVIEW.md` | This independent PASS/FAIL review | New helper-branch report |

The helper delta must be applied only after the Foreman has selected and merged the Final-Hours repository version. It must not be applied as a blind replacement over a newer standard persistence worker branch.

## Required Foreman reruns

Before any release claim, the Foreman must run the v3→v4 Room migration fixture, malformed restore rollback test, active-session process-recreation test, Question Map device flow, full-stem Review flow, merged no-repeat/evidence-family mass selection gate, unique-mastery regression, Final-Hours Tehran/midnight/SIM tests, Kotlin/JVM/lint/debug/release gates, signed APK and bank verification, API 35 instrumentation, install/launch, and progress-preservation checks. Every gate must have observed output; worker reports and compiled tests alone are not release proof.

## References

[1]: https://github.com/rynmrde/Konkor/commit/72dc76e56b7ae625ad1904c76910eeaec5f90f58 "Pinned Konkor baseline commit"
[2]: https://github.com/rynmrde/Konkor/commit/aa004509f2dacf50ade853eda36a7a76ae2cd6a5 "Final-Hours overlay branch tip"
[3]: https://github.com/rynmrde/Konkor/commit/77d55808293f7258a36de0e3f1e57166233c70a7 "Duplicate/mastery overlay branch tip"
[4]: https://github.com/rynmrde/Konkor/commit/ad25e780b115d2bc144d6d3218c8104f0fb5bae5 "Review/Question Map branch tip"
[5]: https://github.com/rynmrde/Konkor/commit/c6360595b852bad956296b1f820ab9c69c952e28 "Question Map persistence helper branch tip"