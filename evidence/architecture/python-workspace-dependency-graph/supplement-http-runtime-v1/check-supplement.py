"""Stdlib checker/composer for the frozen supplement; never resolves or installs."""
import argparse
import hashlib
import html
import json
import re
import subprocess
import tomllib
from pathlib import Path

E = Path('evidence/architecture/python-workspace-dependency-graph')
S = E / 'supplement-http-runtime-v1'
D = Path('docs/02-architecture/design-reviews/python-workspace-dependency-graph/supplement-http-runtime-v1')
INDEX = 'file:///opt/dsgeorref-python-inputs/simple'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def composition():
    old = read(E / 'resolution-inputs.json')
    delta = read(S / 'resolution-delta.json')
    packages = {p['name']: p for p in old['packages']}
    for name in delta['removals']:
        del packages[name]
    packages.update({p['name']: p for p in delta['packages']})
    return old, delta, packages

def composed_files(packages):
    # Preserve unchanged historical metadata blocks and simple pages byte-for-byte.
    historical_config = (E / 'resolver-config.toml').read_text(encoding='utf-8')
    header, *blocks = historical_config.split('[[dependency-metadata]]')
    historical = {tomllib.loads('[[dependency-metadata]]'+b)['dependency-metadata'][0]['name']: b for b in blocks}
    old_names = {p['name']: p['version'] for p in read(E/'resolution-inputs.json')['packages']}
    files = {}
    config = header
    for name, p in sorted(packages.items()):
        if old_names.get(name) == p['version']:
            files[f'simple/{name}/index.html'] = subprocess.check_output(['git','show','cb198c9e8340e0675c36679de426abf922e1c569:'+ (E/'simple'/name/'index.html').as_posix()])
            config += '[[dependency-metadata]]'+historical[name]
        else:
            links = ['<a href="'+html.escape(f['url']+'#sha256='+f['digests']['sha256'], quote=True)+'" data-requires-python="'+html.escape(f['requires_python'] or '', quote=True)+'">'+html.escape(f['filename'])+'</a><br>' for f in p['files']]
            files[f'simple/{name}/index.html'] = ('<!DOCTYPE html>\n<html><body>\n'+'\n'.join(links)+'\n</body></html>\n').encode()
            config += '[[dependency-metadata]]\n'
            for key, value in [('name',name),('version',p['version']),('requires-python',p['requires_python'] or ''),('requires-dist',p['requires_dist']),('provides-extra',p['provides_extra'])]:
                config += key+' = '+json.dumps(value)+'\n'
            config += '\n'
    files['simple/index.html'] = ('<!DOCTYPE html>\n<html><body>\n'+'\n'.join(f'<a href="{n}/">{n}</a><br>' for n in sorted(packages))+'\n</body></html>\n').encode()
    files['resolver-config.toml'] = config.encode()
    return files

def verify_historical(supplement):
    historical = read(E/'digests.json')
    assert len(historical['files']) == 55
    assert digest(subprocess.check_output(['git','show',supplement['historical_graph_sha']+':'+(E/'digests.json').as_posix()])) == supplement['historical_manifest_sha256']
    # The immutable digest manifest is checked separately in addition to its 55 entries.
    for entry in historical['files']+[{'path':(E/'digests.json').as_posix(),'sha256':supplement['historical_manifest_sha256']}]:
        blob = subprocess.check_output(['git','show',supplement['historical_graph_sha']+':'+entry['path']])
        assert digest(blob) == entry['sha256'], entry['path']
        worktree_blob = subprocess.check_output(['git','hash-object','--path='+entry['path'],entry['path']],text=True).strip()
        historical_blob = subprocess.check_output(['git','rev-parse',supplement['historical_graph_sha']+':'+entry['path']],text=True).strip()
        assert worktree_blob == historical_blob, entry['path']
    for entry in read(S/'source-inputs.json'):
        assert digest(subprocess.check_output(['git','show',entry['baseline_sha']+':'+entry['path']])) == entry['sha256']

def verify_project(supplement, old, delta, packages):
    expected = dict(old['selected'])
    for name in delta['removals']: del expected[name]
    expected.update(delta['replacements']); expected.update(delta['additions'])
    assert {n:p['version'] for n,p in packages.items()} == expected
    assert len(expected) == supplement['expected_distribution_count'] == 54
    proposed = tomllib.loads((S/'supplement-pyproject-proposed.toml').read_text())
    groups = supplement['groups']
    assert proposed['project']['dependencies'] == groups['runtime']
    assert proposed['dependency-groups'] == {g:groups[g] for g in ['dev','test']}
    root_names = {r.split('==')[0].split('[')[0] for values in groups.values() for r in values}
    assert len(root_names) == 14
    assert all(expected[r.split('==')[0].split('[')[0]] == r.split('==')[1] for values in groups.values() for r in values)
    constraints = [n+'=='+v for n,v in sorted(expected.items()) if n not in root_names and n!='psycopg-binary']
    assert len(constraints) == supplement['expected_constraint_count'] == 39
    assert proposed['tool']['uv']['constraint-dependencies'] == constraints
    delta_constraints = [r for r in constraints if r.split('==')[0] in delta['additions'] or r.split('==')[0] in delta['replacements']]
    assert (S/'constraints-delta.txt').read_text().splitlines() == delta_constraints == supplement['constraints_delta']
    assert expected['psycopg-binary'] == expected['psycopg'] == '3.3.9'
    assert proposed['project']['requires-python'] == '>=3.12,<3.13'
    assert proposed['tool']['uv']['environments'] == proposed['tool']['uv']['required-environments']
    assert "python_full_version == '3.12.13'" in proposed['tool']['uv']['environments'][0]
    assert proposed['tool']['uv']['default-groups'] == [] and proposed['tool']['uv']['package'] is False
    return expected, root_names

