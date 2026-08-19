# HELP A1 — Official-Source Geology 153 Blocker

**Worker role:** Official-source / real-exam / key / quarantine authority — post-completion helper assignment  
**Account label:** `KONKOR-A1-M1-OFFICIAL`  
**Helper branch:** `parallel/help-a1-official-geo153`  
**Baseline:** `origin/main` commit `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
**Scope:** `real_1401_in_geo_153` only. No merge to `main`, no release, and no mutation of the immutable frozen bank.

> **Decision:** The official booklet proves the original stem and exposes the fallback-text corruption. However, the official Sanjesh answer-key endpoint was not readable in this environment, and the frozen record expressly declares `official_key_verified=false` and `needs_official_key_reconciliation=true`. Therefore no corrected raw stem/options/key is published as bank truth. The required release-safe outcome is a **single-ID delivery exclusion** until a readable official key reconciles the item.

## Frozen-record and evidence ledger

| Field | Frozen value or evidence | Consequence |
|---|---|---|
| ID | `real_1401_in_geo_153` | Exact, single-item scope. |
| Source type | `official_exam_stem_training` | Official-origin training stem; not a verified `real_exam` record. |
| Booklet provenance | 1401, domestic session, `zamin 401 nobat1,2.pdf`, page 3, question 153 | The stored authoritative booklet crop is traceable to the source file. [1] |
| Official-key provenance | `https://result2.sanjesh.org/Keys/Sarasari1401/NOET/Questionskey.aspx` | Direct internal-browser retrieval closed the connection; this is an access limitation, not key evidence. [2] |
| Current key state | `correct_index=1`, `official_key_verified=false`, `needs_official_key_reconciliation=true` | The stored index cannot be promoted or silently corrected. |
| Delivery flags | `TRAIN`, `selected_scope=true`, `eligible_for_training=true`, `needs_human_review=true`, `eligible_for_safety_evidence=false` | Guard old sessions and every non-safe delivery path; do not rely solely on normal safe-only selection. |
| Holdout state | `eligible_for_simulation=false`; absent from SIM1/SIM2/FINAL | No protected-pool change is needed. |

## Booklet finding and reconstruction boundary

The high-resolution, page-coordinate rendering of the official booklet confirms this stem:

> `۱۵۳- دامنة امواج زمین‌لرزه‌ای با بزرگی ۷ ریشتر، به ترتیب چند برابر دامنة امواج زمین‌لرزه‌های ۶ و ۸ ریشتری است؟`

The rendered booklet also visibly contains four mathematical options. Its right-to-left print layout supports the visual pairs below, but no replacement database text is issued because the options’ RTL fraction ordering is presentation-sensitive and, more importantly, the official key could not be read. A formula-based inference must not substitute for the official answer key.

| Printed option label | Visual content from official crop | Bank-repair status |
|---|---|---|
| ۱ | `۲ ، ۱/۲` | Not published as corrected raw option text. |
| ۲ | `۱۰ ، ۱۰` | Not published as corrected raw option text. |
| ۳ | `۱ ، ۱/۳۱/۶` | Not published as corrected raw option text. |
| ۴ | `۱۰ ، ۱/۱۰` | Not published as corrected raw option text. |

The frozen fallback instead contains malformed fragments such as `، ۲` and `۳۱/۶،`; the source crop’s own display contract already says the crop is authoritative. This proves a learner-visible corruption risk, especially because the existing review UI renders both the crop and the fallback stem/options.[1] The available booklet proves the question text, but does **not** by itself prove the official keyed option. The requested exact reconstruction threshold is therefore not met.

## Required safe exclusion overlay

The integration-ready patch is `overlays/geo153/HELP_A1_OFFICIAL_GEO153_EXCLUSION.patch`. It introduces `QuestionDeliveryExclusions.GEO153` and blocks only `real_1401_in_geo_153`. It does **not** edit the frozen DB, gzip, question row, source metadata, source crop, stored answer index, prior attempts, mastery, backups, or simulation history.

| Delivery surface | Overlay control | Safety result |
|---|---|---|
| New TRAIN selection | `poolIds`, `trainingCandidates`, and `distinctAlternative` reject the blocked ID. | The item cannot be selected through ordinary, due-credit, remediation, or last-resort candidate paths. |
| SIM1/SIM2/FINAL | `simulationIds` asserts that a blocked ID cannot occur in a protected pool. | Current holdouts remain disjoint; any future accidental leak fails closed. |
| Session creation | A final `ids.none(QuestionDeliveryExclusions::blocks)` assertion occurs before persistence. | No newly persisted active session can contain the item. |
| Session resume and test/review rendering | `sessionCompatible`, `activeSummary`, and `startOrResume` classify a session containing the item as incompatible. | The item is withheld before a test or review question is returned. |
| Existing active session | Existing repository behavior snapshots raw JSON then closes only the incompatible active session. | Prior attempts, mastery, settings, backups, and raw session evidence are preserved. |
| Submit boundary | `submit` requires compatibility. | A stale incompatible session fails closed rather than generating a new scored attempt from the malformed item. |

> **Integration requirement:** Apply the overlay as one coherent change and run the listed repository and instrumentation tests. A selector-only patch is insufficient because active test/review sessions and restored backups can otherwise reach the malformed fallback text.

## Deterministic safety checks

`tests/verify_geo153_exclusion_overlay.py` completed with the following factual results.

| Gate | Result | Evidence |
|---|---|---|
| Exact ID scope | PASS | Exactly one frozen question matches `real_1401_in_geo_153`. |
| Unresolved-key flags | PASS | The item is official-origin training, has `official_key_verified=false`, and requires official-key reconciliation. |
| Holdout integrity | PASS | `SIM1 ∪ SIM2 ∪ FINAL` contains 244 IDs; the target is absent from all pools. |
| New-selection coverage | PASS | The overlay covers pool, simulation, candidate, and alternative selection APIs. |
| Resume/review coverage | PASS | The overlay covers compatibility, active summary, resume, and submit boundaries. |
| Progress preservation | PASS | The existing incompatible-session contract snapshots raw session JSON before closing only the active session. |
| Immutable-bank mutation | PASS | Overlay contains no bundled-bank asset, gzip, SQL update, source metadata, or question-row mutation. |

## Handoff condition

The item may be reconsidered only when a readable official Sanjesh key or notice identifies the exact 1401 domestic experimental-science booklet, question 153, and keyed option. At that point, a standard worker should compare the official key with the booklet crop, repair the raw visible fallback fields with bidirectional-rendering tests, preserve the stable ID and progress, and remove this exclusion only after test/review/resume/migration gates pass.

## References

[1]: https://drive.google.com/drive/folders/1lV90myeWo3jl5sBsbBbV2MU-InI3d2nL "Authoritative project archive — Geology folder"
[2]: https://result2.sanjesh.org/Keys/Sarasari1401/NOET/Questionskey.aspx "Stored official Sanjesh 1401 key endpoint"
