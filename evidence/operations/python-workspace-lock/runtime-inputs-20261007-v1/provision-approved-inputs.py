"""Materialize only approved uv/index bytes; never provision or download Python."""
import datetime
import hashlib
import io
import json
import pathlib
import subprocess
import sys
import tarfile

AUTHORITY = 'cb198c9e8340e0675c36679de426abf922e1c569'
BASE = 'ee0841d54d9bc1472ebbaa2b12dd1720d0aa9819'
PREVIOUS = 'd587a882adf8d0a531b8ac55dc21041fb3b526a6'
TARGET = '/opt/dsgeorref-python-inputs'
UNC = pathlib.Path(r'\\wsl.localhost\Ubuntu\opt\dsgeorref-python-inputs')
EVIDENCE = pathlib.Path(__file__).resolve().parent
COMMANDS = []


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(argv, data=None):
    result = subprocess.run(argv, input=data, capture_output=True, check=False)
    entry = {'argv': argv, 'exit_code': result.returncode,
             'stderr': result.stderr.decode('utf-8', errors='replace')}
    if argv[:2] == ['git', 'show']:
        entry.update(stdout_sha256=sha(result.stdout), stdout_bytes=len(result.stdout))
    else:
        entry['stdout'] = result.stdout.decode('utf-8', errors='replace')
    if data is not None:
        entry.update(stdin_sha256=sha(data), stdin_bytes=len(data))
    COMMANDS.append(entry)
    assert result.returncode == 0, entry
    return result.stdout


def blob(ref, path):
    return run(['git', 'show', f'{ref}:{path}'])


assert run(['git', 'rev-parse', 'HEAD']).decode().strip() == PREVIOUS
assert run(['git', 'branch', '--show-current']).decode().strip() == 'codex/issue-0875-task-0773-python-workspace-lock'
assert all(line[3:].startswith('evidence/operations/python-workspace-lock/')
           for line in run(['git', 'status', '--porcelain']).decode().splitlines())
manifest_path = 'evidence/architecture/python-workspace-dependency-graph/digests.json'
manifest_bytes = blob(AUTHORITY, manifest_path)
assert manifest_bytes == blob('HEAD', manifest_path)
manifest = json.loads(manifest_bytes)
checks = []
for item in manifest['files']:
    content = blob(AUTHORITY, item['path'])
    assert sha(content) == item['sha256'] and len(content) == item['bytes']
    assert blob('HEAD', item['path']) == content
    checks.append(dict(item, match=True))
graph = json.loads(blob(AUTHORITY, 'docs/02-architecture/design-reviews/python-workspace-dependency-graph/approved-dependency-graph.yaml'))
archive_name = 'uv-x86_64-unknown-linux-gnu.tar.gz'
archive = UNC / archive_name
expected = graph['resolver']['linux_amd64_archive_sha256']
actual = sha(archive.read_bytes())
assert actual == expected
attestation = json.loads((EVIDENCE / 'uv-attestation.json').read_text(encoding='utf-8'))
assert attestation['exit_code'] == 0
verified = json.loads(attestation['stdout'])
assert any(result['verificationResult']['signature']['certificate']['sourceRepositoryURI'] == 'https://github.com/astral-sh/uv'
           and any(subject['name'] == archive_name and subject['digest']['sha256'] == expected
                   for subject in result['verificationResult']['statement']['subject'])
           for result in verified)
