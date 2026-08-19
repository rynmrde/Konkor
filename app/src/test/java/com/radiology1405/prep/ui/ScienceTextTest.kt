package com.radiology1405.prep.ui

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ScienceTextTest {
    @Test
    fun learnerFacingScientificText_translatesInternalTaxonomyKeys() {
        val rendered = learnerFacingScientificText(
            "wrong_condition و partial_truth و calculation_trap و time_management"
        )

        assertFalse(rendered.contains("wrong_condition"))
        assertFalse(rendered.contains("partial_truth"))
        assertFalse(rendered.contains("calculation_trap"))
        assertFalse(rendered.contains("time_management"))
        assertTrue(rendered.contains("نادیده‌گرفتن شرط"))
        assertTrue(rendered.contains("درستِ ناقص"))
        assertTrue(rendered.contains("خطای محاسبه"))
        assertTrue(rendered.contains("مدیریت زمان"))
    }
}
