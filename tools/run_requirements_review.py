from __future__ import annotations
import csv,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def rows(rel):
 with (ROOT/rel).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
crit=rows('docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv')
issues=rows('docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv')
reqs=rows('docs/07-assurance/REQUIREMENT_REVIEW_MATRIX.csv')
sprints=rows('docs/07-assurance/SPRINT_GATE_REQUIREMENTS_REVIEW.csv')
if len(issues)!=871: errors.append(f'issues reviewed: {len(issues)}')
if len(reqs)!=376: errors.append(f'requirements reviewed: {len(reqs)}')
if not crit: errors.append('criterion matrix empty')
for r in crit:
 if r['status']!='PASS': errors.append(f"criterion not PASS {r['criterion_id']}")
 if not r['adr_ids']: errors.append(f"criterion without ADR {r['criterion_id']}")
 if r['conflict']!='NONE' or r['redundancy']!='NONE' or r['missing_requirement']!='NO' or r['impossible']!='NO' or r['cycle']!='NO': errors.append(f"open RR defect {r['criterion_id']}")
for r in reqs:
 if r['status']!='PASS' or not r['governing_adrs']: errors.append(f"bad requirement review {r['requirement_id']}")
for p in ROOT.glob('docs/01-product/requirements/REQ-*.md'):
 t=p.read_text(encoding='utf-8')
 if re.search(r'## Requisito\s*\n\s*Requisito verific[aá]vel por',t,re.I): errors.append(f'non-semantic requirement {p.name}')
 if re.search(r'test_dp\d+_decision_\d+',t): errors.append(f'historical test id {p.name}')
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
 o=json.loads(p.read_text())
 if o.get('requirements_review_status')!='PASS': errors.append(f"task RR not pass {p.name}")
 if len(o.get('acceptance_criterion_ids',[]))!=len(o.get('acceptance_criteria',[])): errors.append(f"criterion id count {p.name}")
 if not o.get('governing_adrs'): errors.append(f"task without ADR {p.name}")

for rel in ['docs/01-product/FUNCTIONAL_REQUIREMENTS.md','docs/01-product/NON_FUNCTIONAL_REQUIREMENTS_INDEX.md','docs/01-product/REQUIREMENTS_BASELINE.md']:
 t=(ROOT/rel).read_text(encoding='utf-8')
 if 'Requisito verificável por' in t: errors.append(f'non-semantic aggregate requirement in {rel}')

# Criterion identity and task/matrix correspondence.
criterion_ids=[r['criterion_id'] for r in crit]
if len(criterion_ids)!=len(set(criterion_ids)): errors.append('duplicate criterion IDs')
crit_by_id={r['criterion_id']:r for r in crit}
issue_ids=[r['issue_id'] for r in issues]
if len(issue_ids)!=len(set(issue_ids)): errors.append('duplicate issue review rows')
if any(int(r['criteria_count'])<=0 for r in issues): errors.append('issue without acceptance criteria')
reviewed_issue_ids=set(issue_ids)
for r in crit:
 if r['issue_id'] not in reviewed_issue_ids: errors.append(f"criterion for unreviewed issue {r['criterion_id']}")
 if not r['criterion_text'].strip(): errors.append(f"empty criterion {r['criterion_id']}")
 if r['basis_type'] not in {'DIRECT_REQUIREMENT','ARCHITECTURAL_CONTROL'}: errors.append(f"bad basis {r['criterion_id']}")

# Every TaskEnvelope criterion must match the matrix text, issue and story exactly.
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
 o=json.loads(p.read_text())
 ids=o.get('acceptance_criterion_ids',[]); texts=o.get('acceptance_criteria',[])
 for cid,text in zip(ids,texts):
  row=crit_by_id.get(cid)
  if row is None: errors.append(f"task criterion absent from matrix {p.name}:{cid}"); continue
  if row['issue_id']!=o['issue_id'] or row['story_id']!=o['story_id']: errors.append(f"task criterion ownership mismatch {p.name}:{cid}")
  if row['criterion_text']!=text: errors.append(f"task criterion text mismatch {p.name}:{cid}")

# Requirement IDs and statements must be unique, substantive and traceable.
req_ids=[r['requirement_id'] for r in reqs]
if len(req_ids)!=len(set(req_ids)): errors.append('duplicate requirement review rows')
req_files=list(ROOT.glob('docs/01-product/requirements/REQ-*.md'))
if len(req_files)!=len(reqs): errors.append(f"requirement file/matrix mismatch {len(req_files)}/{len(reqs)}")
for p in req_files:
 t=p.read_text(encoding='utf-8')
 m=re.search(r'## Requisito\s*\n\s*(.+?)(?:\n\n|\n## )',t,re.S|re.I)
 if not m or len(re.sub(r'[`*_#]','',m.group(1)).strip())<35: errors.append(f"insubstantial requirement statement {p.name}")

# Epic graph cycles and sprint-order consistency.
epics={}
for p in ROOT.glob('docs/06-delivery/epics/EPIC-*.md'):
 t=p.read_text(encoding='utf-8'); eid=re.search(r'# (EPIC-\d{3})',t).group(1)
 deps=re.findall(r'EPIC-\d{3}',(re.search(r'^- \*\*Dependências:\*\* (.*)$',t,re.M) or [None,''])[1])
 sprint=int(re.search(r'SPRINT-(\d{3})',t).group(1)); epics[eid]=(deps,sprint)
estate={x:0 for x in epics}
def evisit(n):
 if estate[n]==1:return False
 if estate[n]==2:return True
 estate[n]=1
 for d in epics[n][0]:
  if d not in epics: errors.append(f'missing epic dependency {n}->{d}');continue
  if epics[d][1]>epics[n][1]: errors.append(f'epic dependency reverses sprint {n}->{d}')
  if not evisit(d):return False
 estate[n]=2;return True
if any(estate[n]==0 and not evisit(n) for n in epics): errors.append('epic cycle')

# Cycle checks for stories and epics.
g=json.loads((ROOT/'docs/06-delivery/STORY_DEPENDENCY_GRAPH.json').read_text())
adj={n['id']:[] for n in g['nodes']}
for e in g['edges']: adj[e['from']].append(e['to'])
state={x:0 for x in adj}
def visit(n):
 if state[n]==1:return False
 if state[n]==2:return True
 state[n]=1
 for m in adj[n]:
  if not visit(m):return False
 state[n]=2;return True
if any(state[n]==0 and not visit(n) for n in adj): errors.append('story cycle')
if errors:
 print('REQUIREMENTS REVIEW VALIDATION FAILED')
 for e in errors[:300]:print('-',e)
 sys.exit(1)
print('REQUIREMENTS REVIEW VALIDATION PASS')
print('issues:',len(issues));print('criteria:',len(crit));print('requirements:',len(reqs));print('sprint gates:',len(sprints))
