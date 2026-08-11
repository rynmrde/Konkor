from pathlib import Path
import math,random,struct,sys,wave
A=Path(sys.argv[1]); I=A/'icons'; L=A/'illustrations'; U=A/'audio'
for p in (I,L,U):p.mkdir(parents=True,exist_ok=True)
P={
'home':'M5 11 12 5l7 6v9h-5v-5h-4v5H5z','dashboard':'M5 5h6v6H5z M13 5h6v4h-6z M13 11h6v8h-6z M5 13h6v6H5z','test':'M7 4h10v3h2v13H5V7h2z M8 11h8 M8 15h5','review':'M6 5h12v14H6z M9 9h6 M9 13h6 M9 17h4','wrong':'M7 7l10 10 M17 7 7 17','correct':'M6 12l4 4 8-9','blank':'M6 7h12v10H6z M9 12h6','focus':'M12 5a7 7 0 1 0 0 14 7 7 0 1 0 0-14 M12 9a3 3 0 1 0 0 6 3 3 0 1 0 0-6','adhd':'M8 7c-2 1-3 3-3 5s1 4 3 5 M16 7c2 1 3 3 3 5s-1 4-3 5 M10 8v8 M14 8v8 M10 12h4','themes':'M12 4a8 8 0 1 0 0 16c2 0 2-3 4-3h2c2 0 2-3 0-5-2-5-6-8-6-8z M8 10h.1 M11 7h.1 M15 8h.1','sound':'M5 10h4l4-4v12l-4-4H5z M16 9c2 2 2 4 0 6 M18 7c4 3 4 7 0 10','music':'M9 17a2 2 0 1 1-2-2h2V7l9-2v10a2 2 0 1 1-2-2V8l-7 2z','haptics':'M8 5h8v14H8z M5 8v8 M19 8v8 M11 8h2v8h-2z','settings':'M12 9a3 3 0 1 0 0 6 3 3 0 1 0 0-6 M12 4v2 M12 18v2 M4 12h2 M18 12h2 M6 6l2 2 M16 16l2 2 M18 6l-2 2 M8 16l-2 2','timer':'M9 4h6 M12 7v6l4 2 M7 7a8 8 0 1 0 10 0','progress':'M5 18h14 M7 15v-4 M12 15V7 M17 15V5','streak':'M12 4c2 4 5 5 5 9a5 5 0 0 1-10 0c0-3 2-5 4-7 0 3 1 4 1 4 1-2 1-4 0-6z','bookmark':'M7 5h10v15l-5-3-5 3z','flag':'M7 20V5 M8 6h9l-2 4 2 4H8','next':'M9 6l6 6-6 6','previous':'M15 6l-6 6 6 6','start':'M8 6l10 6-10 6z','pause':'M8 6h3v12H8z M13 6h3v12h-3z','resume':'M8 6l10 6-10 6z M6 5v14','plan':'M6 5h12v15H6z M9 3v4 M15 3v4 M8 10h8 M8 14h5','calendar':'M6 6h12v14H6z M9 3v5 M15 3v5 M6 10h12 M9 13h2 M13 13h2 M9 16h2','mastery':'M12 4l2 4 5 1-4 4 1 5-4-2-4 2 1-5-4-4 5-1z','analytics':'M5 19V9 M10 19V5 M15 19v-7 M20 19H4','export':'M12 4v11 M8 8l4-4 4 4 M6 14v5h12v-5','import':'M12 15V4 M8 11l4 4 4-4 M6 14v5h12v-5','close':'M7 7l10 10 M17 7 7 17','check':'M6 12l4 4 8-9'}
T='<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{}"/></svg>'
for n,p in P.items():(I/f'{n}.svg').write_text(T.format(p),encoding='utf-8')
ILL={
'round_complete':'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180"><rect x="18" y="18" width="284" height="144" rx="30" fill="#111827"/><circle cx="160" cy="82" r="42" fill="#34d399" opacity=".16"/><path d="M137 83l16 16 33-38" fill="none" stroke="#6ee7b7" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><path d="M98 135h124" stroke="#94a3b8" stroke-width="6" stroke-linecap="round" opacity=".45"/></svg>',
'focus_complete':'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180"><rect x="18" y="18" width="284" height="144" rx="30" fill="#0b1020"/><circle cx="160" cy="88" r="52" fill="none" stroke="#38bdf8" stroke-width="7" opacity=".35"/><circle cx="160" cy="88" r="32" fill="none" stroke="#a78bfa" stroke-width="7" opacity=".7"/><circle cx="160" cy="88" r="11" fill="#e2e8f0"/></svg>',
'streak':'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180"><rect x="18" y="18" width="284" height="144" rx="30" fill="#120d18"/><path d="M160 40c18 28 38 37 38 65 0 23-17 39-38 39s-38-16-38-39c0-19 12-32 26-47-1 18 5 24 12 30 9-12 10-28 0-48z" fill="#fb7185"/><path d="M160 91c9 11 17 18 17 30 0 10-7 17-17 17s-17-7-17-17c0-9 6-16 13-23 0 8 2 12 4 15 4-6 4-13 0-22z" fill="#fde68a"/></svg>',
'empty_state':'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180"><rect x="18" y="18" width="284" height="144" rx="30" fill="#0f172a"/><rect x="88" y="48" width="144" height="86" rx="16" fill="#1e293b" stroke="#64748b" stroke-width="3"/><path d="M112 75h96M112 94h72M112 113h52" stroke="#94a3b8" stroke-width="7" stroke-linecap="round"/><circle cx="222" cy="126" r="23" fill="#22c55e"/><path d="M211 126l8 8 14-17" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/></svg>',
'splash':'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180"><rect width="320" height="180" rx="36" fill="#07111f"/><circle cx="160" cy="88" r="56" fill="none" stroke="#38bdf8" stroke-width="5" opacity=".32"/><circle cx="160" cy="88" r="35" fill="none" stroke="#a78bfa" stroke-width="5" opacity=".66"/><path d="M132 88h56M160 60v56" stroke="#e2e8f0" stroke-width="8" stroke-linecap="round"/><circle cx="160" cy="88" r="10" fill="#6ee7b7"/></svg>'}
for n,s in ILL.items():(L/f'{n}.svg').write_text(s,encoding='utf-8')
SR=16000
def wav(path,s):
 with wave.open(str(path),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(b''.join(struct.pack('<h',max(-32767,min(32767,int(x*32767)))) for x in s))
def tone(f,d,a=.18):
 n=int(SR*d);return [a*math.sin(2*math.pi*f*i/SR)*min(1,i/(SR*.015),max(0,(n-i)/(SR*.06))) for i in range(n)]
def seq(fs):
 o=[]
 for f,d,a in fs:o+=tone(f,d,a)+[0]*int(SR*.025)
 return o
S={'sfx_select':tone(520,.07,.10),'sfx_submit':seq([(330,.08,.13),(440,.11,.14)]),'sfx_correct':seq([(523.25,.12,.17),(659.25,.17,.15)]),'sfx_wrong':seq([(196,.13,.15),(164.81,.18,.13)]),'sfx_complete':seq([(392,.10,.12),(523.25,.12,.13),(659.25,.19,.14)]),'sfx_focus_start':seq([(261.63,.08,.08),(392,.14,.10)]),'sfx_focus_end':seq([(392,.09,.08),(261.63,.14,.08)])}
for n,s in S.items():wav(U/f'{n}.wav',s)
N=SR*8;r=random.Random(1405)
amb=[.085*math.sin(2*math.pi*110*i/SR)+.028*math.sin(2*math.pi*165*i/SR)+.02*math.sin(2*math.pi*220*i/SR) for i in range(N)]
last=0;brown=[]
for _ in range(N):last=(last+.025*r.uniform(-1,1))/1.025;brown.append(max(-.24,min(.24,last*2.1)))
prev=0;drop=0;rain=[]
for i in range(N):
 w=r.uniform(-1,1);hp=w-prev*.92;prev=w
 if r.random()<.0007:drop=r.uniform(.12,.28)
 drop*=.997;rain.append(max(-.3,min(.3,.085*hp+drop*math.sin(2*math.pi*1800*i/SR))))
pulse=[.05*math.sin(2*math.pi*147*i/SR)+.03*((.5+.5*math.sin(2*math.pi*.5*i/SR))**3)*math.sin(2*math.pi*294*i/SR) for i in range(N)]
for n,s in [('focus_ambient',amb),('focus_rain',rain),('focus_brown',brown),('focus_pulse',pulse)]:wav(U/f'{n}.wav',s)
print('MEDIA_GENERATE PASS',len(P),len(ILL),len(S),4)
