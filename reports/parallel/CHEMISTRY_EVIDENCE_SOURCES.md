# Chemistry QA Evidence Sources

## Pinned Repository Baseline

The active GitHub default branch `main` was pinned at commit `72dc76e56b7ae625ad1904c76910eeaec5f90f58` before work began. The active release workflow was read from the pinned path [`.github/workflows/radiology-v614-rescue.yml`](https://github.com/rynmrde/Konkor/blob/72dc76e56b7ae625ad1904c76910eeaec5f90f58/.github/workflows/radiology-v614-rescue.yml). It downloads the frozen V6.1 project from Drive, verifies the bank hashes, and applies `radiology_v614_rescue_patch/overlay.tar.xz`.

## Frozen Project and Bank

| Resource | Authoritative location | Verified finding |
|---|---|---|
| Frozen Android V6.1 project | [Drive file](https://drive.google.com/file/d/14RbsAhiS1Cj3Y_JgPfR0pf1rmeXgxJUc/view) | ZIP MD5 `625cb4477fb4d27c99eb3a11760b13bf`; embedded gzip SHA-256 `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`; expanded DB SHA-256 `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c`. |
| V6.1.4 overlay | [GitHub path](https://github.com/rynmrde/Konkor/tree/72dc76e56b7ae625ad1904c76910eeaec5f90f58/radiology_v614_rescue_patch) | Overlay SHA-256 `d17bdd905def35a45caa32aa5a0b07b6196ecc78de493a340bf36fac0c0103c3`; static inspection showed the archive contains app source and validators but not the bank asset. |

## Supplied Official Chemistry Sources

| Resource | Drive source | Relevant verified evidence |
|---|---|---|
| Chemistry 1 / Grade 10 | [Shimi 10.pdf](https://drive.google.com/file/d/1rmRyR509x-8bDAS0FG6WiP9R5DtXjfXH/view) | PDF page 88 text states that the molar volume of one mole of gas at STP is **22.4 L**. This supports the candidate’s STP gas-volume calculations. |
| Chemistry 2 / Grade 11 | [Shimi 11.pdf](https://drive.google.com/file/d/15JZUrFMTgbTuWI0TkfpzUVfGCXhqIL1q/view) | Retrieved for scope cross-check. |
| Chemistry 3 / Grade 12 | [Shimi 12.pdf](https://drive.google.com/file/d/1G_aP6CYOsuGmkqdtcwMBvJXc6g4UorkF/view) | Retrieved for scope cross-check. |
| Official Chemistry archive folder | [Drive folder](https://drive.google.com/drive/folders/1HY_9LuGRtpqhpvSRyCdJH-Gce0j4Iacc) | Contains the supplied textbooks and 1398–1404 Chemistry booklets. |

> The candidate does not claim newly verified official-exam provenance for authored items. It labels the five new questions as textbook-bounded authored training and retains all recovered official questions’ source-provenance fields.

## Machine-Scan Baseline

The frozen V6.1 database passed `PRAGMA quick_check`. It contains 267 Chemistry records: 238 authored, 22 official-exam-stem training, 5 quarantined key-conflict, and 2 real-exam records. The scan identified review-facing raw internal labels and generic template language across most authored Chemistry reviews, five exact duplicate/cosmetic groups, and a 17-item highest-priority selected stoichiometry subset.

