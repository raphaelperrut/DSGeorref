from __future__ import annotations
import csv, json, re, sys, tomllib
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def check_sequence(paths, pattern, prefix, start=1):
    ids=[]; rx=re.compile(pattern)
    for p in paths:
        m=rx.search(p.name)
        if m: ids.append(int(m.group(1)))
    ids=sorted(set(ids)); expected=list(range(start,start+len(ids)))
    if ids!=expected: errors.append(f'{prefix} sequence invalid')
    return len(ids)

counts={
 'adrs':check_sequence(ROOT.glob('docs/02-architecture/adrs/ADR-*.md'),r'ADR-(\d{3})','ADR'),
 'components':check_sequence(ROOT.glob('docs/02-architecture/components/COMP-*.md'),r'COMP-(\d{3})','COMP'),
 'modules':check_sequence(ROOT.glob('docs/02-architecture/modules/MOD-*.md'),r'MOD-(\d{3})','MOD'),
 'sprints':check_sequence(ROOT.glob('docs/06-delivery/sprints/SPRINT-*.md'),r'SPRINT-(\d{3})','SPRINT'),
 'epics':check_sequence(ROOT.glob('docs/06-delivery/epics/EPIC-*.md'),r'EPIC-(\d{3})','EPIC'),
 'parent_issues':check_sequence(ROOT.glob('docs/06-delivery/issues/ISSUE-*.md'),r'ISSUE-(\d{4})','ISSUE'),
 'stories':check_sequence(ROOT.glob('docs/06-delivery/stories/STORY-*.md'),r'STORY-(\d{4})','STORY'),
 'tasks':check_sequence(ROOT.glob('.codex/tasks/TASK-*.json'),r'TASK-(\d{4})','TASK'),
 'requirements':len(list(ROOT.glob('docs/01-product/requirements/REQ-*.md'))),
}
expected={'adrs':58,'components':18,'modules':18,'sprints':12,'epics':110,'parent_issues':110,'stories':760,'tasks':760,'requirements':376}
for k,v in expected.items():
    if counts[k]!=v: errors.append(f'{k}: expected {v}, found {counts[k]}')


# Phase D definitive ADR inventory.
phase_d_required=['docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.md','docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.json','docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv','docs/02-architecture/ADR_DEPENDENCY_GRAPH.json','docs/02-architecture/sar/SAR-180-PHASE-D-ADR-DEFINITIVO.md']
for rel in phase_d_required:
    if not (ROOT/rel).exists(): errors.append(f'missing Phase D artifact {rel}')
if counts.get('adrs') != 58: errors.append('Phase D ADR count drift')

# JSON/YAML syntax.
for p in ROOT.rglob('*.json'):
    try: json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'invalid JSON {p.relative_to(ROOT)}: {e}')
for p in list(ROOT.rglob('*.yaml'))+list(ROOT.rglob('*.yml')):
    try: yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'invalid YAML {p.relative_to(ROOT)}: {e}')

# Task schema validation.
schema=json.loads((ROOT/'.codex/tasks/TASK_ENVELOPE.schema.json').read_text(encoding="utf-8"))
validator=Draft202012Validator(schema)
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
    obj = json.loads(p.read_text(encoding="utf-8"))
    for e in validator.iter_errors(obj): errors.append(f'{p.name}: {e.message}')

# Story dependency graph references and cycles.
graph=json.loads((ROOT/'docs/06-delivery/STORY_DEPENDENCY_GRAPH.json').read_text(encoding="utf-8"))
node_ids={n['id'] for n in graph['nodes']}
adj={n:set() for n in node_ids}
for e in graph['edges']:
    if e['from'] not in node_ids or e['to'] not in node_ids: errors.append(f'bad story edge {e}')
    else: adj[e['from']].add(e['to'])
state={n:0 for n in node_ids}
def visit(n):
    if state[n]==1: return False
    if state[n]==2: return True
    state[n]=1
    for m in adj[n]:
        if not visit(m): return False
    state[n]=2; return True
