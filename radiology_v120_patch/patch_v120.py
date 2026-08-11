from pathlib import Path
import re,shutil,subprocess,sys
R=Path(sys.argv[1] if len(sys.argv)>1 else 'project'); P=Path(sys.argv[2] if len(sys.argv)>2 else 'radiology_v120_patch')
A=R/'app/src/main/assets'; H=A/'index.html'; E=A/'experience.js'
if not H.exists() or not E.exists(): raise SystemExit('V120: v1.1 assets missing')
before=H.read_text(encoding='utf-8')
critical=['validateBank','ensureOptionOrder','microWeights','allocate','pickSubject','buildRound','updateMastery','calcRound','finishReview','submitRound','ensureDay','projectionBreakdown','safetyStatus']
def block(s,n):
 m=re.search(r'(?m)^[ \t]*function\s+'+re.escape(n)+r'\s*\([^)]*\)\s*\{',s)
 if not m: raise RuntimeError('core function missing: '+n)
 i=m.end();depth=1;quote=None;esc=False;line=False;multi=False
 while i<len(s) and depth:
  c=s[i];d=s[i+1] if i+1<len(s) else ''
  if line:
   if c=='\n':line=False
  elif multi:
   if c=='*' and d=='/':multi=False;i+=1
  elif quote:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c==quote:quote=None
  else:
   if c=='/' and d=='/':line=True;i+=1
   elif c=='/' and d=='*':multi=True;i+=1
   elif c in "'\"`":quote=c
   elif c=='{':depth+=1
   elif c=='}':depth-=1
  i+=1
 if depth:raise RuntimeError('unbalanced core '+n)
 return s[m.start():i]
core0={n:block(before,n) for n in critical}
subprocess.run([sys.executable,str(P/'generate_media.py'),str(A)],check=True)
for n in ['professional.js','professional.css']:shutil.copy2(P/n,A/n)
h=before
if 'professional.css' not in h:h=h.replace('</head>','<link rel="stylesheet" href="professional.css">\n</head>')
if 'professional.js' not in h:h=h.replace('</body>','<script src="professional.js"></script>\n</body>')
h=h.replace('🎯 صبح ۳۰ مرداد: کنکور تجربی','<img src="icons/calendar.svg" class="inlineIcon" alt=""> صبح ۳۰ مرداد: کنکور تجربی')
h=h.replace('<div style="font-size:36px">📚</div>','<div><img src="icons/import.svg" style="width:40px;height:40px" alt=""></div>')
h=h.replace('<button id="flagBtn" class="btn ghost">⚑ نشان</button>','<button id="flagBtn" class="btn ghost"><img src="icons/flag.svg" class="inlineIcon" alt=""> نشان</button>')
h=h.replace('<button id="reviewFlag" class="btn ghost">⚑ نشان</button>','<button id="reviewFlag" class="btn ghost"><img src="icons/flag.svg" class="inlineIcon" alt=""> نشان</button>')
h=h.replace("${r.flags[id]?'⚑':''}","${r.flags[id]?'<img src=\"icons/flag.svg\" class=\"inlineIcon\" alt=\"\">':''}")
h=h.replace('el("flagBtn").textContent=r.flags[q.id]?"⚑ نشان‌دار":"⚐ نشان"','el("flagBtn").innerHTML=r.flags[q.id]?\'<img src="icons/flag.svg" class="inlineIcon" alt=""> نشان‌دار\':\'<img src="icons/flag.svg" class="inlineIcon" alt=""> نشان\'')
h=h.replace('el("reviewFlag").textContent=r.flags[q.id]?"⚑ نشان‌دار":"⚐ نشان"','el("reviewFlag").innerHTML=r.flags[q.id]?\'<img src="icons/flag.svg" class="inlineIcon" alt=""> نشان‌دار\':\'<img src="icons/flag.svg" class="inlineIcon" alt=""> نشان\'')
h=h.replace("ok?'درست ✅':blank?'نزده ⏭':'غلط ❌'","ok?'درست <img src=\"icons/correct.svg\" class=\"inlineIcon\" alt=\"\">':blank?'نزده':'غلط <img src=\"icons/wrong.svg\" class=\"inlineIcon\" alt=\"\">'")
h=h.replace('بانک معتبر بارگذاری شد ✅','بانک معتبر بارگذاری شد').replace('چهار راند امروز کامل شد ✅','چهار راند امروز کامل شد')
H.write_text(h,encoding='utf-8')
core1={n:block(h,n) for n in critical};changed=[n for n in critical if core0[n]!=core1[n]]
if changed:raise RuntimeError('V120 touched core: '+','.join(changed))
print('V120_CORE_INTEGRITY PASS',len(critical))
js=E.read_text(encoding='utf-8')
def replace_fn(src,name,new):
 m=re.search(r'function\s+'+re.escape(name)+r'\s*\([^)]*\)\s*\{',src)
 if not m:raise RuntimeError('experience fn missing '+name)
 i=m.end();depth=1;quote=None;esc=False
 while i<len(src) and depth:
  c=src[i]
  if quote:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c==quote:quote=None
  else:
   if c in "'\"`":quote=c
   elif c=='{':depth+=1
   elif c=='}':depth-=1
  i+=1
 if depth:raise RuntimeError('unbalanced '+name)
 return src[:m.start()]+new+src[i:]
