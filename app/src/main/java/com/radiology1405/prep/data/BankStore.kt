package com.radiology1405.prep.data

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import com.radiology1405.prep.engine.RescueProfile
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.io.FileInputStream
import java.io.FileNotFoundException
import java.io.FileOutputStream
import java.security.MessageDigest
import java.util.zip.GZIPInputStream

class BankStore(private val context: Context) : AutoCloseable {
    companion object {
        // AAPT treats source assets ending in .gz specially: it stores the expanded
        // payload in the APK under the same name with the .gz suffix removed.
        private const val PACKAGED_ASSET = "radiology1405_bank_v6_1.db"
        private const val SOURCE_GZIP_ASSET = "radiology1405_bank_v6_1.db.gz"
        private const val DB_NAME = "radiology1405_bank_v6_1.db"
        const val EXPECTED_DB_SHA256 = "d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c"
        private const val EXPECTED_GZIP_SHA256 = "b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14"
        const val EXPECTED_QUESTIONS = 1216
        const val EXPECTED_VERIFIED_REAL = 17
        const val EXPECTED_AUTHORED = 1112
        const val EXPECTED_PROVISIONAL_STEMS = 71
        const val EXPECTED_QUARANTINED = 16
        private const val BIOLOGY_V615_PATCH_ASSET = "biology_v615_patch.json"
        private const val PATCHED_DB_SHA256 = "00f881e78e26326532b8b771134970052ddb296fc0e556ab30a980c95656ef14"
        private const val PATCHED_VERIFIED_REAL = 17
        private const val PATCHED_PROVISIONAL_STEMS = 71
        private const val BIOLOGY_V615_PATCH_SHA256 = "3943af9a9d83872c846c7458fae330184be44b7b1aead7502f1c2620c99ebb5d"
    }

    private val dbDelegate = lazy(LazyThreadSafetyMode.SYNCHRONIZED) { openVerified() }
    private val db: SQLiteDatabase by dbDelegate

    private fun sha256(file: File): String {
        val digest = MessageDigest.getInstance("SHA-256")
        FileInputStream(file).use { input ->
            val buffer = ByteArray(1024 * 1024)
            while (true) {
                val count = input.read(buffer)
                if (count <= 0) break
                digest.update(buffer, 0, count)
            }
        }
        return digest.digest().joinToString("") { "%02x".format(it) }
    }

    private fun copyExpandedBundledDb(target: File) {
        target.parentFile?.mkdirs()
        val temp = File(target.parentFile, "$DB_NAME.installing")
        if (temp.exists()) temp.delete()

        val packaged = try {
            context.assets.open(PACKAGED_ASSET)
        } catch (_: FileNotFoundException) {
            null
        }
        if (packaged != null) {
            packaged.use { input ->
                FileOutputStream(temp).buffered(1024 * 1024).use { output ->
                    input.copyTo(output, 1024 * 1024)
                    output.flush()
                }
            }
        } else {
            // Defensive fallback for packaging pipelines that preserve the .gz suffix.
            val sourceGzip = File(context.cacheDir, "$SOURCE_GZIP_ASSET.fallback")
            try {
                context.assets.open(SOURCE_GZIP_ASSET).use { compressed ->
                    FileOutputStream(sourceGzip).use { output ->
                        compressed.copyTo(output, 1024 * 1024)
                        output.fd.sync()
                    }
                }
                require(sha256(sourceGzip) == EXPECTED_GZIP_SHA256) { "Bundled bank archive checksum failed" }
                GZIPInputStream(FileInputStream(sourceGzip), 1024 * 1024).use { input ->
                    FileOutputStream(temp).buffered(1024 * 1024).use { output ->
                        input.copyTo(output, 1024 * 1024)
                        output.flush()
                    }
                }
            } finally {
                sourceGzip.delete()
            }
        }

        require(sha256(temp) == EXPECTED_DB_SHA256) { "Immutable base bank checksum failed" }
        applyBiologyV615Patch(temp)
        require(sha256(temp) == PATCHED_DB_SHA256) { "Patched Biology bank checksum failed" }
        if (target.exists() && !target.delete()) error("Cannot replace invalid bank")
        if (!temp.renameTo(target)) {
            temp.copyTo(target, overwrite = true)
            temp.delete()
        }
    }


