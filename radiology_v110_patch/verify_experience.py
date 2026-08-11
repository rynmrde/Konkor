from pathlib import Path
root=Path(__file__).resolve().parents[1]
h=(root/'app/src/main/assets/index.html').read_text(encoding='utf-8')
css=(root/'app/src/main/assets/experience.css').read_text(encoding='utf-8')
js=(root/'app/src/main/assets/experience.js').read_text(encoding='utf-8')
b=(root/'app/src/main/java/com/radiology1405/prep/AndroidBridge.kt').read_text(encoding='utf-8')
m=(root/'app/src/main/java/com/radiology1405/prep/MainActivity.kt').read_text(encoding='utf-8')
g=(root/'app/build.gradle.kts').read_text(encoding='utf-8')
assert 'experience.css' in h and 'experience.js' in h
for token in ['theme-oled','theme-midnight','theme-forest','theme-violet','theme-ice','theme-sunset','motion-snappy','focusPlayer','feedbackPulse']:
    assert token in css, token
for token in ['adhdMode','focusAudioMode','sfxToggle','hapticToggle','focusTimer','reviewFeedback','startFocusAudio','Brown Noise']:
    assert token in js, token
assert '@JavascriptInterface fun haptic' in b
assert 'performHaptic' in m and 'HapticFeedbackConstants' in m
assert 'versionCode = 110' in g and 'versionName = "1.1.0"' in g
print('EXPERIENCE_VERIFY PASS themes/audio/haptics/adhd/pro-ui')
