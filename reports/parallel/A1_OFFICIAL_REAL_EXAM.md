# A1 Official-Source / Real-Exam / Key / Quarantine Audit

**Worker role:** Official-source / real-exam / key / quarantine authority  
**Account label:** `KONKOR-A1-M1-OFFICIAL`  
**Branch:** `parallel/a1-official-real-exam`  
**Baseline:** `origin/main` commit `72dc76e56b7ae625ad1904c76910eeaec5f90f58` (recorded before this audit).  
**Baseline release context:** tag `radiology1405-apk-v6.1.4-20260817`, version `6.1.4` / versionCode `165`, and workflow `32031100891` were recorded as the current baseline context. No merge to `main` and no release publication were performed.

> **Decision:** The 17 active `real_exam` records remain verified. All 16 historical key-conflict records remain quarantined. No question is relabeled, resolved, marked obsolete, moved into a simulation, or otherwise changed in this worker branch.

## Result ledger

| Status | Exact count | Audit result |
|---|---:|---|
| Active verified `real_exam` records | 17 | Retained after exact answer-key, source, option-count, and 1405-scope checks. |
| Key-unverified historical candidates | 16 | The 16 pre-existing `quarantined_key_conflict` records remain unverified for release purposes. |
| Relabeled records | 0 | No evidence supported changing a source type. |
| Quarantined records | 16 | Preserved without key or pool changes. |
| Resolved historical key conflicts | 0 | No record was resolved without readable authoritative primary-key access. |
| Obsolete for 1405 | 0 | All 33 audited candidates store `obsolete_for_1405=false`; no contrary textbook evidence was located in scope. |
| Protected holdout records | 244 | 117 in SIM1, 117 in SIM2, and 10 in FINAL. |
| Holdout leak | 0 | Every protected record is `authored`; no real-exam or quarantined ID occurs in SIM1, SIM2, or FINAL. |

## Active 1403 first-session records

The active set contains 15 Biology and 2 Chemistry records from the 1403 first-session domestic experimental-science examination. Each has four options, an in-range zero-based key index, a retained source-booklet reference and source page, a declared official origin, `access_pool=TRAIN`, and `obsolete_for_1405=false`.

The internally opened key PDF visibly identifies itself as **«کلید سؤالات آزمون اختصاصی (سراسری) سال ۱۴۰۳ ـ نوبت اول»** for the experimental-science group. Its independent option rows were transcribed and deterministically compared with all 17 stored keys: **17/17 matched**. The locally acquired key PDF digest is `898ad1ae6d582f1225c02ce30c46f986898010b994173ec8e1e2e32ff1c7df66`. The source booklets and key copy are archive-hosted copies, not represented as official-host downloads; the retained classification depends on the identity-bearing key table plus exact option-row comparison, not a fabricated claim that the archive host is Sanjesh.[1]

| Subject | Active records | Key-row check | Four-option check | Current-1405 scope flag |
|---|---:|---:|---:|---:|
| Biology | 15 | 15/15 matched | 15/15 | 15/15 not obsolete |
| Chemistry | 2 | 2/2 matched | 2/2 | 2/2 not obsolete |
| **Total** | **17** | **17/17 matched** | **17/17** | **17/17 not obsolete** |

## Whole-candidate structural and booklet audit

The frozen verified JSON was downloaded through the configured Drive connection and its immutable SHA-256 matched `54f349cbcd731b89d440d2f9486c2126efef564b57f223082610a344913b263d`. It contains 1,216 records: 17 `real_exam`, 16 `quarantined_key_conflict`, 71 `official_exam_stem_training`, and 1,112 `authored`.[2]

All eight unique booklet PDFs referenced by the 33 active real-exam and quarantined candidates were acquired through the configured Drive connection and processed read-only. The deterministic audit found all 33 stored source-page values within the corresponding extracted PDF page count; all 33 candidates have four options and in-range answer indices; and all 33 have the required stored year, session, number, source-file, source-URL, and subject fields. Exact normalized stem anchors were found for 32/33. The remaining candidate, `real_1401_in_chem_081`, is already quarantined; its PDF extraction produced an 0.815 fallback similarity rather than an exact normalized anchor, so it is explicitly **not** promoted or otherwise relied upon.

## Quarantine authority finding

The 16 historical conflict IDs are preserved exactly as supplied:

