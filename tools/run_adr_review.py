from __future__ import annotations
import csv,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
errors=[]
adr_files=sorted(ROOT.glob('docs/02-architecture/adrs/ADR-*.md'))
ids=[int(re.search(r'ADR-(\d{3})',p.name).group(1)) for p in adr_files]
if ids!=list(range(1,59)): errors.append(f'ADR sequence: {ids[:3]}...{ids[-3:]}')
idx=list(csv.DictReader((ROOT/'docs/00-governance/ADR_INDEX.csv').open(encoding='utf-8-sig')))
if len(idx)!=58: errors.append(f'ADR_INDEX count {len(idx)}')
known={r['adr_id'] for r in idx}
for p in adr_files:
 t=p.read_text(encoding='utf-8')
 for h in ['## Contexto','## Decisão','## Invariantes','## Alternativas consideradas','## Racional da seleção','## Consequências e trade-offs','## Dependências arquiteturais','## Gate de mudança','## Verificação de conformidade','## Rastreabilidade SAR']:
  if h not in t: errors.append(f'{p.name} missing {h}')
 if '**Decisões em aberto:** `Nenhuma`' not in t: errors.append(f'{p.name} open decision')
g=json.loads((ROOT/'docs/02-architecture/ADR_DEPENDENCY_GRAPH.json').read_text())
if len(g['nodes'])!=58 or g.get('cycles')!=0: errors.append('ADR graph count/cycles')
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
 o=json.loads(p.read_text())
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
print(json.dumps({'status':'PASS','adrs':58,'requirements':376,'cycles':0,'open_decisions':0},ensure_ascii=False,indent=2))
