from pathlib import Path
import hashlib,re,shutil,subprocess,sys
R=Path(sys.argv[1] if len(sys.argv)>1 else 'project'); P=Path(sys.argv[2] if len(sys.argv)>2 else 'radiology_v120_patch')
A=R/'app/src/main/assets'; H=A/'index.html'; E=A/'experience.js'; C=A/'experience.css'
if not H.exists() or not E.exists() or not C.exists(): raise SystemExit('V120: v1.1 assets missing')
index_before=hashlib.sha256(H.read_bytes()).hexdigest()
subprocess.run([sys.executable,str(P/'generate_media.py'),str(A)],check=True)
for n in ['professional.js','professional.css']: shutil.copy2(P/n,A/n)
css=C.read_text(encoding='utf-8'); procss=(P/'professional.css').read_text(encoding='utf-8')
if '/* V120_PROFESSIONAL_CSS */' not in css: css += '\n/* V120_PROFESSIONAL_CSS */\n'+procss+'\n'
C.write_text(css,encoding='utf-8')
js=E.read_text(encoding='utf-8')
def replace_fn(src,name,new):
 m=re.search(r'function\s+'+re.escape(name)+r'\s*\([^)]*\)\s*\{',src)
 if not m: raise RuntimeError('experience fn missing '+name)
 i=m.end();depth=1;quote=None;esc=False;line=False;multi=False
 while i<len(src) and depth:
  c=src[i];d=src[i+1] if i+1<len(src) else ''
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
 if depth: raise RuntimeError('unbalanced '+name)
 return src[:m.start()]+new+src[i:]
play="function playSfx(kind){if(state?.settings?.sfx===false)return;const map={select:'sfx_select',submit:'sfx_submit',correct:'sfx_correct',wrong:'sfx_wrong',done:'sfx_complete',focus_start:'sfx_focus_start',focus_end:'sfx_focus_end'},n=map[kind];if(!n)return;try{const p=new Audio(`audio/${n}.wav`);p.preload='auto';p.volume=clamp(Number(state?.settings?.sfxVolume??45)/100,0,.75);audio.fileSfx=audio.fileSfx||[];audio.fileSfx=audio.fileSfx.filter(x=>!x.ended);audio.fileSfx.push(p);p.play().catch(()=>{})}catch(e){console.warn('sfx-file',e)}}"
start="function startFocusAudio(){stopFocusAudio(true);if(!state?.settings?.focusAudio)return updateFocusPlayer();try{const mode=state.settings.focusAudioMode||'ambient',p=new Audio(`audio/focus_${mode}.wav`);p.loop=true;p.preload='auto';p.volume=clamp(Number(state.settings.focusVolume??18)/100,0,.6);audio.filePlayer=p;p.play().then(()=>playSfx('focus_start')).catch(e=>{audio.filePlayer=null;console.warn('focus-file',e);toast('پخش صدا روی این WebView در دسترس نیست');updateFocusPlayer()})}catch(e){console.warn('focus-file',e)}updateFocusPlayer()}"
stop="function stopFocusAudio(silent=false){if(audio.filePlayer){try{audio.filePlayer.pause();audio.filePlayer.currentTime=0}catch(_){}audio.filePlayer=null}for(const n of audio.nodes||[]){try{n.stop?.()}catch(_){}try{n.disconnect?.()}catch(_){}}audio.nodes=[];if(audio.pulseTimer)clearInterval(audio.pulseTimer);audio.pulseTimer=null;if(audio.focusGain){try{audio.focusGain.disconnect()}catch(_){}}audio.focusGain=null;if(!silent&&state?.settings?.sfx!==false)playSfx('focus_end');updateFocusPlayer()}"
volume="function setFocusVolume(v){if(!state)return;state.settings.focusVolume=Number(v);if(audio.filePlayer)audio.filePlayer.volume=clamp(Number(v)/100,0,.6);if(audio.focusGain&&audio.ctx)audio.focusGain.gain.setTargetAtTime(clamp(Number(v)/100,0,.6),audio.ctx.currentTime,.05);save();updateFocusPlayer();if($('focusVolume')){$('focusVolume').value=v;$('focusVolText').textContent=`${v}%`}}"
player="function updateFocusPlayer(){if(!state||!$('focusPlayer'))return;const enabled=!!state.settings.focusAudio,playing=!!(audio.filePlayer&&!audio.filePlayer.paused)||!!audio.focusGain;$('focusPlayer').classList.toggle('hidden',!enabled);const b=$('focusPlayBtn');if(b){b.dataset.iconName=playing?'pause':'start';b.setAttribute('aria-label',playing?'مکث صدای تمرکز':'پخش صدای تمرکز');b.textContent=''}$('focusAudioTitle').textContent=AUDIO_TITLES[state.settings.focusAudioMode]||'Focus Audio';$('focusAudioState').textContent=playing?'در حال پخش • آفلاین':'برای پخش لمس کن';$('focusQuickVolume').value=state.settings.focusVolume??18}"
for n,x in [('playSfx',play),('startFocusAudio',start),('stopFocusAudio',stop),('setFocusVolume',volume),('updateFocusPlayer',player)]: js=replace_fn(js,n,x)
js=js.replace("if(audio.focusGain)stopFocusAudio();else","if((audio.filePlayer&&!audio.filePlayer.paused)||audio.focusGain)stopFocusAudio();else")
js=js.replace('Chime کوتاه؛ بدون فایل خارجی.','افکت صوتی واقعی و کوتاه؛ داخل خود اپ.')
js=js.replace('Ambient، باران، Brown Noise یا Pulse؛ در خود اپ ساخته می‌شود.','Ambient، باران، Brown Noise یا Pulse؛ فایل صوتی واقعی و کاملاً آفلاین.')
if "const baseConfirmV120=window.confirm.bind(window);" not in js:
 ins="\nconst baseConfirmV120=window.confirm.bind(window);window.confirm=function(msg){const ok=baseConfirmV120(msg);if(ok&&String(msg).includes('Submit کل راند'))playSfx('submit');return ok};\n"
 pos=js.rfind('\n})();')
 if pos<0: raise RuntimeError('experience IIFE close missing')
 js=js[:pos]+ins+js[pos:]
