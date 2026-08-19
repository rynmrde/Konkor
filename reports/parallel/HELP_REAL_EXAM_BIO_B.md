# Helper Report — Official Real-Exam Source Recovery and Quarantine Guard

## Baseline and helper scope

This independent helper branch, `parallel/help-real-exam-bio-b`, was created from the currently pinned GitHub `main` commit [`72dc76e56b7ae625ad1904c76910eeaec5f90f58`](https://github.com/rynmrde/Konkor/commit/72dc76e56b7ae625ad1904c76910eeaec5f90f58). It follows completion of Biology-B’s deterministic W04 scientific cohort and targets the highest-priority remaining scientific-evidence bottleneck: recovery of official Sanjesh source/key paths for recent real-exam and quarantine evidence.

No question payload, answer key, source label, source type, access pool, holdout membership, quarantine state, stable ID, bank digest, or Room-progress identity was changed. This is an audit-only helper delivery.

## Independent official notice recovery

The official public Sanjesh notices were extracted directly. They establish session/year/document paths but do not by themselves resolve a quarantined key discrepancy. The 1404 N1 notice is deliberately documented as **wrong-session evidence** for the 1404 N2 quarantine record and is not used to promote, rekey, or authenticate that item. [1] [2] [3]

| Session | Official notice evidence | Direct official booklet/key paths observed | Retrieval result in this helper |
|---|---|---|---|
| 1402 N2, Experimental Sciences | Notice dated 1402/04/14 identifies the second session | Biology: `.../1402/sar/qtir/tajrobi/tajrobi.pdf`; key: `.../1402/sar/keys/tajrobi.pdf` | Both HTTPS requests returned **403** |
| 1403 N1, Experimental Sciences | Notice dated 1403/02/06 identifies the first session | Biology: `.../1403/sar/stage1/note/tajrobi/zist.pdf`; key: `.../1403/Sar/Stage1/Keys/tajrobi.pdf` | Both HTTPS requests returned **403** |
| 1404 N2, Experimental Sciences | No official N2 publication record was recovered | None recovered | **Still unresolved** |
| 1404 N1, Experimental Sciences | Official notice dated 1404/02/11 | Biology: `.../1404/sar/qnote/tajrobi/1.pdf`; key: `.../1404/sar/keys/tajrobi.pdf` | Excluded as wrong-session evidence for 1404 N2 |

> **Conservative conclusion:** A path shown in an official notice establishes the official session family, but a 403 response does not supply the authoritative document bytes or answer-key comparison needed to resolve a historical key conflict. No record is promoted from `QUARANTINE` on this basis.

## Frozen contract revalidation

The checksum-pinned verified JSON was downloaded read-only through the authorized Drive connection. SHA-256 matched the required immutable reference: `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d`. The inherited non-disclosing invariant audit was rerun against that exact file.

| Gate | Observed result |
|---|---|
| Verified JSON SHA-256 | **PASS** — `54f349…263d` |
| Question identity and four-option/key contract | **PASS** — 1,216 unique questions |
| Source-type counts | **PASS** — authored 1,112; official-stem training 71; active real exam 17; quarantine 16 |
| Active recent real-exam contract | **PASS** — 17 active recent records, all 1403 N1 inside-Iran as expected |
| Recent quarantine contract | **PASS** — exactly three, one each in 1402 N2, 1403 N1, and 1404 N2; all remain human-review-only and safety-ineligible |
| Holdout integrity | **PASS** — SIM1 117, SIM2 117, FINAL 10; pairwise disjoint and blueprint-exact |
| Direct official PDF/key probes | **PASS as documented negative evidence** — 4/4 paths returned 403; no bytes accepted as source evidence |

The helper deliberately does not print or store SIM1/SIM2/FINAL question identifiers, stems, options, crop data, or answers.

## Integration and safety notes

This helper report may be used to update the Foreman’s evidence log. It is **not** authority to change any source URL, answer key, `official_origin` flag, frequency claim, quarantine status, or safety eligibility. A future resolution requires a successfully retrieved official key for the exact year/session and an observed comparison at the relevant question number. Non-official mirrors may be locator material only and cannot establish correctness or authenticity.

No bank migration is required because the bank was not edited. The missing official 1404 N2 publication record remains a release-evidence blocker for resolving that single historical conflict, not a basis for reducing the active real-exam count or altering the frozen V6.1 hash.

## References

[1]: [Sanjesh — 1402 second-session question booklets and key](https://sanjesh.org/fa-IR/sanjesh/4936/news/view/14591/10633/Staging)

[2]: [Sanjesh — 1403 first-session question booklets and key](https://sanjesh.org/fa-IR/sanjesh/4936/news/view/14591/11277/Staging)

[3]: [Sanjesh — 1404 first-session question booklets and key; wrong session for 1404 N2](https://sanjesh.org/fa-IR/sanjesh/4936/news/view/14591/11941/Staging)

[4]: [Prior 1402–1404 source and holdout audit](https://github.com/rynmrde/Konkor/blob/parallel/real-exam-1402-1404/reports/parallel/REAL_EXAM_1402_1404.md)