    private fun applyBiologyV615Patch(target: File) {
        val patchBytes = context.assets.open(BIOLOGY_V615_PATCH_ASSET).use { it.readBytes() }
        require(MessageDigest.getInstance("SHA-256").digest(patchBytes).joinToString("") { "%02x".format(it) } == BIOLOGY_V615_PATCH_SHA256) {
            "Biology V6.1.5 patch checksum failed"
        }
        val updates = JSONObject(String(patchBytes, Charsets.UTF_8)).getJSONArray("updates")
        val writable = SQLiteDatabase.openDatabase(target.absolutePath, null, SQLiteDatabase.OPEN_READWRITE)
        try {
            writable.beginTransaction()
            for (index in 0 until updates.length()) {
                val update = updates.getJSONObject(index)
                val id = update.getString("id")
                val current = writable.rawQuery("SELECT full_json FROM question WHERE id=?", arrayOf(id)).use { cursor ->
                    require(cursor.moveToFirst()) { "Missing Biology patch question: $id" }
                    JSONObject(cursor.getString(0))
                }
                val fields = update.getJSONObject("fields")
                val keys = fields.keys()
                while (keys.hasNext()) {
                    val key = keys.next()
                    current.put(key, fields.get(key))
                }
                val sourceType = update.getString("source_type")
                writable.execSQL("UPDATE question SET source_type=?, full_json=? WHERE id=?", arrayOf(sourceType, current.toString(), id))
            }
            writable.setTransactionSuccessful()
        } finally {
            if (writable.inTransaction()) writable.endTransaction()
            writable.close()
        }
    }

    private fun installAsset(target: File) = copyExpandedBundledDb(target)

    private fun scalar(opened: SQLiteDatabase, sql: String): Int =
        opened.rawQuery(sql, null).use { cursor -> require(cursor.moveToFirst()); cursor.getInt(0) }

    private fun openVerified(): SQLiteDatabase {
        val target = context.getDatabasePath(DB_NAME)
        if (!target.exists() || sha256(target) != PATCHED_DB_SHA256) installAsset(target)
        val opened = SQLiteDatabase.openDatabase(target.absolutePath, null, SQLiteDatabase.OPEN_READONLY)
        val integrity = opened.rawQuery("PRAGMA quick_check", null).use { cursor -> cursor.moveToFirst(); cursor.getString(0) }
        require(integrity == "ok") { "Bank quick_check failed: $integrity" }
        val total = scalar(opened, "SELECT COUNT(*) FROM question")
        val real = scalar(opened, "SELECT COUNT(*) FROM question WHERE source_type='real_exam'")
        val authored = scalar(opened, "SELECT COUNT(*) FROM question WHERE source_type='authored'")
        val provisional = scalar(opened, "SELECT COUNT(*) FROM question WHERE source_type='official_exam_stem_training'")
        val quarantined = scalar(opened, "SELECT COUNT(*) FROM question WHERE source_type='quarantined_key_conflict'")
        require(
            total == EXPECTED_QUESTIONS && real == PATCHED_VERIFIED_REAL && authored == EXPECTED_AUTHORED &&
                provisional == PATCHED_PROVISIONAL_STEMS && quarantined == EXPECTED_QUARANTINED
        ) {
            "Bank count mismatch: total=$total verifiedReal=$real authored=$authored provisional=$provisional quarantine=$quarantined"
        }
        return opened
    }

    fun question(id: String): Question? = db.rawQuery(
        "SELECT full_json FROM question WHERE id=? LIMIT 1", arrayOf(id)
    ).use { cursor -> if (cursor.moveToFirst()) Question.fromJson(cursor.getString(0)) else null }

    fun rootJson(key: String): String? = db.rawQuery(
        "SELECT json FROM bank_root WHERE key=? LIMIT 1", arrayOf(key)
    ).use { cursor -> if (cursor.moveToFirst()) cursor.getString(0) else null }

    fun dayPlans(): List<DayPlan> = rootJson("day_plan")?.let(DayPlan::fromRootJson).orEmpty()

    private fun rescueSafe(question: Question): Boolean =
        question.accessPool == "TRAIN" && question.eligibleForSafetyEvidence && !question.needsHumanReview

    fun poolIds(
        pool: String,
        microtopics: List<String> = emptyList(),
        safeOnly: Boolean = false,
    ): List<String> {
        val args = mutableListOf(pool)
        val topicClause = if (microtopics.isEmpty()) "" else {
            args += microtopics
            " AND microtopic IN (${microtopics.joinToString(",") { "?" }})"
        }
        return db.rawQuery(
            "SELECT id FROM question WHERE access_pool=?$topicClause ORDER BY subject, priority DESC, id",
            args.toTypedArray(),
        ).use { cursor ->
            buildList {
                while (cursor.moveToNext()) {
                    val id = cursor.getString(0)
                    if (!safeOnly || question(id)?.let(::rescueSafe) == true) add(id)
                }
            }
        }
    }