play=r'''function playSfx(kind){if(state?.settings?.sfx===false)return;const map={select:'sfx_select',submit:'sfx_submit',correct:'sfx_correct',wrong:'sfx_wrong',done:'sfx_complete',focus_start:'sfx_focus_start',focus_end:'sfx_focus_end'},n=map[kind];if(!n)return;try{const p=new Audio(`audio/${n}.wav`);p.preload='auto';p.volume=clamp(Number(state?.settings?.sfxVolume??45)/100,0,.75);audio.fileSfx=audio.fileSfx||[];audio.fileSfx=audio.fileSfx.filter(x=>!x.ended);audio.fileSfx.push(p);p.play().catch(()=>{})}catch(e){console.warn('sfx-file',e)}}'''
start=r'''function startFocusAudio(){stopFocusAudio(true);if(!state?.settings?.focusAudio)return updateFocusPlayer();try{const mode=state.settings.focusAudioMode||'ambient',p=new Audio(`audio/focus_${mode}.wav`);p.loop=true;p.preload='auto';p.volume=clamp(Number(state.settings.focusVolume??18)/100,0,.6);audio.filePlayer=p;p.play().then(()=>playSfx('focus_start')).catch(e=>{audio.filePlayer=null;console.warn('focus-file',e);toast('پخش صدا روی این WebView در دسترس نیست');updateFocusPlayer()})}catch(e){console.warn('focus-file',e)}updateFocusPlayer()}'''
stop=r'''function stopFocusAudio(silent=false){if(audio.filePlayer){try{audio.filePlayer.pause();audio.filePlayer.currentTime=0}catch(_){}audio.filePlayer=null}for(const n of audio.nodes||[]){try{n.stop?.()}catch(_){}try{n.disconnect?.()}catch(_){}}audio.nodes=[];if(audio.pulseTimer)clearInterval(audio.pulseTimer);audio.pulseTimer=null;if(audio.focusGain){try{audio.focusGain.disconnect()}catch(_){}}audio.focusGain=null;if(!silent&&state?.settings?.sfx!==false)playSfx('focus_end');updateFocusPlayer()}'''
volume=r'''function setFocusVolume(v){if(!state)return;state.settings.focusVolume=Number(v);if(audio.filePlayer)audio.filePlayer.volume=clamp(Number(v)/100,0,.6);if(audio.focusGain&&audio.ctx)audio.focusGain.gain.setTargetAtTime(clamp(Number(v)/100,0,.6),audio.ctx.currentTime,.05);save();updateFocusPlayer();if($('focusVolume')){$('focusVolume').value=v;$('focusVolText').textContent=`${v}%`}}'''
player=r'''function updateFocusPlayer(){if(!state||!$('focusPlayer'))return;const enabled=!!state.settings.focusAudio,playing=!!(audio.filePlayer&&!audio.filePlayer.paused)||!!audio.focusGain;$('focusPlayer').classList.toggle('hidden',!enabled);const b=$('focusPlayBtn');if(b){b.dataset.iconName=playing?'pause':'start';b.setAttribute('aria-label',playing?'مکث صدای تمرکز':'پخش صدای تمرکز');b.textContent=''}$('focusAudioTitle').textContent=AUDIO_TITLES[state.settings.focusAudioMode]||'Focus Audio';$('focusAudioState').textContent=playing?'در حال پخش • آفلاین':'برای پخش لمس کن';$('focusQuickVolume').value=state.settings.focusVolume??18}'''
for n,x in [('playSfx',play),('startFocusAudio',start),('stopFocusAudio',stop),('setFocusVolume',volume),('updateFocusPlayer',player)]:js=replace_fn(js,n,x)
js=js.replace("if(audio.focusGain)stopFocusAudio();else","if((audio.filePlayer&&!audio.filePlayer.paused)||audio.focusGain)stopFocusAudio();else")
js=js.replace('Chime کوتاه؛ بدون فایل خارجی.','افکت صوتی واقعی و کوتاه؛ داخل خود اپ.')
js=js.replace('Ambient، باران، Brown Noise یا Pulse؛ در خود اپ ساخته می‌شود.','Ambient، باران، Brown Noise یا Pulse؛ فایل صوتی واقعی و کاملاً آفلاین.')
if "const baseConfirmV120=window.confirm.bind(window);" not in js:
 ins="\nconst baseConfirmV120=window.confirm.bind(window);window.confirm=function(msg){const ok=baseConfirmV120(msg);if(ok&&String(msg).includes('Submit کل راند'))playSfx('submit');return ok};\n"
 js=js.replace('\n})();',ins+'\n})();')
