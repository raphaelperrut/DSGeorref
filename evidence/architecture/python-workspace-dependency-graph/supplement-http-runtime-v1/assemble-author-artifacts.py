"""Assemble author artifacts from frozen delta; no resolution, installs or root edits."""
import hashlib,json,re,subprocess
from pathlib import Path
E=Path('evidence/architecture/python-workspace-dependency-graph')
S=E/'supplement-http-runtime-v1'
D=Path('docs/02-architecture/design-reviews/python-workspace-dependency-graph/supplement-http-runtime-v1')
def write(p,v):
    p.write_text(v,encoding='utf-8',newline='\n')
def dump(p,v): write(p,json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def sha(b): return hashlib.sha256(b).hexdigest()
old=json.loads((E/'resolution-inputs.json').read_text()); delta=json.loads((S/'resolution-delta.json').read_text())
g=json.loads(Path('docs/02-architecture/design-reviews/python-workspace-dependency-graph/approved-dependency-graph.yaml').read_text())
selected=old['selected']|delta['replacements']|delta['additions']
for n in delta['removals']: del selected[n]
groups={k:[r.split('==')[0]+'=='+selected[r.split('==')[0].split('[')[0]] for r in v] for k,v in g['groups'].items()}
groups['runtime']+=['fastapi==0.162.4','uvicorn==0.54.0','pydantic==2.13.4']
groups={k:sorted(v) for k,v in groups.items()}
roots={r.split('==')[0].split('[')[0] for values in groups.values() for r in values}
constraints=[n+'=='+v for n,v in sorted(selected.items()) if n not in roots and n!='psycopg-binary']
changed_constraints=[r for r in constraints if r.split('==')[0] in delta['additions'] or r.split('==')[0] in delta['replacements']]
write(S/'constraints-delta.txt','\n'.join(changed_constraints)+'\n')
proposed=(E/'pyproject-proposed.toml').read_text()
proposed=re.sub(r'^dependencies = .*$', 'dependencies = '+json.dumps(groups['runtime']),proposed,flags=re.M)
for group in ['dev','test']: proposed=re.sub(r'^'+group+r' = .*$',group+' = '+json.dumps(groups[group]),proposed,flags=re.M)
proposed=re.sub(r'^constraint-dependencies = .*$', 'constraint-dependencies = '+json.dumps(constraints),proposed,flags=re.M)
write(S/'supplement-pyproject-proposed.toml',proposed)
inputs=['pyproject.toml','.python-version','requirements-validation.txt','src/backend/dsgeorref/contexts/identity_access/adapters/local_identity/requirements.txt','src/backend/dsgeorref/contexts/identity_access/adapters/local_identity/development_http.py','src/backend/dsgeorref/contexts/identity_access/adapters/local_identity/asgi.py','src/backend/dsgeorref/contexts/identity_access/adapters/local_identity/README.md','docs/03-engineering/TECHNOLOGY_BASELINE.yaml','.github/workflows/ci.yml','.codex/tasks/operations/TASK-0773.json','docs/03-engineering/contexts/engineering_governance/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/dependency-inventory.json']
source=[]
for p in inputs:
    blob=subprocess.check_output(['git','show',delta['baseline_sha']+':'+p]); source.append({'path':p,'sha256':sha(blob),'baseline_sha':delta['baseline_sha']})
dump(S/'source-inputs.json',source)
reconciliation=[]
for line in Path('requirements-validation.txt').read_text().splitlines():
    name,version=line.split('=='); normalized=name.lower().replace('_','-').split('[')[0]
    commit=subprocess.check_output(['git','log',delta['baseline_sha'],'-1','--format=%H','-S'+line,'--','requirements-validation.txt'],text=True).strip()
    reconciliation.append({'name':normalized,'historical_pin':old['selected'][normalized],'current_manifest_pin':version,'proposed_workspace_pin':selected[normalized],'introduction_commit':commit,'story_issue':'No dedicated Story/Issue asserted for dependency-maintenance commits; linked PR authority recorded in rationale.','applicability':'runtime + validation/test' if normalized in ['celery','cryptography','psycopg'] else 'test' if normalized=='pytest' else 'dev'})
dump(S/'pin-reconciliation.json',reconciliation)
python=json.loads((S/'cpython-artifact.json').read_text()); provenance=json.loads((S/'cpython-provenance-verification.json').read_text())
python['cryptographic_provenance_verified']=provenance['exit_code']==0
python['provenance_verification']='gh attestation verify --repo astral-sh/python-build-standalone exited 0; complete verification result and signed bundles captured alongside this record'
dump(S/'cpython-artifact.json',python)
supp={'schema_version':'1.0.0','supplement_version':'http-runtime-v1.0.0','story':'STORY-0768','issue':'ISSUE-0875','status':'AUTHOR_CANDIDATE_PENDING_INDEPENDENT_REVIEW','approval_claimed':False,'owner_authorization':'https://github.com/raphaelperrut/DSGeorref/issues/104#issuecomment-6897551659','historical_graph_sha':delta['historical_graph_sha'],'baseline_sha':delta['baseline_sha'],'historical_manifest_sha256':sha(subprocess.check_output(['git','show',delta['historical_graph_sha']+':'+(E/'digests.json').as_posix()])),'historical_artifact_count_excluding_digest_manifest':55,'composition':'historical selected minus removals, then explicit replacements and additions from resolution-delta.json; historical package metadata reused by reference for unchanged name/version','direct_roots_additional':['fastapi==0.162.4','uvicorn==0.54.0','pydantic==2.13.4'],'pins_reconciled':delta['replacements'],'removals':delta['removals'],'transitive_additions':{n:v for n,v in delta['additions'].items() if n not in roots},'constraints_delta':changed_constraints,'constraints_removed':['tzdata==2026.5'],'groups':groups,'expected_distribution_count':len(selected),'expected_constraint_count':len(constraints),'expected_direct_root_count':len(roots),'pydantic_authority':'TECHNOLOGY_BASELINE.yaml validation family 2.13.x, reference_release 2.13.4; direct import introduced aab71a75b5c76453b1b160153ce770321ddf7f85; FastAPI 0.162.4 Requires-Dist pydantic>=2.9.0; no Conda derivation','python_authority':{'record':str(S/'cpython-artifact.json').replace('\\','/'),'version':'3.12.13','sha256':python['computed_sha256'],'complete':python['cryptographic_provenance_verified']},'applicability':{'runtime':'backend HTTP + migration/worker roots; no optional HTTP/server extras','dev':'current repository validators and typing/lint tools','test':'pytest group; no inference from developer installed packages','platform':'CPython 3.12.13 / Linux amd64 / glibc>=2.28 / standalone prefix /usr/local','excluded':'Conda/native stack, API image/TLS, benchmarks, product changes'},'resolver_inputs_complete':True,'task_0773_executable':False,'independent_review_required':['Arquiteto independente','DevOps','QA','Reviewer']}
dump(D/'supplement.json',supp)
print(json.dumps({'distributions':len(selected),'constraints':len(constraints),'removed':delta['removals'],'new_transitives':supp['transitive_additions']}))
