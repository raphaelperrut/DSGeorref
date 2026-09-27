from __future__ import annotations
import csv,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
errors=[]
TOTAL_ADR_RECORDS=59
ACTIVE_ACCEPTED_ADRS=58
SUPERSEDED_ADRS=1
OPEN_ARCHITECTURAL_DECISIONS=0
PHASE_D_HISTORICAL_ADR_RECORDS=57
adr_files=sorted(ROOT.glob('docs/02-architecture/adrs/ADR-*.md'))
ids=[int(re.search(r'ADR-(\d{3})',p.name).group(1)) for p in adr_files]
if ids!=list(range(1,TOTAL_ADR_RECORDS+1)): errors.append(f'ADR sequence: {ids[:3]}...{ids[-3:]}')
if [adr_id for adr_id in ids if adr_id <= PHASE_D_HISTORICAL_ADR_RECORDS] != list(range(1,PHASE_D_HISTORICAL_ADR_RECORDS+1)): errors.append('Phase D ADR historical baseline drift')
idx=list(csv.DictReader((ROOT/'docs/00-governance/ADR_INDEX.csv').open(encoding='utf-8-sig')))
if len(idx)!=TOTAL_ADR_RECORDS: errors.append(f'ADR_INDEX count {len(idx)}')
known={r['adr_id'] for r in idx}
accepted=sum(r['status']=='Accepted' for r in idx)
superseded=sum(r['status']=='Superseded' for r in idx)
if accepted!=ACTIVE_ACCEPTED_ADRS: errors.append(f'ADR_INDEX Accepted count {accepted}')
if superseded!=SUPERSEDED_ADRS: errors.append(f'ADR_INDEX Superseded count {superseded}')
if next((r['status'] for r in idx if r['adr_id']=='ADR-058'),None)!='Superseded': errors.append('ADR-058 status')
if next((r['status'] for r in idx if r['adr_id']=='ADR-059'),None)!='Accepted': errors.append('ADR-059 status')
for p in adr_files:
 t=p.read_text(encoding='utf-8')
 for h in ['## Contexto','## Decisão','## Invariantes','## Alternativas consideradas','## Racional da seleção','## Consequências e trade-offs','## Dependências arquiteturais','## Gate de mudança','## Verificação de conformidade','## Rastreabilidade SAR']:
  if h not in t: errors.append(f'{p.name} missing {h}')
 if '**Decisões em aberto:** `Nenhuma`' not in t: errors.append(f'{p.name} open decision')
g=json.loads((ROOT/'docs/02-architecture/ADR_DEPENDENCY_GRAPH.json').read_text())
if len(g['nodes'])!=TOTAL_ADR_RECORDS or g.get('cycles')!=0: errors.append('ADR graph count/cycles')
adj={n['id']:[] for n in g['nodes']}
for e in g['edges']:
 if e['from'] not in known or e['to'] not in known: errors.append(f'unknown edge {e}')
 else: adj[e['from']].append(e['to'])
state={x:0 for x in known}
def dfs(n):
 if state[n]==1:return False
 if state[n]==2:return True
 state[n]=1
 for m in adj[n]:
  if not dfs(m):return False
 state[n]=2;return True
if not all(dfs(n) for n in known if state[n]==0): errors.append('ADR cycle')
req=list(csv.DictReader((ROOT/'docs/01-product/REQUIREMENT_INDEX.csv').open(encoding='utf-8-sig')))
if len(req)!=376: errors.append('requirement count')
for r in req:
 if r['owner'] not in known: errors.append(f"{r['requirement_id']} invalid owner {r['owner']}")
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
 o=json.loads(p.read_text(encoding='utf-8'))
 if not o.get('governing_adrs'): errors.append(f'{p.name} missing governing_adrs')
 for a in o.get('governing_adrs',[]):
  if a not in known: errors.append(f'{p.name} invalid {a}')
  expected=next((ROOT/'docs/02-architecture/adrs').glob(a+'-*.md'),None)
  if expected is None: errors.append(f'{p.name} missing file for {a}')
for p in ROOT.rglob('*'):
 if not p.is_file() or p.suffix.lower() not in {'.md','.csv','.json','.yaml','.yml','.txt'}: continue
 if 'PHASE-D-ADR-REVIEW-REPORT' in p.name: continue
 t=p.read_text(encoding='utf-8',errors='ignore')
 for m in re.finditer(r'ADR-(\d{3})',t):
  a='ADR-'+m.group(1)
  if a not in known: errors.append(f'{p.relative_to(ROOT)} references {a}')
if errors:
 print(json.dumps({'status':'FAIL','errors':errors[:200],'error_count':len(errors)},ensure_ascii=False,indent=2));sys.exit(1)
print(json.dumps({
 'status':'PASS',
 'adrs':TOTAL_ADR_RECORDS,
 'total_adr_records':TOTAL_ADR_RECORDS,
 'active_accepted_adrs':ACTIVE_ACCEPTED_ADRS,
 'superseded_adrs':SUPERSEDED_ADRS,
 'phase_d_historical_adr_records':PHASE_D_HISTORICAL_ADR_RECORDS,
 'requirements':376,
 'cycles':0,
 'open_decisions':OPEN_ARCHITECTURAL_DECISIONS,
 'open_architectural_decisions':OPEN_ARCHITECTURAL_DECISIONS
},ensure_ascii=False,indent=2))