for n in node_ids:
    if state[n]==0 and not visit(n): errors.append('story dependency cycle detected'); break

# Index counts and traceability.
def rows(path):
    with (ROOT/path).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
issue_rows=rows('docs/06-delivery/ISSUE_INDEX.csv')
story_rows=rows('docs/06-delivery/STORY_INDEX.csv')
req_rows=rows('docs/01-product/REQUIREMENT_INDEX.csv')
trace_rows=rows('docs/06-delivery/TRACEABILITY_MATRIX.csv')
if len(issue_rows)!=870: errors.append(f'ISSUE_INDEX expected 870, found {len(issue_rows)}')
if len(story_rows)!=760: errors.append(f'STORY_INDEX expected 760, found {len(story_rows)}')
if len(req_rows)!=376: errors.append(f'REQUIREMENT_INDEX expected 376, found {len(req_rows)}')
if len(trace_rows)!=376: errors.append(f'TRACEABILITY expected 376, found {len(trace_rows)}')
if any(not r['stories'] for r in trace_rows): errors.append('active requirement without story coverage')

story_by_id={r['story_id']:r for r in story_rows}
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
    obj=json.loads(p.read_text(encoding="utf-8"))
    row=story_by_id.get(obj.get('story_id'))
    if not row: errors.append(f'{p.name}: story absent from index'); continue
    for key in ['issue_id','task_id','epic_id']:
        if obj.get(key)!=row.get(key): errors.append(f'{p.name}: {key} differs from STORY_INDEX')
    if obj.get('sprint_id')!=row.get('sprint'): errors.append(f'{p.name}: sprint differs from STORY_INDEX')
    for ref in obj.get('references',[]):
        if not (ROOT/ref).exists(): errors.append(f'{p.name}: missing reference {ref}')

# Markdown relative links.
for p in ROOT.rglob('*.md'):
    text=p.read_text(encoding='utf-8',errors='ignore')
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
        if target.startswith(('http://','https://','#','mailto:')): continue
        t=target.split('#')[0]
        if t and not (p.parent/t).resolve().exists(): errors.append(f'broken link {p.relative_to(ROOT)} -> {target}')

# No obsolete project-history IDs/artifacts in active tree.
forbidden_names={'CHANGELOG.md','DECISION_LOG.md','DECISION_PACKAGE_HISTORY.csv','LEGACY_ADR_CONSOLIDATION_MAP.csv','BROWNFIELD_ADOPTION_REGISTER.md','IMPLEMENTATION_ISSUE_CATALOG.md'}
for p in ROOT.rglob('*'):
    if p.name in forbidden_names: errors.append(f'forbidden artifact: {p.relative_to(ROOT)}')
    if p.is_file() and p.suffix.lower() in {'.md','.csv','.json','.yaml','.yml','.txt'}:
        text=p.read_text(encoding='utf-8',errors='ignore')
        if re.search(r'\bDP-\d{3}\b',text): errors.append(f'obsolete decision ID in {p.relative_to(ROOT)}')
        if re.search(r'(?<![A-Z0-9-])(?:FND|PLT|DAT|JOB|CLI|GEO|WEB|REV|EDU|REP|OPS|SEC|PUB|REL|LAB)-\d{3}(?![A-Z0-9-])',text): errors.append(f'obsolete work-package ID in {p.relative_to(ROOT)}')