assert {p.name for p in UNC.iterdir()} == {archive_name}, 'Unexpected target contents; stop'
run(['wsl', '-d', 'Ubuntu', '-u', 'root', '--', '/usr/bin/tar', '-xzf', f'{TARGET}/{archive_name}', '-C', TARGET])
uv_path = f'{TARGET}/uv-x86_64-unknown-linux-gnu/uv'
uv_version = run(['wsl', '-d', 'Ubuntu', '--', uv_path, '--version']).decode().strip()
assert uv_version.split()[:2] == ['uv', '0.12.19'], uv_version
simple_prefix = 'evidence/architecture/python-workspace-dependency-graph/simple/'
snapshot_files = [item for item in manifest['files'] if item['path'].startswith(simple_prefix)]
assert len(snapshot_files) == 44
payload = io.BytesIO()
with tarfile.open(fileobj=payload, mode='w', format=tarfile.USTAR_FORMAT) as bundle:
    for item in sorted(snapshot_files, key=lambda record: record['path']):
        content = blob(AUTHORITY, item['path'])
        relative = item['path'][len(simple_prefix):]
        assert '..' not in pathlib.PurePosixPath(relative).parts
        info = tarfile.TarInfo('simple/' + relative)
        info.size = len(content)
        info.mode = 0o644
        info.mtime = 0
        bundle.addfile(info, io.BytesIO(content))
run(['wsl', '-d', 'Ubuntu', '-u', 'root', '--', '/usr/bin/tar', '-xf', '-', '-C', TARGET], payload.getvalue())
run(['wsl', '-d', 'Ubuntu', '-u', 'root', '--', '/usr/bin/mkdir', '-m', '0755', f'{TARGET}/cache'])
expected_snapshot = {item['path'][len(simple_prefix):]: item['sha256'] for item in snapshot_files}
actual_snapshot = {path.relative_to(UNC / 'simple').as_posix(): sha(path.read_bytes())
                   for path in (UNC / 'simple').rglob('*') if path.is_file()}