js=re.sub(r'[\U0001F000-\U0001FAFF]','',js)
E.write_text(js,encoding='utf-8')
gp=R/'app/build.gradle.kts';g=gp.read_text(encoding='utf-8');g=re.sub(r'versionCode\s*=\s*\d+','versionCode = 120',g,count=1);g=re.sub(r'versionName\s*=\s*"[^"]+"','versionName = "1.2.0"',g,count=1);gp.write_text(g,encoding='utf-8')
res=R/'app/src/main/res';(res/'drawable').mkdir(parents=True,exist_ok=True);(res/'values').mkdir(parents=True,exist_ok=True);(res/'mipmap-anydpi').mkdir(parents=True,exist_ok=True);(res/'mipmap-anydpi-v26').mkdir(parents=True,exist_ok=True)
(res/'values/v120_colors.xml').write_text('<resources><color name="v120_launcher_bg">#07111F</color></resources>',encoding='utf-8')
fg='''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108"><path android:fillColor="@android:color/transparent" android:strokeColor="#38BDF8" android:strokeWidth="5" android:pathData="M54,20 A34,34 0,1 0,54,88 A34,34 0,1 0,54,20"/><path android:fillColor="@android:color/transparent" android:strokeColor="#A78BFA" android:strokeWidth="5" android:pathData="M54,34 A20,20 0,1 0,54,74 A20,20 0,1 0,54,34"/><path android:fillColor="#6EE7B7" android:pathData="M48,48h12v12h-12z"/><path android:fillColor="@android:color/transparent" android:strokeColor="#E2E8F0" android:strokeWidth="5" android:strokeLineCap="round" android:pathData="M54,39v30 M39,54h30"/></vector>'''
(res/'drawable/ic_launcher_foreground.xml').write_text(fg,encoding='utf-8')
ad='<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/v120_launcher_bg"/><foreground android:drawable="@drawable/ic_launcher_foreground"/></adaptive-icon>'
for n in ['ic_launcher.xml','ic_launcher_round.xml']:(res/'mipmap-anydpi-v26'/n).write_text(ad,encoding='utf-8')
shutil.copy2(res/'drawable/ic_launcher_foreground.xml',res/'mipmap-anydpi/ic_launcher.xml');shutil.copy2(res/'drawable/ic_launcher_foreground.xml',res/'mipmap-anydpi/ic_launcher_round.xml')
shutil.copy2(P/'verify_v120.py',R/'tests/verify_v120.py')
print('PATCH_V120 PASS')
