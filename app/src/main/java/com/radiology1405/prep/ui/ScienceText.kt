package com.radiology1405.prep.ui

import androidx.compose.material3.LocalContentColor
import androidx.compose.material3.LocalTextStyle
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.TextUnit

private const val LRI = '\u2066'
private const val PDI = '\u2069'

private val scienceRun = Regex(
    "[A-Za-z0-9₀-₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻′°→←↔×·√ΩΔθπ∞=<>/().∩∪|]+(?:[ \\t]*[A-Za-z0-9₀-₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻′°→←↔×·√ΩΔθπ∞=<>/().∩∪]+)*"
)

private val learnerFacingLabels = linkedMapOf(
    "condition_wrong" to "نادیده‌گرفتن شرط",
    "wrong_condition" to "نادیده‌گرفتن شرط",
    "truth_partial" to "درستِ ناقص",
    "partial_truth" to "درستِ ناقص",
    "overgeneralization" to "تعمیم نادرست",
    "correct_reasoning" to "استدلال درست",
    "calculation_trap" to "خطای محاسبه",
    "calculation_error" to "خطای محاسبه",
    "unit_mistake" to "خطای واحد",
    "direction_error" to "خطای جهت",
    "false_absolute" to "مطلق‌انگاری نادرست",
    "keyword_trap" to "پاسخ‌دادن بر پایهٔ کلیدواژه",
    "knowledge_gap" to "نیاز به مرور مفهوم",
    "forgotten_rule" to "فراموشی قاعده",
    "misread" to "بدخوانی صورت سؤال",
    "time_management" to "مدیریت زمان",
    "careless_error" to "بی‌دقتی",
)

private val reviewBoilerplate = listOf(
    Regex("منشأ دام این گزینه [^.]* است\\.\\s*"),
    Regex("منشأ دام: [^.]*\\.\\s*"),
    Regex("این گزینه با همهٔ شرط‌ها سازگار است\\.\\s*"),
    Regex("این گزینه با همه شرط ها سازگار است\\.\\s*"),
    Regex("این گزاره با کتاب سازگار است؛\\s*"),
    Regex("این گزاره دام مفهومی دارد؛\\s*"),
    Regex("از کلیدواژه جواب نده؛ شرط هر گزینه را بسنج\\.\\s*"),
    Regex("روش کنترل:\\s*"),
    Regex("نکتهٔ تثبیتی:\\s*"),
)

/** Replaces internal labels and removes only stock review filler; question-specific reasoning is preserved. */
fun learnerFacingScientificText(value: String): String {
    val localized = learnerFacingLabels.entries.fold(value) { rendered, (internal, label) ->
        rendered.replace(internal, label, ignoreCase = true)
    }
    return reviewBoilerplate.fold(localized) { rendered, filler -> filler.replace(rendered, "") }
        .replace(Regex("\\s{2,}"), " ")
        .trim()
}

/** Unicode bidi isolation keeps formula direction intact inside a Persian paragraph. */
fun isolateScientificRuns(value: String): String = scienceRun.replace(learnerFacingScientificText(value)) { match ->
    "$LRI${match.value}$PDI"
}

fun removeScientificIsolates(value: String): String = value.replace(LRI.toString(), "").replace(PDI.toString(), "")

@Composable
fun ScienceText(
    text: String,
    modifier: Modifier = Modifier,
    color: Color = LocalContentColor.current,
    fontSize: TextUnit = TextUnit.Unspecified,
    style: TextStyle? = null,
    textAlign: TextAlign? = null,
) {
    Text(
        text = isolateScientificRuns(text),
        modifier = modifier,
        color = color,
        fontSize = fontSize,
        style = style ?: LocalTextStyle.current,
        textAlign = textAlign,
    )
}
