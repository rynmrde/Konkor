from pathlib import Path
import hashlib,re,sys,wave,xml.etree.ElementTree as ET
R=Path(sys.argv[1] if len(sys.argv)>1 else '.');A=R/'app/src/main/assets';H=A/'index.html'
for n in ['index.html','experience.js','experience.css','professional.js','professional.css']:
 p=A/n
 if not p.exists() or p.stat().st_size<50:raise SystemExit('missing '+str(p))
# V1.2 is forbidden from touching the core single-file HTML.
hf=R/'tests/v120_index_before.sha256'
if not hf.exists():raise SystemExit('missing index integrity record')
expected=hf.read_text(encoding='utf-8').split()[0];actual=hashlib.sha256(H.read_bytes()).hexdigest()
if actual!=expected:raise SystemExit('index/core SHA changed')
e=(A/'experience.js').read_text(encoding='utf-8');ec=(A/'experience.css').read_text(encoding='utf-8');pjs=(A/'professional.js').read_text(encoding='utf-8')
if '/* V120_PROFESSIONAL_JS */' not in e or 'proThemeGrid' not in e:raise SystemExit('professional JS not loaded through experience layer')
if '/* V120_PROFESSIONAL_CSS */' not in ec or '.proThemeGrid' not in ec:raise SystemExit('professional CSS not loaded through experience layer')
for token in ['LEGACY','replaceLegacy','MutationObserver','proThemeGrid','proSplash','illustrations/round_complete.svg','illustrations/empty_state.svg']:
 if token not in pjs:raise SystemExit('professional UI missing '+token)
icons=['home','dashboard','test','review','wrong','correct','blank','focus','adhd','themes','sound','music','haptics','settings','timer','progress','streak','bookmark','flag','next','previous','start','pause','resume','plan','calendar','mastery','analytics','export','import','close','check']
ills=['round_complete','focus_complete','streak','empty_state','splash']
for n in icons:
 f=A/'icons'/f'{n}.svg';ET.parse(f)
 if f.stat().st_size<170:raise SystemExit('tiny icon '+n)
for n in ills:
 f=A/'illustrations'/f'{n}.svg';ET.parse(f)
 if f.stat().st_size<180:raise SystemExit('tiny illustration '+n)
sfx=['select','submit','correct','wrong','complete','focus_start','focus_end'];focus=['ambient','rain','brown','pulse']
def wavcheck(f,loop=False):
 with wave.open(str(f),'rb') as w:
  if w.getnchannels()!=1 or w.getframerate()!=16000 or w.getsampwidth()!=2:raise SystemExit('bad wav '+f.name)
  dur=w.getnframes()/w.getframerate()
  if loop and dur<7.9:raise SystemExit('short loop '+f.name)
  if not loop and dur<.04:raise SystemExit('short sfx '+f.name)
for n in sfx:wavcheck(A/'audio'/f'sfx_{n}.wav')
for n in focus:wavcheck(A/'audio'/f'focus_{n}.wav',True)
def fn(s,n):
 m=re.search(r'function\s+'+re.escape(n)+r'\s*\([^)]*\)\s*\{',s)
 if not m:raise SystemExit('missing UX function '+n)
 i=m.end();d=1;q=None;esc=False;line=False;multi=False
 while i<len(s) and d:
  c=s[i];x=s[i+1] if i+1<len(s) else ''
  if line:
   if c=='\n':line=False
  elif multi:
   if c=='*' and x=='/':multi=False;i+=1
  elif q:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c==q:q=None
  else:
   if c=='/' and x=='/':line=True;i+=1
   elif c=='/' and x=='*':multi=True;i+=1
   elif c in "'\"`":q=c
   elif c=='{':d+=1
   elif c=='}':d-=1
  i+=1
 return s[m.start():i]
ps=fn(e,'playSfx');fs=fn(e,'startFocusAudio');fv=fn(e,'setFocusVolume');up=fn(e,'updateFocusPlayer')
if 'new Audio(' not in ps or 'beep(' in ps:raise SystemExit('SFX still synthesized')
if 'new Audio(' not in fs or 'createOscillator' in fs or 'createBufferSource' in fs:raise SystemExit('focus still synthesized')
if 'filePlayer.volume' not in fv:raise SystemExit('focus volume missing')
if "dataset.iconName=playing?'pause':'start'" not in up:raise SystemExit('play pause icon missing')
if "Submit کل راند" not in e or "playSfx('submit')" not in e:raise SystemExit('submit SFX hook missing')
g=(R/'app/build.gradle.kts').read_text(encoding='utf-8')
if 'versionCode = 120' not in g or 'versionName = "1.2.0"' not in g:raise SystemExit('version not 1.2.0')
for f in [R/'app/src/main/res/drawable/ic_launcher_foreground.xml',R/'app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml',R/'app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml',R/'app/src/main/res/values/v120_colors.xml']:ET.parse(f)
print('VERIFY_V120 PASS core_index_sha='+actual+' icons=32 illustrations=5 sfx=7 focus_loops=4 version=1.2.0')
