from __future__ import annotations
from pathlib import Path
import csv,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def rows(rel):
 with (ROOT/rel).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
stories=rows('docs/06-delivery/STORY_INDEX.csv'); issues=rows('docs/06-delivery/ISSUE_INDEX.csv'); sprints=rows('docs/06-delivery/SPRINT_INDEX.csv'); matrix=rows('docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv')
if len(matrix)!=870:errors.append(f'Phase F matrix expected 870, found {len(matrix)}')
if {r['issue_id'] for r in matrix}!={r['issue_id'] for r in issues}:errors.append('Phase F issue coverage drift')
sc={s:sum(1 for r in stories if r['sprint']==s) for s in {r['sprint'] for r in stories}}
for row in sprints:
 p=ROOT/'docs/06-delivery/sprints'/row['file']; t=p.read_text()
 vals=[int(x) for x in re.findall(r'\*\*Histórias:\*\* `?(\d+)',t)]
 if not vals or any(v!=sc[row['sprint_id']] for v in vals):errors.append(f"{row['sprint_id']}: story count drift")
 if '## Sprint Review — Fase F' not in t:errors.append(f"{row['sprint_id']}: Phase F section absent")
 if not (ROOT/f"docs/07-assurance/phase-f/{row['sprint_id']}-REVIEW.md").exists():errors.append(f"{row['sprint_id']}: detailed report absent")
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
 d=json.loads(p.read_text()); rv=d.get('phase_f_review',{})
 if d.get('sprint_review_status')!='PASS' or d.get('sprint_review_baseline')!='SAR-v2.9-PHASE-F':errors.append(f'{p.name}: Phase F metadata invalid')
 for k in ['dependencies','files','api','database','frontend','geo','ai','tests','artifacts','acceptance_criteria','review']:
  if rv.get(k,{}).get('status')!='PASS':errors.append(f'{p.name}: {k} not PASS')
 if rv.get('api',{}).get('applicability')=='APPLICABLE':
  for ref in ['contracts/http/openapi.yaml','contracts/http/OPERATION_CATALOG.json','contracts/http/API_CONTRACT_INDEX.csv']:
   if ref not in d.get('references',[]):errors.append(f'{p.name}: API contract reference absent {ref}')
 if len(d.get('acceptance_criteria',[]))!=len(d.get('acceptance_criterion_ids',[])):errors.append(f'{p.name}: acceptance mismatch')
for r in matrix:
 if r['overall_status']!='PASS':errors.append(f"{r['issue_id']}: overall not PASS")
report=json.loads((ROOT/'docs/07-assurance/PHASE-F-SPRINT-REVIEW-REPORT.json').read_text())
if report.get('status')!='APPROVED' or report.get('blocking_findings_open')!=0:errors.append('Phase F report not approved')
if errors:
 print('SPRINT REVIEW FAILED');print('\n'.join(errors[:200]));sys.exit(1)
print('SPRINT REVIEW PASS');print('sprints: 12');print('issues: 870');print('stories: 760');print('matrix rows:',len(matrix))