assert actual_snapshot == expected_snapshot, 'Approved simple snapshot mismatch; stop'
assert {path.name for path in UNC.iterdir()} == {archive_name, 'uv-x86_64-unknown-linux-gnu', 'simple', 'cache'}
assert not list((UNC / 'cache').iterdir())
executables = {path.name: sha(path.read_bytes()) for path in (UNC / 'uv-x86_64-unknown-linux-gnu').iterdir() if path.is_file()}
python_probe = run(['wsl', '-d', 'Ubuntu', '--', '/bin/bash', '-lc', "if [ -x /usr/local/bin/python3.12 ]; then /usr/local/bin/python3.12 -I -B -c 'import sys; print(sys.version); print(sys.base_prefix); print(sys.executable)'; else printf '%s\\n' 'APPROVED_PYTHON_MISSING: /usr/local/bin/python3.12'; fi"]).decode()
assert 'APPROVED_PYTHON_MISSING: /usr/local/bin/python3.12' in python_probe
assert run(['git', 'diff', '--name-only']) == b''
assert blob('HEAD', 'pyproject.toml') == blob(BASE, 'pyproject.toml')
assert not pathlib.Path('uv.lock').exists()
report = {
    'task': 'TASK-0773', 'issue': 'ISSUE-0875', 'story': 'STORY-0768', 'role': 'ROLE-009',
    'recorded_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'previous_preflight_sha': PREVIOUS, 'base_sha': BASE, 'graph_authority_sha': AUTHORITY,
    'progress': 'BLOCKED_EXTERNAL_PYTHON_INPUT',
    'python_blocker_classification': 'EXTERNAL_INPUT_MISSING',
    'python_classification_basis': {'handoff': 'Provide previously approved interpreter outside Conda at /usr/local/bin/python3.12; no automatic Python downloads',
                                   'graph_python_authority': graph['scope']['python_authority'],
                                   'missing': [{'path': '/usr/local/bin/python3.12', 'version': 'CPython 3.12.13',
                                                'source': 'NOT_SPECIFIED_BY_APPROVED_AUTHORITY for standalone non-Conda WSL runtime',
                                                'digest': 'NOT_SPECIFIED_BY_APPROVED_AUTHORITY',
                                                'provisioning_recipe': 'NOT_SPECIFIED_BY_APPROVED_AUTHORITY'}],
                                   'native_runtime': 'Conda artifact/image is authority for separate native environment and expressly excluded; not a provisioning input for this workspace'},
    'python_3_12_13_provisioned': False, 'python_path': '/usr/local/bin/python3.12 (ABSENT)',
    'uv_blocker_classification': 'PROVISIONABLE_FROM_APPROVED_AUTHORITY',
    'uv_0_12_19_validated': True, 'uv_version_output': uv_version, 'uv_path': uv_path,
    'uv_origin': graph['resolver']['linux_amd64_archive_url'],
    'uv_archive_expected_sha256': expected, 'uv_archive_actual_sha256': actual,
    'uv_attestation': 'PASS; GitHub producer astral-sh/uv; actual command/result stored in uv-attestation.json',
    'uv_executable_sha256': executables,
    'python_inputs_classification': 'PROVISIONABLE_FROM_APPROVED_AUTHORITY',
    'python_inputs_materialized': True, 'python_inputs_path': TARGET, 'python_inputs_digests_valid': True,
    'python_inputs_origin': f'Exact simple/** Git blobs from {AUTHORITY}; archive from fixed graph URL; no recapture or live PyPI metadata',
    'simple_snapshot_file_digests': actual_snapshot, 'simple_snapshot_file_count': 44,
    'config_origin': graph['resolver']['config'], 'cache': 'empty exclusive directory; no wheels downloaded or installed',
    'authority_digests_valid': True, 'authority_files': checks, 'integrity_manifest_sha256': sha(manifest_bytes),
    'metadata_host_python': {'version': sys.version, 'executable': sys.executable,
                            'usage': 'Git blob integrity, transport exact index bytes, evidence; never resolution/install certification'},
    'preflight': 'BLOCKED', 'python_probe': python_probe,
    'pyproject_changed': False, 'pyproject_git_blob_sha256': sha(blob('HEAD', 'pyproject.toml')),
    'pyproject_graph_match': 'NOT_MATERIALIZED', 'uv_lock_generated': False, 'uv_lock_sha256': None,
    'direct_dependencies_match': 'NOT_RUN', 'groups_match': 'NOT_RUN', 'transitive_closure_match': 'NOT_RUN',
    'constraints_match': 'NOT_RUN', 'unexpected_packages': 'NOT_EVALUATED (no lock/install)',
    'lock_check': 'NOT_RUN', 'frozen_install': 'NOT_RUN', 'essential_imports': 'NOT_RUN',
    'dependency_graph_changed': False, 'material_decision_required': False, 'external_input_missing': '/usr/local/bin/python3.12: approved standalone CPython 3.12.13',
    'blocker_high': ['Approved non-Conda CPython 3.12.13 missing; no approved provisioning recipe/source/digest supplied'],
    'ready_for_qa': False, 'deviations': [], 'make_verify': 'NOT_RUN per explicit containment',
    'benchmark': 'NOT_RUN', 'native_stack': 'UNTOUCHED', 'issue_0876': 'UNTOUCHED',
    'preparation_commands_already_executed': [
        {'argv': ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', '/usr/bin/test', '!', '-e', TARGET], 'exit_code': 0},
        {'argv': ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', '/usr/bin/mkdir', '-m', '0755', TARGET], 'exit_code': 0},
        {'argv': ['wsl', '-d', 'Ubuntu', '-u', 'root', '--', '/usr/bin/curl', '--fail', '--location', '--proto', '=https', '--proto-redir', '=https', '--output', f'{TARGET}/{archive_name}', graph['resolver']['linux_amd64_archive_url']], 'exit_code': 0},
        {'argv': ['wsl', '-d', 'Ubuntu', '--', '/usr/bin/sha256sum', f'{TARGET}/{archive_name}'], 'exit_code': 0, 'stdout': f'{actual}  {TARGET}/{archive_name}\n'}],
    'commands': COMMANDS,
    'candidate_binding': 'Evidence-only commit containing report; execution remains incomplete',
}
with (EVIDENCE / 'provisioning-result.json').open('x', encoding='utf-8', newline='\n') as handle:
    json.dump(report, handle, ensure_ascii=False, indent=2)
    handle.write('\n')
print(json.dumps({'progress': report['progress'], 'uv': uv_version,
                  'uv_archive_sha256': actual, 'uv_executable_sha256': executables,
                  'simple_files_validated': len(actual_snapshot),
                  'python_probe': python_probe}, indent=2))