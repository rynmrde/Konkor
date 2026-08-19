# V6.2 Chemistry QA Overlay Candidate

This isolated overlay is intended to be applied **after** the existing `radiology_v614_rescue_patch/overlay.tar.xz` during integration. It is not a release and does not modify a GitHub release or `main`.

The branch stores this binary archive as eight transport parts because the connected repository endpoint rejects a single payload above its size limit. Run `bash reassemble_overlay.sh` in this directory before extraction. The script joins the parts, verifies SHA-256 `1e47e59d162b25407eeafd08cb2d251a385c84e4a60b56fb16186ac5004f9502`, and validates the archive listing.

The overlay contains the immutable compressed asset `app/src/main/assets/radiology1405_bank_v6_2.db.gz` and an updated `BankStore.kt`. The loader opens a new `radiology1405_bank_v6_2.db` cache entry, verifies the expanded SQLite SHA-256, and keeps the V6.1 packaged asset archived. It does not alter the separate Room progress database, so past attempts remain intact. Five retired cosmetic-variant IDs are retained only as obsolete records; five distinct replacement IDs are added and no progress/mastery is transferred between them.

| Item | Value |
|---|---|
| Baseline main commit | `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Candidate expanded DB SHA-256 | `ed84693259455e6da488af23a7fa39c6548ea64e95bee6a93ba5cedf8f7656c6` |
| Candidate gzip SHA-256 | `47ba0670e5c3b22e5823dfb577ade40267f530fd40f7d4a2b8c8119b9f67cbce` |
| Candidate questions | 1,221 |
| Chemistry questions | 272 |
| Active selected Chemistry TRAIN questions | 203 |

Integration must update the release workflow and static validation intentionally for the V6.2 asset name/hashes/counts, retain V6.1 hash checks for the archived source, then run the full release-authority test matrix.