# SAR completeness and technology closure.
required_sar = [
 'docs/02-architecture/sar/SAR-000-START-HERE.md',
 'docs/02-architecture/sar/SAR-010-SYSTEM-CONTEXT.md',
 'docs/02-architecture/sar/SAR-030-QUALITY-ATTRIBUTE-SCENARIOS.md',
 'docs/02-architecture/sar/SAR-070-CONTRACT-VIEW.md',
 'docs/02-architecture/sar/SAR-130-TRACEABILITY-AND-CONSISTENCY.md',
 'docs/02-architecture/sar/SAR-140-IMPLEMENTATION-GUARDRAILS.md',
 'docs/02-architecture/sar/SAR-150-PHASE-A-ARCHITECTURE-REVIEW.md',
 'docs/03-engineering/TECHNOLOGY_BASELINE.yaml',
 'docs/03-engineering/TECHNOLOGY_VERIFICATION.md',
 'docs/03-engineering/PYTHON_312_RUNTIME_POLICY.md',
 'docs/03-engineering/PYTHON_CODE_ARCHITECTURE_STANDARD.md',
 'contracts/architecture/python-module-boundaries.yaml',
 'docs/07-assurance/PHASE-A-ARCHITECTURE-REVIEW-REPORT.json',
 'docs/07-assurance/DEPENDENCY_AUDIT.json',
 'docs/07-assurance/PHASE-F-SPRINT-REVIEW-REPORT.json',
 'docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv',
 'docs/02-architecture/sar/SAR-200-PHASE-F-SPRINT-REVIEW.md',
]
for rel in required_sar:
    if not (ROOT/rel).exists(): errors.append(f'missing SAR artifact {rel}')

tech = yaml.safe_load((ROOT/'docs/03-engineering/TECHNOLOGY_BASELINE.yaml').read_text(encoding="utf-8"))
if tech.get('status') != 'APPROVED_FOR_IMPLEMENTATION': errors.append('technology baseline not approved')
if tech.get('execution_authorization') != 'BLOCKED_EXTERNAL': errors.append('technology execution authorization drift')
if not tech.get('official_verification',{}).get('path'): errors.append('technology verification evidence absent')
if not tech.get('decisions'): errors.append('technology baseline empty')
for d in tech.get('decisions',[]):
    if not all(d.get(k) for k in ['area','technology','version_family','decision','exact_pin']):
        errors.append(f'incomplete technology decision {d}')
areas={d.get('area') for d in tech.get('decisions',[])}
if 'frontend-types-compat' not in areas: errors.append('TypeScript 7 compatibility lane absent')
if 'language-backend-compat-313' not in areas: errors.append('Python 3.13 future compatibility lane absent')
if 'language-backend-compat-314' not in areas: errors.append('Python 3.14 future integration target absent')
python_primary=next((d for d in tech.get('decisions',[]) if d.get('area')=='language-backend'),{})
if python_primary.get('version_family') != '3.12.13': errors.append('Python 3.12.13 is not the primary runtime')
react=next((d for d in tech.get('decisions',[]) if d.get('area')=='frontend-ui'),{})
if react.get('minimum_safe_patch') != '19.2.4': errors.append('React security floor absent')
local_dev=(ROOT/'docs/03-engineering/LOCAL_DEVELOPMENT.md').read_text(encoding='utf-8')
if 'Python 3.12 como runtime primário' not in local_dev: errors.append('local development Python 3.12 primary runtime absent')
if 'Python 3.13 como lane futura não bloqueante' not in local_dev: errors.append('local development Python 3.13 future lane absent')
if 'Python 3.14 como alvo de integração posterior' not in local_dev: errors.append('local development Python 3.14 future target absent')
if 'TypeScript 7.0 em lane obrigatória' not in local_dev: errors.append('local development TypeScript compatibility lane absent')


# Python 3.12 configuration and Phase A review.
if (ROOT/'.python-version').read_text(encoding='utf-8').strip() != '3.12.13': errors.append('.python-version must select 3.12.13')
pyproject=tomllib.loads((ROOT/'pyproject.toml').read_text(encoding='utf-8'))
if pyproject.get('project',{}).get('requires-python') != '>=3.12,<3.13': errors.append('pyproject requires-python drift')
if pyproject.get('tool',{}).get('ruff',{}).get('target-version') != 'py312': errors.append('Ruff target must be py312')
if pyproject.get('tool',{}).get('mypy',{}).get('python_version') != '3.12': errors.append('mypy Python version must be 3.12')
ar=json.loads((ROOT/'docs/07-assurance/PHASE-A-ARCHITECTURE-REVIEW-REPORT.json').read_text(encoding="utf-8"))
if ar.get('architecture_approved') is not True: errors.append('Phase A architecture review not approved')
if ar.get('runtime',{}).get('primary') != 'CPython 3.12.13': errors.append('Phase A runtime drift')
if ar.get('implementation_readiness') not in {'READY','CONDITIONAL','READY_FOR_PHASE_B'}: errors.append('invalid implementation readiness state')

