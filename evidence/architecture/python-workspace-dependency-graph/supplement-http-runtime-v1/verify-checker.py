"""Meaningful rejection checks of frozen metadata integrity and closure."""
import copy
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('supplement_check', ROOT/'check-supplement.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
original_read = check.read

def reject(label, transform):
    def altered(path):
        value = copy.deepcopy(original_read(path))
        return transform(path, value)
    check.read = altered
    try:
        check.check(verify_digests=False, audit=True)
    except AssertionError:
        return {'case':label,'result':'rejected'}
    finally:
        check.read = original_read
    raise AssertionError('accepted invalid input: '+label)

results=[]
results.append(reject('wrong expected constraint count', lambda p,d: d|{'expected_constraint_count':40} if p.name=='supplement.json' else d))
results.append(reject('unreachable extra distribution', lambda p,d: d|{'additions':d['additions']|{'injected-package':'1.0'}} if p.name=='resolution-delta.json' else d))
results.append(reject('missing active HTTP edge', lambda p,d: d|{'affected_edges':[e for e in d['affected_edges'] if e['child']!='h11']} if p.name=='resolution-delta.json' else d))
def incompatible(path,data):
    if path.name=='resolution-delta.json':
        p=next(p for p in data['packages'] if p['name']=='fastapi')
        p['requires_dist']=[r for r in p['requires_dist'] if not r.startswith('pydantic>=')]+['pydantic>=99']
        data['affected_edges']=[e for e in data['affected_edges'] if not (e['parent']=='fastapi' and e['child']=='pydantic')]+[{'parent':'fastapi','child':'pydantic','requirement':'pydantic>=99'}]
    return data
results.append(reject('declared version conflict', incompatible))
packages=check.check(verify_digests=False,audit=True)
first=check.composed_files(packages); second=check.composed_files(packages)
assert first==second
# Exercise materialization to a temporary directory; never create lock or root files.
with tempfile.TemporaryDirectory(prefix='dsgeorref-compose-check-') as tmp:
    base=Path(tmp)
    for name,data in first.items():
        p=base/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data)
    assert {p.relative_to(base).as_posix():p.read_bytes() for p in base.rglob('*') if p.is_file()}==first
results.append({'case':'repeatable composer and on-disk round trip','result':'passed','composed_files':len(first)})
print(json.dumps({'checks':results,'approval_claimed':False},indent=2))