    fun simulationIds(pool: String): List<String> {
        val root = JSONObject(rootJson("simulation_blueprints") ?: return emptyList())
        val ids = root.getJSONObject(pool).getJSONArray("question_ids")
        return buildList {
            for (i in 0 until ids.length()) {
                val id = ids.getString(i)
                val question = question(id) ?: error("Holdout question $id is missing")
                require(question.accessPool == pool) { "Holdout pool mismatch for $id" }
                require(question.sourceType == "authored" && question.eligibleForSafetyEvidence && !question.needsHumanReview) {
                    "Ineligible Safety item in $pool: $id"
                }
                add(id)
            }
        }
    }

    fun trainingCandidates(
        microtopics: List<String>,
        excluded: Set<String>,
        limit: Int,
        safeOnly: Boolean = false,
    ): List<String> {
        if (limit <= 0) return emptyList()
        val args = mutableListOf<String>()
        val where = StringBuilder("access_pool='TRAIN' AND obsolete=0 AND selected_scope=1")
        if (microtopics.isNotEmpty()) {
            where.append(" AND microtopic IN (")
            where.append(microtopics.joinToString(",") { "?" })
            where.append(")")
            args += microtopics
        }
        return db.rawQuery(
            "SELECT id FROM question WHERE $where ORDER BY priority DESC, difficulty, id LIMIT ?",
            (args + (limit * 5).coerceAtLeast(100).toString()).toTypedArray(),
        ).use { cursor ->
            buildList {
                while (cursor.moveToNext() && size < limit) {
                    val id = cursor.getString(0)
                    if (id !in excluded && (!safeOnly || question(id)?.let(::rescueSafe) == true)) add(id)
                }
            }
        }
    }

    fun distinctAlternative(
        microtopic: String,
        excluded: Set<String>,
        preferredLevels: List<String> = emptyList(),
        safeOnly: Boolean = false,
    ): String? {
        val args = mutableListOf(microtopic)
        val levelFilter = if (preferredLevels.isEmpty()) "" else {
            args += preferredLevels
            " AND teaching_ladder_level IN (${preferredLevels.joinToString(",") { "?" }})"
        }
        return db.rawQuery(
            "SELECT id FROM question WHERE access_pool='TRAIN' AND obsolete=0 AND microtopic=?$levelFilter ORDER BY priority DESC, id LIMIT 80",
            args.toTypedArray(),
        ).use { cursor ->
            while (cursor.moveToNext()) {
                val id = cursor.getString(0)
                if (id !in excluded && (!safeOnly || question(id)?.let(::rescueSafe) == true)) return@use id
            }
            null
        }
    }

    fun rescueProfiles(): List<RescueProfile> {
        val safeCounts = mutableMapOf<String, Int>()
        db.rawQuery("SELECT microtopic, full_json FROM question WHERE access_pool='TRAIN'", null).use { cursor ->
            while (cursor.moveToNext()) {
                val topic = cursor.getString(0)
                if (rescueSafe(Question.fromJson(cursor.getString(1)))) {
                    safeCounts[topic] = (safeCounts[topic] ?: 0) + 1
                }
            }
        }
        val coverage = JSONArray(rootJson("coverage_plan") ?: error("coverage_plan is missing from frozen bank"))
        return buildList {
            for (index in 0 until coverage.length()) {
                val row = coverage.getJSONObject(index)
                val factors = row.getJSONObject("priority_factors")
                val microtopics = row.getJSONArray("microtopics")
                require(microtopics.length() == 1) { "Rescue triage requires one microtopic per coverage row" }
                val microtopic = microtopics.getString(0)
                add(
                    RescueProfile(
                        subject = row.getString("subject"),
                        microtopic = microtopic,
                        expectedQuestions = row.getDouble("expected_questions"),
                        recentFrequency = factors.getDouble("frequency_1402_1404_weighted"),
                        historicalFrequency = factors.getDouble("frequency_1398_1404_weighted"),
                        stability = factors.getDouble("stability"),
                        learningMinutes = factors.getInt("learning_time_minutes"),
                        prerequisiteCost = factors.getInt("prerequisite_cost"),
                        averageDifficulty = factors.getInt("average_difficulty"),
                        errorRisk = factors.getDouble("error_risk"),
                        trapRisk = factors.getInt("trap_risk"),
                        calculationLoad = factors.getInt("calculation_load"),
                        masteryProbability11Days = factors.getDouble("probability_of_mastery_in_11_days"),
                        safeTrainQuestions = safeCounts[microtopic] ?: 0,
                    )
                )
            }
        }
    }

    override fun close() {
        if (dbDelegate.isInitialized() && db.isOpen) db.close()
    }
}
