import hashlib,json,os,pathlib,platform,shutil,subprocess,sys,tarfile,time,traceback,urllib.request
os.chdir('/workspace')
P=pathlib.Path
E=P('evidence/architecture/python-workspace-dependency-graph'); S=E/'supplement-http-runtime-v1'
R=P('evidence/operations/python-workspace-lock/linux-native-20261115')
PY='/usr/local/bin/python3.12'; UV='/usr/local/bin/uv'; INPUT=P('/opt/dsgeorref-python-inputs')
sha=lambda p:hashlib.sha256(P(p).read_bytes()).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='fe08938fff3fcd0dd2281f24d1c87e9b414c3aaf'
assert not subprocess.check_output(['git','status','--porcelain'])
assert sys.version_info[:3]==(3,12,13) and sys.executable==PY and sys.base_prefix=='/usr/local'
assert subprocess.check_output([UV,'--version'],text=True).startswith('uv 0.12.19 ')
assert sha('pyproject.toml')=='dbda77fcae1fb41df059c905a318c2dbc807c067cf51909047fcc9f2b936255a'
checks=[]
for entry in json.loads((E/'digests.json').read_text())['files']+json.loads((S/'digests.json').read_text())['files']:
 checks.append(dict(path=entry['path'],expected=entry['sha256'],actual=sha(entry['path'])))
assert all(x['expected']==x['actual'] for x in checks),[x for x in checks if x['expected']!=x['actual']]
canonical=json.loads(P('evidence/operations/python-workspace-lock/eol-preflight-20261115/forced-checkout-inputs.json').read_text())
checks=[dict(path=x['path'],expected=x['blob_sha256'],actual=sha(x['path'])) for x in canonical['inputs']]
assert len(checks)==79 and len({x['path'] for x in checks})==79 and all(x['expected']==x['actual'] for x in checks),[x for x in checks if x['expected']!=x['actual']]
R.mkdir(parents=True,exist_ok=False)
shutil.copyfile('/tmp/stage1.py',R/'stage1-driver.py')
state=dict(source_bundle_created=True,source_bundle_valid=True,source_commit_present=True,linux_native_head='fe08938fff3fcd0dd2281f24d1c87e9b414c3aaf',linux_native_worktree_clean=True,windows_bind_mount_used_as_worktree=False,byte_sensitive_input_match='79/79',pyproject_input_sha256=sha('pyproject.toml'),python_version=platform.python_version(),python_executable=sys.executable,python_base_prefix=sys.base_prefix,python_binary_sha256=sha(PY),uv_version=subprocess.check_output([UV,'--version'],text=True).strip(),uv_binary_sha256=sha(UV),platform=platform.platform(),glibc=platform.libc_ver(),execution_image='task0773-toolchain:disposable-20261115',execution_image_id='sha256:dac23529b5f684e683232f0d298fb944094b3971e27437b7680b9edc8ed8d4ed',historical_approved_graph_sha='cb198c9e8340e0675c36679de426abf922e1c569',supplement_approved_sha='de58c489594fff294b687ef310b80452c29c8aa0',task_0773_amendment_sha='fd8d87c5f87c55ed11c9edc068ec651a500ec3a6',baseline_merge_sha='18d769e903abeae5d9a2c9d772a64baa96cb47e8',network_fallback_used=False)
def save(): (R/'execution-state.json').write_text(json.dumps(state,indent=2)+'\n')
def run(name,args,cwd='/workspace',env=None):
 print(name,flush=True); started=time.time(); p=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True)
 data=dict(name=name,args=args,cwd=cwd,exit_code=p.returncode,elapsed_seconds=round(time.time()-started,3),stdout=p.stdout,stderr=p.stderr)
 with (R/'commands.jsonl').open('a') as f: f.write(json.dumps(data)+'\n')
 (R/(name+'.log')).write_text(p.stdout+p.stderr)
 assert p.returncode==0,name+': '+(p.stderr or p.stdout)[-2500:]
 state[name]='PASS';save();return p.stdout