def verify_closure(supplement, old, delta, packages, expected, root_names):
    changed = {p['name'] for p in delta['packages']}
    edges = [e for e in old['active_edges'] if e['parent'] not in changed and e['parent'] in expected]+delta['affected_edges']
    reached = set(root_names)
    while True:
        following = reached | {e['child'] for e in edges if e['parent'] in reached}
        if following == reached: break
        reached = following
    assert reached == set(expected)
    for edge in edges:
        assert edge['parent'] in expected and edge['child'] in expected
        assert edge['requirement'] in packages[edge['parent']]['requires_dist']
    artifacts = {}
    for n,p in packages.items():
        assert p['files'], n
        for f in p['files']:
            assert f['url'].startswith('https://files.pythonhosted.org/') and f['filename'].endswith('.whl')
            assert re.fullmatch('[0-9a-f]{64}', f['digests']['sha256'])
            artifacts[n, p['version'], f['url']] = 'sha256:'+f['digests']['sha256']
    assert all(p.get('license_expression') or p.get('license') for p in delta['packages'])
    config = tomllib.loads(composed_files(packages)['resolver-config.toml'].decode())
    assert {p['name']:p['version'] for p in config['dependency-metadata']} == expected
    assert config['index'] == [{'name':'approved-python-snapshot','url':INDEX,'default':True}]
    assert config['required-version'] == '==0.12.19' and config['no-build'] and config['python-downloads'] == 'never'
    python = read(S/'cpython-artifact.json')
    assert python['computed_sha256'] == supplement['python_authority']['sha256']
    assert python['asset']['digest'] == 'sha256:'+python['computed_sha256']
    assert python['release_immutable'] and python['cryptographic_provenance_verified']
    assert read(S/'cpython-provenance-verification.json')['exit_code'] == 0
    return edges, artifacts

def audit_metadata(delta, packages, expected, edges):
    from packaging.requirements import Requirement
    from packaging.utils import canonicalize_name
    from packaging.version import Version
    active = []
    for n,p in sorted(packages.items()):
        for text in p['requires_dist']:
            req = Requirement(text)
            if req.marker and not any(req.marker.evaluate(delta['environment']|{'extra':x}) for x in (['','binary'] if n=='psycopg' else [''])): continue
            child = canonicalize_name(req.name)
            assert not req.extras and child in expected and Version(expected[child]) in req.specifier, (n,text)
            active.append((n,child,text))
    assert set(active) == {(e['parent'],e['child'],e['requirement']) for e in edges}

def verify_manifest():
    manifest = read(S/'digests.json')
    paths = {p.as_posix() for folder in [S,D] for p in folder.rglob('*') if p.is_file() and p!=S/'digests.json'}
    assert paths == {e['path'] for e in manifest['files']}
    for entry in manifest['files']:
        assert digest(Path(entry['path']).read_bytes().replace(b'\r\n', b'\n')) == entry['sha256'], entry['path']

def verify_lock(lock, expected, artifacts):
    data = tomllib.loads(Path(lock).read_text())
    locked = data['package']
    # uv 0.12.19 includes the local virtual project, outside the 54 externals.
    assert 'dsgeorref' not in expected
    roots = [p for p in locked if p['name'] == 'dsgeorref']
    assert len(roots) == 1, 'expected exactly one virtual project root'
    root = roots[0]
    assert root['version'] == '0.0.0' and root['source'] == {'virtual':'.'}
    assert 'sdist' not in root and 'wheels' not in root
    locked = [p for p in locked if p['name'] != 'dsgeorref']
    assert len(locked) == len(expected) and {p['name']:p['version'] for p in locked} == expected
    for p in locked:
        # Only these two exact spellings identify the approved local registry.
        source = p['source']
        if source == {'registry':'/opt/dsgeorref-python-inputs/simple'}:
            source = {'registry':INDEX}
        assert source == {'registry':INDEX} and not p.get('sdist') and p.get('wheels')
        for wheel in p['wheels']:
            identity = (p['name'], p['version'], wheel['url'])
            assert artifacts.get(identity) == wheel['hash'], identity

def check(verify_digests=True, lock=None, audit=False):
    supplement = read(D/'supplement.json')
    old, delta, packages = composition()
    verify_historical(supplement)
    expected, root_names = verify_project(supplement, old, delta, packages)
    edges, artifacts = verify_closure(supplement, old, delta, packages, expected, root_names)
    if audit:
        audit_metadata(delta, packages, expected, edges)
    if verify_digests:
        verify_manifest()
    if lock:
        verify_lock(lock, expected, artifacts)
    return packages

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit-metadata',action='store_true',help='Author-only full marker/specifier audit using existing packaging; no install')
    parser.add_argument('--check-lock')
    parser.add_argument('--compose',type=Path)
    args = parser.parse_args()
    packages = check(lock=args.check_lock,audit=args.audit_metadata)
    if args.compose:
        assert not args.compose.exists(), 'output must not exist; no overwrite'
        for name,data in composed_files(packages).items():
            target = args.compose/name; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(data)
    print(json.dumps({'structural_integrity':'PASS','distributions':len(packages),'constraints':39,'historical_entries_preserved':55,'approval_claimed':False}))
