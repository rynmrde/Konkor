import sqlite3,json,re,hashlib,unicodedata
from collections import defaultdict,Counter
DB='/home/ubuntu/physics-review/radiology1405_bank_v6_1.db'
c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
rows=c.execute("select * from question where subject=?",('فیزیک',)).fetchall()
records=[]
for r in rows:
 q=json.loads(r['full_json'])
 opts=q.get('options') or []
 def txt(x):
  if isinstance(x,str): return x
  if isinstance(x,dict): return ' '.join(str(v) for v in x.values())
  return str(x)
 opts=[txt(x) for x in opts]
 alltxt=json.dumps(q,ensure_ascii=False)
 stimulus=q.get('stimulus') or {}
 records.append({'id':r['id'],'pool':r['access_pool'],'source_type':r['source_type'],'key':q.get('correct_index',r['correct_index']),'opts':opts,'stem':txt(q.get('stem','')),'analysis':txt(q.get('correct_analysis','')),'alltxt':alltxt,'stimulus':stimulus,'followup':r['followup_group'],'scenario':r['scenario_family']})

def norm(s,mask=False):
 s=unicodedata.normalize('NFKC',s or '').lower().replace('ي','ی').replace('ك','ک')
 if mask:s=re.sub(r'[+-]?(?:\d+(?:[.,/]\d+)?|[a-zA-Z])','#',s)
 return re.sub(r'\W+',' ',s,flags=re.UNICODE).strip()
def sig(r): return norm(r['stem'])+'||'+'|'.join(norm(x) for x in r['opts'])
def fullsig(r): return sig(r)+'||'+norm(json.dumps(r['stimulus'],ensure_ascii=False))
def groups(items,key):
 d=defaultdict(list)
 for r in items:d[key(r)].append(r['id'])
 return [v for v in d.values() if len(v)>1]
raw_pat=r'\b(?:wrong_condition|partial_truth|overgeneralization|calculation_trap|unit_mistake|condition_wrong|truth_partial)\b'
comp=[r['id'] for r in records if isinstance(r['stimulus'],dict) and r['stimulus'].get('type')=='comparison']
short=[r['id'] for r in records if len(norm(r['analysis']))<60]
raw=[r['id'] for r in records if re.search(raw_pat,r['alltxt'],re.I)]
exact=groups(records,fullsig)
reordered=groups(records,lambda r:norm(r['stem'])+'||'+'|'.join(sorted(norm(x) for x in r['opts']))+'||'+norm(json.dumps(r['stimulus'],ensure_ascii=False)))
numeric=groups(records,lambda r:norm(r['stem'],True)+'||'+'|'.join(norm(x,True) for x in r['opts'])+'||'+norm(json.dumps(r['stimulus'],ensure_ascii=False),True))
follow=defaultdict(list)
for r in records:
 if r['followup']:follow[r['followup']].append(r['id'])
follow_pairs={k:v for k,v in follow.items() if len(v)>1}
print(json.dumps({'total':len(records),'pools':Counter(r['pool'] for r in records),'source_types':Counter(r['source_type'] for r in records),'raw_enum_ids':raw,'short_analysis_ids':short,'comparison_ids':comp,'exact_full_payload_groups':exact,'reordered_groups':reordered,'numeric_groups':numeric,'same_followup_groups':follow_pairs,'key_invalid_ids':[r['id'] for r in records if not isinstance(r['key'],int) or not 0<=r['key']<len(r['opts'])],'option_count_bad':[r['id'] for r in records if len(r['opts'])!=4]},ensure_ascii=False,indent=2))
