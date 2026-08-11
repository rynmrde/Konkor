from pathlib import Path
import re,sys,wave,xml.etree.ElementTree as ET
R=Path(sys.argv[1] if len(sys.argv)>1 else 'project');A=R/'app/src/main/assets'
req=['index.html','experience.js','experience.css','professional.js','professional.css']
for n in req:
 p=A/n
 if not p.exists() or p.stat().st_size<50:raise SystemExit('missing '+str(p))
h=(A/'index.html').read_text(encoding='utf-8');e=(A/'experience.js').read_text(encoding='utf-8');pjs=(A/'professional.js').read_text(encoding='utf-8')
for x in ['professional.css','professional.js','icons/calendar.svg','icons/import.svg','icons/flag.svg','icons/correct.svg','icons/wrong.svg']:
 if x not in h:raise SystemExit('HTML integration missing '+x)
legacy=['🎯','📚','✅','❌','⚑','⚐','⏭']
for ch in legacy:
 if ch in h:raise SystemExit('legacy emoji remains '+repr(ch))
if re.search(r'[\U0001F000-\U0001FAFF]',h+e+pjs):raise SystemExit('high-plane emoji remains')
icons=['home','dashboard','test','review','wrong','correct','blank','focus','adhd','themes','sound','music','haptics','settings','timer','progress','streak','bookmark','flag','next','previous','start','pause','resume','plan','calendar','mastery','analytics','export','import','close','check']
ills=['round_complete','focus_complete','streak','empty_state','splash']
for n in icons:
 f=A/'icons'/f'{n}.svg';ET.parse(f)
 if f.stat().st_size<170:raise SystemExit('tiny icon '+n)
for n in ills:
 f=A/'illustrations'/f'{n}.svg';ET.parse(f)
 if f.stat().st_size<180:raise SystemExit('tiny illustration '+n)
sfx=['select','submit','correct','wrong','complete','focus_start','focus_end'];focus=['ambient','rain','brown','pulse']
def wavcheck(f,focus_loop=False):
 with wave.open(str(f),'rb') as w:
  if w.getnchannels()!=1 or w.getframerate()!=16000 or w.getsampwidth()!=2:raise SystemExit('bad wav format '+f.name)
  dur=w.getnframes()/w.getframerate()
  if focus_loop and dur<7.9:raise SystemExit('focus loop too short '+f.name)
  if not focus_loop and dur<.04:raise SystemExit('sfx too short '+f.name)
for n in sfx:wavcheck(A/'audio'/f'sfx_{n}.wav')
for n in focus:wavcheck(A/'audio'/f'focus_{n}.wav',True)
for n in ['sfx_select','sfx_submit','sfx_correct','sfx_wrong','sfx_complete','sfx_focus_start','sfx_focus_end']:
 if n not in e:raise SystemExit('SFX not wired '+n)
for n in focus:
 if f'focus_${{mode}}.wav' not in e and f'focus_{n}.wav' not in e:raise SystemExit('focus audio wiring missing')
def fn(s,n):
 m=re.search(r'function\s+'+re.escape(n)+r'\s*\([^)]*\)\s*\{',s)
 if not m:raise SystemExit('missing function '+n)
 i=m.end();d=1;q=None;esc=False
 while i<len(s) and d:
  c=s[i]
  if q:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c==q:q=None
  else:
   if c in "'\"`":q=c
   elif c=='{':d+=1
   elif c=='}':d-=1
  i+=1
 return s[m.start():i]
ps=fn(e,'playSfx');fs=fn(e,'startFocusAudio');fv=fn(e,'setFocusVolume');up=fn(e,'updateFocusPlayer')
if 'new Audio(' not in ps or 'beep(' in ps:raise SystemExit('SFX still synthesized')
if 'new Audio(' not in fs or 'createOscillator' in fs or 'createBufferSource' in fs:raise SystemExit('focus audio still synthesized')
if 'filePlayer.volume' not in fv:raise SystemExit('live focus volume not wired')
if "dataset.iconName=playing?'pause':'start'" not in up:raise SystemExit('play pause icon not wired')
if "Submit کل راند" not in e or "playSfx('submit')" not in e:raise SystemExit('submit SFX hook missing')
for token in ['proThemeGrid','proSplash','MutationObserver','illustrations/round_complete.svg','illustrations/empty_state.svg']:
 if token not in pjs:raise SystemExit('professional UI missing '+token)
g=(R/'app/build.gradle.kts').read_text(encoding='utf-8')
if 'versionCode = 120' not in g or 'versionName = "1.2.0"' not in g:raise SystemExit('version not 1.2.0')
for f in [R/'app/src/main/res/drawable/ic_launcher_foreground.xml',R/'app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml',R/'app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml',R/'app/src/main/res/values/v120_colors.xml']:
 ET.parse(f)
print('VERIFY_V120 PASS icons=32 illustrations=5 sfx=7 focus_loops=4 version=1.2.0')
