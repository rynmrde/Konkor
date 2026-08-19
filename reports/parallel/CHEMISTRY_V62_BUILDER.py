#!/usr/bin/env python3
"""Build a versioned, audited Chemistry v6.2 candidate from the frozen v6.1 bank.

This script never changes the frozen source. It copies the database, cleans review-facing
internal labels for every Chemistry item, rewrites the priority-74 explanations with
question-specific reasoning, retires five cosmetic variants, and appends five distinct
training replacements with new IDs.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import json
import re
import shutil
import sqlite3
import sys
from pathlib import Path
from typing import Any

if len(sys.argv) != 4:
    raise SystemExit("usage: build_v620_chemistry_bank.py SOURCE_DB OUTPUT_DIR AUDIT_DIR")

SOURCE_DB = Path(sys.argv[1])
OUT_DIR = Path(sys.argv[2])
AUDIT_DIR = Path(sys.argv[3])
OUT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
OUT_DB = OUT_DIR / "radiology1405_bank_v6_2.db"
OUT_GZ = OUT_DIR / "radiology1405_bank_v6_2.db.gz"

RETIRED: dict[str, str] = {
    "v3_chem_17_06": "v62_chem_17_06",
    "v3_chem_17_07": "v62_chem_17_07",
    "v3_chem_17_08": "v62_chem_17_08",
    "v3_chem_17_09": "v62_chem_17_09",
    "v3_chem_17_10": "v62_chem_17_10",
}

LABELS = {
    "wrong_condition": "خطای تعیین شرط یا نسبت واکنش",
    "condition_wrong": "خطای تعیین شرط یا نسبت واکنش",
    "partial_truth": "برداشت ناقص از رابطهٔ شیمیایی",
    "truth_partial": "برداشت ناقص از رابطهٔ شیمیایی",
    "calculation_trap": "خطای محاسبه یا نسبت‌گیری",
    "unit_mistake": "خطای واحد",
    "overgeneralization": "تعمیم نادرست",
    "correct_reasoning": "استدلال درست",
}
GENERIC_SENTENCES = [
    "از کلیدواژه جواب نده؛ شرط هر گزینه را بسنج.",
    "تیپ را تشخیص بده، واحدها را یکسان کن و بعد از راه",
    "پیش برو.",
    "این مسئله یک زنجیرهٔ پیوسته دارد؛ خروجی هر مرحله ورودی مرحلهٔ بعد است.",
    "صورت را به بخش‌های مستقل تقسیم کن و داده یا قید تعیین‌کننده را علامت بزن.",
    "پاسخ صحیح با ارزیابی مستقل اجزای سؤال به‌دست می‌آید.",
    "این گزینه با همهٔ شرط‌ها سازگار است.",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def clean_text(text: Any) -> Any:
    if not isinstance(text, str):
        return text
    result = text
    for raw, friendly in LABELS.items():
        result = re.sub(rf"\b{re.escape(raw)}\b", friendly, result, flags=re.IGNORECASE)
    for sentence in GENERIC_SENTENCES:
        result = result.replace(sentence, " ")
    result = re.sub(r"روش کنترل:\s*", "", result)
    result = re.sub(r"منشأ دام این گزینه [^.]+ است\.\s*", "", result)
    result = re.sub(r"این گزینه با یک خطای رایج در قید، جهت، واحد یا استثنا ساخته شده است\.\s*", "", result)
    result = re.sub(r"این انتخاب معمولاً وقتی رخ می‌دهد که یکی از شرط‌ها زودتر از بقیه قطعی فرض شود\.\s*", "", result)
    result = re.sub(r"مسیر این گزینه از یک برداشت نزدیک اما ناقص عبور می‌کند\.\s*", "", result)
    result = re.sub(r"نکتهٔ تثبیتی:\s*", "", result)
    result = re.sub(r"\s+", " ", result).strip()
    # De-duplicate immediate repeated sentences after template removal.
    chunks = [chunk.strip() for chunk in re.split(r"(?<=[.!؟])\s+", result) if chunk.strip()]
    deduped: list[str] = []
    for chunk in chunks:
        if not deduped or chunk != deduped[-1]:
            deduped.append(chunk)
    return " ".join(deduped)


def clean_recursive(value: Any) -> Any:
    if isinstance(value, str):
        return clean_text(value)
    if isinstance(value, list):
        return [clean_recursive(item) for item in value]
    if isinstance(value, dict):
        return {key: clean_recursive(item) for key, item in value.items()}
    return value


def review_default(q: dict[str, Any]) -> dict[str, Any]:
    options = q["options"]
    correct_index = q["correct_index"]
    correct = clean_text(q.get("correct_analysis", ""))
    fast = clean_text(q.get("fast_method", ""))
    distractors = {str(key): clean_text(value) for key, value in (q.get("distractor_analyses") or {}).items()}
    answers: dict[str, str] = {}
    for index, option in enumerate(options):
        if index == correct_index:
            answers[str(index)] = correct
        else:
            specific = distractors.get(str(index), "")
            answers[str(index)] = f"گزینهٔ {index + 1} نادرست است، زیرا {specific} پاسخ درست «{options[correct_index]}» است."
    blank = f"پاسخ درست «{options[correct_index]}» است. {correct}"
    if fast:
        blank += f" راه کوتاه: {fast}"
    return {"correct": correct, "wrong_by_original_option": answers, "blank": blank}


def set_explanations(q: dict[str, Any], correct: str, distractors: dict[int, str], fast: str, lesson: str) -> None:
    q["correct_analysis"] = correct
    q["distractor_analyses"] = {str(index): text for index, text in distractors.items()}
    q["fast_method"] = fast
    q["start_method"] = fast
    q["short_lesson"] = lesson
    q["review_default"] = review_default(q)


def fingerprint(q: dict[str, Any]) -> str:
    body = json.dumps({"stem": q["stem"], "options": q["options"], "correct_index": q["correct_index"]}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def question_template(source: dict[str, Any], *, identifier: str, stem: str, options: list[str], correct_index: int,
                      correct: str, distractors: dict[int, str], fast: str, lesson: str, form: str, difficulty: int,
                      seconds: int, subskill: str, evidence: str, page: int | None = None) -> dict[str, Any]:
    q = copy.deepcopy(source)
    q.update({
        "id": identifier,
        "source_type": "authored",
        "v6_source_type": "authored",
        "official_origin": False,
        "retrieved_from_archive": False,
        "source_file": None,
        "source_url": None,
        "source_page": None,
        "source_file_id": None,
        "source_file_sha256": None,
        "source_pdf_page_index": None,
        "official_answer_key_url": None,
        "answer_key_official_origin": False,
        "answer_key_retrieved_from_archive": False,
        "answer_key_crosscheck": None,
        "key_provenance": {},
        "exam_year": None,
        "exam_session": None,
        "question_number": None,
        "stimulus": None,
        "stem": stem,
        "options": options,
        "correct_index": correct_index,
        "v6_stored_correct_index": correct_index,
        "priority": 74.0,
        "difficulty": difficulty,
        "question_type": "calculation",
        "question_form": form,
        "scenario_family": form,
        "scenario_family_fa": "محاسبهٔ شیمی با دادهٔ تازه",
        "scenario_model": f"v6_2_chemistry::{identifier}",
        "scenario_variant": 1,
        "stem_template_id": f"v6_2::{form}::{identifier}",
        "normalized_stem_template": f"v6_2::{form}",
        "calculation_required": True,
        "estimated_solve_time_seconds": seconds,
        "reasoning_steps_estimate": 2 if form == "numerical_single_stage" else 3,
        "subskill": subskill,
        "subskill_index": 0,
        "followup_group": "مول، استوکیومتری و گازها::v6_2_distinct_retest",
        "selected_scope": True,
        "obsolete_for_1405": False,
        "runtime_scope_status": "A_CORE_FULL",
        "access_pool": "TRAIN",
        "teaching_ladder_level": "L3_APPLICATION",
        "eligible_for_training": True,
        "eligible_for_safety_evidence": False,
        "eligible_for_simulation": False,
        "needs_human_review": False,
        "needs_official_key_reconciliation": False,
        "closest_real_exam_pattern": None,
        "related_real_exam_patterns": [],
        "real_exam_anchor_patterns": [],
        "anchor_match": {
            "shared_skill": "مول، استوکیومتری و گازها",
            "changed_dimension": "new numbers, substance context, and calculation path",
            "why_not_clone": "A new authored training item; it does not reconstruct an official stem or option set.",
        },
        "authored_basis": "Supplied official Chemistry textbook scope plus arithmetic re-solve; calibrated training only, not labelled as a real exam item.",
        "form_calibration_basis": "Calculation form retained within the existing 1398–1404-calibrated Chemistry training framework; no direct official-stem claim.",
        "konkur_level": True,
        "konkur_level_basis": "Textbook-bounded, multi-step Chemistry calculation with plausible unit/ratio distractors; authored training, not an official question claim.",
        "problem_model": "stoichiometric_calculation",
        "required_skills": ["تبدیل داده به مول", "کاربرد ضرایب واکنش", "کنترل واحد", "کنترل معقول بودن پاسخ"],
        "common_traps": ["نسبت واکنش", "واحد"],
        "main_trap": "استفاده از نسبت یا واحد نادرست",
        "error_tags_supported": ["knowledge_gap", "calculation_error", "misread", "careless_error"],
        "textbook_refs": [{
            "book": "شیمی ۱",
            "book_code": "110210",
            "edition_print_year": 1402,
            "page": page,
            "section": "مول، استوکیومتری و گازها",
        }],
        "v4_rewrite_reason": "v6_2_chemistry_duplicate_replacement",
        "replaced_v3_question_id": None,
        "semantic_leakage_repaired": False,
        "scientific_verification_v6_2": {
            "status": "TEXTBOOK_SCOPE_AND_ARITHMETIC_VERIFIED",
            "evidence": evidence,
            "review_scope": "author-created training item; exact calculation independently re-solved",
        },
    })
    set_explanations(q, correct, distractors, fast, lesson)
    q["semantic_fingerprint"] = fingerprint(q)
    return q


# Question-specific rewrite for the deep-reviewed, selected priority-74 items.
DEEP: dict[str, dict[str, Any]] = {
    "real_1403_n1in_chem_103": {
        "correct": "گزینهٔ ۲ درست است. در مقایسهٔ آنتالپی فروپاشی، بزرگی بار یون‌ها و کوچکی شعاع یون‌ها تعیین‌کننده است. Al₂O₃ با یون‌های Al³⁺ و O²⁻ سهم بسیار بزرگی در b دارد؛ AlF₃ نیز c را از مجموع MgO و KI بزرگ‌تر می‌کند، در حالی که KI و NaBr شبکه‌های ضعیف‌تری دارند. بنابراین b > c > a.",
        "d": {
            0: "c را کوچک‌تر از a می‌گیرد، اما حضور AlF₃ با یون Al³⁺ باعث می‌شود c از مجموع MgO و KI بزرگ‌تر باشد.",
            1: "ترتیب درست است، زیرا Al₂O₃ و LiF مجموع b را بیشترین و AlF₃ مجموع c را از a بزرگ‌تر می‌کنند.",
            2: "c را از b بزرگ‌تر می‌گیرد؛ اثر جاذبهٔ Al³⁺–O²⁻ در Al₂O₃ از Al³⁺–F⁻ در AlF₃ قوی‌تر است.",
            3: "b را از c و a کوچک‌تر می‌گیرد، در حالی که وجود Al₂O₃ این نتیجه را رد می‌کند.",
        },
        "fast": "ابتدا Al₂O₃ را به‌علت بارهای ۳+ و ۲− بزرگ‌ترین سهم بگیر؛ سپس AlF₃ را از نمک‌های تک‌بار قوی‌تر بدان.",
        "lesson": "برای رتبه‌بندی انرژی شبکه، حاصل‌ضرب بار یون‌ها و شعاع یون‌ها را هم‌زمان بسنج.",
    },
    "v3_chem_17_01": {
        "correct": "گزینهٔ ۳ درست است. ضرایب واکنشِ موازنه‌شده نسبت تعداد مول‌های مواد را نشان می‌دهند؛ بنابراین نسبت‌های استوکیومتری مستقیماً از ضرایب خوانده می‌شوند.",
        "d": {
            0: "کم بودن جرم به‌تنهایی محدودکننده را تعیین نمی‌کند؛ باید برای هر واکنش‌دهنده مقدار مول را بر ضریب واکنش تقسیم کرد.",
            1: "جرم یک مول هر ماده برابر جرم مولی همان ماده است و جرم مولی مواد مختلف یکسان نیست.",
            2: "درست است، زیرا ضرایب واکنش موازنه‌شده نسبت مولی مواد را تعیین می‌کنند.",
            3: "بازده درصدی از نسبت مقدار واقعی به مقدار نظری به‌دست می‌آید و برای فرآوردهٔ خالصِ یک واکنش معمولی از ۱۰۰٪ بیشتر نمی‌شود.",
        },
        "fast": "ضرایب را فقط به‌عنوان نسبت مولی بخوان، نه نسبت جرم.",
        "lesson": "برای یافتن محدودکننده، ابتدا جرم را به مول تبدیل کن و سپس نسبت n/ضریب را مقایسه کن.",
    },
    "v3_chem_17_02": {
        "correct": "گزینهٔ ۴ درست است. CH₄ + 2O₂ → CO₂ + 2H₂O موازنه است و ضریب CH₄ با CO₂ برابر ۱ است؛ پس ۰٫۵ mol CH₄ دقیقاً ۰٫۵ mol CO₂ می‌دهد.",
        "d": {0: "۰٫۲۵ mol از نصف‌کردن بی‌دلیل نسبت ۱:۱ به‌دست می‌آید.", 1: "۱ mol با دوبرابر کردن مقدار CH₄ به‌دست می‌آید، در حالی که نسبت CH₄:CO₂ برابر ۱:۱ است.", 2: "۲ mol ضریب O₂ را به‌اشتباه به CO₂ نسبت می‌دهد.", 3: "درست است؛ ضریب‌های CH₄ و CO₂ هر دو ۱ هستند."},
        "fast": "در واکنش موازنه‌شده، نسبت ضریب CO₂ به CH₄ برابر ۱/۱ است.",
        "lesson": "در مسائل مولیِ واکنش، فقط نسبت ضرایب واکنش‌دهنده و فرآوردهٔ خواسته‌شده را به‌کار ببر.",
    },
    "v3_chem_17_03": {
        "correct": "گزینهٔ ۱ درست است. درصد بازده = (جرم واقعی / جرم نظری) × ۱۰۰ = (۳۰ g / ۴۰ g) × ۱۰۰ = ۷۵٪.",
        "d": {0: "درست است؛ مقدار واقعی ۳۰ g نسبت به مقدار نظری ۴۰ g برابر ۷۵٪ است.", 1: "۲۵٪ اختلافِ ۱۰۰ و ۷۵ است، نه بازده واکنش.", 2: "۱۳۳٪ از وارونۀ نسبت ۴۰/۳۰ به‌دست می‌آید و بازده را معکوس گرفته است.", 3: "۷۰٪ از داده‌های مسئله به‌دست نمی‌آید."},
        "fast": "همیشه مقدار واقعی را بر مقدار نظری تقسیم کن و در ۱۰۰ ضرب کن.",
        "lesson": "بازده درصدی باید بعد از یافتن مقدار نظری و با واحدهای هم‌نوع محاسبه شود.",
    },
    "v3_chem_17_04": {
        "correct": "گزینهٔ ۲ درست است. با ثابت بودن فشار و مقدار گاز، قانون شارل می‌دهد V₂/V₁ = T₂/T₁. دما از ۳۰۰ K به ۶۰۰ K می‌رسد، پس V₂/V₁ = ۶۰۰/۳۰۰ = ۲ و حجم دو برابر می‌شود.",
        "d": {0: "نصف‌شدن برخلاف رابطهٔ مستقیم حجم و دمای کلوین است.", 1: "درست است؛ دوبرابر شدن T برحسب کلوین حجم را دو برابر می‌کند.", 2: "چهاربرابر شدن از داده‌های ۶۰۰/۳۰۰ به‌دست نمی‌آید.", 3: "در فشار ثابت، حجم با دمای کلوین تغییر می‌کند."},
        "fast": "در فشار و مول ثابت، نسبت حجم‌ها همان نسبت دماهای کلوین است.",
        "lesson": "قانون شارل با دمای کلوین کار می‌کند؛ از دمای سلسیوس در نسبت‌گیری استفاده نکن.",
    },
    "v3_chem_17_05": {
        "correct": "گزینهٔ ۳ درست است. برای H₂ مقدار n/ضریب = ۳/۲ = ۱٫۵ و برای O₂ مقدار n/ضریب = ۲/۱ = ۲ است؛ پس H₂ محدودکننده است. در 2H₂ → 2H₂O نسبت ۱:۱ است، بنابراین ۳ mol H₂، ۳ mol H₂O می‌سازد.",
        "d": {0: "۱ mol با استفاده از نسبت نادرست تولید می‌شود.", 1: "۲ mol مقدار موجود O₂ را بدون توجه به محدودکننده به محصول نسبت می‌دهد.", 2: "درست است؛ H₂ محدودکننده است و نسبت H₂:H₂O برابر ۱:۱ است.", 3: "۴ mol بیش از مقداری است که ۳ mol H₂ می‌تواند تولید کند."},
        "fast": "برای هر واکنش‌دهنده n/ضریب را بنویس؛ کوچک‌تر، محدودکننده است.",
        "lesson": "محدودکننده با جرم یا مول خام تعیین نمی‌شود؛ مقایسۀ n/ضریب لازم است.",
    },
    "v3_chem_17_14": {
        "correct": "گزینهٔ ۴ درست است. در STP، ۱۱٫۲ L = ۱۱٫۲/۲۲٫۴ = ۰٫۵ mol است. پس M = ۲۲ g / ۰٫۵ mol = ۴۴ g·mol⁻¹ و جرم ۰٫۲۵ mol برابر ۰٫۲۵ × ۴۴ = ۱۱ g است.",
        "d": {0: "جرم مولی ۲۲ g·mol⁻¹ مقدار ۲۲ g را به‌اشتباه جرم یک مول فرض می‌کند.", 1: "جرم مولی ۴۴ درست است، اما ۰٫۲۵ mol از گاز ۴۴ g·mol⁻¹ جرمی برابر ۱۱ g دارد، نه ۵٫۵ g.", 2: "هم جرم مولی و هم جرم نمونه با تبدیل حجم به مول ناسازگارند.", 3: "درست است؛ n=۰٫۵ mol، سپس M=۴۴ g·mol⁻¹ و m=۱۱ g."},
        "fast": "در STP ابتدا V را بر ۲۲٫۴ L·mol⁻¹ تقسیم کن، سپس از m=nM استفاده کن.",
        "lesson": "در زنجیرۀ حجم–مول–جرم، واحد هر مرحله را همراه عدد بنویس.",
    },
    "v3_chem_17_15": {
        "correct": "گزینهٔ ۱ درست است. n(KClO₃)=۲۴٫۵ g / ۱۲۲٫۵ g·mol⁻¹ = ۰٫۲۰ mol. از 2KClO₃ → 3O₂، n(O₂)=۰٫۲۰×۳/۲=۰٫۳۰ mol و در STP، V=۰٫۳۰×۲۲٫۴=۶٫۷۲ L.",
        "d": {0: "درست است؛ نسبت ۳/۲ و حجم مولی ۲۲٫۴ L·mol⁻¹ به ۶٫۷۲ L می‌رسد.", 1: "۴٫۴۸ L حاصل حذف نسبت ۳/۲ و فرض ۰٫۲۰ mol O₂ است.", 2: "۳٫۳۶ L از استفادهٔ نادرست از ۳/۴ به‌جای ۳/۲ می‌آید.", 3: "۱۳٫۴۴ L نسبت O₂ را دو برابر مقدار درست می‌گیرد."},
        "fast": "جرم KClO₃ → مول؛ ضرب در ۳/۲ برای O₂؛ سپس ضرب در ۲۲٫۴ L·mol⁻¹.",
        "lesson": "نسبت ضرایب فقط پس از تبدیل داده به مول وارد محاسبه می‌شود.",
    },
    "v3_chem_17_16": {
        "correct": "گزینهٔ ۲ درست است. جرم خالص Mg برابر ۱۰ g×۰٫۶۰=۶٫۰ g است؛ n(Mg)=۶٫۰/۲۴=۰٫۲۵ mol. در Mg + 2HCl → MgCl₂ + H₂ نسبت Mg:H₂ برابر ۱:۱ است، پس V(H₂)=۰٫۲۵×۲۲٫۴=۵٫۶ L در STP.",
        "d": {0: "۹٫۳۳ L از به‌کاربردن جرم ناخالص ۱۰ g به‌جای جرم خالص ۶ g به‌دست می‌آید.", 1: "درست است؛ خلوص ۶۰٪ ابتدا ۶٫۰ g Mg می‌دهد و سپس ۵٫۶ L H₂.", 2: "۲٫۸ L نسبت Mg:H₂ را به‌اشتباه نصف می‌کند.", 3: "۱۳٫۴۴ L با جرم خالص و نسبت ۱:۱ سازگار نیست."},
        "fast": "ابتدا درصد خلوص را به جرم خالص تبدیل کن؛ سپس جرم → مول → حجم گاز.",
        "lesson": "در مسائل خلوص، فقط بخش خالص نمونه وارد معادلهٔ واکنش می‌شود.",
    },
    "v3_chem_17_17": {
        "correct": "گزینهٔ ۳ درست است. برای مصرف ۳ mol H₂ در واکنش 2H₂+O₂→2H₂O به ۳×۱/۲=۱٫۵ mol O₂ نیاز است. از ۲ mol O₂، مقدار ۰٫۵ mol باقی می‌ماند و به‌سبب نسبت 2H₂:2H₂O، ۳ mol H₂، ۳ mol H₂O تولید می‌کند.",
        "d": {0: "۴ mol آب بیش از مقدار مجاز با ۳ mol H₂ است.", 1: "۲ mol آب و ۱ mol O₂ با نسبت ضرایب واکنش سازگار نیست.", 2: "درست است؛ H₂ محدودکننده، آب ۳ mol و O₂ باقی‌مانده ۰٫۵ mol است.", 3: "مقدار آب درست است اما O₂ باقی‌مانده را ۱ mol می‌گیرد، در حالی که ۱٫۵ mol مصرف شده است."},
        "fast": "از H₂، O₂ لازم را با ضریب ۱/۲ حساب کن؛ سپس O₂ باقی‌مانده را کم کن.",
        "lesson": "در مسائل محدودکننده و باقیمانده، محصول و واکنش‌دهندۀ اضافی را در دو گام جدا محاسبه کن.",
    },
    "v3_chem_17_18": {
        "correct": "گزینهٔ ۴ درست است. جرم خالص CaCO₃ برابر ۲۵ g×۰٫۸۰=۲۰ g است و n(CaCO₃)=۲۰/۱۰۰=۰٫۲۰ mol. در CaCO₃→CaO+CO₂ نسبت ۱:۱ است؛ بنابراین n(CO₂)=۰٫۲۰ mol و V=۰٫۲۰×۲۲٫۴=۴٫۴۸ L در STP.",
        "d": {0: "۵٫۶۰ L از استفادهٔ جرم ناخالص ۲۵ g و نادیده‌گرفتن خلوص ۸۰٪ می‌آید.", 1: "۲٫۲۴ L مقدار CO₂ را به‌اشتباه نصف می‌کند.", 2: "۴۴٫۸ L در تبدیل مول به حجم یک مرتبهٔ ده‌دهی خطا دارد.", 3: "درست است؛ جرم خالص ۲۰ g برابر ۰٫۲۰ mol و حجم CO₂ برابر ۴٫۴۸ L است."},
        "fast": "۲۵×۰٫۸۰ → ۲۰ g؛ ۲۰/۱۰۰ → ۰٫۲۰ mol؛ سپس ×۲۲٫۴ L·mol⁻¹.",
        "lesson": "برای حجم گاز از نمونهٔ ناخالص، ترتیب خلوص → مول → نسبت واکنش → حجم را حفظ کن.",
    },
    "v3_chem_17_19": {
        "correct": "گزینهٔ ۱ درست است. برای ۰٫۲۵ mol N₂ به ۰٫۷۵ mol H₂ نیاز است؛ چون ۱ mol H₂ داریم، N₂ محدودکننده است. از N₂+3H₂→2NH₃، مقدار نظری NH₃ برابر ۰٫۲۵×۲=۰٫۵۰ mol و جرم نظری ۰٫۵۰×۱۷=۸٫۵ g است. با بازده ۸۰٪، جرم واقعی ۰٫۸۰×۸٫۵=۶٫۸ g می‌شود.",
        "d": {0: "درست است؛ بازده ۸۰٪ پس از جرم نظری ۸٫۵ g اعمال می‌شود و ۶٫۸ g می‌دهد.", 1: "۸٫۵ g جرم نظری است و بازده ۸۰٪ روی آن اعمال نشده است.", 2: "۱۳٫۶ g دو برابر جرم واقعی درست است و از نسبت واکنش به‌دست نمی‌آید.", 3:"۳٫۴ g فقط نصف جرم واقعی ۶٫۸ g است و از اعمال نادرست بازده یا نسبت واکنش به‌دست می‌آید."},
        "fast": "محدودکننده → NH₃ نظری → جرم نظری → ضرب در ۰٫۸۰.",
        "lesson": "بازده را تنها پس از یافتن مقدار نظری فرآورده اعمال کن.",
    },
}


# Targeted repairs for every remaining active structural-scan flag, including two holdout
# explanations. Stems, options, keys, pools, and question identities are unchanged.
SECONDARY: dict[str, dict[str, Any]] = {
    "real_1404_n1in_chem_110": {
        "correct": "گزینهٔ ۴ درست است. اتیل بوتانوات با فرمول C₆H₁₂O₂ دارای ۱۲ اتم H و نفتالن C₁₀H₈ دارای ۸ اتم H است؛ نسبت Hها ۱۲/۸=۱٫۵ است. ترفتالیک اسید C₈H₆O₄ چهار O و اتیلن‌گلیکول C₂H₆O₂ دو O دارد، پس اختلاف Oها ۲ است. بنابراین ۱٫۵/۲=۰٫۷۵.",
        "d": {0:"۱٫۵/۲ برابر ۰٫۷۵ است، نه ۰٫۵۰.",1:"۱٫۰۰ از تقسیم ۸ بر ۸ یا حذف اختلاف Oها به‌دست می‌آید.",2:"۰٫۲۵ با فرمول‌های مولکولی و نسبت‌های خواسته‌شده سازگار نیست.",3:"درست است؛ نسبت ۱۲/۸ بر اختلاف ۴−۲ تقسیم می‌شود و ۰٫۷۵ می‌دهد."},
        "fast":"فرمول‌ها را بنویس: Hها ۱۲ و ۸؛ Oها ۴ و ۲؛ سپس (۱۲/۸)/(۴−۲).",
        "lesson":"در سوال‌های فرمول مولکولی، ابتدا شمار اتم هر عنصر را جداگانه استخراج کن.",
    },
    "real_1404_n2in_chem_088": {
        "correct": "گزینهٔ ۴ درست است. برای جرم m از چربی، گرمای مفید برابر ۰٫۸۰×۳۹m=۳۱٫۲m است. برای جرم x از زغال‌سنگ، گرمای مفید ۰٫۵۰×۳۰x=۱۵x است. شرط سؤال ۳۱٫۲m=۲(۱۵x) است؛ پس x/m=۳۱٫۲/۳۰=۱٫۰۴.",
        "d": {0:"۰٫۵۲ تنها نصف نسبت درست است و شرط «دو برابر» را برعکس اعمال می‌کند.",1:"۰٫۲۶ با معادلهٔ گرمای مفید دو سوخت سازگار نیست.",2:"۲٫۰۸ دو برابر کردن نادرست نسبت ۱٫۰۴ است.",3:"درست است؛ جرم زغال‌سنگ باید ۱٫۰۴ برابر جرم چربی باشد."},
        "fast":"گرمای مفید بر گرم: چربی ۰٫۸۰×۳۹=۳۱٫۲ و زغال‌سنگ ۰٫۵۰×۳۰=۱۵ kJ·g⁻¹؛ شرط دوبرابر را معادله کن.",
        "lesson":"برای مواد ناخالص، ابتدا ارزش سوختی را در کسر خلوص ضرب کن.",
    },
    "real_1404_n2in_chem_104": {
        "correct": "گزینهٔ ۴ درست است. چون X²⁺ اکسنده‌تر از Z²⁺ است، فلز Z کاهنده‌تر از X است. فلزهای D، Z و X با Cu²⁺ واکنش می‌دهند، پس هر سه از Cu کاهنده‌ترند و A از Cu ضعیف‌تر است. رسوب A و X از محلول یون‌هایشان به‌وسیلهٔ D یعنی D از A و X کاهنده‌تر است؛ رسوب ندادن Z یعنی Z از D کاهنده‌تر است. در نتیجه Z > D > X > Cu > A.",
        "d": {0:"X را از D و Z کاهنده‌تر می‌گیرد، در حالی که X²⁺ از Z²⁺ اکسنده‌تر است و D می‌تواند X²⁺ را کاهش دهد.",1:"D را از Cu ضعیف‌تر می‌گیرد، اما D با Cu²⁺ واکنش می‌دهد و Cu را رسوب می‌دهد.",2:"X را از Z کاهنده‌تر می‌گیرد؛ این با مقایسهٔ قدرت اکسندگی یون‌های X²⁺ و Z²⁺ ناسازگار است.",3:"درست است؛ هر سه داده به ترتیب Z > D > X > Cu > A می‌رسند."},
        "fast":"واکنش با Cu²⁺ یعنی فلز از Cu کاهنده‌تر است؛ رسوب دادن یون فلز دیگر یعنی فلز جامد کاهنده‌تر است.",
        "lesson":"قدرت اکسندگی یون و قدرت کاهندگی فلز متناظر در جهت مخالف رتبه‌بندی می‌شوند.",
    },
    "v3_chem_17_20": {
        "correct": "گزینهٔ ۲ درست است. در CH₄+2O₂→CO₂+2H₂O و در دما و فشار یکسان، نسبت حجم‌ها برابر نسبت ضرایب است. بنابراین V(O₂)=۲×۵٫۶ L=۱۱٫۲ L و V(CO₂)=۱×۵٫۶ L=۵٫۶ L.",
        "d": {0:"حجم O₂ را نصف مقدار لازم گرفته است؛ نسبت CH₄:O₂ برابر ۱:۲ است.",1:"درست است؛ O₂ دو برابر و CO₂ برابر حجم CH₄ مصرف‌شده است.",2:"۲۲٫۴ L نسبت O₂ را چهار برابر می‌گیرد.",3:"حجم CO₂ را بدون دلیل دو برابر گرفته است."},
        "fast":"برای گازهای هم‌دما و هم‌فشار، حجم‌ها را مستقیماً با ضرایب واکنش مقیاس کن.",
        "lesson":"نسبت حجم گازهای هم‌شرایط همان نسبت ضرایب واکنش موازنه‌شده است.",
    },
    "v3_chem_21_15": {
        "correct": "گزینهٔ ۳ درست است. انحلال‌پذیری ۳۰ g در ۱۰۰ g آب یعنی ۱۳۰ g محلول شامل ۱۰۰ g آب و ۳۰ g حل‌شونده است. چون ۲۶۰ g محلول دو برابر ۱۳۰ g است، جرم آب ۲۰۰ g و جرم حل‌شونده ۶۰ g خواهد بود.",
        "d": {0:"۷۸ g حل‌شونده با نسبت ۳۰ به ۱۰۰ سازگار نیست.",1:"۲۳۰ g آب و ۳۰ g حل‌شونده نسبت محلول اشباع را نادیده می‌گیرد.",2:"درست است؛ ۲۶۰/۱۳۰=۲، پس آب ۲۰۰ g و حل‌شونده ۶۰ g است.",3:"۱۰۰ g آب و ۱۶۰ g حل‌شونده نسبت انحلال‌پذیری را وارونه می‌کند."},
        "fast":"نسبت محلول اشباع ۱۳۰:۱۰۰:۳۰ است؛ ۲۶۰ g یعنی دو برابر.",
        "lesson":"انحلال‌پذیری «g حل‌شونده در ۱۰۰ g آب» را با جرم کل محلول اشتباه نگیر.",
    },
    "v3_chem_22_03": {
        "correct": "گزینهٔ ۳ درست است. برای اسید قوی تک‌پروتونیِ رقیق، ده‌برابر رقیق‌کردن یعنی [H₃O⁺] از C به C/10 می‌رسد. pH₂=−log(C/10)=−log C+۱=pH₁+۱؛ پس pH یک واحد زیاد می‌شود.",
        "d": {0:"یک واحد کم‌شدن جهت رابطهٔ لگاریتمی را برعکس می‌کند.",1:"تغییر pH لگاریتمی است؛ ده‌برابر رقیق‌کردن ۱۰ واحد تغییر نمی‌دهد.",2:"درست است؛ کاهش ده‌برابری [H₃O⁺] یک واحد pH را افزایش می‌دهد.",3:"pH با تغییر ده‌برابری غلظت H₃O⁺ ثابت نمی‌ماند."},
        "fast":"[H₃O⁺] ÷۱۰ یعنی pH +۱.",
        "lesson":"هر تغییر ضریب ۱۰ در [H₃O⁺] یک واحد با علامت مخالف در pH ایجاد می‌کند.",
    },
    "v3_chem_22_07": {
        "correct": "گزینهٔ ۳ درست است. در اسید قوی تک‌پروتونی رقیق، رقیق‌سازی ده‌برابری [H₃O⁺] را به یک‌دهم می‌رساند. چون pH=−log[H₃O⁺]، داریم pH₂=pH₁+۱؛ pH یک واحد بالا می‌رود.",
        "d": {0:"کم‌شدن یک واحدی pH برای افزایش ده‌برابری [H₃O⁺] رخ می‌دهد، نه رقیق‌سازی.",1:"ده‌برابر رقیق‌کردن ۱۰ واحد pH را تغییر نمی‌دهد.",2:"درست است؛ [H₃O⁺] یک‌دهم می‌شود و pH یک واحد زیاد می‌شود.",3:"رابطهٔ pH با [H₃O⁺] لگاریتمی است، پس تغییر می‌کند."},
        "fast":"C→C/10، بنابراین pH→pH+1.",
        "lesson":"قانون pH فقط با غلظت برحسب mol·L⁻¹ و در ناحیهٔ اسید قوی رقیق به‌کار می‌رود.",
    },
    "v3_chem_23_13": {
        "correct": "گزینهٔ ۱ درست است. از 2N₂O₅→4NO₂+O₂، به ازای مصرف ۲ mol N₂O₅، چهار mol NO₂ و یک mol O₂ تشکیل می‌شود. پس r(NO₂)=(۴/۲)×۰٫۰۳۰=۰٫۰۶۰ M·s⁻¹ و r(O₂)=(۱/۲)×۰٫۰۳۰=۰٫۰۱۵ M·s⁻¹.",
        "d": {0:"درست است؛ NO₂ دو برابر و O₂ نصف سرعت مصرف N₂O₅ تشکیل می‌شود.",1:"نسبت ضرایب ۲:۴:۱ را نادیده می‌گیرد.",2:"نسبت‌های NO₂ و O₂ را جابه‌جا می‌کند.",3:"هر دو سرعت را دو برابر مقدار درست می‌گیرد."},
        "fast":"سرعت تشکیل هر فرآورده = سرعت مصرف N₂O₅ × ضریب فرآورده/۲.",
        "lesson":"در سرعت‌های واکنش، نسبت ضرایب معادله برای نرخ‌های گونه‌ها به‌کار می‌رود.",
    },
    "v3_chem_24_03": {
        "correct": "گزینهٔ ۳ درست است. واکنش A→B دارای ΔH=+۶۰ kJ است. وارونۀ آن B→A دارای ΔH=−۶۰ kJ می‌شود. با دوبرابر شدن معادله، ΔH نیز دوبرابر است: ΔH(2B→2A)=۲×(−۶۰)=−۱۲۰ kJ.",
        "d": {0:"−۶۰ kJ فقط وارونگی را اعمال می‌کند و ضریب ۲ را نادیده می‌گیرد.",1:"+۱۲۰ kJ ضریب ۲ را اعمال کرده اما علامت را پس از وارونگی عوض نکرده است.",2:"درست است؛ وارونگی علامت و ضریب ۲ اندازهٔ ΔH را دو برابر می‌کند.",3:"+۶۰ kJ واکنش اصلی است، نه واکنش وارونهٔ دوبرابرشده."},
        "fast":"وارونه: علامت عوض؛ ضریب ۲: مقدار ΔH دو برابر.",
        "lesson":"ΔH کمیت گسترده است: با ضرب واکنش در ضریب، همان ضریب را می‌گیرد.",
    },
    "v3_chem_24_07": {
        "correct": "گزینهٔ ۳ درست است. A→B با ΔH=+۶۰ kJ است؛ برای B→A علامت به −۶۰ kJ تغییر می‌کند. واکنش 2B→2A دوبرابر است، بنابراین ΔH=۲×(−۶۰)=−۱۲۰ kJ.",
        "d": {0:"اثر ضریب ۲ را حذف می‌کند و فقط آنتالپی واکنش وارونه را گزارش می‌دهد.",1:"وارونه شدن واکنش را بدون تغییر علامت نوشته است.",2:"درست است؛ هم علامت وارونگی و هم ضریب ۲ اعمال می‌شود.",3:"آنتالپی واکنش اولیه را بدون هیچ تبدیل نشان می‌دهد."},
        "fast":"+۶۰ → −۶۰ با وارونگی؛ سپس ×۲ → −۱۲۰ kJ.",
        "lesson":"در قانون هس، جهت واکنش علامت ΔH و ضریب واکنش اندازهٔ ΔH را تعیین می‌کند.",
    },
    "v3_chem_25_05": {
        "correct": "گزینهٔ ۱ درست است. در Zn→Zn²⁺+2e⁻، عدد اکسایش Zn از ۰ به +۲ می‌رود؛ افزایش دو واحدی عدد اکسایش به معنای از دست دادن ۲ الکترون به‌ازای هر اتم Zn است.",
        "d": {0:"درست است؛ ضریب 2e⁻ در نیم‌واکنش نشان می‌دهد هر Zn دو الکترون از دست می‌دهد.",1:"۱ الکترون افزایش عدد اکسایش را فقط یک واحد فرض می‌کند.",2:"۳ الکترون با تغییر عدد اکسایش ۰ به +۲ سازگار نیست.",3:"۴ الکترون ضریب الکترون را بی‌دلیل دو برابر می‌کند."},
        "fast":"Zn⁰→Zn²⁺ یعنی از دست دادن ۲e⁻.",
        "lesson":"قدر مطلق تغییر عدد اکسایش، تعداد الکترون‌های مبادله‌شده به‌ازای همان اتم است.",
    },
    "v3_chem_25_09": {
        "correct": "گزینهٔ ۱ درست است. Zn⁰→Zn²⁺ یعنی عدد اکسایش روی دو واحد افزایش یافته است؛ پس هر اتم Zn دو الکترون از دست می‌دهد و نیم‌واکنش Zn→Zn²⁺+2e⁻ موازنه می‌شود.",
        "d": {0:"درست است؛ افزایش ۰ به +۲ معادل از دست دادن ۲e⁻ است.",1:"۱ الکترون تنها افزایش یک واحدی عدد اکسایش را جبران می‌کند.",2:"۳ الکترون با بار یون Zn²⁺ سازگار نیست.",3:"۴ الکترون بار نیم‌واکنش را نامتعادل می‌کند."},
        "fast":"Zn²⁺ نسبت به Zn⁰ دو بار مثبت‌تر است؛ پس ۲e⁻ خارج شده است.",
        "lesson":"در نیم‌واکنش‌ها، تعداد الکترون‌ها باید هم بار و هم تعداد اتم‌ها را موازنه کند.",
    },
}


def new_questions(template: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        question_template(template, identifier="v62_chem_17_06",
            stem="در واکنش CaCO₃ + 2HCl → CaCl₂ + CO₂ + H₂O، اگر ۵٫۰ g CaCO₃ خالص با HCl اضافی واکنش دهد، حجم CO₂ در STP چند لیتر است؟ (M(CaCO₃)=۱۰۰ g·mol⁻¹)",
            options=["۰٫۵۶ L", "۱٫۱۲ L", "۲٫۲۴ L", "۵٫۶۰ L"], correct_index=1,
            correct="گزینهٔ ۲ درست است. n(CaCO₃)=۵٫۰ g / ۱۰۰ g·mol⁻¹=۰٫۰۵ mol است. نسبت CaCO₃:CO₂ برابر ۱:۱ است؛ بنابراین n(CO₂)=۰٫۰۵ mol و V=۰٫۰۵×۲۲٫۴ L·mol⁻¹=۱٫۱۲ L در STP.",
            distractors={0:"۰٫۵۶ L نسبت ۱:۱ را به‌اشتباه نصف می‌کند.",1:"درست است؛ ۰٫۰۵ mol CO₂ در STP حجمی برابر ۱٫۱۲ L دارد.",2:"۲٫۲۴ L مقدار مول CO₂ را دو برابر می‌گیرد.",3:"۵٫۶۰ L حجم ۰٫۲۵ mol است و با ۵٫۰ g CaCO₃ سازگار نیست."},
            fast="۵٫۰/۱۰۰=۰٫۰۵ mol؛ سپس ۰٫۰۵×۲۲٫۴=۱٫۱۲ L.", lesson="با واکنش‌دهندۀ اضافی، مقدار فرآورده فقط از مقدار واکنش‌دهندۀ داده‌شده و نسبت ضرایب به‌دست می‌آید.", form="numerical_multi_stage", difficulty=3, seconds=85, subskill="جرم به حجم گاز", evidence="حجم مولی گاز در STP در متن supplied Chemistry 1، PDF page 88 آمده است.", page=88),
        question_template(template, identifier="v62_chem_17_07",
            stem="در واکنش 2Al + 6HCl → 2AlCl₃ + 3H₂، از واکنش کامل ۵٫۴ g Al خالص با HCl اضافی، حجم H₂ در STP چند لیتر است؟ (M(Al)=۲۷ g·mol⁻¹)",
            options=["۲٫۲۴ L", "۴٫۴۸ L", "۶٫۷۲ L", "۱۳٫۴۴ L"], correct_index=2,
            correct="گزینهٔ ۳ درست است. n(Al)=۵٫۴/۲۷=۰٫۲۰ mol. از نسبت 2Al:3H₂، n(H₂)=۰٫۲۰×۳/۲=۰٫۳۰ mol؛ پس V=۰٫۳۰×۲۲٫۴=۶٫۷۲ L در STP.",
            distractors={0:"۲٫۲۴ L حجم ۰٫۱۰ mol است و نسبت ۳/۲ را به‌کار نمی‌برد.",1:"۴٫۴۸ L حجم ۰٫۲۰ mol است و نسبت 2Al:3H₂ حذف شده است.",2:"درست است؛ ۰٫۲۰ mol Al، ۰٫۳۰ mol H₂ و ۶٫۷۲ L H₂ می‌دهد.",3:"۱۳٫۴۴ L مقدار H₂ را دو برابر می‌گیرد."},
            fast="۵٫۴/۲۷=۰٫۲۰؛ ×۳/۲=۰٫۳۰؛ ×۲۲٫۴=۶٫۷۲ L.", lesson="در استوکیومتری، نسبت ضریب‌های واکنش فقط پس از تبدیل جرم به مول اعمال می‌شود.", form="numerical_multi_stage", difficulty=3, seconds=90, subskill="استوکیومتری گاز", evidence="حجم مولی گاز در STP در متن supplied Chemistry 1، PDF page 88 آمده است.", page=88),
        question_template(template, identifier="v62_chem_17_08",
            stem="۲٫۰ L از یک گاز در ۱٫۰ atm و ۳۰۰ K قرار دارد. اگر دما به ۴۵۰ K برسد و فشار به ۰٫۵ atm کاهش یابد، حجم نهایی گاز چند لیتر است؟ (n ثابت است)",
            options=["۱٫۵ L", "۳٫۰ L", "۴٫۵ L", "۶٫۰ L"], correct_index=3,
            correct="گزینهٔ ۴ درست است. از P₁V₁/T₁=P₂V₂/T₂ داریم: V₂=(P₁V₁T₂)/(P₂T₁)=(۱٫۰×۲٫۰×۴۵۰)/(۰٫۵×۳۰۰)=۶٫۰ L. افزایش دما حجم را زیاد و کاهش فشار نیز حجم را زیاد می‌کند.",
            distractors={0:"۱٫۵ L جهت تغییر فشار و دما را نادرست می‌گیرد.",1:"۳٫۰ L فقط اثر افزایش دما را یا فشار را ناقص حساب می‌کند.",2:"۴٫۵ L از نسبت‌های ۴۵۰/۳۰۰ و ۱/۰٫۵ به‌دست نمی‌آید.",3:"درست است؛ قانون ترکیبی گازها حجم ۶٫۰ L می‌دهد."},
            fast="V₂/V₁=(P₁/P₂)×(T₂/T₁)=۲×۱٫۵=۳؛ پس ۲٫۰ L به ۶٫۰ L می‌رسد.", lesson="در قانون ترکیبی گازها، فشار و حجم وارون و دما و حجم مستقیم‌اند؛ دما باید کلوین باشد.", form="numerical_multi_stage", difficulty=3, seconds=90, subskill="قانون ترکیبی گازها", evidence="Item is textbook-bounded gas-law practice; all stated pressure, volume, and Kelvin-temperature relations are explicitly re-solved.", page=None),
        question_template(template, identifier="v62_chem_17_09",
            stem="برای تهیهٔ ۲۵۰ mL محلول ۰٫۱۰ mol·L⁻¹ NaOH، چند مول NaOH لازم است؟",
            options=["۰٫۰۱۰ mol", "۰٫۰۲۵ mol", "۰٫۱۰۰ mol", "۲٫۵۰۰ mol"], correct_index=1,
            correct="گزینهٔ ۲ درست است. از M=n/V داریم n=MV=۰٫۱۰ mol·L⁻¹×۰٫۲۵۰ L=۰٫۰۲۵ mol. پیش از ضرب، ۲۵۰ mL باید به ۰٫۲۵۰ L تبدیل شود.",
            distractors={0:"۰٫۰۱۰ mol حجم محلول را نادیده می‌گیرد.",1:"درست است؛ ۰٫۱۰×۰٫۲۵۰=۰٫۰۲۵ mol.",2:"۰٫۱۰۰ mol مقدار یک لیتر محلول ۰٫۱۰ مولار است، نه ۲۵۰ mL.",3:"۲٫۵۰۰ mol تبدیل mL به L را ۱۰۰۰ برابر نادرست انجام می‌دهد."},
            fast="۲۵۰ mL=۰٫۲۵۰ L؛ سپس n=۰٫۱۰×۰٫۲۵۰=۰٫۰۲۵ mol.", lesson="در رابطهٔ M=n/V، حجم باید برحسب لیتر باشد.", form="numerical_single_stage", difficulty=2, seconds=65, subskill="مولاریته و تبدیل واحد", evidence="Item is textbook-bounded solution-concentration practice; concentration relation and unit conversion were independently re-solved.", page=None),
        question_template(template, identifier="v62_chem_17_10",
            stem="در واکنش Fe₂O₃ + 3CO → 2Fe + 3CO₂، از واکنش کامل ۱۶٫۰ g Fe₂O₃ خالص با CO اضافی، حجم CO₂ در STP چند لیتر است؟ (M(Fe₂O₃)=۱۶۰ g·mol⁻¹)",
            options=["۲٫۲۴ L", "۴٫۴۸ L", "۶٫۷۲ L", "۱۳٫۴۴ L"], correct_index=2,
            correct="گزینهٔ ۳ درست است. n(Fe₂O₃)=۱۶٫۰/۱۶۰=۰٫۱۰ mol. نسبت Fe₂O₃:CO₂ برابر ۱:۳ است؛ پس n(CO₂)=۰٫۳۰ mol و V=۰٫۳۰×۲۲٫۴=۶٫۷۲ L در STP.",
            distractors={0:"۲٫۲۴ L حجم ۰٫۱۰ mol است و نسبت ۱:۳ را حذف می‌کند.",1:"۴٫۴۸ L حجم ۰٫۲۰ mol است و با ضریب ۳ سازگار نیست.",2:"درست است؛ ۰٫۱۰ mol Fe₂O₃، ۰٫۳۰ mol CO₂ و ۶٫۷۲ L CO₂ می‌دهد.",3:"۱۳٫۴۴ L مقدار CO₂ را دو برابر می‌گیرد."},
            fast="۱۶٫۰/۱۶۰=۰٫۱۰؛ ×۳=۰٫۳۰؛ ×۲۲٫۴=۶٫۷۲ L.", lesson="در مسائل جرم–حجم گاز، نسبت مولی را از ضرایب واکنش موازنه‌شده بخوان.", form="numerical_multi_stage", difficulty=3, seconds=85, subskill="نسبت مولی و حجم گاز", evidence="حجم مولی گاز در STP در متن supplied Chemistry 1، PDF page 88 آمده است.", page=88),
    ]


shutil.copyfile(SOURCE_DB, OUT_DB)
conn = sqlite3.connect(OUT_DB)
conn.row_factory = sqlite3.Row
rows = conn.execute("SELECT * FROM question WHERE subject=?", ("شیمی",)).fetchall()
column_names = [info[1] for info in conn.execute("PRAGMA table_info(question)")]
questions: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
for row in rows:
    stored = dict(row)
    questions[stored["id"]] = (stored, json.loads(stored["full_json"]))

# Clean review-facing artifacts throughout Chemistry; use high-priority bespoke rewrites below.
for identifier, (stored, q) in questions.items():
    for field in ("correct_analysis", "short_lesson", "fast_method", "start_method"):
        q[field] = clean_text(q.get(field, ""))
    q["distractor_analyses"] = {str(key): clean_text(value) for key, value in (q.get("distractor_analyses") or {}).items()}
    q["review_default"] = review_default(q)

for identifier, content in DEEP.items():
    stored, q = questions[identifier]
    set_explanations(q, content["correct"], content["d"], content["fast"], content["lesson"])
    q["scientific_verification_v6_2"] = {
        "status": "DEEP_REVIEWED_EXACT_REASONING",
        "scope": "Priority-74 Chemistry item; stem, key, each option, and solution path manually re-solved.",
    }

for identifier, content in SECONDARY.items():
    stored, q = questions[identifier]
    set_explanations(q, content["correct"], content["d"], content["fast"], content["lesson"])
    if identifier in {"v3_chem_25_05", "v3_chem_25_09"}:
        q["calculation_required"] = False
    q["scientific_verification_v6_2"] = {
        "status": "TARGETED_SCAN_REPAIR",
        "scope": "Active scan-flagged Chemistry item; key, all options, and solution path manually checked.",
    }

# Retire the five accidental/cosmetic variants without deleting their historical identities.
retirement_rows: list[dict[str, Any]] = []
for old_id, new_id in RETIRED.items():
    stored, q = questions[old_id]
    q["selected_scope"] = False
    q["obsolete_for_1405"] = True
    q["v6_2_retirement"] = {
        "status": "RETIRED_COSMETIC_OR_ACCIDENTAL_REPEAT",
        "replacement_id": new_id,
        "progress_policy": "Keep historical attempts under the retired ID. Do not transfer mastery or attempts to the replacement because identity changed.",
    }
    stored["selected_scope"] = 0
    stored["obsolete"] = 1
    retirement_rows.append({"retired_id": old_id, "replacement_id": new_id, "reason": "duplicate/cosmetic variant in priority-74 stoichiometry training", "progress_policy": q["v6_2_retirement"]["progress_policy"]})

# Add five new, distinct question identities.
seed = questions["v3_chem_17_15"][1]
new_rows: list[dict[str, Any]] = []
for q in new_questions(seed):
    row = copy.deepcopy(questions["v3_chem_17_15"][0])
    row.update({
        "id": q["id"], "subject": "شیمی", "microtopic": "مول، استوکیومتری و گازها", "source_type": "authored",
        "question_type": q["question_type"], "difficulty": q["difficulty"], "priority": q["priority"], "selected_scope": 1,
        "obsolete": 0, "correct_index": q["correct_index"], "estimated_seconds": q["estimated_solve_time_seconds"],
        "question_form": q["question_form"], "scenario_family": q["scenario_family"], "followup_group": q["followup_group"],
        "subskill": q["subskill"], "has_source_crop": 0, "access_pool": "TRAIN", "teaching_ladder_level": q["teaching_ladder_level"],
        "runtime_scope_status": q["runtime_scope_status"],
    })
    row["full_json"] = json.dumps(q, ensure_ascii=False, separators=(",", ":"))
    new_rows.append(row)

# Persist all changed source rows atomically.
for identifier, (stored, q) in questions.items():
    stored["full_json"] = json.dumps(q, ensure_ascii=False, separators=(",", ":"))
    assignments = ", ".join(f"{column}=?" for column in column_names if column != "id")
    values = [stored[column] for column in column_names if column != "id"] + [identifier]
    conn.execute(f"UPDATE question SET {assignments} WHERE id=?", values)

placeholders = ",".join("?" for _ in column_names)
columns_sql = ",".join(column_names)
for row in new_rows:
    conn.execute(f"INSERT INTO question ({columns_sql}) VALUES ({placeholders})", [row[column] for column in column_names])

metadata = {
    "bank_version": "6.2.0-chemistry-qa-candidate",
    "baseline_db_sha256": sha256(SOURCE_DB),
    "scope": "Chemistry review-quality and duplicate remediation only",
    "question_total": 1221,
    "chemistry_total": 272,
    "deep_reviewed_ids": sorted(DEEP),
    "targeted_scan_repaired_ids": sorted(SECONDARY),
    "retirement_mapping": retirement_rows,
    "source_evidence": {
        "chemistry_1_drive_file_id": "1rmRyR509x-8bDAS0FG6WiP9R5DtXjfXH",
        "chemistry_1_title": "Shimi 10.pdf",
        "molar_volume_source_pdf_page": 88,
        "molar_volume_excerpt": "حجم یک مول گاز در STP برابر با 22.4 لیتر است.",
    },
    "progress_migration": "No destructive Room migration. BankStore must use a new v6_2 asset/database name; the existing progress database remains untouched. Retired questions keep their IDs for historical attempts and replacements receive distinct IDs with no fabricated mastery transfer.",
}
conn.execute("INSERT OR REPLACE INTO bank_root(key,json) VALUES(?,?)", ("v6_2_chemistry_qa", json.dumps(metadata, ensure_ascii=False, separators=(",", ":"))))
conn.commit()
integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
new_total = conn.execute("SELECT COUNT(*) FROM question").fetchone()[0]
chem_total = conn.execute("SELECT COUNT(*) FROM question WHERE subject='شیمی'").fetchone()[0]
selected_train = conn.execute("SELECT COUNT(*) FROM question WHERE subject='شیمی' AND access_pool='TRAIN' AND selected_scope=1 AND obsolete=0").fetchone()[0]
conn.close()
if integrity != "ok" or new_total != 1221 or chem_total != 272 or selected_train != 203:
    raise RuntimeError(f"candidate integrity/count failure: integrity={integrity}, total={new_total}, chem={chem_total}, selected={selected_train}")

with OUT_DB.open("rb") as source, gzip.GzipFile(filename="", mode="wb", fileobj=OUT_GZ.open("wb"), mtime=0) as target:
    shutil.copyfileobj(source, target, length=1024 * 1024)

manifest = {
    "candidate_db": OUT_DB.name,
    "candidate_db_sha256": sha256(OUT_DB),
    "candidate_gzip": OUT_GZ.name,
    "candidate_gzip_sha256": sha256(OUT_GZ),
    "integrity_check": integrity,
    "question_total": new_total,
    "chemistry_total": chem_total,
    "selected_train_chemistry": selected_train,
    "deep_reviewed": len(DEEP),
    "targeted_scan_repairs": len(SECONDARY),
    "retired_cosmetic_variants": len(RETIRED),
    "new_distinct_replacements": len(new_rows),
}
(AUDIT_DIR / "BANK-V6.2-CHEMISTRY-MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(AUDIT_DIR / "CHEMISTRY-V6.2-MIGRATION-MAPPING.json").write_text(json.dumps({"retirements": retirement_rows, "policy": metadata["progress_migration"]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(AUDIT_DIR / "CHEMISTRY-V6.2-DEEP-REVIEW.json").write_text(json.dumps({identifier: {"correct_analysis": questions[identifier][1]["correct_analysis"], "distractor_analyses": questions[identifier][1]["distractor_analyses"], "fast_method": questions[identifier][1]["fast_method"]} for identifier in sorted(DEEP)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(manifest, ensure_ascii=False, indent=2))
