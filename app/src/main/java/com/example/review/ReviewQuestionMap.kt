package com.example.review

import androidx.annotation.DrawableRes
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.itemsIndexed
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.Saver
import androidx.compose.runtime.saveable.listSaver
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.painter.Painter
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.Image

/**
 * Presentation-only outcome. Do not expose persistence or database enum names in the UI.
 */
enum class AnswerOutcome {
  CORRECT,
  WRONG,
  BLANK,
}

enum class ReviewConfidence(val persianLabel: String) {
  LOW("اطمینان کم"),
  MEDIUM("اطمینان متوسط"),
  HIGH("اطمینان زیاد"),
}

enum class ReviewErrorType(val persianLabel: String) {
  CONCEPT("برداشت مفهومی"),
  CALCULATION("محاسبه"),
  READING("خواندن صورت پرسش"),
  MEMORY("بازیابی از حافظه"),
  TIME_MANAGEMENT("مدیریت زمان"),
  OTHER("نیازمند بررسی"),
}

/**
 * The data contract required to make a post-submit Review independent from the active question screen.
 * Option order is preserved exactly as delivered by the question bank.
 */
@Immutable
data class ReviewQuestion(
  val questionId: String,
  val stem: String,
  val options: List<String>,
  val selectedOptionIndex: Int?,
  val correctOptionIndex: Int,
  val confidence: ReviewConfidence?,
  val solution: String,
  val selectedWrongReasoning: String? = null,
  val wrongOptionExplanations: Map<Int, String> = emptyMap(),
  val microtopic: String? = null,
  val source: String? = null,
  val errorType: ReviewErrorType? = null,
  @DrawableRes val figureResId: Int? = null,
) {
  init {
    require(options.size == REQUIRED_OPTION_COUNT) { "Review requires exactly four original options." }
    require(correctOptionIndex in options.indices) { "Correct option must be one of the original options." }
    require(selectedOptionIndex == null || selectedOptionIndex in options.indices) {
      "Selected option must be one of the original options."
    }
  }

  val outcome: AnswerOutcome
    get() = when {
      selectedOptionIndex == null -> AnswerOutcome.BLANK
      selectedOptionIndex == correctOptionIndex -> AnswerOutcome.CORRECT
      else -> AnswerOutcome.WRONG
    }

  companion object {
    const val REQUIRED_OPTION_COUNT = 4
  }
}

data class QuestionMapEntry(
  val questionId: String,
  val selectedOptionIndex: Int? = null,
  val isFlagged: Boolean = false,
  val outcome: AnswerOutcome? = null,
)

enum class QuestionMapVisualState(val persianLabel: String) {
  CURRENT("پرسش جاری"),
  UNANSWERED("بی‌پاسخ"),
  ANSWERED("پاسخ‌داده‌شده"),
  FLAGGED("نشان‌دار"),
  CORRECT("درست"),
  WRONG("نادرست"),
  BLANK("بی‌پاسخ"),
}

fun QuestionMapEntry.visualState(
  isCurrent: Boolean,
  isSubmitted: Boolean,
): QuestionMapVisualState = when {
  isCurrent -> QuestionMapVisualState.CURRENT
  isSubmitted -> when (outcome) {
    AnswerOutcome.CORRECT -> QuestionMapVisualState.CORRECT
    AnswerOutcome.WRONG -> QuestionMapVisualState.WRONG
    AnswerOutcome.BLANK, null -> QuestionMapVisualState.BLANK
  }
  isFlagged -> QuestionMapVisualState.FLAGGED
  selectedOptionIndex == null -> QuestionMapVisualState.UNANSWERED
  else -> QuestionMapVisualState.ANSWERED
}

/**
 * A complete serializable map snapshot. Persist it with the session record (for example in Room)
 * and use [QuestionMapState.restore] on session resume. [rememberQuestionMapState] additionally
 * survives Android configuration and process recreation through the saved-state registry.
 */
@Immutable
data class QuestionMapSnapshot(
  val selectedQuestionId: String,
  val entries: List<QuestionMapEntry>,
)

/**
 * Stateful map controller. It contains only presentation/session facts, never question wording,
 * so the bank remains the source of truth for Review content.
 */
