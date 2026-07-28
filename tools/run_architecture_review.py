from __future__ import annotations
import csv, json, re
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
stories=list(csv.DictReader((ROOT/'docs/06-delivery/STORY_INDEX.csv').open(encoding='utf-8-sig')))
tasks=[json.loads(p.read_text()) for p in ROOT.glob('.codex/tasks/TASK-*.json')]
ops=json.loads((ROOT/'contracts/http/OPERATION_CATALOG.json').read_text())['operations']
graph=json.loads((ROOT/'docs/06-delivery/STORY_DEPENDENCY_GRAPH.json').read_text())
audit=json.loads((ROOT/'docs/07-assurance/DEPENDENCY_AUDIT.json').read_text())
findings={
 'provisional_task_scopes':sum(any(re.search(r'/(?:epic|issue|story|task)-',x,re.I) for x in t.get('allow_paths',[]) if x.startswith('src/')) for t in tasks),
 'stories_over_10_requirements':sum(len([x for x in s['requirements'].split('/') if x])>10 for s in stories),
 'generic_command_requests':sum(1 for o in ops if o.get('request_schema')=='CommandRequest'),
 'generic_resource_responses':sum(1 for o in ops if o.get('response_schema')=='ResourceEnvelope'),
 'contracts_not_frozen':sum(o.get('contract_status')!='FROZEN' for o in ops),
 'cycles':audit.get('cycles')
}
report=json.loads((ROOT/'docs/07-assurance/PHASE-A-ARCHITECTURE-REVIEW-REPORT.json').read_text())
failed={k:v for k,v in findings.items() if v not in (0,False)}
if failed:
 print(json.dumps({'status':'FAIL','findings':findings},ensure_ascii=False,indent=2)); raise SystemExit(1)
print(json.dumps({'status':'PASS','architecture_approved':report['architecture_approved'],'phase_b_entry_approved':report['phase_b_entry_approved'],'findings':findings,'stories':len(stories),'edges':len(graph['edges'])},ensure_ascii=False,indent=2))