# No unresolved legacy issue IDs or empty required sections.
for p in ROOT.rglob('*'):
    if 'exports' in p.parts or p.name in {'manifest.json','SHA256SUMS.txt','VALIDATION_RESULT.txt'}: continue
    if p.is_file() and p.suffix.lower() in {'.md','.csv','.json','.yaml','.yml','.txt'}:
        t=p.read_text(encoding='utf-8',errors='ignore')
        if re.search(r'\bIS-\d{3}\b',t): errors.append(f'obsolete IS id in {p.relative_to(ROOT)}')
        if re.search(r'\b(TBD|TODO|FIXME)\b',t): errors.append(f'placeholder in {p.relative_to(ROOT)}')
        if 'conhecimento técnico de referência' in t: errors.append(f'generated semantic defect in {p.relative_to(ROOT)}')
        if 'Python 3.13 como runtime primário' in t: errors.append(f'Python runtime drift in {p.relative_to(ROOT)}')

for p in ROOT.glob('docs/02-architecture/modules/MOD-*.md'):
    t=p.read_text(encoding='utf-8')
    m=re.search(r'## Boundaries\s*(.*?)(?=\n## |\Z)',t,re.S)
    if not m or len(m.group(1).strip()) < 100: errors.append(f'incomplete module boundary {p.name}')

for p in ROOT.glob('docs/02-architecture/adrs/ADR-*.md'):
    t=p.read_text(encoding='utf-8')
    for h in ['## Alternativas consideradas','## Racional da seleção','## Verificação de conformidade','## Rastreabilidade SAR']:
        if h not in t: errors.append(f'{p.name}: missing {h}')

opcat=json.loads((ROOT/'contracts/http/OPERATION_CATALOG.json').read_text(encoding="utf-8"))
openapi=yaml.safe_load((ROOT/'contracts/http/openapi.yaml').read_text(encoding="utf-8"))
actual={(m.upper(),path) for path,item in openapi['paths'].items() for m in item if m.lower() in {'get','post','put','patch','delete'}}
expected_ops={(o['method'].upper(),o['path']) for o in json.loads((ROOT/'contracts/http/OPERATION_CATALOG.json').read_text(encoding="utf-8"))['operations']}
if actual != expected_ops: errors.append(f'OpenAPI operation catalog drift: expected {len(expected_ops)}, actual {len(actual)}')

for p in ROOT.glob('docs/06-delivery/stories/STORY-*.md'):
    if '## Revisão SAR' not in p.read_text(encoding='utf-8'): errors.append(f'missing SAR review {p.name}')
for p in ROOT.glob('docs/06-delivery/issues/ISSUE-*.md'):
    if '## Revisão SAR do envelope' not in p.read_text(encoding='utf-8'): errors.append(f'missing SAR issue review {p.name}')
for p in ROOT.glob('docs/06-delivery/sprints/SPRINT-*.md'):
    if '## Revisão SAR da sprint' not in p.read_text(encoding='utf-8'): errors.append(f'missing SAR sprint review {p.name}')
    if '## Sprint Review — Fase F' not in p.read_text(encoding='utf-8'): errors.append(f'missing Phase F sprint review {p.name}')



