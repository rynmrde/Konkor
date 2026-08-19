# Independent Biology/Geology Cross-Review

**Reviewer role:** Lite independent reviewer  
**Review branch:** `parallel/review-lite-bio-geo`  
**Baseline:** `origin/main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
**Standard branch reviewed:** [`parallel/a1-biology-geology`](https://github.com/rynmrde/Konkor/tree/parallel/a1-biology-geology)  
**Frozen bank checked:** V6.1 expanded SQLite, SHA-256 `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`  
**Review policy:** No `main` change, release, scientific rewrite, key change, ID change, or frozen-artifact mutation.

## Executive conclusion

The standard Biology/Geology branch’s renderer fix is **effective as a branch-local presentation fix**, and the companion Biology patch validators **PASS against the actual frozen V6.1 SQLite bank**. The standard branch report is not fully self-contained for bank applicability: its branch diff contains the renderer, test, and report, but not the bank or Biology patch payloads. Full applicability is nevertheless independently established by executing the v6.1.5 compact-patch verifier and W04 full-bank verifier against the immutable Drive artifact.

The principal release-relevant failure is an **unreported eight-ID conflict between the v6.1.5 and W04 Biology analysis patches**. Each patch is internally unique, but the following IDs occur in both patches with different analysis fields: `v3_bio_09_01`, `v3_bio_10_01`, `v3_bio_11_01`, `v3_bio_12_01`, `v3_bio_13_01`, `v3_bio_14_01`, `v3_bio_15_01`, and `v3_bio_16_01`. The integrator must reconcile these overlaps and define deterministic patch order or a merged successor patch before integration.

## PASS/FAIL matrix

| Issue | Result | Independent evidence | Handoff meaning |
|---|---|---|---|
| Exact IDs within v6.1.5 patch | **PASS** | 16 updates, 16 unique IDs; the standard compact verifier returned `BIOLOGY_V615_COMPACT_PATCH_OK`. | Safe on its declared immutable base. |
| Exact IDs within W04 patch | **PASS** | 145 updates, 145 unique IDs; W04 validator passed exact lexicographic positions 146–290 and W03/W04 disjointness. | Safe on its declared immutable base. |
| Cross-patch ID identity | **FAIL** | Eight overlapping IDs have different `correct_analysis`, `distractor_analyses`, and `short_lesson` values. | Reconcile before applying both patches; do not silently let order decide. |
| Patch base identity | **PASS** | Both patches declare the frozen DB SHA `d63219dd…b3673c`; downloaded DB independently hashed to the exact value. | Patch base is the expected V6.1 expanded bank. |
| Full-bank applicability | **PASS with scope caveat** | The v6.1.5 and W04 validators executed against the downloaded 30,720,000-byte SQLite bank. | The companion patch branches are executable against the full bank. The standard A1 branch itself does not carry the bank or patch files in its diff. |
| Raw-enum presentation fix | **PASS on standard branch; NOT INTEGRATED on main** | Applying the standard `ScienceText.kt` label map to all 585 active Biology/Geology records removed all independently detected raw-label occurrences: 1,403 before normalization and 0 remaining. | Integrate the renderer branch and run its JVM/UI gates; do not infer that frozen bank bytes were cleaned. |
| Generic-analysis stock-filler fix | **PASS for covered stock fillers; residual content FAIL** | The same renderer contract removed 9,264 detected stock-filler occurrences, leaving 0 of those exact patterns. Three W04 records still triggered independent vague/generic wording flags: `v3_bio_12_08`, `v3_bio_15_11`, `v3_bio_16_13`. | Renderer cleanup is effective; those three records still need scientific wording review. |
| Biology malformed options in W04 patch | **PASS** | All five supplied option repairs have four non-empty options; W04 verifier also checked the exact option-repair set. | No deterministic option defect remains in the supplied W04 payload. |
| Geology malformed options | **FAIL / unresolved** | `real_1401_in_geo_153` remains in the frozen bank with visibly corrupted options such as `"، ۲"` and `"۳۱/۶،"`, despite a valid amplitude-ratio explanation. | Do not auto-rewrite. Reconstruct the authoritative source and create a versioned bank repair or quarantine decision. |
| Paired-statement visibility | **PASS for the applied W04 repairs** | Six IDs receive explicit `A)`/`B)` stems: `v3_bio_10_11`, `v3_bio_11_07`, `v3_bio_12_07`, `v3_bio_14_10`, `v3_bio_15_15`, `v3_bio_16_10`. The remaining five manual repairs receive concrete four-option payloads, including the four former table-row references and the immune causal-chain repair. | The patched W04 payload makes the required statements/options visible. Preserve the exact payload and test it in the packaged bank. |
| Report wording “ten incomplete A/B-or-table references” | **FAIL as stated / needs precision** | Independent extraction found six explicit paired-statement stems and five option repairs, of which four replace table-row placeholders and one repairs the immune causal chain. | Update the handoff wording to distinguish six A/B stems, four table-reference option repairs, and one causal-chain option repair. |
| Scientific bank rewrites on standard branch | **PASS** | Standard A1 branch changed no bank bytes or question IDs; its diff is renderer, regression test, and report only. | Safe from silent frozen-bank mutation; material fixes remain separate. |

## Exact full-bank evidence

The downloaded frozen SQLite contained 596 Biology/Geology records, with the exact subject labels `زیست` (411 records) and `زمین` (185 records). After excluding 11 obsolete/quarantine/holdout records, the active review population was 585 records: 408 Biology and 177 Geology. The expanded DB hash matched the immutable project value, and the database passed the standard W04 validator’s `PRAGMA quick_check` and structural checks.

The standard branch’s `ScienceText.kt` maps the internal taxonomy labels to Persian learner-facing labels and removes only enumerated stock review lead-ins. Independent application of that same mapping to all active Biology/Geology analysis text removed all 1,403 detected raw-label occurrences and all 9,264 occurrences of the covered stock-filler patterns. This is a presentation-layer result; the frozen bank still contains the original analysis strings and must not be described as byte-rewritten.

## Exact patch and paired-statement evidence

The v6.1.5 compact patch has 16 analysis-only updates and no supplied stem/options/key fields. Its own verifier reconstructed the patch against the frozen gzip and preserved the expected question count and source-type counts. The W04 patch has 145 updates, all 145 exact W04 cohort IDs, and no overlap with the W03 cohort selected by its verifier. Its manual repair manifest contains 11 IDs.

Six of those 11 IDs receive explicit paired statements in the patched stem. Four receive full statement options replacing opaque table-row choices: `v3_bio_11_24`, `v3_bio_14_20`, `v3_bio_15_24`, and `v3_bio_16_16`. The remaining `v3_bio_13_15` option repair replaces a malformed causal chain and is not a paired-statement/table repair. The independent comparison against the immutable original confirmed that the original records used either the opaque `دربارهٔ دو عبارت A و B` stem or `با توجه به جدول` stem; the W04 payload supplies the missing visible content for every listed manual repair.

## Safe helper fix

This review branch adds `tools/independent_bio_geo_review.py`. The helper is deterministic and non-mutating. It verifies the frozen DB hash, per-patch update counts and unique IDs, required analysis fields, supplied-option shape, paired-statement markers, exact Biology/Geology subject labels, and cross-patch overlap/conflict IDs. It does not rewrite any bank record or alter any scientific content.

The helper’s new cross-patch check is the only implementation change made by this independent review. No source, answer key, stable ID, holdout, or release artifact was changed.

## Required integrator actions

Before integration, reconcile the eight conflicting cross-patch IDs and record which analysis wins or merge them into one deterministic successor overlay. Integrate the standard renderer and test only after this conflict is resolved. Retain the Geology record `real_1401_in_geo_153` as unresolved until authoritative source reconstruction is complete. Correct the report’s repair-count wording, then run the full Kotlin/JVM/lint/Android/package/migration/Review/Question Map gates on the integrated tree.

## References

[1]: [Standard Biology/Geology branch and report](https://github.com/rynmrde/Konkor/tree/parallel/a1-biology-geology)  
[2]: [Frozen V6.1 Drive folder](https://drive.google.com/drive/folders/1R2IovFE_e0O_vU4IBCSiJpqrwK4LecxK)  
[3]: [Biology v6.1.5 patch branch](https://github.com/rynmrde/Konkor/tree/parallel/bank-biology)  
[4]: [Biology W04 patch branch](https://github.com/rynmrde/Konkor/tree/parallel/bio-b)  
[5]: [Independent review branch](https://github.com/rynmrde/Konkor/tree/parallel/review-lite-bio-geo)