if '/* V120_PROFESSIONAL_JS */' not in js: js += '\n/* V120_PROFESSIONAL_JS */\n'+(P/'professional.js').read_text(encoding='utf-8')+'\n'
E.write_text(js,encoding='utf-8')
gp=R/'app/build.gradle.kts';g=gp.read_text(encoding='utf-8');g=re.sub(r'versionCode\s*=\s*\d+','versionCode = 120',g,count=1);g=re.sub(r'versionName\s*=\s*"[^"]+"','versionName = "1.2.0"',g,count=1);gp.write_text(g,encoding='utf-8')
res=R/'app/src/main/res';(res/'drawable').mkdir(parents=True,exist_ok=True);(res/'values').mkdir(parents=True,exist_ok=True);(res/'mipmap-anydpi').mkdir(parents=True,exist_ok=True);(res/'mipmap-anydpi-v26').mkdir(parents=True,exist_ok=True)
(res/'values/v120_colors.xml').write_text('<resources><color name="v120_launcher_bg">#07111F</color></resources>',encoding='utf-8')
fg="<vector xmlns:android=\"http://schemas.android.com/apk/res/android\" android:width=\"108dp\" android:height=\"108dp\" android:viewportWidth=\"108\" android:viewportHeight=\"108\"><path android:fillColor=\"@android:color/transparent\" android:strokeColor=\"#38BDF8\" android:strokeWidth=\"5\" android:pathData=\"M54,20 A34,34 0,1 0,54,88 A34,34 0,1 0,54,20\"/><path android:fillColor=\"@android:color/transparent\" android:strokeColor=\"#A78BFA\" android:strokeWidth=\"5\" android:pathData=\"M54,34 A20,20 0,1 0,54,74 A20,20 0,1 0,54,34\"/><path android:fillColor=\"#6EE7B7\" android:pathData=\"M48,48h12v12h-12z\"/><path android:fillColor=\"@android:color/transparent\" android:strokeColor=\"#E2E8F0\" android:strokeWidth=\"5\" android:strokeLineCap=\"round\" android:pathData=\"M54,39v30 M39,54h30\"/></vector>"
(res/'drawable/ic_launcher_foreground.xml').write_text(fg,encoding='utf-8')
ad='<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/v120_launcher_bg"/><foreground android:drawable="@drawable/ic_launcher_foreground"/></adaptive-icon>'
for n in ['ic_launcher.xml','ic_launcher_round.xml']:(res/'mipmap-anydpi-v26'/n).write_text(ad,encoding='utf-8')
shutil.copy2(res/'drawable/ic_launcher_foreground.xml',res/'mipmap-anydpi/ic_launcher.xml');shutil.copy2(res/'drawable/ic_launcher_foreground.xml',res/'mipmap-anydpi/ic_launcher_round.xml')
(R/'tests').mkdir(parents=True,exist_ok=True);shutil.copy2(P/'verify_v120.py',R/'tests/verify_v120.py')
(R/'tests/v120_index_before.sha256').write_text(index_before+'  app/src/main/assets/index.html\n',encoding='utf-8')
index_after=hashlib.sha256(H.read_bytes()).hexdigest()
if index_after!=index_before: raise RuntimeError('V120 modified index/core HTML')
print('V120_INDEX_CORE_INTEGRITY PASS',index_before)
print('PATCH_V120 PASS')