# Definition of Ready guards introduced by Phase A.
story_status={r['story_id']:r.get('status','').lower() for r in story_rows}
story_req_count={r['story_id']:len([x for x in r.get('requirements','').split('/') if x]) for r in story_rows}
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
    obj=json.loads(p.read_text(encoding="utf-8"))
    status=story_status.get(obj['story_id'],'')
    if status == 'ready':
        if story_req_count.get(obj['story_id'],0) > 20:
            errors.append(f"{obj['story_id']}: Ready story has more than 20 requirements")
        if any(path.startswith('src/') and ('/epic-' in path or '/issue-' in path) for path in obj.get('allow_paths',[])):
            errors.append(f"{obj['story_id']}: Ready story has backlog-oriented source path")

# The Phase A report must account for current contract and task refinements.
def generic_http_counts(spec):
    req=resp=0
    for item in spec.get('paths',{}).values():
        for method,op in item.items():
            if method.lower() not in {'get','post','put','patch','delete'}: continue
            schema=op.get('requestBody',{}).get('content',{}).get('application/json',{}).get('schema',{})
            if schema.get('$ref','').endswith('/CommandRequest'): req+=1
            refs=[]
            for response in op.get('responses',{}).values():
                if isinstance(response,dict):
                    r=response.get('content',{}).get('application/json',{}).get('schema',{}).get('$ref','')
                    refs.append(r)
            if any(r.endswith('/ResourceEnvelope') for r in refs): resp+=1
    return req,resp
generic_req,generic_resp=generic_http_counts(openapi)
if generic_req != 0: errors.append('Phase A generic request count drift')
if generic_resp != 0: errors.append('Phase A generic response count drift')

# Portfolio and hard-dependency consistency.
epic_rows=rows('docs/06-delivery/EPIC_INDEX.csv')
if len(epic_rows)!=110: errors.append(f'EPIC_INDEX expected 110, found {len(epic_rows)}')
node_meta={n['id']:n for n in graph['nodes']}
graph_deps={n:set() for n in node_ids}
for e in graph['edges']:
    if e['to'] in graph_deps: graph_deps[e['to']].add(e['from'])
    if e['from'] in node_meta and e['to'] in node_meta:
        src=int(node_meta[e['from']]['sprint'].split('-')[1])
        dst=int(node_meta[e['to']]['sprint'].split('-')[1])
        if src>dst: errors.append(f'hard dependency reverses sprint order: {e}')
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
    obj=json.loads(p.read_text(encoding="utf-8"))
    if set(obj.get('dependencies',[])) != graph_deps.get(obj['story_id'],set()):
        errors.append(f'{p.name}: task dependencies differ from hard dependency graph')
for p in ROOT.glob('docs/06-delivery/epics/EPIC-*.md'):
    t=p.read_text(encoding='utf-8')
    if 'To be linked during story refinement' in t: errors.append(f'unlinked epic requirements in {p.name}')
    if 'Associado pelos requisitos e ADR owner' in t: errors.append(f'generic release gate in {p.name}')
    if 'Definidas pelos contratos aplicáveis de produto e componente' in t: errors.append(f'generic architecture references in {p.name}')
    reqline=re.search(r'^- Requisitos: (.*)$',t,re.M)
    if reqline and ('…' in reqline.group(1) or '...' in reqline.group(1)): errors.append(f'truncated requirement list in {p.name}')
for p in ROOT.glob('docs/02-architecture/adrs/ADR-*.md'):
    t=p.read_text(encoding='utf-8')
    if '**Decisões em aberto:** `Nenhuma`' not in t: errors.append(f'open architecture decision in {p.name}')


# Phase A closure gates.
openapi_text=(ROOT/'contracts/http/openapi.yaml').read_text(encoding='utf-8')
if 'CommandRequest' in openapi_text or 'ResourceEnvelope' in openapi_text: errors.append('generic HTTP envelope remains')
opcat=json.loads((ROOT/'contracts/http/OPERATION_CATALOG.json').read_text(encoding="utf-8"))['operations']
if len(opcat)!=56 or any(o.get('contract_status')!='FROZEN' or not o.get('specific_contract') or not o.get('permission') or not o.get('error_codes') for o in opcat): errors.append('HTTP contract freeze incomplete')
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
    obj=json.loads(p.read_text(encoding="utf-8"))
    if any(re.search(r'/(?:epic|issue|story|task)-',x,re.I) for x in obj.get('allow_paths',[]) if x.startswith('src/')): errors.append(f'{p.name}: transient production scope')
