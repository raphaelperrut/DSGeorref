"""Read-only authority/runtime preflight; writes only this run's evidence JSON."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import tomllib

BASE = 'ee0841d54d9bc1472ebbaa2b12dd1720d0aa9819'
AUTHORITY = 'cb198c9e8340e0675c36679de426abf922e1c569'
SOURCE_BASE = '926a6a8c9a69a838b165cca9df6c4ebb9c03c8d6'
EVIDENCE = pathlib.Path(__file__).resolve().parent
COMMANDS = []


def command(argv):
    result = subprocess.run(argv, capture_output=True, check=False)
    COMMANDS.append({'argv': argv, 'exit_code': result.returncode,
                     'stdout': result.stdout.decode('utf-8', errors='replace'),
                     'stderr': result.stderr.decode('utf-8', errors='replace')})
    return result


def git(*args):
    result = command(['git', *args])
    assert result.returncode == 0, COMMANDS[-1]
    return result.stdout


def blob(ref, path):
    return git('show', f'{ref}:{path}')


def digest(data):
    return hashlib.sha256(data).hexdigest()


assert git('rev-parse', 'HEAD').decode().strip() == BASE
branch = git('branch', '--show-current').decode().strip()
assert branch == 'codex/issue-0875-task-0773-python-workspace-lock'
initial_status = git('status', '--porcelain').decode()
assert all(line[3:].startswith('evidence/operations/python-workspace-lock/')
           for line in initial_status.splitlines()), initial_status
manifest_path = 'evidence/architecture/python-workspace-dependency-graph/digests.json'
manifest_bytes = blob(AUTHORITY, manifest_path)
assert manifest_bytes == blob(BASE, manifest_path)
manifest = json.loads(manifest_bytes)
authority_checks = []
for entry in manifest['files']:
    authority_bytes = blob(AUTHORITY, entry['path'])
    check = dict(entry)
    check.update(actual_sha256=digest(authority_bytes), actual_bytes=len(authority_bytes),
                 base_blob_identical=authority_bytes == blob(BASE, entry['path']))
    assert check['actual_sha256'] == entry['sha256']
    assert check['actual_bytes'] == entry['bytes']
    assert check['base_blob_identical']
    authority_checks.append(check)
import jsonschema
jsonschema.validate(json.loads(blob(BASE, '.codex/tasks/operations/TASK-0773.json')),
                    json.loads(blob(BASE, '.codex/tasks/TASK_ENVELOPE.schema.json')))
graph = json.loads(blob(AUTHORITY, manifest['files'][0]['path']))
base_pyproject = blob(BASE, 'pyproject.toml')
assert base_pyproject == blob(SOURCE_BASE, 'pyproject.toml')
assert base_pyproject == git('show', 'HEAD:pyproject.toml')
proposed_path = 'evidence/architecture/python-workspace-dependency-graph/pyproject-proposed.toml'
proposed = tomllib.loads(blob(AUTHORITY, proposed_path).decode())
assert proposed['project']['dependencies'] == graph['groups']['runtime']
assert proposed['dependency-groups'] == {key: graph['groups'][key] for key in ('dev', 'test')}
assert 'psycopg[binary]==3.3.6' in graph['groups']['runtime']
assert 'sqlalchemy==2.1.2' in graph['groups']['runtime']
constraints_path = 'docs/02-architecture/design-reviews/python-workspace-dependency-graph/constraints.txt'
assert 'referencing==0.37.0' in blob(AUTHORITY, constraints_path).decode().splitlines()
probe = '''uname -sm; getconf GNU_LIBC_VERSION; if [ -x /usr/local/bin/python3.12 ]; then /usr/local/bin/python3.12 -I -B -c 'import sys; print(sys.version); print(sys.base_prefix); print(sys.executable)'; sha256sum /usr/local/bin/python3.12; else printf '%s\n' 'APPROVED_PYTHON_MISSING: /usr/local/bin/python3.12'; fi; if [ -d /opt/dsgeorref-python-inputs ]; then ls -ld /opt/dsgeorref-python-inputs; if [ -x /opt/dsgeorref-python-inputs/uv-x86_64-unknown-linux-gnu/uv ]; then /opt/dsgeorref-python-inputs/uv-x86_64-unknown-linux-gnu/uv --version; fi; else printf '%s\n' 'APPROVED_INPUT_DIRECTORY_MISSING: /opt/dsgeorref-python-inputs'; fi'''
probe_result = command(['wsl', '-d', 'Ubuntu', '--', 'bash', '-lc', probe])
assert probe_result.returncode == 0
probe_output = probe_result.stdout.decode()
assert 'APPROVED_PYTHON_MISSING: /usr/local/bin/python3.12' in probe_output
assert 'APPROVED_INPUT_DIRECTORY_MISSING: /opt/dsgeorref-python-inputs' in probe_output
report = {
    'task': 'TASK-0773', 'issue': 'ISSUE-0875', 'story': 'STORY-0768', 'executor_role': 'ROLE-009',
    'recorded_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'progress': 'BLOCKED_AT_PREFLIGHT', 'base_sha': BASE, 'graph_authority_sha': AUTHORITY,
    'branch': branch, 'worktree': str(pathlib.Path.cwd()),
    'checkout_clean_before_evidence': True, 'task_envelope_schema': 'PASS',
    'authority_digests_valid': True, 'authority_files': authority_checks,
    'integrity_manifest_sha256': digest(manifest_bytes),
    'review_binding': 'Architecture Review/QA/Final Review PASS on authority SHA, supplied by human; no execution approval claimed',
    'approved_policy': {'python': graph['scope']['python_resolution_and_sync'],
                        'platform': graph['scope']['platform'], 'resolver': graph['resolver'],
                        'resolution': graph['transitive_policy']},
    'runtime_probe': COMMANDS[-1],
    'python_version': 'UNAVAILABLE at approved /usr/local/bin/python3.12; CPython 3.12.13 not validated',
    'python_digest': None, 'uv_version': 'NOT_VALIDATED; approved input directory absent',
    'uv_executable_digest': None, 'uv_archive_actual_digest': None,
    'uv_attestation': 'NOT_RUN', 'index_materialized': False,
    'metadata_checks_host_python': {'version': sys.version, 'executable': sys.executable,
                                   'usage': 'Git blob hashing, TOML/schema metadata and evidence only; never resolver/sync/runtime certification'},
    'pyproject_changed': False, 'pyproject_git_blob_sha256': digest(base_pyproject),
    'pyproject_worktree_sha256': digest(pathlib.Path('pyproject.toml').read_bytes()),
    'approved_proposed_pyproject_sha256': digest(blob(AUTHORITY, proposed_path)),
    'approved_proposed_pyproject_graph_match': 'PASS (input only; not materialized)',
    'pyproject_graph_match': 'NOT_MATERIALIZED', 'uv_lock_generated': False, 'uv_lock_sha256': None,
    'direct_dependencies_match': 'NOT_RUN', 'groups_match': 'NOT_RUN',
    'transitive_closure_match': 'NOT_RUN', 'constraints_match': 'NOT_RUN',
    'graph_to_lock_correspondence': 'NOT_RUN', 'unexpected_packages': 'NOT_EVALUATED (lock/install absent)',
    'lock_check': 'NOT_RUN', 'frozen_install_runtime': 'NOT_RUN', 'frozen_install_dev_test': 'NOT_RUN',
    'frozen_install_offline': 'NOT_RUN', 'second_lock_reproduction': 'NOT_RUN', 'essential_imports': 'NOT_RUN',
    'approved_versions_confirmed': {'workspace_psycopg': '3.3.6', 'sqlalchemy': '2.1.2',
                                    'referencing': '0.37.0 (approved constraint; installed state NOT_RUN)',
                                    'native_psycopg': '3.2.9 (separate authority; untouched)'},
    'dependency_graph_changed': False, 'material_decision_required': False,
    'deviations': [], 'material_deviations': [],
    'blocker_high': ['Approved CPython runtime missing at /usr/local/bin/python3.12',
                     'Approved resolver/index input directory missing at /opt/dsgeorref-python-inputs'],
    'stop_condition': 'TASK-0773: runtime/resolver immutable artifact unavailable or unverifiable; no replacement allowed',
    'make_verify': 'NOT_RUN per explicit user containment; blocked before manifest/lock changes',
    'benchmark': 'NOT_RUN', 'ready_for_qa': False,
    'candidate_binding': 'Evidence-only commit containing this report; obtain SHA via git rev-parse HEAD after commit',
    'commands': COMMANDS,
}
output = EVIDENCE / 'preflight.json'
with output.open('x', encoding='utf-8', newline='\n') as handle:
    json.dump(report, handle, ensure_ascii=False, indent=2)
    handle.write('\n')
print(json.dumps({'progress': report['progress'], 'authority_digests_valid': True,
                  'authority_files_checked': len(authority_checks), 'evidence': str(output),
                  'runtime_output': probe_output}, indent=2))