class QuestionMapState private constructor(
  entries: List<QuestionMapEntry>,
  selectedQuestionId: String,
) {
  var entries: List<QuestionMapEntry> by mutableStateOf(entries)
    private set

  var selectedQuestionId: String by mutableStateOf(selectedQuestionId)
    private set

  init {
    require(entries.isNotEmpty()) { "A Question Map needs at least one question." }
    require(entries.map { it.questionId }.distinct().size == entries.size) {
      "Question Map question IDs must be unique."
    }
    require(entries.any { it.questionId == selectedQuestionId }) {
      "Selected question must exist in the Question Map."
    }
  }

  fun select(questionId: String) {
    require(entries.any { it.questionId == questionId }) { "Cannot select an unknown question." }
    selectedQuestionId = questionId
  }

  fun updateAnswer(questionId: String, selectedOptionIndex: Int?) {
    updateEntry(questionId) { it.copy(selectedOptionIndex = selectedOptionIndex) }
  }

  fun setFlagged(questionId: String, isFlagged: Boolean) {
    updateEntry(questionId) { it.copy(isFlagged = isFlagged) }
  }

  fun recordOutcome(questionId: String, outcome: AnswerOutcome) {
    updateEntry(questionId) { it.copy(outcome = outcome) }
  }

  fun snapshot(): QuestionMapSnapshot = QuestionMapSnapshot(
    selectedQuestionId = selectedQuestionId,
    entries = entries,
  )

  private fun updateEntry(questionId: String, transform: (QuestionMapEntry) -> QuestionMapEntry) {
    var found = false
    entries = entries.map { entry ->
      if (entry.questionId == questionId) {
        found = true
        transform(entry)
      } else {
        entry
      }
    }
    require(found) { "Cannot update an unknown question." }
  }

  companion object {
    fun create(
      entries: List<QuestionMapEntry>,
      selectedQuestionId: String = entries.firstOrNull()?.questionId
        ?: error("A Question Map needs at least one question."),
    ): QuestionMapState = QuestionMapState(entries, selectedQuestionId)

    fun restore(snapshot: QuestionMapSnapshot): QuestionMapState =
      QuestionMapState(snapshot.entries, snapshot.selectedQuestionId)

    /**
     * Bundle-safe saver: IDs, selected options, flags, outcomes, and current location are all kept.
     * This is intentionally independent of any ViewModel so callers can also persist [snapshot] in Room.
     */
    fun saver(): Saver<QuestionMapState, Any> = listSaver(
      save = { state ->
        listOf(
          state.selectedQuestionId,
          ArrayList(state.entries.map { it.questionId }),
          ArrayList(state.entries.map { it.selectedOptionIndex?.toString() ?: "" }),
          ArrayList(state.entries.map { it.isFlagged.toString() }),
          ArrayList(state.entries.map { it.outcome?.name ?: "" }),
        )
      },
      restore = { saved ->
        val selectedId = saved[0] as String
        val ids = saved[1] as ArrayList<*>
        val answers = saved[2] as ArrayList<*>
        val flags = saved[3] as ArrayList<*>
        val outcomes = saved[4] as ArrayList<*>
        val restoredEntries = ids.indices.map { index ->
          QuestionMapEntry(
            questionId = ids[index] as String,
            selectedOptionIndex = (answers[index] as String).ifBlank { null }?.toInt(),
            isFlagged = (flags[index] as String).toBoolean(),
            outcome = (outcomes[index] as String).ifBlank { null }?.let(AnswerOutcome::valueOf),
          )
        }
        QuestionMapState(restoredEntries, selectedId)
      },
    )
  }
}

@Composable
fun rememberQuestionMapState(
  entries: List<QuestionMapEntry>,
  selectedQuestionId: String = entries.firstOrNull()?.questionId
    ?: error("A Question Map needs at least one question."),
): QuestionMapState = rememberSaveable(saver = QuestionMapState.saver()) {
  QuestionMapState.create(entries, selectedQuestionId)
}

/**
 * A full-block, directly tappable Question Map. It is deliberately self-contained: the caller
 * supplies navigation in [onQuestionSelected], so navigating previous/next or reopening a map does
 * not rebuild or lose map state.
 */
@Composable
fun QuestionMap(
  state: QuestionMapState,
  isSubmitted: Boolean,
  onQuestionSelected: (String) -> Unit,
  modifier: Modifier = Modifier,
) {
  CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
    Column(
      modifier = modifier
        .fillMaxWidth()
        .semantics { contentDescription = "نقشهٔ کامل پرسش‌های این بخش" },
      verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
      Text(
        text = "نقشهٔ پرسش‌ها",
        style = MaterialTheme.typography.titleLarge,
        fontWeight = FontWeight.Bold,
      )
      Text(
        text = if (isSubmitted) {
          "برای باز کردن مرور هر پرسش، شمارهٔ آن را لمس کنید."
        } else {
          "برای رفتن مستقیم به هر پرسش، شمارهٔ آن را لمس کنید."
        },
        style = MaterialTheme.typography.bodyMedium,
      )
      QuestionMapLegend(isSubmitted = isSubmitted)
      LazyVerticalGrid(
        columns = GridCells.Adaptive(minSize = 52.dp),
        modifier = Modifier
          .fillMaxWidth()
          .heightIn(min = 88.dp, max = 360.dp),
        contentPadding = PaddingValues(2.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
      ) {
        itemsIndexed(state.entries, key = { _, entry -> entry.questionId }) { index, entry ->
          val visualState = entry.visualState(
            isCurrent = entry.questionId == state.selectedQuestionId,
            isSubmitted = isSubmitted,
          )
          QuestionMapCell(
            number = index + 1,
            visualState = visualState,
            onClick = {
              state.select(entry.questionId)
              onQuestionSelected(entry.questionId)
            },
          )
        }
      }
    }
  }
}

