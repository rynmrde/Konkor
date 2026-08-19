# Independent Physics Quantitative and Scientific Cross-Review

**Reviewed branch:** `parallel/a2-physics`  
**Reviewed commit:** `04b571947ab0c8c40b5025b121f8442a3e5911f2`  
**Baseline stated by worker:** `72dc76e56b7ae625ad1904c76910eeaec5f90f58`  
**Helper branch target:** `parallel/help-independent-physics-review`  
**Scope:** frozen V6.1.4 Physics bank, standard Physics report claims, deterministic counts/IDs, and spot scientific recomputation. No bank rewrite, main change, merge, or release was performed.

## Executive finding

The Physics worker’s core frozen-bank counts and most deterministic claims are independently reproducible. The immutable bank hashes match the project baselines, the Physics subject contains **187 records**, pool totals are **TRAIN 142 / SIM1 22 / SIM2 22 / FINAL 1**, source types are **authored 180 / official-stem training 7**, all records have four options and valid keys, and the exact short-analysis and comparison-stimulus ID lists match the report.

The review nevertheless returns **RELEASE BLOCKED / CONDITIONAL FAIL** because the report documents 168 raw learner-facing enum leaks, six short analyses, missing comparison-stimulus rendering, and ID-only normal-session exclusion. In addition, the report contains a factual record-ID error: it attributes the latent-heat calculation to `real_1402_n2in_phys_075`, while the bank shows that ID is the magnetic Lorentz-force question; the latent-heat question is `real_1404_n2in_phys_075`. No scientific key correction is requested from the reviewed calculations, but the report itself is not fully factually clean.

## Gate results

| Gate | Result | Independent evidence |
|---|---|---|
| Frozen gzip SHA-256 | **PASS** | `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14` |
| Expanded SQLite SHA-256 | **PASS** | `d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c` |
| Physics row count | **PASS** | 187 records in `question` for subject `فیزیک`. |
| Pool counts | **PASS** | TRAIN 142, SIM1 22, SIM2 22, FINAL 1; no QUARANTINE rows observed. |
| Source-type counts | **PASS** | Authored 180, official-stem training 7. |
| Four-option and key validity | **PASS** | Deterministic scan: no option-count or invalid-key IDs. |
| Raw-enum claim | **PASS as a count; FAIL as a release gate** | Deterministic all-payload scan found 168 affected IDs, matching the report. The leak itself remains a required defect. |
| Six short-analysis IDs | **PASS** | Exact list reproduced: `v3_phys_30_04`, `v3_phys_30_06`, `v3_phys_30_08`, `v3_phys_30_10`, `v3_phys_33_05`, `v3_phys_35_05`. |
| Comparison-stimulus IDs | **PASS** | Exact list reproduced: `v3_phys_30_02`, `v3_phys_33_02`, `v3_phys_34_03`. |
| Full-payload exact duplicates | **PASS** | Independent canonical full-payload scan found zero groups. |
| Reordered-option duplicates | **PASS** | Independent stimulus-aware canonical scan found zero groups. |
| Numeric-reskin candidates | **PASS** | Independent stimulus-aware numeric-masked scan found zero groups. |
| Same-followup pair existence | **PASS** | `v3_phys_30_04`/`v3_phys_30_08` share `فشار، چگالی و شاره‌ها::subskill_4`; `v3_phys_30_06`/`v3_phys_30_10` share `فشار، چگالی و شاره‌ها::subskill_2`. |
| Same-followup exclusion in normal selection | **FAIL / OPEN** | Local V6.1.4 `BankStore.kt` trace checks `id !in excluded` in `trainingCandidates` and `distinctAlternative`; it does not apply follow-up-group or scenario-fingerprint exclusion. |
| Corrected analysis completeness | **FAIL / OPEN** | The six short records include formula and units, but some omit the physical condition/model and the full substitution path. The report itself correctly identifies the need for expansion. |
| Scientific key spot checks | **PASS for reviewed cohort** | Work-energy, latent heat, Fahrenheit/Celsius, wave-on-string, capacitor energy, Lorentz force, solenoid field, continuity, density, Ohm’s law, and wave speed recomputed correctly for the sampled records. |
| Report factual consistency | **FAIL** | The report’s latent-heat row uses `real_1402_n2in_phys_075`; the bank proves that ID is the magnetic-force item. Correct latent-heat ID is `real_1404_n2in_phys_075`. |
| Standard Physics SECOND_PASS | **NOT AVAILABLE AT REVIEW TIME** | Current Composio branch inventory contained `parallel/a2-physics` at the specified commit but no branch name containing Physics SECOND_PASS/second-pass. This gate should be rerun when that branch advances. |

## Deterministic claim details