| Year / session group | IDs | Disposition |
|---|---:|---|
| 1401 domestic Biology and Chemistry | 6 | Remain `QUARANTINE`; direct result/key endpoint could not be read in the internal browser. |
| 1401 domestic and foreign Geology | 7 | Remain `QUARANTINE`; no readable primary key was obtained. |
| 1402 second-session domestic Biology | 1 | Remains `QUARANTINE`; the official 1402 key was identified by a contemporaneous publication, but the direct Sanjesh file returned a 403 access block from this environment. |
| 1403 first-session domestic Chemistry | 1 | Remains `QUARANTINE`; no authoritative conflict-resolution evidence was collected. |
| 1404 second-session domestic Geology | 1 | Remains `QUARANTINE`; no authoritative conflict-resolution evidence was collected. |
| **Total** | **16** | **0 resolved; 16 preserved** |

The primary Sanjesh routes were not silently substituted with reasoning, mirrors, or the frozen internal scientific-resolution report. The direct 1402 key URL returned Sanjesh’s 403 access block; the 1401 result/key endpoint closed the connection, after which the internal browser became unavailable. These are access limitations, not evidence for either key choice. A contemporaneous report documents the official 1402 experimental-science key URL, but it is not a substitute for reading that key.[3]

## Holdout integrity

The deterministic pool check returned 244 protected IDs: SIM1=117, SIM2=117, and FINAL=10. All are `source_type=authored`; the query for non-authored protected IDs returned zero rows. The frozen blueprint declarations also state `verified_real_count=0` in each protected pool. No active or quarantined historical item was found in SIM1, SIM2, or FINAL.

## Implementation and migration decision

No bank artifact, Room schema, migration, question ID, source metadata, key, access pool, holdout assignment, or packaged-bank hash was changed. This is intentional: the active records’ stored keys matched the inspected 1403 table, while the 16 historical conflicts lacked the required readable primary-key evidence for resolution. Therefore a bank mutation would add migration and release risk without evidence-backed benefit. Stable IDs and all existing user progress remain unaffected.

## Reproduction artifacts

The worker retained the following read-only audit artifacts outside the repository checkout: `primary_evidence_log.md`, `record_booklet_audit.tsv`, `record_booklet_audit_summary.md`, `active_1403_key_comparison.tsv`, and `active_1403_key_comparison.md`. The local scripts are audit-only and do not alter the frozen archive.

## Residual limitation and handoff

The current environment could not read direct official Sanjesh key endpoints because of documented access blocks/connection failure. Future resolution of any of the 16 quarantined records requires a readable official Sanjesh key or notice that identifies the exact year, session, booklet, question number, and option. Until then, their quarantine is mandatory. No release gate is waived by this report.

## References

[1]: https://dl.konkur.in/2024/04/tajrobi1403-key-%5Bkonkur.in%5D1.pdf "Archive-hosted 1403 first-session experimental-science key PDF inspected through the internal browser"
[2]: https://drive.google.com/drive/folders/1R2IovFE_e0O_vU4IBCSiJpqrwK4LecxK "Frozen V6.1 archive folder"
[3]: https://farsnews.ir/University_and_Seminary/1689401626000085045 "Contemporaneous publication linking the 1402 official Sanjesh experimental-science answer key"


---

# SECOND_PASS_REVIEW — Paired-Statement Visible-Stem and Cross-Worker Recheck

**Review trigger:** The visible-stem QA report on `parallel/help-a2-visible-stem-qa` identified 21 active TRAIN questions whose learner-visible stem omits the substantive A/B claims while the options require a truth-value decision about those claims.[4]

> **Second-pass decision:** All 21 affected records are **authored training items**, not `real_exam` records. Each pair can be reconstructed **verbatim from the immutable frozen bank’s own `stimulus.left` and `stimulus.right` fields**, which retain the labelled `مورد A` and `مورد B` strings. This is sufficient bank evidence to restore the visible stem exactly; it is not external official-exam evidence and must never be represented as such. Until an integration restores the two strings to the rendered stem and validates every delivery path, the conservative disposition is **quarantine/demote from normal training selection**.

## Exact paired-statement dispositions

The frozen bank gzip again matched `b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14`. Each row below has non-empty exact labelled A/B text in the immutable bank representation. The immediate required outcome is identical for all rows: use the listed text verbatim in the visible stem, preserve the ID and progress mapping, and otherwise quarantine/demote it. No claim is reconstructed from answer key, explanation, model guesswork, or textbook paraphrase.[4] [5]

