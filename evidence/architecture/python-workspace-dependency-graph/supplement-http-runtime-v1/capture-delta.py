import json, urllib.request, hashlib, subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.tags import compatible_tags, cpython_tags
from packaging.utils import canonicalize_name, parse_wheel_filename
from packaging.version import Version
OUT=Path(__file__).resolve().parent
OLD=json.loads((OUT.parent/'resolution-inputs.json').read_text())
ENV=OLD['environment']
BASE='051ed667565bdce1eb22745aee35861a6d4be119'
CUTOFF=datetime.fromisoformat('2026-11-15T03:45:13+00:00')
platforms=[f'manylinux_2_{n}_x86_64' for n in range(28,4,-1)]+['manylinux2014_x86_64','manylinux2010_x86_64','manylinux1_x86_64']
TAGS=set(cpython_tags((3,12),abis=['cp312'],platforms=platforms))|set(compatible_tags((3,12),interpreter='cp312',platforms=platforms))
CACHE={}
def fetch(name,version=None):
    url=f'https://pypi.org/pypi/{name}/'+(f'{version}/' if version else '')+'json'
    if url not in CACHE:
        with urllib.request.urlopen(url,timeout=40) as r: CACHE[url]=json.load(r)
    return CACHE[url]
def wheel_ok(f):
    return (f['packagetype']=='bdist_wheel' and not f.get('yanked') and datetime.fromisoformat(f['upload_time_iso_8601'].replace('Z','+00:00'))<=CUTOFF and (not f.get('requires_python') or Version('3.12.13') in SpecifierSet(f['requires_python'])) and bool(parse_wheel_filename(f['filename'])[3]&TAGS))
PIN=dict(OLD['selected'])
PIN.update({'fastapi':'0.162.4','uvicorn':'0.54.0','pydantic':'2.13.4','celery':'5.7.0','cryptography':'50.0.2','psycopg':'3.3.8','psycopg-binary':'3.3.8','pytest':'9.2.0','ruff':'0.17.4','mypy':'2.4.1'})
HIST={p['name']:p for p in OLD['packages']}
DELTA={}
def metadata(n,v):
    if n in HIST and HIST[n]['version']==v: return HIST[n]
    if (n,v) not in DELTA:
        d=fetch(n,v)
        assert not d['info']['requires_python'] or Version('3.12.13') in SpecifierSet(d['info']['requires_python'])
        files=[{k:f[k] for k in ('filename','url','digests','requires_python','upload_time_iso_8601')} for f in d['urls'] if wheel_ok(f)]
        assert files,(n,v,'no eligible wheel')
        DELTA[n,v]={'name':n,'version':v,'requires_python':d['info']['requires_python'],'requires_dist':d['info']['requires_dist'] or [],'provides_extra':d['info'].get('provides_extra') or [],'license_expression':d['info'].get('license_expression'),'license':d['info'].get('license'),'files':files,'metadata_origin':f'https://pypi.org/pypi/{n}/{v}/json'}
    return DELTA[n,v]
ROOTS={Requirement(r).name.lower().replace('_','-') for group in json.loads(Path('docs/02-architecture/design-reviews/python-workspace-dependency-graph/approved-dependency-graph.yaml').read_text())['groups'].values() for r in group}|{'fastapi','uvicorn','pydantic'}
HARD=ROOTS|{'mako','markupsafe','typing-extensions','psycopg-binary'}
selected=dict(PIN)
for iteration in range(30):
    requirements=defaultdict(list); edges=[]
    for n,v in sorted(selected.items()):
        for value in metadata(n,v)['requires_dist']:
            req=Requirement(value)
            if req.marker and not any(req.marker.evaluate(ENV|{'extra':e}) for e in (['','binary'] if n=='psycopg' else [''])): continue
            assert not req.extras,('nested extra needs authority',value)
            child=canonicalize_name(req.name); requirements[child].append(req.specifier)
            edges.append({'parent':n,'child':child,'requirement':value})
    following={n:PIN[n] for n in sorted(ROOTS)}
    for n,specs in requirements.items():
        if n in PIN and all(Version(PIN[n]) in spec for spec in specs):
            following[n]=PIN[n]; continue
        assert n not in HARD,(n,[str(s) for s in specs])
        candidates=sorted((Version(v) for v,files in fetch(n)['releases'].items() if not Version(v).is_prerelease and not Version(v).is_devrelease and all(Version(v) in s for s in specs) and any(wheel_ok(f) for f in files)),reverse=True)
        assert candidates,n
        following[n]=str(candidates[0]); metadata(n,following[n])
    if following==selected: break
    selected=following
else: raise RuntimeError('closure did not converge')
result={'baseline_sha':BASE,'historical_graph_sha':'cb198c9e8340e0675c36679de426abf922e1c569','cutoff_utc':CUTOFF.isoformat(),'environment':ENV,'selection_policy':'Historical exact pins remain frozen except explicit manifest reconciliations. For new unpinned transitives choose greatest stable compatible wheel release at baseline timestamp; freeze result for independent review, never reselect operationally.','replacements':{n:v for n,v in selected.items() if n in OLD['selected'] and OLD['selected'][n]!=v},'additions':{n:v for n,v in selected.items() if n not in OLD['selected']},'packages':[metadata(n,v) for n,v in sorted(selected.items()) if n not in HIST or HIST[n]['version']!=v],'affected_edges':[e for e in edges if e['parent'] not in HIST or HIST[e['parent']]['version']!=selected[e['parent']]],'removals':sorted(set(OLD['selected'])-set(selected)),'expected_distribution_count':len(selected)}
(OUT/'resolution-delta.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'additions':result['additions'],'replacements':result['replacements'],'count':len(selected)}))
