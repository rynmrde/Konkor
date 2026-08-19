# Lite A1 Official-Source Support Report

## Worker identity and baseline

| Field | Observed value |
|---|---|
| Role | `KONKOR-A1-L1-OFFICIAL-SUPPORT` |
| Account label | `A1` |
| Repository | [`rynmrde/Konkor`](https://github.com/rynmrde/Konkor) |
| Current ref | `refs/heads/main` |
| Newest origin/main SHA | `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Access route | Existing enabled Composio connector → active GitHub account `github_senam-unware` |
| Read-only proof | `GITHUB_GET_A_REPOSITORY` returned `rynmrde/Konkor`, default branch `main`, pushed timestamp `2026-08-19T13:14:39Z` |
| Worker write scope | No GitHub write, merge, release, or scientific-bank mutation performed |

The mandatory connector precheck succeeded after the explicit task override. The existing `composio` connector was enabled, its GitHub toolkit connection was reported `ACTIVE`, and a minimal read-only repository metadata call succeeded. No standalone GitHub or Google Drive connector was used.

## Repository and artifact inventory

The current `origin/main` tree contains the Android project shell, historical rescue patch directories, and patch archives. It does **not** expose the frozen verified JSON bank, gzip bank, or SQLite database as individual repository paths. The newest rescue overlay is available as `radiology_v614_rescue_patch/overlay.tar.xz`; its manifest and selected validator/model files were decoded through the Composio-fetched response.

| Artifact or assertion | Evidence observed |
|---|---|
| Current main commit | `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Historical overlay baseline recorded in manifest | `67c4618120438a58ed31401d50338c661efe7615` |
| App identity in manifest | `com.rynmrde.konkor`, versionCode `165`, versionName `6.1.4` |
| Frozen verified JSON hash | `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d` |
| Frozen source gzip hash | `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14` |
| Frozen expanded SQLite hash | `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c` |
| V6.1.4 overlay hash | `d17bdd905def35a45caa32aa5a0b07b6196ecc78de493a340bf36fac0c0103c3` |

The mismatch between the current `main` SHA and the older commit recorded in the rescue manifest is a **baseline-drift finding**, not evidence of a bank change. The primary worker must verify the current packaged bank and current workflow before relying on historical manifest claims.

## Deterministic source and status findings

The manifest and validator/model code preserve the following bank-level claims: **1,216 total questions, 17 claimed verified real-exam records, 1,112 authored records, 71 official-stem training records, 16 quarantined key-conflict records, 56 microtopics, and 104 official-source crops**. The validator asserts four-option questions, valid correct indices, bank hashes, SQLite `PRAGMA quick_check`, 56 coverage rows, 16 `access_pool='QUARANTINE'` rows, and authored-only eligible simulation items.

The Kotlin question model explicitly supports `source_type`, nullable `source_file`, nullable `source_page`, `official_key_verified`, `source_crop`, `source_crop_sha256`, `needs_human_review`, `eligible_for_safety_evidence`, and `access_pool`. The model therefore provides the fields needed for record-level source verification, but the actual question rows were not present as a readable repository file in the current tree. Consequently, this worker found **no defensible record-level candidate list** for individual real-exam rows, missing pages, year/session inconsistencies, or source-file mismatches. It would be unsafe to infer those candidates from aggregate counts or to fabricate them.

| Audit category | Result | Required interpretation |
|---|---|---|
| Claimed `real_exam` records | Aggregate count `17` observed; individual rows unavailable | Requires direct frozen-bank inspection through Composio Drive or a repository-exposed bank artifact |
| Missing or weak source fields | Not determinable from patch-only payload | Do not promote or demote records until rows are inspected |
| Year/session/question-number inconsistencies | Not determinable | Compare every real-exam row against authoritative booklet/key evidence |
| Obsolete rows | Not determinable from patch-only payload | Run bank-level obsolete and selected-scope queries |
| Quarantine | Expected count `16`; validator asserts `access_pool='QUARANTINE'` count `16` | Confirm all remain excluded from training and both SIM pools |
| Holdout/SIM eligibility | Validator/model rules observed | Require authored, eligible, not human-review, and matching access-pool checks |
| Source crops | Validator asserts `104` | Verify crop hash and source-file/page linkage in the actual bank |
| Scientific answers | No changes | This support worker made no answer or explanation edits |

## Candidate list and machine-readable handoff

The machine-readable candidate list is saved at [`LITE_A1_OFFICIAL_SOURCE_CANDIDATES.json`](./LITE_A1_OFFICIAL_SOURCE_CANDIDATES.json). It records the current baseline SHA, the aggregate claims, the source-payload gap, and the exact follow-up queries that require the frozen JSON or SQLite artifact. The list intentionally contains no fabricated question IDs or source citations.

The highest-priority unresolved blocker is **access to the frozen bank rows through the already connected Composio route**. Once the authoritative bank is available, the primary or official-source worker should enumerate `source_type='real_exam'`, `source_type='official_exam_stem_training'`, and `source_type='quarantined_key_conflict'`; validate source file/page and official key fields; compare years and sessions; and verify that quarantine and SIM disjointness hold. Historical hashes must be checked before and after any read-only extraction, and archived artifacts must not be overwritten.

## References

[1]: https://github.com/rynmrde/Konkor "Konkor repository"

[2]: https://github.com/rynmrde/Konkor/tree/72dc76e56b7ae625ad1904c76910eeaec5f90f58 "Konkor at current origin/main baseline"

[3]: https://github.com/rynmrde/Konkor/blob/72dc76e56b7ae625ad1904c76910eeaec5f90f58/radiology_v614_rescue_patch/MANIFEST.txt "V6.1.4 rescue overlay manifest"

[4]: https://github.com/rynmrde/Konkor/blob/72dc76e56b7ae625ad1904c76910eeaec5f90f58/radiology_v614_rescue_patch/overlay.tar.xz "V6.1.4 rescue overlay archive"