| ID | Subject | Exact A claim from `stimulus.left` | Exact B claim from `stimulus.right` | Evidence class | Required disposition |
|---|---|---|---|---|---|
| `v3_bio_02_12` | زیست | DNAپلیمراز رشتهٔ جدید را فقط در جهت ۵′ به ۳′ طویل می‌کند. | هر جهش الزاماً رخ‌نمود جاندار را تغییر می‌دهد. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_bio_05_12` | زیست | چرخهٔ کربس در مادهٔ زمینه‌ای راکیزه انجام می‌شود. | در خود قندکافت کربن‌دی‌اکسید آزاد می‌شود. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_bio_06_07` | زیست | اکسیژن آزادشده در فتوسنتز از شکستن آب به‌دست می‌آید. | گیاهان CAM معمولاً روزنه‌های خود را در روز باز می‌کنند. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_bio_07_15` | زیست | افزایش فشار هیدروستاتیک مویرگ خروج آب به مایع میان‌بافتی را تقویت می‌کند. | همهٔ سیاهرگ‌ها خون کم‌اکسیژن حمل می‌کنند. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_bio_08_07` | زیست | صفرا آنزیم گوارشی ندارد و با ریزکردن قطره‌های چربی سطح تماس را زیاد می‌کند. | پرزهای فراوان، ویژگی اصلی رودهٔ بزرگ برای جذب مواد غذایی‌اند. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_bio_10_11` | زیست | تراوش خون در کلافک و ورود مواد به کپسول بومن آغاز می‌شود. | آلدوسترون فقط و مستقیماً بازجذب آب را زیاد می‌کند. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_bio_11_07` | زیست | بازشدن کانال‌های ولتاژی سدیم، فاز سریع ناقطبی‌شدن را ایجاد می‌کند. | ناقل عصبی از یاختهٔ پس‌سیناپسی به فضای سیناپسی رها می‌شود. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_bio_12_07` | زیست | هورمون‌های تیروئیدی معمولاً سوخت‌وساز پایه را افزایش می‌دهند. | FSH و LH را هیپوتالاموس ترشح می‌کند. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_bio_14_10` | زیست | HCG در اوایل بارداری به حفظ جسم زرد کمک می‌کند. | لقاح معمولاً در حفرهٔ رحم انجام می‌شود. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_bio_15_15` | زیست | پس از لقاح مضاعف در نهاندانگان، تخم و یاختهٔ آغازین آندوسپرم تشکیل می‌شوند. | همهٔ عناصر رسانای آوند چوبی در بلوغ زنده‌اند. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_bio_16_10` | زیست | رانش ژنی در جمعیت‌های کوچک اثر نسبی بیشتری دارد. | صفات اکتسابی هر فرد الزاماً به نسل بعد منتقل می‌شوند. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_chem_20_03` | شیمی | افزایش نیروهای بین‌مولکولی معمولاً نقطهٔ جوش را افزایش می‌دهد. | جفت‌الکترون ناپیوندی هیچ اثری بر شکل مولکول ندارد. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_chem_26_03` | شیمی | ایزومرهای ساختاری فرمول مولکولی یکسان و اتصال اتمی متفاوت دارند. | فرمول عمومی آلکن زنجیری تک‌پیونددوگانه CₙH₂ₙ₊₂ است. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_chem_54_07` | شیمی | خوردگی آهن یک فرایند اکسایش‌ـ‌کاهش است و حضور آب و اکسیژن آن را تسهیل می‌کند. | هر سنگ معدنی با عیار بیشتر، بدون توجه به هزینه‌ها، الزاماً اقتصادی‌تر است. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_phys_30_02` | فیزیک | نیروی شناوری برابر وزن شارهٔ جابه‌جا‌شده است. | در لولهٔ باریک‌تر، سرعت شارهٔ پایا کمتر است. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_phys_33_02` | فیزیک | در اتصال موازی، اختلاف پتانسیل دو سر شاخه‌ها یکسان است. | ولت‌سنج آرمانی مقاومت ناچیز دارد. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_phys_34_03` | فیزیک | جهت جریان القایی با تغییری که آن را ایجاد کرده مخالفت می‌کند. | سیم موازی میدان بیشترین نیروی مغناطیسی را می‌گیرد. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_geo_45_09` | زمین | در مرز واگرا پوستهٔ اقیانوسی جدید می‌تواند ساخته شود. | گسل امتدادلغز فقط جابه‌جایی قائم ایجاد می‌کند. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_geo_46_08` | زمین | سنگ دگرگونی بدون ذوب کامل و بر اثر دما/فشار تغییر می‌کند. | سختی موس مقدار مقاومت سنگ در برابر ضربه است. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_geo_47_07` | زمین | افزایش عیار معمولاً ارزش اقتصادی ذخیره را بیشتر می‌کند. | عیار هیچ ارتباطی با مقدار مادهٔ مفید ندارد. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |
| `v3_geo_49_08` | زمین | خاک حاصل برهم‌کنش سنگ مادر، اقلیم، جانداران، پستی‌وبلندی و زمان است. | حذف پوشش گیاهی معمولاً فرسایش آبی را کم می‌کند. | Immutable authored-bank `stimulus` | Restore verbatim to visible stem; otherwise quarantine/demote |

| Paired-statement subject | Exact resolvable items | Unresolved from frozen bank | Immediate safe status |
|---|---:|---:|---|
| Biology | 11 | 0 | Restore all 11 verbatim or quarantine/demote all 11 |
| Chemistry | 3 | 0 | Restore all 3 verbatim or quarantine/demote all 3 |
| Physics | 3 | 0 | Restore all 3 verbatim or quarantine/demote all 3 |
| Geology | 4 | 0 | Restore all 4 verbatim or quarantine/demote all 4 |
| **Total** | **21** | **0** | **No visible-stem release until every item is restored or excluded** |

A correct bank repair must retain each stable ID, preserve existing attempts/progress, use non-destructive migration, restore the exact A/B strings in every applicable presentation and review path, and add a deterministic regression gate for non-empty visible A/B claims. A selector-only workaround is insufficient unless it blocks the item from new training, session resume, review reopening, backup restore, and any other reachable rendering path.[4]

## Active real-exam and historical-conflict cross-worker recheck

No contradiction was found that changes the A1 official-source disposition of **17 active `real_exam` records retained** and **16 historical key conflicts quarantined**.

| Worker branch examined | Relevant change found | Effect on the 17 verified active records | Effect on the 16 conflicts | Second-pass disposition |
|---|---|---|---|---|
| `parallel/real-exam-source-audit` | Audit report and validator only; no bank mutation. Its retained counts agree: 17 active real-exam, 16 quarantined, 0 resolutions. | No contradiction. | No contradiction. | Retain A1 result. |
| `parallel/real-exam-1402-1404` | Audit report and validator only; no question-data artifact in the branch diff. | No contradiction. | No contradiction. | Retain A1 result. |
| `parallel/bank-biology` | Sixteen analysis-only update IDs; exact intersection with A1’s 17 real + 16 quarantine IDs is zero. | No contradiction. | No contradiction. | Retain A1 result. |
| `parallel/bank-chemistry` | Overlay candidate changes review content for active `real_1403_n1_chem_102`, `real_1403_n1_chem_109` and quarantined `real_1401_in_chem_081`, `_099`, `_105`, `_106`, `real_1403_n1in_chem_106`. The exact-diff manifest lists only `review_default` for those seven IDs. | No source type, option, answer key, source metadata, official-key field, or obsolete status is changed. | Quarantine/key-conflict status is not changed. | No contradiction; integration must preserve the authoritative fields unchanged. |
| `parallel/a1-biology-geology` | Reviewed diff is UI/test/report oriented; no packaged-bank or audited real/quarantine-data artifact appears in the reviewed change set. | No contradiction found. | No contradiction found. | Retain A1 result. |

The active 1403 key match remains **17/17**, with source page, four-option, and current-scope findings unchanged. The 16 historical conflict records remain **0 resolved / 16 quarantined**: downstream explanation or review-text changes do not constitute authoritative key evidence and cannot promote, rewrite, or clear a quarantine.[1] [2] [6] [7] [8] [9]

## Second-pass references

[4]: https://github.com/rynmrde/Konkor/blob/parallel/help-a2-visible-stem-qa/reports/parallel/A2_HELP_VISIBLE_STEM_QA.md "A2 visible paired-statement QA blocker report"
[5]: https://drive.google.com/drive/folders/1R2IovFE_e0O_vU4IBCSiJpqrwK4LecxK "Frozen V6.1 source archive"
[6]: https://github.com/rynmrde/Konkor/compare/main...parallel/real-exam-source-audit "Real-exam source-audit branch comparison"
[7]: https://github.com/rynmrde/Konkor/compare/main...parallel/real-exam-1402-1404 "Recent real-exam audit branch comparison"
[8]: https://github.com/rynmrde/Konkor/blob/parallel/bank-biology/app/src/main/assets/biology_v615_patch.json "Biology patch manifest"
[9]: https://github.com/rynmrde/Konkor/blob/parallel/bank-chemistry/reports/parallel/CHEMISTRY_V62_EXACT_DIFF.json "Chemistry exact-diff manifest"