@Composable
private fun QuestionMapLegend(isSubmitted: Boolean) {
  val legendStates = if (isSubmitted) {
    listOf(
      QuestionMapVisualState.CURRENT,
      QuestionMapVisualState.CORRECT,
      QuestionMapVisualState.WRONG,
      QuestionMapVisualState.BLANK,
    )
  } else {
    listOf(
      QuestionMapVisualState.CURRENT,
      QuestionMapVisualState.UNANSWERED,
      QuestionMapVisualState.ANSWERED,
      QuestionMapVisualState.FLAGGED,
    )
  }
  Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
    legendStates.forEach { visualState ->
      Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
        Box(
          modifier = Modifier
            .size(10.dp)
            .clip(CircleShape)
            .background(visualState.color()),
        )
        Text(visualState.persianLabel, style = MaterialTheme.typography.labelSmall)
      }
    }
  }
}

@Composable
private fun QuestionMapCell(
  number: Int,
  visualState: QuestionMapVisualState,
  onClick: () -> Unit,
) {
  val colors = mapCellColors(visualState)
  Surface(
    modifier = Modifier
      .size(52.dp)
      .clip(RoundedCornerShape(14.dp))
      .clickable(onClick = onClick)
      .semantics { contentDescription = "پرسش $number، ${visualState.persianLabel}" },
    color = colors.first,
    contentColor = colors.second,
  ) {
    Box(contentAlignment = Alignment.Center) {
      Text(number.toString(), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
    }
  }
}

@Composable
private fun QuestionMapVisualState.color(): Color = mapCellColors(this).first

@Composable
private fun mapCellColors(state: QuestionMapVisualState): Pair<Color, Color> = when (state) {
  QuestionMapVisualState.CURRENT -> MaterialTheme.colorScheme.primary to MaterialTheme.colorScheme.onPrimary
  QuestionMapVisualState.UNANSWERED -> MaterialTheme.colorScheme.surfaceVariant to MaterialTheme.colorScheme.onSurfaceVariant
  QuestionMapVisualState.ANSWERED -> MaterialTheme.colorScheme.secondaryContainer to MaterialTheme.colorScheme.onSecondaryContainer
  QuestionMapVisualState.FLAGGED -> MaterialTheme.colorScheme.tertiaryContainer to MaterialTheme.colorScheme.onTertiaryContainer
  QuestionMapVisualState.CORRECT -> MaterialTheme.colorScheme.primaryContainer to MaterialTheme.colorScheme.onPrimaryContainer
  QuestionMapVisualState.WRONG -> MaterialTheme.colorScheme.errorContainer to MaterialTheme.colorScheme.onErrorContainer
  QuestionMapVisualState.BLANK -> MaterialTheme.colorScheme.surfaceVariant to MaterialTheme.colorScheme.onSurfaceVariant
}

/**
 * Standalone post-submit review. All learner-facing wording is Persian and the screen renders the
 * original stem, every option, answers, outcome, confidence, and question-specific evidence from
 * [ReviewQuestion] without depending on the active attempt screen.
 */
@Composable
fun StandaloneReview(
  question: ReviewQuestion,
  modifier: Modifier = Modifier,
  figurePainter: Painter? = question.figureResId?.let { resourceId -> painterResource(id = resourceId) },
) {
  CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
    Column(
      modifier = modifier
        .fillMaxWidth()
        .verticalScroll(rememberScrollState())
        .padding(16.dp)
        .semantics { contentDescription = "مرور کامل پرسش" },
      verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
      ReviewHeader(question)
      Text(
        text = question.stem,
        style = MaterialTheme.typography.titleMedium,
        fontWeight = FontWeight.SemiBold,
      )
      if (figurePainter != null) {
        Image(
          painter = figurePainter,
          contentDescription = "شکل پرسش",
          contentScale = ContentScale.Fit,
          modifier = Modifier.fillMaxWidth(),
        )
      }
      Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        question.options.forEachIndexed { index, option ->
          OriginalOptionRow(
            index = index,
            option = option,
            isSelected = question.selectedOptionIndex == index,
            isCorrect = question.correctOptionIndex == index,
          )
        }
      }
      AnswerSummary(question)
      ReviewMetadata(question)
      if (question.solution.isNotBlank()) {
        ReviewSection(title = "راه‌حل و استدلال") {
          Text(question.solution, style = MaterialTheme.typography.bodyLarge)
        }
      }
      if (question.outcome == AnswerOutcome.WRONG && !question.selectedWrongReasoning.isNullOrBlank()) {
        ReviewSection(title = "چرا گزینهٔ انتخاب‌شده نادرست است؟") {
          Text(question.selectedWrongReasoning, style = MaterialTheme.typography.bodyLarge)
        }
      }
      val usefulDistractors = question.wrongOptionExplanations
        .filterKeys { it in question.options.indices && it != question.correctOptionIndex }
        .filterValues { it.isNotBlank() }
      if (usefulDistractors.isNotEmpty()) {
        ReviewSection(title = "بررسی گزینه‌های نادرست") {
          Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            usefulDistractors.toSortedMap().forEach { (index, explanation) ->
              Text(
                text = "گزینهٔ ${persianOptionLetter(index)}: $explanation",
                style = MaterialTheme.typography.bodyMedium,
              )
            }
          }
        }
      }
    }
  }
}