for r in story_rows:
    reqs=[x for x in r.get('requirements','').split('/') if x]
    if len(reqs)>10: errors.append(f"{r['story_id']}: more than 10 requirements")
for n in range(19,26):
    if not list(ROOT.glob(f'docs/02-architecture/adrs/ADR-{n:03d}-*.md')): errors.append(f'ADR-{n:03d} missing')
if python_primary.get('version_family') != '3.12.13': errors.append('Python exact patch is not 3.12.13')
if ar.get('open_actions'): errors.append('Phase A still has open actions')
if ar.get('phase_b_entry_approved') is not True: errors.append('Phase B entry not approved')



# Phase B Requirements Review closure.
required_phase_b = [
 'docs/06-delivery/PHASE-B-REQUIREMENTS-REVIEW-CHARTER.md',
 'docs/07-assurance/PHASE-B-REQUIREMENTS-REVIEW-REPORT.md',
 'docs/07-assurance/PHASE-B-REQUIREMENTS-REVIEW-REPORT.json',
 'docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv',
 'docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv',
 'docs/07-assurance/REQUIREMENT_REVIEW_MATRIX.csv',
 'docs/07-assurance/SPRINT_GATE_REQUIREMENTS_REVIEW.csv',
 'docs/02-architecture/sar/SAR-160-PHASE-B-REQUIREMENTS-REVIEW.md',
 'tools/run_requirements_review.py',
]
for rel in required_phase_b:
    if not (ROOT/rel).exists(): errors.append(f'missing Phase B artifact {rel}')
rr=json.loads((ROOT/'docs/07-assurance/PHASE-B-REQUIREMENTS-REVIEW-REPORT.json').read_text(encoding="utf-8"))
if rr.get('approved') is not True or rr.get('blocking_findings_open') != 0: errors.append('Phase B not approved')
crit_rows=rows('docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv')
issue_rr_rows=rows('docs/07-assurance/ISSUE_REQUIREMENTS_REVIEW.csv')
req_rr_rows=rows('docs/07-assurance/REQUIREMENT_REVIEW_MATRIX.csv')
if len(issue_rr_rows)!=870: errors.append(f'Phase B issue review expected 870, found {len(issue_rr_rows)}')
if len(req_rr_rows)!=376: errors.append(f'Phase B requirement review expected 376, found {len(req_rr_rows)}')
for r in crit_rows:
    if r.get('status')!='PASS' or not r.get('adr_ids'): errors.append(f"bad criterion review {r.get('criterion_id')}")
for p in ROOT.glob('docs/01-product/requirements/REQ-*.md'):
    t=p.read_text(encoding='utf-8')
    if re.search(r'## Requisito\s*\n\s*Requisito verific[aá]vel por',t,re.I): errors.append(f'non-semantic requirement {p.name}')
    if re.search(r'test_dp\d+_decision_\d+',t): errors.append(f'historical test id {p.name}')
for rel in ['docs/01-product/FUNCTIONAL_REQUIREMENTS.md','docs/01-product/NON_FUNCTIONAL_REQUIREMENTS_INDEX.md','docs/01-product/REQUIREMENTS_BASELINE.md']:
    t=(ROOT/rel).read_text(encoding='utf-8')
    if 'Requisito verificável por' in t: errors.append(f'non-semantic aggregate requirement in {rel}')
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
    o=json.loads(p.read_text(encoding="utf-8"))
    if o.get('requirements_review_status')!='PASS': errors.append(f'{p.name}: Phase B not PASS')
    if len(o.get('acceptance_criterion_ids',[])) != len(o.get('acceptance_criteria',[])): errors.append(f'{p.name}: criterion ID mismatch')
