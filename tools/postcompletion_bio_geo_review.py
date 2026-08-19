#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,sqlite3,sys
from pathlib import Path

CONFLICTS=[f'v3_bio_{i:02d}_01' for i in range(9,17)]
RESIDUAL=['v3_bio_12_08','v3_bio_15_11','v3_bio_16_13']
BIO_STIM=['v3_bio_02_12','v3_bio_05_12','v3_bio_06_07','v3_bio_07_15','v3_bio_08_07','v3_bio_10_11','v3_bio_11_07','v3_bio_12_07','v3_bio_14_10','v3_bio_15_15','v3_bio_16_10']
GEO_STIM=['v3_geo_45_09','v3_geo_46_08','v3_geo_47_07','v3_geo_49_08']
VISIBLE=['v3_bio_11_24','v3_bio_13_15','v3_bio_14_20','v3_bio_15_24','v3_bio_16_16']
RAW=('condition_wrong','wrong_condition','truth_partial','partial_truth','overgeneralization','calculation_trap','calculation_error','unit_mistake','unit_error','direction_error','false_absolute','keyword_trap','knowledge_gap','forgotten_rule','misread','time_management','careless_error')

def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

def load_bank(p):
 o=json.loads(Path(p).read_text()); rows=o['questions'] if isinstance(o,dict) and isinstance(o.get('questions'),list) else o
 return {str(q['id']):q for q in rows}, o

def text(q): return ' '.join(str(q.get(k,'')) for k in ('stem','correct_analysis','short_lesson','fast_method','main_trap','distractor_analyses'))

def stim(q):
 s=q.get('stimulus') or q.get('paired_stimulus') or q.get('pair')
 return s if isinstance(s,dict) else None

def main(successor, bank_path, science_path, app_path):
 s=json.loads(Path(successor).read_text()); updates=s.get('updates',[]); by={u['id']:u for u in updates}; bank,root=load_bank(bank_path)
 out={'successor':{},'residual':{},'stimulus':{},'geo153':{},'stable_ids':{},'regressions':{}}
 out['successor']={'update_count':len(updates),'unique_ids':len(by),'conflict_ids_present':[x for x in CONFLICTS if x in by],'conflict_sources':{x:by.get(x,{}).get('source_payload') for x in CONFLICTS},'all_conflicts_compact_owned':all(by.get(x,{}).get('source_payload')=='biology-v6.1.5-analysis-safety' for x in CONFLICTS),'analysis_only':all(set(u.get('fields',{}))=={'correct_analysis','distractor_analyses','short_lesson'} for u in updates),'all_successor_ids_in_bank':all(x in bank for x in by)}
 for x in RESIDUAL:
  q=bank.get(x,{}); out['residual'][x]={'in_successor':x in by,'bank_present':x in bank,'correct_index':q.get('correct_index'),'analysis_update_fields':sorted((by.get(x,{}).get('fields') or {}).keys()),'stem':q.get('stem'),'options':q.get('options')}
 comparisons=BIO_STIM+GEO_STIM
 stems=[str(bank[x].get('stem','')) for x in comparisons if x in bank]
 pairs=[(str((stim(bank[x]) or {}).get('left','')),str((stim(bank[x]) or {}).get('right',''))) for x in comparisons if x in bank]
 out['stimulus']={'biology_ids':BIO_STIM,'geology_ids':GEO_STIM,'biology_count':len([x for x in BIO_STIM if x in bank]),'geology_count':len([x for x in GEO_STIM if x in bank]),'all_canonical_nonempty':all(isinstance(stim(bank.get(x,{})),dict) and str(stim(bank[x]).get('left','')).strip() and str(stim(bank[x]).get('right','')).strip() for x in comparisons),'duplicate_stems':len(stems)-len(set(stems)),'duplicate_structured_pairs':len(pairs)-len(set(pairs)),'records':{x:{'subject':bank.get(x,{}).get('subject'),'stimulus_keys':sorted((stim(bank.get(x,{})) or {}).keys()),'left':(stim(bank.get(x,{})) or {}).get('left'),'right':(stim(bank.get(x,{})) or {}).get('right'),'stem':bank.get(x,{}).get('stem'),'options':bank.get(x,{}).get('options')} for x in comparisons}}
 geo=bank.get('real_1401_in_geo_153',{})
 out['geo153']={'bank_present':'real_1401_in_geo_153' in bank,'successor_present':'real_1401_in_geo_153' in by,'official_key_verified':geo.get('official_key_verified'),'needs_human_review':geo.get('needs_human_review'),'needs_official_key_reconciliation':geo.get('needs_official_key_reconciliation'),'eligible_for_simulation':geo.get('eligible_for_simulation'),'options':geo.get('options')}
 out['stable_ids']={'bank_count':len(bank),'successor_unknown_ids':[x for x in by if x not in bank],'successor_ids_in_bank':sum(1 for x in by if x in bank),'bank_ids_unique':len(bank)==len(set(bank)),'visible_excluded_ids':s.get('selection_excluded_ids'),'visible_ids_not_in_successor':all(x not in by for x in VISIBLE)}
 science=Path(science_path).read_text(); app=Path(app_path).read_text()
 out['regressions']={'science_map_present':all(f'"{x}"' in science for x in RAW),'raw_token_count_in_science_map':sum(1 for x in RAW if f'"{x}"' in science),'global_boilerplate_deletion_absent': 'reviewBoilerplate.fold' not in science and 'replace(Regex("منشأ دام' not in science,'canonical_pair_render_present': all(x in app for x in ('question.stem','pair.leftLabel','pair.rightLabel')),'test_call_sites':app.count('QuestionStemCard(question, compact)')}
 print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__': main(*sys.argv[1:])
