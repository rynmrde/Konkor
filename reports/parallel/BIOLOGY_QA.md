# Biology Question-Bank and Analysis Quality Report

## Scope and baseline

This worker audited **Biology only** against the newest available repository baseline: `main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58`, which corresponds to the published **V6.1.4 Three-Day Rescue** release. The release’s immutable base bank remains unchanged: its expanded SQLite SHA-256 is `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c` and its gzip SHA-256 is `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`.

The audit used the supplied official Iranian Biology textbooks for grades 10–12 after confirming their title pages, and inspected the supplied 1403 first-session Biology source booklet. The latter contains the stem corresponding to `real_1403_n1_bio_016`, but the supplied source set did not provide a separately authoritative answer key capable of verifying the fifteen `real_1403_n1_bio_*` records. Those records are therefore treated conservatively, rather than being silently trusted as verified real-exam questions. [1] [2] [3] [4]

| Baseline item | Verified value |
|---|---|
| Repository and branch | `rynmrde/Konkor`, `main` |
| Baseline commit | `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Baseline release | `radiology1405-apk-v6.1.4-20260817` |
| Biology inventory | 411 total: 369 authored, 24 official-stem training, 15 `real_exam`, and 3 quarantined conflicts |
| Active machine-scan scope | 408 active records; 3 quarantined conflict records excluded |
| Worker branch | `parallel/bank-biology` |

## Audit method and counts

The all-item deterministic scan checked active Biology records for malformed option sets, invalid keys, missing or generic explanations, raw UI/internal enums, source-label safety, implausibly short distractors, and exact/near duplicate candidates. The final-hours deep review included the rescue-visible high-priority set: one top-priority authored TRAIN record for every Biology microtopic, together with every unique high-priority generic-analysis or short-option finding. The review was tied to the actual runtime selection path, which obtains only safe TRAIN alternatives and excludes `needs_human_review` records from rescue-safe evidence.

| Required count | Result | Interpretation |
|---|---:|---|
| Machine-scanned | 408 | All active Biology records; no active record was skipped. |
| Deep-reviewed | 44 | Rescue-priority and machine-flagged authored TRAIN subset. |
| Rewritten | 16 | Stable-ID authored TRAIN questions received question-specific analysis rewrites. |
| Replaced | 0 | No stem, option set, correct index, or question identity was replaced. |
| Analysis-rewritten | 16 | Correct explanation, all four option explanations, and short lesson rewritten per item. |
| Rejected | 15 | `real_exam` verification labels rejected, not question content: reclassified as key-unverified official-stem training. |
| Duplicate candidates flagged | 64 | 15 exact-stem, 15 identical-option-set, and 34 near/cosmetic candidates. |
| Raw UI/internal enums found | 0 | No `condition_wrong`, `truth_partial`, or comparable UI leakage found. |

The duplicate total is deliberately a **candidate** count rather than a false claim that all 64 are accidental duplicates. Repeated generic stems such as “کدام عبارت درست است؟” are not alone proof of duplicate learning content. The candidate list remains available for explicit pairwise adjudication; unique-mastery inflation must not be assumed away.

## Evidence-backed changes

Six of the rewritten questions are in the current Biology Tier-A rescue surface—gene expression, cell division, respiration, circulation, digestion, and endocrine regulation. The remaining ten supply the corresponding top-priority concept anchor for the other Biology microtopics. Each rewrite now identifies the precise biological process, gives a direct reason for the keyed option, states why every relevant wrong option fails, and removes generic “keyword/control/trap” filler.

| Question IDs | Change | Preserved invariants |
|---|---|---|
| `v3_bio_01_01`, `04_01`, `09_01`, `07_01`, `08_01`, `12_01` | Tier-A analysis rewrites for transcription direction, S phase/mitosis, gas-exchange pressure gradients, SA-node pacing, pepsin/bile/absorption, and insulin action. | ID, stem, options, key, pool, and source label preserved. |
| `v3_bio_02_01`, `16_01`, `05_01`, `15_01`, `11_01`, `10_01`, `14_01`, `03_01`, `13_01`, `06_01` | Top-priority rewrites for semiconservative replication, evolution, cellular respiration, plants, neurophysiology, nephron transport, reproduction, ABO/X-linked inheritance, immunity, and photosynthesis. | ID, stem, options, key, pool, and source label preserved. |
| `real_1403_n1_bio_003`, `010`, `012`, `014`, `016`, `019`, `022`, `024`, `028`, `029`, `032`, `033`, `041`, `042`, `044` | Reclassified from `real_exam` to `official_exam_stem_training`; `official_key_verified=false`, `needs_human_review=true`, and `eligible_for_safety_evidence=false`. | Original stem, figure/source-crop payload, options, key field, ID, pool, and all attempt references preserved. |

The compact runtime patch has a SHA-256 of `2e8b610ff4b488122c37d79d4bea9f61d401340925974da4763da5d6cc4ade55`. It applies transactionally to an app-private copy of the immutable V6.1 asset and must yield the patched runtime SQLite SHA-256 `4672be5706823b86e6187f9f3ddfbb929ce81af240f900b748de90848f087112` before the database is opened read-only. This approach preserves the archived bank in the APK and avoids any destructive replacement or Room migration.

## Validation

The compact patch verifier reconstructs the app-private database from the immutable gzip asset, applies every patch field in deterministic order, confirms `PRAGMA quick_check`, verifies the source-type counts, and asserts the exact patched SQLite checksum. The legacy static suite was also run against a staged tree containing the compact patch; it passed the packaged-base-asset check, native-experience static checks, UX checks, Day Selector checks, and V6.1.4 rescue triage/holdout checks.

| Validation | Result |
|---|---|
| `tests/verify_biology_v615.py` compact apply, SQLite integrity, count and patched-hash check | **PASS** |
| `tests/validate_v6_1.py` on compact staging tree | **PASS** |
| V6.1 packaged asset hash and base SQLite integrity | **PASS** |
| Rescue A15/B21/C20/Q0, 869 mandatory learning minutes, SIM isolation | **PASS** |
| Immutable V6.1 gzip retained beside compact patch | **PASS** |
| Candidate re-scan: unverified `real_exam` label findings | **0** |
| Candidate re-scan: raw UI/internal enum findings | **0** |

The candidate re-scan still reports **110 generic-filler instances**, down from 115, and **39 active human-review records**. Twenty-four are the pre-existing official-stem training items; the additional fifteen are the deliberately declassified 1403-N1 records. This is an honest residual-risk count, not a claim that all Biology explanations are now fully remediated.

## Files changed and integration instructions

The intended branch payload contains `app/src/main/assets/biology_v615_patch.json`, `app/src/main/java/com/radiology1405/prep/data/BankStore.kt`, and `tests/verify_biology_v615.py`. It additionally contains this report. The immutable `radiology1405_bank_v6_1.db.gz` asset is not replaced. `BankStore` verifies that immutable base asset, applies the compact Biology patch only when the private runtime copy is missing or does not match the patched hash, then opens the patched copy read-only.

> **Integration instruction:** Apply the compact patch files from `parallel/bank-biology` after checking the exact branch commit recorded below. Do not merge the earlier full-bank candidate artifact. Run `python3 tests/verify_biology_v615.py` and then `python3 tests/validate_v6_1.py`. Build/install instrumentation must additionally exercise first launch, process recreation, and a Biology rescue session so that the base-to-patched installation path—not only a pre-existing app database—is tested.

No Room migration is required because every question ID, stem, option set, correct index, access pool, and holdout assignment remains stable. Existing attempts and mastery rows continue to point to the same question IDs. The fifteen reclassified records are excluded from rescue-safe selection through the existing `eligible_for_safety_evidence` and `needs_human_review` gates.

| Commit record | Value |
|---|---|
| Baseline commit | `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Biology implementation commit | [`09ab5fc6ee77cd8b06af2a744b543836795320bc`](https://github.com/rynmrde/Konkor/commit/09ab5fc6ee77cd8b06af2a744b543836795320bc) |
| Report commit | This report update is committed separately to the same worker branch; no main/release action is authorized. |

## Unresolved risks

The remaining 64 duplicate candidates require item-by-item semantic adjudication before any question is removed, merged, or allowed to affect unique mastery. The remaining generic-analysis flags also need continued Biology-only review, with priority given to rescue-safe authored TRAIN questions. Finally, the fifteen declassified 1403-N1 records should remain out of the safety-evidence path until an authoritative Sanjesh answer key is obtained and independently mapped to each stable ID.

## References

[1]: https://drive.google.com/file/d/1H6V7321-jC8n3MByS4dQ1V2qDHnbrS6f/view "زیست‌شناسی (1), grade 10 official textbook"
[2]: https://drive.google.com/file/d/1Mjyb4dvdsQj51orLsYkvJoHKJBTw7Wjl/view "زیست‌شناسی (2), grade 11 official textbook"
[3]: https://drive.google.com/file/d/1bj2hURks0yOZSEtXJBZRHlzUh4gHBJ-l/view "زیست‌شناسی (3), grade 12 official textbook"
[4]: https://drive.google.com/file/d/1RLMr0QK1qYDfLduSzIwV2U_3UbYUH8Gm/view "1403 first-session Biology source booklet"