@Composable
private fun ReviewHeader(question: ReviewQuestion) {
  val outcomeLabel = when (question.outcome) {
    AnswerOutcome.CORRECT -> "پاسخ درست"
    AnswerOutcome.WRONG -> "پاسخ نادرست"
    AnswerOutcome.BLANK -> "بی‌پاسخ"
  }
  Surface(
    color = when (question.outcome) {
      AnswerOutcome.CORRECT -> MaterialTheme.colorScheme.primaryContainer
      AnswerOutcome.WRONG -> MaterialTheme.colorScheme.errorContainer
      AnswerOutcome.BLANK -> MaterialTheme.colorScheme.surfaceVariant
    },
    shape = RoundedCornerShape(16.dp),
  ) {
    Text(
      text = outcomeLabel,
      modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp),
      style = MaterialTheme.typography.titleSmall,
      fontWeight = FontWeight.Bold,
    )
  }
}

@Composable
private fun OriginalOptionRow(
  index: Int,
  option: String,
  isSelected: Boolean,
  isCorrect: Boolean,
) {
  val containerColor = when {
    isCorrect -> MaterialTheme.colorScheme.primaryContainer
    isSelected -> MaterialTheme.colorScheme.errorContainer
    else -> MaterialTheme.colorScheme.surfaceVariant
  }
  val note = when {
    isCorrect && isSelected -> "انتخاب شما و پاسخ درست"
    isCorrect -> "پاسخ درست"
    isSelected -> "انتخاب شما"
    else -> null
  }
  Card(colors = CardDefaults.cardColors(containerColor = containerColor)) {
    Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
      Text(
        text = "گزینهٔ ${persianOptionLetter(index)}: $option",
        style = MaterialTheme.typography.bodyLarge,
      )
      if (note != null) {
        Text(note, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold)
      }
    }
  }
}

@Composable
private fun AnswerSummary(question: ReviewQuestion) {
  val selected = question.selectedOptionIndex?.let { "گزینهٔ ${persianOptionLetter(it)}" } ?: "بی‌پاسخ"
  val correct = "گزینهٔ ${persianOptionLetter(question.correctOptionIndex)}"
  ReviewSection(title = "پاسخ‌ها") {
    Text("پاسخ شما: $selected", style = MaterialTheme.typography.bodyLarge)
    Text("پاسخ درست: $correct", style = MaterialTheme.typography.bodyLarge)
    Text(
      "میزان اطمینان: ${question.confidence?.persianLabel ?: "ثبت نشده"}",
      style = MaterialTheme.typography.bodyLarge,
    )
  }
}

@Composable
private fun ReviewMetadata(question: ReviewQuestion) {
  val metadata = buildList {
    question.microtopic?.takeIf(String::isNotBlank)?.let { add("ریز‌مبحث: $it") }
    question.source?.takeIf(String::isNotBlank)?.let { add("منبع: $it") }
    question.errorType?.let { add("نوع خطا: ${it.persianLabel}") }
  }
  if (metadata.isNotEmpty()) {
    Text(
      text = metadata.joinToString("  •  "),
      style = MaterialTheme.typography.labelMedium,
      color = MaterialTheme.colorScheme.onSurfaceVariant,
    )
  }
}

@Composable
private fun ReviewSection(
  title: String,
  content: @Composable () -> Unit,
) {
  Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)) {
    Column(
      modifier = Modifier.padding(14.dp),
      verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
      Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold)
      content()
    }
  }
}

private fun persianOptionLetter(index: Int): String = when (index) {
  0 -> "۱"
  1 -> "۲"
  2 -> "۳"
  3 -> "۴"
  else -> (index + 1).toString()
}
