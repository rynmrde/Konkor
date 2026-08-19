package com.example.review

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class QuestionMapStateTest {
  private val initialEntries = listOf(
    QuestionMapEntry(questionId = "q-1"),
    QuestionMapEntry(questionId = "q-2", selectedOptionIndex = 1),
    QuestionMapEntry(questionId = "q-3", isFlagged = true),
    QuestionMapEntry(questionId = "q-4"),
  )

  @Test
  fun beforeSubmit_exposesCurrentUnansweredAnsweredAndFlaggedStates() {
    val state = QuestionMapState.create(initialEntries, selectedQuestionId = "q-1")

    val visualStates = state.entries.associate { entry ->
      entry.questionId to entry.visualState(
        isCurrent = entry.questionId == state.selectedQuestionId,
        isSubmitted = false,
      )
    }

    assertEquals(QuestionMapVisualState.CURRENT, visualStates["q-1"])
    assertEquals(QuestionMapVisualState.ANSWERED, visualStates["q-2"])
    assertEquals(QuestionMapVisualState.FLAGGED, visualStates["q-3"])
    assertEquals(QuestionMapVisualState.UNANSWERED, visualStates["q-4"])
  }

  @Test
  fun afterSubmit_exposesCorrectWrongAndBlankWithoutLeakingInternalNames() {
    val state = QuestionMapState.create(initialEntries, selectedQuestionId = "q-1")
    state.recordOutcome("q-1", AnswerOutcome.CORRECT)
    state.recordOutcome("q-2", AnswerOutcome.WRONG)
    state.recordOutcome("q-3", AnswerOutcome.BLANK)

    val visualStates = state.entries.associate { entry ->
      entry.questionId to entry.visualState(
        isCurrent = false,
        isSubmitted = true,
      )
    }

    assertEquals(QuestionMapVisualState.CORRECT, visualStates["q-1"])
    assertEquals(QuestionMapVisualState.WRONG, visualStates["q-2"])
    assertEquals(QuestionMapVisualState.BLANK, visualStates["q-3"])
    assertFalse(QuestionMapVisualState.WRONG.persianLabel.contains("_"))
  }

  @Test
  fun snapshot_restoreKeepsSelectionAnswerFlagAndOutcomeForSessionResume() {
    val state = QuestionMapState.create(initialEntries, selectedQuestionId = "q-1")
    state.select("q-3")
    state.updateAnswer("q-3", selectedOptionIndex = 2)
    state.setFlagged("q-3", isFlagged = true)
    state.recordOutcome("q-3", AnswerOutcome.WRONG)

    val restored = QuestionMapState.restore(state.snapshot())
    val restoredEntry = restored.entries.single { it.questionId == "q-3" }

    assertEquals("q-3", restored.selectedQuestionId)
    assertEquals(2, restoredEntry.selectedOptionIndex)
    assertTrue(restoredEntry.isFlagged)
    assertEquals(AnswerOutcome.WRONG, restoredEntry.outcome)
  }

  @Test(expected = IllegalArgumentException::class)
  fun reviewQuestion_rejectsMissingOriginalOptions() {
    ReviewQuestion(
      questionId = "invalid",
      stem = "صورت پرسش",
      options = listOf("۱", "۲", "۳"),
      selectedOptionIndex = null,
      correctOptionIndex = 0,
      confidence = null,
      solution = "استدلال مشخص",
    )
  }
}