for p in ROOT.glob('docs/06-delivery/sprints/SPRINT-*.md'):
    t=p.read_text(encoding='utf-8')
    if 'ADRs 001–058 aceitas' not in t: errors.append(f'{p.name}: stale ADR baseline')
    if '## Requirements Review — Fase B' not in t: errors.append(f'{p.name}: missing Phase B review')


# Phase C Domain-Driven Design closure.
required_phase_c=[
 'docs/06-delivery/PHASE-C-DOMAIN-DRIVEN-DESIGN-CHARTER.md',
 'docs/07-assurance/PHASE-C-DOMAIN-DRIVEN-DESIGN-REPORT.md',
 'docs/07-assurance/PHASE-C-DOMAIN-DRIVEN-DESIGN-REPORT.json',
 'docs/02-architecture/ddd/BOUNDED_CONTEXT_INDEX.csv',
 'docs/02-architecture/ddd/CONTEXT_MAP.csv',
 'contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv',
 'docs/02-architecture/sar/SAR-170-PHASE-C-DOMAIN-DRIVEN-DESIGN.md',
 'tools/run_domain_driven_design_review.py',
]
for rel in required_phase_c:
    if not (ROOT/rel).exists(): errors.append(f'missing Phase C artifact {rel}')
phase_c=json.loads((ROOT/'docs/07-assurance/PHASE-C-DOMAIN-DRIVEN-DESIGN-REPORT.json').read_text(encoding="utf-8"))
if phase_c.get('approved') is not True or phase_c.get('blocking_findings_open') != 0: errors.append('Phase C not approved')
ctx_rows=rows('docs/02-architecture/ddd/BOUNDED_CONTEXT_INDEX.csv')
if len(ctx_rows)!=16: errors.append(f'expected 16 bounded contexts, found {len(ctx_rows)}')
ctx_ids={r['context_id'] for r in ctx_rows}
for r in epic_rows:
    if r.get('bounded_context') not in ctx_ids: errors.append(f"{r['epic_id']}: bounded context absent")
for r in story_rows:
    if r.get('bounded_context') not in ctx_ids or r.get('ddd_status')!='PASS': errors.append(f"{r['story_id']}: DDD ownership invalid")
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
    o=json.loads(p.read_text(encoding="utf-8"))
    if o.get('bounded_context') not in ctx_ids or o.get('ddd_review_status')!='PASS': errors.append(f'{p.name}: DDD task metadata invalid')
    if any(re.match(r'src/backend/dsgeorref/(?:domain|application|adapters)/',x) for x in o.get('allow_paths',[])): errors.append(f'{p.name}: global backend layer path')


# Phase E executable specifications closure.
required_phase_e=[
 'docs/02-architecture/specifications/SPEC-000-SPECIFICATION-FRAMEWORK.md',
 'docs/02-architecture/specifications/SPEC-001-PROMPT-BUNDLE-CONTRACT.md',
 'docs/02-architecture/specifications/SPEC-002-EDIT-CASE-REGISTRY-CONTRACT.md',
 'docs/02-architecture/specifications/SPEC-003-AI-BACKEND-PROTOCOL-CONTRACT.md',
 'docs/02-architecture/specifications/SPEC-004-TEMPLATE-CONTRACT.md',
 'docs/02-architecture/specifications/SPEC-005-ARTIFACT-CONTRACT.md',
 'docs/07-assurance/PHASE-E-SPECIFICATION-REVIEW-REPORT.md',
 'docs/07-assurance/PHASE-E-SPECIFICATION-REVIEW-REPORT.json',
 'docs/07-assurance/SPECIFICATION_APPLICABILITY_MATRIX.csv',
 'docs/07-assurance/SPECIFICATION_CONFORMANCE_MATRIX.csv',
 'tools/run_specification_review.py',
]
for rel in required_phase_e:
    if not (ROOT/rel).exists(): errors.append(f'missing Phase E artifact {rel}')
