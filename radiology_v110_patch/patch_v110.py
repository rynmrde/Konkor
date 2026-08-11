from pathlib import Path
import re, shutil, sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'project')
patch=Path(sys.argv[2] if len(sys.argv)>2 else 'radiology_v110_patch')
assets=root/'app/src/main/assets'; assets.mkdir(parents=True,exist_ok=True)
shutil.copy2(patch/'experience.css',assets/'experience.css')
shutil.copy2(patch/'experience.js',assets/'experience.js')

# HTML: load the experience layer after core styles/code, without touching the bank logic.
hp=assets/'index.html'; h=hp.read_text(encoding='utf-8')
if 'experience.css' not in h:
    h=h.replace('</head>','<link rel="stylesheet" href="experience.css">\n</head>')
if 'experience.js' not in h:
    h=h.replace('</body>','<script src="experience.js"></script>\n</body>')
# Keep useful native bridge diagnostics even when patching the original source snapshot.
if "raw?.startsWith('__BANK_ERROR__:')" not in h:
    h=h.replace("const raw=window.AndroidBridge.getBankIndex();\n if(!raw)","const raw=window.AndroidBridge.getBankIndex();\n if(raw?.startsWith('__BANK_ERROR__:'))throw Error('Bank: '+raw.slice('__BANK_ERROR__:'.length));\n if(!raw)")
if "getQuestionJson?.(String(id));if(raw?.startsWith('__BANK_ERROR__:')" not in h:
    h=h.replace("const raw=window.AndroidBridge?.getQuestionJson?.(String(id));if(raw)q=JSON.parse(raw)","const raw=window.AndroidBridge?.getQuestionJson?.(String(id));if(raw?.startsWith('__BANK_ERROR__:'))throw Error(raw);if(raw)q=JSON.parse(raw)")
hp.write_text(h,encoding='utf-8')

# Bank: use Android raw resource and open read-only DB without localized-collator writes.
bp=root/'app/src/main/java/com/radiology1405/prep/BankDb.kt'; b=bp.read_text(encoding='utf-8')
b=b.replace('context.assets.open(ASSET).use { compressed ->','context.resources.openRawResource(R.raw.radiology1405_bank_v5).use { compressed ->')
if 'SQLiteDatabase.NO_LOCALIZED_COLLATORS' not in b:
    b=b.replace('SQLiteDatabase.openDatabase(target.absolutePath, null, SQLiteDatabase.OPEN_READONLY)','SQLiteDatabase.openDatabase(target.absolutePath, null, SQLiteDatabase.OPEN_READONLY or SQLiteDatabase.NO_LOCALIZED_COLLATORS)')
bp.write_text(b,encoding='utf-8')

# Bridge: diagnostics + native haptics.
brp=root/'app/src/main/java/com/radiology1405/prep/AndroidBridge.kt'; br=brp.read_text(encoding='utf-8')
simple='''    @JavascriptInterface fun getBankIndex(): String {\n        bank.verifyCounts()\n        return indexJson\n    }\n\n    @JavascriptInterface fun getQuestionJson(id: String): String = bank.questionJson(id) ?: ""'''
robust='''    @JavascriptInterface fun getBankIndex(): String = try {\n        bank.verifyCounts()\n        indexJson\n    } catch (t: Throwable) {\n        "__BANK_ERROR__:${t.javaClass.simpleName}:${t.message ?: "unknown"}"\n    }\n\n    @JavascriptInterface fun getQuestionJson(id: String): String = try {\n        bank.questionJson(id) ?: ""\n    } catch (t: Throwable) {\n        "__BANK_ERROR__:${t.javaClass.simpleName}:${t.message ?: "unknown"}"\n    }'''
if simple in br: br=br.replace(simple,robust)
if '@JavascriptInterface fun haptic' not in br:
    br=br.replace('    @JavascriptInterface fun exportProgress(raw: String) { activity.requestProgressExport(raw) }','    @JavascriptInterface fun exportProgress(raw: String) { activity.requestProgressExport(raw) }\n\n    @JavascriptInterface fun haptic(kind: String) { activity.performHaptic(kind) }')
brp.write_text(br,encoding='utf-8')

# Activity: native, system-respecting haptic feedback. No vibration permission is required.
mp=root/'app/src/main/java/com/radiology1405/prep/MainActivity.kt'; m=mp.read_text(encoding='utf-8')
if 'import android.os.Build' not in m: m=m.replace('import android.os.Bundle','import android.os.Bundle\nimport android.os.Build')
if 'import android.view.HapticFeedbackConstants' not in m: m=m.replace('import android.view.View','import android.view.HapticFeedbackConstants\nimport android.view.View')
if 'fun performHaptic(kind: String)' not in m:
    method='''\n    fun performHaptic(kind: String) {\n        if (!::webView.isInitialized) return\n        runOnUiThread {\n            val base = kind.substringBefore(':')\n            val level = kind.substringAfter(':', "medium")\n            val constant = when {\n                base == "correct" && Build.VERSION.SDK_INT >= 30 -> HapticFeedbackConstants.CONFIRM\n                base == "wrong" && Build.VERSION.SDK_INT >= 30 -> HapticFeedbackConstants.REJECT\n                base == "timer" -> HapticFeedbackConstants.LONG_PRESS\n                level == "strong" -> HapticFeedbackConstants.LONG_PRESS\n                else -> HapticFeedbackConstants.VIRTUAL_KEY\n            }\n            webView.performHapticFeedback(constant)\n            if (level == "strong" && base == "wrong") {\n                webView.postDelayed({ webView.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY) }, 70)\n            }\n        }\n    }\n'''
    m=m.replace('\n    fun requestProgressExport(raw: String) {',method+'\n    fun requestProgressExport(raw: String) {')
mp.write_text(m,encoding='utf-8')

# Safe Android upgrade version.
gp=root/'app/build.gradle.kts'; g=gp.read_text(encoding='utf-8')
g=re.sub(r'versionCode\s*=\s*\d+','versionCode = 110',g,count=1)
g=re.sub(r'versionName\s*=\s*"[^"]+"','versionName = "1.1.0"',g,count=1)
gp.write_text(g,encoding='utf-8')

# Self-contained source validation.
shutil.copy2(patch/'verify_experience.py',root/'tests/verify_experience.py')
print('PATCH_V110 PASS')