(R/'input-byte-hashes.json').write_text(json.dumps(checks,indent=2)+'\n');save()
try:
 print('PREFLIGHT PASS: native clone clean, toolchain exact, 79/79 byte-exact',flush=True)
 run('historical-clone',['git','clone','/transfer/source.bundle','/tmp/task0773-historical'])
 run('historical-checkout',['git','checkout','--detach',state['historical_approved_graph_sha']],cwd='/tmp/task0773-historical')
 run('historical-checker',[PY,'-I','-B',str(E/'check-structure.py'),'--verify-digests'],cwd='/tmp/task0773-historical')
 run('supplement-input-checker',[PY,'-I','-B',str(S/'check-supplement.py')])
 INPUT.mkdir(parents=True,exist_ok=False)
 artifacts=[('uv','https://github.com/astral-sh/uv/releases/download/0.12.19/uv-x86_64-unknown-linux-gnu.tar.gz','23bf5552d220e0842b65c862097b2ebaeba0064b74eda5e565e77fd25969d8c8','uv-x86_64-unknown-linux-gnu/uv',UV),('cpython','https://github.com/astral-sh/python-build-standalone/releases/download/20260602/cpython-3.12.13%2B20260602-x86_64-unknown-linux-gnu-install_only.tar.gz','9be5c21b78dbc371e739bc7faf3b007b8e607335f780bdd2e0dd44a6e3580d76','python/bin/python3.12',PY)]
 for name,url,expected,member,binary in artifacts:
  print('Verifying fixed '+name+' archive and installed binary',flush=True)
  archive=INPUT/(name+'.tar.gz')
  with urllib.request.urlopen(url,timeout=45) as response,archive.open('wb') as f: shutil.copyfileobj(response,f)
  actual=sha(archive); assert actual==expected,(name,'archive checksum',actual,expected)
  with tarfile.open(archive,'r:gz') as tar: binary_digest=hashlib.sha256(tar.extractfile(member).read()).hexdigest()
  assert binary_digest==sha(binary),(name,'installed binary does not match approved archive')
  state[name+'_artifact']=dict(url=url,sha256=actual,installed_binary_sha256=binary_digest,valid=True,provenance_authority='Approved historical/supplement provenance records; no new attestation claim')
  save()
 run('compose-inputs',[PY,'-I','-B',str(S/'check-supplement.py'),'--compose',str(R/'composed')])
 shutil.copytree(R/'composed/simple',INPUT/'simple')
 def hashes(root): return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
 composed=hashes(R/'composed/simple'); assert composed==hashes(INPUT/'simple')
 (R/'composed-hashes.json').write_text(json.dumps(hashes(R/'composed'),indent=2)+'\n')
 assert not P('uv.lock').exists()
 shutil.copyfile(S/'supplement-pyproject-proposed.toml','pyproject.toml')
 state['pyproject_materialized']=True;state['pyproject_final_sha256']=sha('pyproject.toml')
 import tomllib
 project=tomllib.loads(P('pyproject.toml').read_text())
 roots=project['project']['dependencies']+sum(project['dependency-groups'].values(),[])
 assert len(roots)==14 and len(project['tool']['uv']['constraint-dependencies'])==39
 state['direct_root_count']=14;state['constraint_count']=39;save()
 env=dict(PATH='/usr/local/bin:/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
 base=[UV,'--config-file',str(R/'composed/resolver-config.toml'),'--cache-dir',str(INPUT/'cache')]
 run('uv-lock',base+['lock','--python',PY,'--no-python-downloads','--no-build'],env=env)
 state['uv_lock_sha256']=sha('uv.lock');save()
 run('uv-lock-check',base+['lock','--check','--python',PY,'--no-python-downloads','--no-build'],env=env)
 run('supplement-lock-checker',[PY,'-I','-B',str(S/'check-supplement.py'),'--check-lock','uv.lock'])
 lock=tomllib.loads(P('uv.lock').read_text());assert len(lock['package'])==54
 state['distribution_count']=54;state['stage1']='PASS';save();print('STAGE1 PASS',flush=True)
except Exception as exc:
 state['blocker']=str(exc);state['stage1']='STOP';save();(R/'failure.log').write_text(traceback.format_exc());print(traceback.format_exc(),flush=True);sys.exit(1)

