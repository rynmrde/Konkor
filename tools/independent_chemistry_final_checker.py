import hashlib,json,sqlite3,re,unicodedata,tarfile
from pathlib import Path
from collections import defaultdict
ROOT=Path('/home/ubuntu/chem-final-review')
DB=Path('/home/ubuntu/physics-review/radiology1405_bank_v6_1.db')
GZ=Path('/home/ubuntu/physics-review/radiology1405_bank_v6_1.db.gz')
OV=ROOT/'src/rynmrde-Konkor-4e9a2f2/radiology_v614_rescue_patch/overlay.tar.xz'
MODELS=ROOT/'overlay/app/src/main/java/com/radiology1405/prep/data/Models.kt'
expected_gz='b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14'
expected_db='d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c'
expected_overlay='8f3ac3751a92534c7767afce31d36f880b1c0aaabac68e15bbe6be396c9609d2'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
con=sqlite3.connect(DB); con.row_factory=sqlite3.Row
rows=con.execute("select * from question where subject=?",('شیمی',)).fetchall()
records=[]
for r in rows:
 q=json.loads(r['full_json']); records.append((r,q))
models=MODELS.read_text()
override_ids=re.findall(r'\"([^\"]+)\"\s+to\s+\"',models[models.find('correctedChemistryAnalyses'):models.find(')',models.find('correctedChemistryAnalyses'))+1])
# Robustly use the report's exact 19 IDs as the expected reviewed set.
expected_ids=['v3_chem_17_03','v3_chem_17_05','v3_chem_17_07','v3_chem_17_09','v3_chem_17_16','v3_chem_17_17','v3_chem_21_15','v3_chem_21_19','real_1404_n1in_chem_079','v3_chem_18_14','v3_chem_18_17','v3_chem_18_20','v3_chem_22_17','v3_chem_22_18','v3_chem_23_02','v3_chem_23_06','v3_chem_23_10','v3_chem_23_13','real_1404_n1in_chem_105']
byid={r['id']:q for r,q in records}
structured=[]
for r,q in records:
 s=q.get('stimulus') or {}
 if s.get('type') in ('data_table','comparison'): structured.append((r['id'],s))
def norm(x,mask=False):
 x=unicodedata.normalize('NFKC',str(x or '')).replace('ي','ی').replace('ك','ک').lower()
 if mask:x=re.sub(r'[+\-]?\d+(?:[.,/]\d+)?','#',x)
 return re.sub(r'\s+',' ',re.sub(r'[^\w#]+',' ',x)).strip()
def stim_sig(s):
 if s.get('type')=='data_table': return '||'.join(norm(x) for x in [s.get('caption',''),*(s.get('headers') or []),*[c for row in s.get('rows') or [] for c in row]])
 if s.get('type')=='comparison': return '||'.join(norm(s.get(k,'')) for k in ('left_label','left','right_label','right'))
 return ''
def core_stem(stem):
 for p in ('داده‌های زیر را با مدل مناسب پیوند دهید…','برای حل مسئلهٔ زیر، کدام پاسخ نهایی با مسیر کنترل درست جفت شده است؟'):
  stem=stem.replace(p,'')
 return norm(stem)
def sig(r,q,mask=False):
 s=q.get('stimulus') or {}
 return core_stem(q.get('stem',''))+'||'+stim_sig(s)+(('||'+ '|'.join(sorted(norm(x,mask) for x in q.get('options',[])))) if not (core_stem(q.get('stem',''))+'||'+stim_sig(s)).strip() or len(core_stem(q.get('stem',''))+'||'+stim_sig(s))<24 else '')
# duplicate groups among all structured records, and previous claims' old groups remain only as old-wrapper collisions
structured_sigs=defaultdict(list)
for r,q in records:
 if (q.get('stimulus') or {}).get('type') in ('data_table','comparison'): structured_sigs[sig(r,q)].append(r['id'])
structured_dupes=[v for v in structured_sigs.values() if len(v)>1]
# final active train structural checks
active=[(r,q) for r,q in records if r['access_pool']=='TRAIN' and r['selected_scope'] and not r['obsolete']]
bad=[]
for r,q in active:
 if len(q.get('options') or [])!=4 or not isinstance(q.get('correct_index'),int) or not 0<=q['correct_index']<4: bad.append(r['id'])
visible_tokens=[]
for r,q in records:
 txt=json.dumps(q,ensure_ascii=False)
 if re.search(r'\b(?:wrong_condition|partial_truth|truth_partial|overgeneralization|correct_reasoning|calculation_trap)\b',txt): visible_tokens.append(r['id'])
# override evidence: every override must exist and have substantial text with formula/result evidence
missing=[i for i in expected_ids if i not in models]
override_checks={}
for i in expected_ids:
 m=re.search(r'\"'+re.escape(i)+r'\"\s+to\s+\"([^\"]*)\"',models)
 text=m.group(1) if m else ''
 override_checks[i]={'present':bool(m),'len':len(text),'has_equation':bool(re.search(r'[=→]',text)),'has_numeric':bool(re.search(r'[0-9۰-۹]',text)),'has_chem_or_unit':bool(re.search(r'(?:mol|M|L|g|جرم|مول|لیتر|درصد|٪|mL|M·s|e⁻|H⁺|O₂)',text))}
print(json.dumps({'gzip_sha256':sha(GZ),'db_sha256':sha(DB),'overlay_sha256':sha(OV),'chemistry_total':len(records),'active_train':len(active),'structured_stimulus_total':len(structured),'structured_ids':[i for i,_ in structured],'structured_signature_duplicate_groups':structured_dupes,'bad_active_train_structure':bad,'raw_token_ids_in_frozen_json':visible_tokens,'expected_override_count':len(expected_ids),'missing_override_ids':missing,'override_checks':override_checks},ensure_ascii=False,indent=2))
