package com.example.review

import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.example.ui.theme.MyApplicationTheme
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class ReviewQuestionMapInstrumentedTest {
  @get:Rule
  val composeRule = createComposeRule()

  @Test
  fun questionMap_isTappableAndShowsPreSubmitPersianStates() {
    val selectedQuestionId = mutableStateOf<String?>(null)
    val state = QuestionMapState.create(
      entries = listOf(
        QuestionMapEntry(questionId = "q-1"),
        QuestionMapEntry(questionId = "q-2", selectedOptionIndex = 0),
        QuestionMapEntry(questionId = "q-3", isFlagged = true),
      ),
    )

    composeRule.setContent {
      MyApplicationTheme {
        QuestionMap(
          state = state,
          isSubmitted = false,
          onQuestionSelected = { selectedQuestionId.value = it },
        )
      }
    }

    composeRule.onNodeWithContentDescription("پرسش 2، پاسخ‌داده‌شده").performClick()
    composeRule.runOnIdle { assertEquals("q-2", selectedQuestionId.value) }
    composeRule.onNodeWithContentDescription("پرسش 2، پرسش جاری").assertIsDisplayed()
    composeRule.onNodeWithText("نشان‌دار").assertIsDisplayed()
  }

  @Test
  fun standaloneReview_showsAllOriginalEvidenceAndPersianPresentationLabels() {
    val question = ReviewQuestion(
      questionId = "q-1",
      stem = "صورت کامل پرسش آزمون",
      options = listOf("گزینهٔ اول", "گزینهٔ دوم", "گزینهٔ سوم", "گزینهٔ چهارم"),
      selectedOptionIndex = 1,
      correctOptionIndex = 2,
      confidence = ReviewConfidence.LOW,
      solution = "با مقایسهٔ داده‌های صورت پرسش، گزینهٔ سوم با شرط داده‌شده سازگار است.",
      selectedWrongReasoning = "گزینهٔ دوم شرط اصلی پرسش را نادیده می‌گیرد.",
      wrongOptionExplanations = mapOf(
        0 to "گزینهٔ اول با دادهٔ اول سازگار نیست.",
        1 to "گزینهٔ دوم نتیجهٔ مخالف شرط پرسش را بیان می‌کند.",
        3 to "گزینهٔ چهارم از اطلاعات کافی نتیجه‌گیری نمی‌کند.",
      ),
      microtopic = "مهارت نمونه",
      source = "منبع نمونه",
      errorType = ReviewErrorType.CONCEPT,
    )

    composeRule.setContent {
      MyApplicationTheme { StandaloneReview(question) }
    }

    composeRule.onNodeWithText("صورت کامل پرسش آزمون").assertIsDisplayed()
    question.options.forEach { option -> composeRule.onNodeWithText(option, substring = true).assertIsDisplayed() }
    composeRule.onNodeWithText("پاسخ شما: گزینهٔ ۲").assertIsDisplayed()
    composeRule.onNodeWithText("پاسخ درست: گزینهٔ ۳").assertIsDisplayed()
    composeRule.onNodeWithText("میزان اطمینان: اطمینان کم").assertIsDisplayed()
    composeRule.onNodeWithText("راه‌حل و استدلال").assertIsDisplayed()
    composeRule.onNodeWithText("چرا گزینهٔ انتخاب‌شده نادرست است؟").assertIsDisplayed()
    composeRule.onNodeWithText("بررسی گزینه‌های نادرست").assertIsDisplayed()
  }
}