if len(list(ROOT.glob('docs/02-architecture/specifications/SPEC-00[1-5]-*.md'))) != 5: errors.append('Phase E specification count drift')
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
    o=json.loads(p.read_text(encoding="utf-8"))
    if o.get('specification_review_status')!='PASS': errors.append(f'{p.name}: specification review not PASS')
    if o.get('specification_baseline')!='SAR-v2.9-PHASE-F': errors.append(f'{p.name}: specification baseline drift')
    if o.get('adr_baseline')!='SAR-v2.9-PHASE-F': errors.append(f'{p.name}: ADR baseline drift after Phase E')
    if len(o.get('applicable_specifications',[])) < 2: errors.append(f'{p.name}: missing specification applicability')
phase_e_report_path=ROOT/'docs/07-assurance/PHASE-E-SPECIFICATION-REVIEW-REPORT.json'
if phase_e_report_path.exists():
    pe=json.loads(phase_e_report_path.read_text(encoding="utf-8"))
    if pe.get('approved') is not True or pe.get('blocking_findings_open') != 0: errors.append('Phase E not approved')

# Phase F sprint-by-sprint review.
phase_f=json.loads((ROOT/'docs/07-assurance/PHASE-F-SPRINT-REVIEW-REPORT.json').read_text(encoding="utf-8"))
if phase_f.get('status')!='APPROVED' or phase_f.get('blocking_findings_open')!=0: errors.append('Phase F review not approved')
phase_f_rows=rows('docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv')
if len(phase_f_rows)!=870: errors.append(f'Phase F matrix expected 870, found {len(phase_f_rows)}')
if {r['issue_id'] for r in phase_f_rows}!={r['issue_id'] for r in issue_rows}: errors.append('Phase F issue coverage drift')
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
    o=json.loads(p.read_text(encoding="utf-8")); rv=o.get('phase_f_review',{})
    if o.get('sprint_review_status')!='PASS' or o.get('sprint_review_baseline')!='SAR-v2.9-PHASE-F': errors.append(f'{p.name}: Phase F metadata invalid')
    for k in ['dependencies','files','api','database','frontend','geo','ai','tests','artifacts','acceptance_criteria','review']:
        if rv.get(k,{}).get('status')!='PASS': errors.append(f'{p.name}: Phase F {k} not PASS')
for s in rows('docs/06-delivery/SPRINT_INDEX.csv'):
    actual=sum(1 for r in story_rows if r['sprint']==s['sprint_id'])
    text=(ROOT/'docs/06-delivery/sprints'/s['file']).read_text(encoding="utf-8")
    vals=[int(x) for x in re.findall(r'\*\*Histórias:\*\* `?(\d+)',text)]
    if not vals or any(v!=actual for v in vals): errors.append(f"{s['sprint_id']}: Phase F story count drift")



# Phase G CTO review.
phase_g=json.loads((ROOT/'docs/07-assurance/PHASE-G-CTO-REVIEW-REPORT.json').read_text(encoding="utf-8"))
if phase_g.get('status')!='APPROVED' or phase_g.get('blocking_findings_open')!=0: errors.append('Phase G not approved')
phase_g_rows=rows('docs/07-assurance/PHASE-G-ISSUE-INVESTMENT-REVIEW.csv')
if len(phase_g_rows)!=870: errors.append(f'Phase G matrix expected 870, found {len(phase_g_rows)}')
for p in ROOT.glob('.codex/tasks/TASK-*.json'):
    o=json.loads(p.read_text(encoding="utf-8"))
    if o.get('cto_review_status')!='PASS' or o.get('cto_review_baseline')!='SAR-v3.0-PHASE-G': errors.append(f'{p.name}: Phase G metadata invalid')

if errors:
    print('VALIDATION FAILED')
    for e in errors[:300]: print('-',e)
    sys.exit(1)
print('VALIDATION PASS')
for k,v in counts.items(): print(f'{k}: {v}')
print(f"issues total: {len(issue_rows)}")
