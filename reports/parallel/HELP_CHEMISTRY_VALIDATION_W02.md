# Helper Preflight: Chemistry V6.2 Candidate

**Helper worker:** `KONKOR-W02-REAL-RECENT`  
**Helper branch:** `parallel/help-chemistry-validation-w02`  
**Baseline:** `72dc76e56b7ae625ad1904c76910eeaec5f90f58` (`main`)  
**Chemistry candidate branch reviewed:** `parallel/bank-chemistry` at `2a9b001e7d7f534affec3aed80fa4c33913fac28`  
**Helper implementation commit:** `94910d23bfe08cf925ffee5bea50c047d44bae34` (published helper branch)  
**Local helper commits:** `d0240acb12a183dec709746a53ca5d73d5ad6d9f`, `ddda99c069533538875d7af4e6e868ac02f9b694`

## Scope

This helper task independently preflighted the transport-split V6.2 Chemistry overlay because the Chemistry QA report declares that Kotlin compilation, JVM tests, lint, packaging, instrumentation, install/launch, and persistence gates remain release-authority work. It did **not** edit the Chemistry worker branch, the frozen V6.1 bank, main, or any release.

The eight overlay parts were reconstructed in a disposable directory without executing worker-provided code. The reconstructed `overlay.tar.xz` SHA-256 was observed as `1e47e59d162b25407eeafd08cb2d251a385c84e4a60b56fb16186ac5004f9502`, exactly matching the candidate manifest. Archive listing showed only the expected V6.2 gzip bank and `BankStore.kt` overlay files.

## Independent preflight result

| Check | Observed result |
|---|---:|
| Reconstructed Chemistry overlay archive SHA-256 | **PASS** — `1e47e59d162b25407eeafd08cb2d251a385c84e4a60b56fb16186ac5004f9502` |
| Candidate gzip SHA-256 | **PASS** — `47ba0670e5c3b22e5823dfb577ade40267f530fd40f7d4a2b8c8119b9f67cbce` |
| Candidate expanded SQLite SHA-256 | **PASS** — `ed84693259455e6da488af23a7fa39c6548ea64e95bee6a93ba5cedf8f7656c6` |
| Candidate SQLite `PRAGMA quick_check` | **PASS** |
| Candidate IDs / four options / valid key / non-empty correct analysis | **PASS** — 1,221 unique records |
| Source-type counts | **PASS** — authored 1,117; official-stem training 71; real exam 17; quarantined conflict 16 |
| Access-pool counts | **PASS** — TRAIN 961; SIM1 117; SIM2 117; FINAL 10; QUARANTINE 16 |
| SIM1/SIM2/FINAL counts and pairwise isolation | **PASS** — 117 / 117 / 10; overlap 0 |
| Simulation blueprint exact membership | **PASS** |
| Protected real-exam and quarantine records checked | **PASS** — 33 present; no identity, source, key, options, analysis, or content changes |
| Allowed review-default-only changes | 7 Chemistry records: 2 active real-exam and 5 quarantine records; no content or safety-state changes |

The helper preflight initially treated every JSON-field change in protected records as prohibited, which failed. A non-disclosing field-level comparator showed that the only changes were `review_default` preferences on seven Chemistry records; there were no option, key, stem, explanation, source, pool, eligibility, or quarantine-state changes. The preflight was narrowed appropriately: review preference may change, while all protected identity/content fields remain invariant.

## Files added on this helper branch

| File | Purpose |
|---|---|
| `helper_chemistry_candidate_preflight.py` | Independent non-disclosing candidate checker for checksum, SQLite, structural, source/pool, protected-record, and holdout invariants. |
| `compare_candidate_immutable_records.py` | Diagnostic comparator that reports only affected real/quarantine IDs and changed field names; it does not print question or holdout content. |
| `reports/parallel/HELP_CHEMISTRY_VALIDATION_W02.md` | This integration handoff. |

**Bank-ID and migration implications:** This helper branch changes no bank data and requires no Room migration. The chemistry candidate itself is a separately versioned V6.2 asset and must retain V6.1 assets/evidence. Its cache separation still requires the foreman to prove active-session compatibility, review rendering of retired IDs, backup/restore behavior, and no unique-mastery inflation after migration.

## Integration notes

The integrator may use the helper preflight scripts as an additional static gate only after reconstructing the Chemistry overlay. The two scripts intentionally assume the extracted candidate at `.helper_chemistry/extracted/`; production integration should either reproduce that directory or adapt the paths without weakening assertions.

This **does not** clear the final release gates. In particular, the foreman must still validate combined V6.1.4 and V6.2 overlay ordering, update version/hash-aware workflow checks deliberately, build and sign the APK, inspect packaged assets, run Android API 35 instrumentation, and exercise Review, Question Map, process recreation, migration, duplicate-free normal sessions, intentional review, and final-hours behavior.
