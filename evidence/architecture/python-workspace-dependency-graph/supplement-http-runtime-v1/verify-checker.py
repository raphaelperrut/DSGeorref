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
# Use frozen package records to exercise the real TOML reader and artifact binding.
old, delta, _ = check.composition()
supplement = check.read(check.D/'supplement.json')
expected, roots = check.verify_project(supplement, old, delta, packages)
_, artifacts = check.verify_closure(supplement, old, delta, packages, expected, roots)

def wheel_record(package):
    file = package['files'][0]
    return {'url':file['url'], 'hash':'sha256:'+file['digests']['sha256']}

fixture = {'package':[
    {'name':name, 'version':package['version'], 'source':{'registry':check.INDEX},
     'wheels':[wheel_record(package)]}
    for name, package in sorted(packages.items())
]}

def validate_fixture(data, path):
    lines = []
    for package in data['package']:
        lines += ['[[package]]', 'name = '+json.dumps(package['name']),
                  'version = '+json.dumps(package['version']),
                  'source = {registry = '+json.dumps(check.INDEX)+'}',
                  'wheels = ['+', '.join(
                      '{url = '+json.dumps(w['url'])+', hash = '+json.dumps(w['hash'])+'}'
                      for w in package['wheels'])+']', '']
    path.write_text('\n'.join(lines), encoding='utf-8')
    check.verify_lock(path, expected, artifacts)

def reject_artifact(label, transform, path):
    data = copy.deepcopy(fixture)
    transform(data['package'])
    try:
        validate_fixture(data, path)
    except AssertionError:
        return {'case':label, 'result':'rejected'}
    raise AssertionError('accepted invalid artifact: '+label)

with tempfile.TemporaryDirectory(prefix='dsgeorref-artifact-check-') as tmp:
    path = Path(tmp)/'artifact-fixture.toml'  # Never generate a workspace uv.lock.
    validate_fixture(fixture, path)
    results.append({'case':'correct frozen artifact identities', 'result':'passed',
                    'distributions':len(expected),
                    'constraints':supplement['expected_constraint_count']})
    results.append(reject_artifact('cross-distribution artifact swap',
        lambda rows: rows[0]['wheels'].__setitem__(0, copy.deepcopy(rows[1]['wheels'][0])), path))
    results.append(reject_artifact('h11 artifact assigned to all distributions',
        lambda rows: [row.update(wheels=[wheel_record(packages['h11'])]) for row in rows], path))
    historical = {p['name']:p for p in old['packages']}
    replaced = next(row['name'] for row in fixture['package']
                    if row['name'] in historical
                    and row['version'] != historical[row['name']]['version'])
    def older_version(rows):
        row = next(row for row in rows if row['name']==replaced)
        row['wheels'] = [wheel_record(historical[replaced])]
    results.append(reject_artifact('same-distribution historical-version artifact swap',
                                   older_version, path))
    results.append(reject_artifact('incorrect artifact hash',
        lambda rows: rows[0]['wheels'][0].update(hash='sha256:'+'0'*64), path))
    results.append(reject_artifact('unknown artifact with otherwise valid hash',
        lambda rows: rows[0]['wheels'][0].update(
            url=rows[0]['wheels'][0]['url']+'.unknown'), path))
print(json.dumps({'checks':results,'approval_claimed':False},indent=2))