The scan independently reproduced the worker’s **187** total, the 142/22/22/1 pool split, the 180/7 source split, all six short-analysis IDs, and all three comparison IDs. It also reproduced zero full-payload, reordered-option, and numeric-reskin groups when the stored comparison stimulus is included in the canonical signature. The apparent same-followup groups are broader five-question teaching families; the two pairs called out by the worker are present and share the same numeric scenario, so the selector risk is real even though they are not exact bank duplicates.

The raw-enum count is also reproducible at **168 Physics records**. The test searched the complete serialized question payload for the worker’s internal labels, including `wrong_condition`, `partial_truth`, `overgeneralization`, `calculation_trap`, and `unit_mistake`. This is a valid count confirmation, but not a PASS of the user-facing gate: the labels remain unacceptable learner-visible content.

## Spot scientific recomputation

The following calculations were independently checked against the bank stems and the stored analyses.

| Record | Independent recomputation | Result |
|---|---|---|
| `real_1402_n2in_phys_070` | \(\Delta K=\frac12(0.2)(18^2-10^2)=22.4\,J\); weight work is \(mgh=30\,J\); therefore air work is \(-7.6\,J\). | **PASS** |
| `real_1404_n2in_phys_075` | From boiling onward, \(Q=mL=4\times2256=9024\,kJ\); at 2 kJ/s, \(t=4512\,s=75.2\,min\). | **PASS** |
| `real_1402_n2in_phys_073` | \(5C=1.8C+32\Rightarrow C=10\); \(K=C+273=283\,K\). | **PASS** |
| `real_1402_n2in_phys_056` | \(\mu=\rho\pi r^2=0.0234\,kg/m\); \(v=\sqrt{234/0.0234}=100\,m/s\); \(\lambda=0.5\,m\); crest-to-next-trough is 25 cm. | **PASS** |
| `real_1403_n1in_phys_063` | Battery disconnected means fixed charge; increasing plate spacing by 1.5 makes \(C\) divide by 1.5 and \(U=Q^2/(2C)\) multiply by 1.5, from 4 to 6 mJ. | **PASS** |
| `real_1402_n2in_phys_075` | At 90°, \(B=F/(qv)=0.5\,T\); south × east is upward for a positive charge, so the electron force is downward. | **PASS** |
| `real_1403_n1in_phys_074` | \(B=\mu_0NI/L=2.4\times10^{-3}\,T=24\,G\), after converting 10 cm and 400 mA. | **PASS** |
| `v3_phys_30_04` / `v3_phys_30_08` | Continuity under steady incompressible flow: \(A_1v_1=A_2v_2\), hence \(v_2=(6/2)3=9\,m/s\). | **Key PASS; analysis completeness OPEN** |
| `v3_phys_30_06` / `v3_phys_30_10` | \(\rho=m/V=4/0.002=2000\,kg/m^3\). | **Key PASS; analysis completeness OPEN** |
| `v3_phys_33_05` | Ohm’s law: \(I=V/R=12/6=2\,A\). | **Key PASS; analysis completeness OPEN** |
| `v3_phys_35_05` | Wave relation: \(v=f\lambda=5\times2=10\,m/s\). | **Key PASS; analysis completeness OPEN** |

The duplicated report ID is material to evidence quality. The bank record `real_1402_n2in_phys_075` begins with an electron in a magnetic field and contains the Lorentz-force analysis; it is not the 4 kg kettle latent-heat question. The kettle question is `real_1404_n2in_phys_075`. This is a report correction, not a speculative bank correction.

## SECOND_PASS status

A fresh Composio branch inventory was checked after the specified Physics commit. No standard Physics SECOND_PASS branch was present at that time. The report’s embedded `SECOND_PASS_REVIEW` section is documentation in the original report, not an independently published second branch. When a distinct standard SECOND_PASS branch appears, this helper review must rerun the same bank/hash/count/ID/duplicate and spot-scientific gates against its exact commit.

## Safe helper output and limits

This review adds only deterministic validation scripts and this report. It does not mutate the frozen bank, rewrite analysis, alter IDs or keys, change SIM membership, or claim release readiness. The required next repairs are comparison-stimulus rendering, semantic/follow-up exclusion in normal selection, and source-grounded rewrites for the 168 affected distractor analyses. All changed-bank work must be versioned and migration-tested rather than applied directly to V6.1.4.

## References

[1]: https://github.com/rynmrde/Konkor/commit/04b571947ab0c8c40b5025b121f8442a3e5911f2 "Specified Physics QA commit"
[2]: https://github.com/rynmrde/Konkor/tree/radiology1405-apk-v6.1.4-20260817 "V6.1.4 release tag"
[3]: https://drive.google.com/file/d/1r8IvfWT7R_ihzfLC6QyoGQNQiDFrvhZZ/view "Frozen V6.1 bank archive"
[4]: http://chap.sch.ir/books/13332 "Ministry Physics textbook portal"
