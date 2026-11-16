import os,pathlib,subprocess,json,time,hashlib,tomllib,shutil,traceback
os.chdir('/workspace')
P=pathlib.Path
R=P('evidence/operations/python-workspace-lock/linux-native-20261115/resume-after-checker')
R.mkdir(exist_ok=False)
PY='/usr/local/bin/python3.12'; UV='/usr/local/bin/uv'
S=P('evidence/architecture/python-workspace-dependency-graph/supplement-http-runtime-v1')
CONFIG='/workspace/evidence/operations/python-workspace-lock/linux-native-20261115/composed/resolver-config.toml'
CACHE='/opt/dsgeorref-python-inputs/cache'
env=dict(PATH='/usr/local/bin:/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
sha=lambda p:hashlib.sha256(P(p).read_bytes()).hexdigest()
expected='bd70e02748e7f09b5ca7fd544862f3b7d1deec30365a65c66552795839ce5cf2'
state={}
def save(): (R/'results.json').write_text(json.dumps(state,indent=2)+'\n')
def run(name,args,cwd='/workspace',environment=env,required=True):
 print(name,flush=True)
 with (R/(name+'.log')).open('w') as log:
  start=time.time(); proc=subprocess.run(args,cwd=cwd,env=environment,stdout=log,stderr=subprocess.STDOUT)
 data=dict(name=name,args=args,cwd=cwd,environment=environment,exit_code=proc.returncode,elapsed_seconds=round(time.time()-start,3))
 with (R/'commands.jsonl').open('a') as f:f.write(json.dumps(data)+'\n')
 state[name]='PASS' if proc.returncode==0 else 'FAIL'; save()
 print((R/(name+'.log')).read_text()[-5000:],flush=True)
 if required: assert proc.returncode==0,name
 return proc.returncode
try:
 assert sha('uv.lock')==expected
 state.update(preexisting_lock_sha256=expected,restored_lock_sha256=sha('uv.lock'),lock_preserved_exactly=True,merge_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),main_sha='e2123eb4ac178103b1169ced32c2b680d3d320fb',checker_approved_sha='94ab889c32f5d21f74c5353fa1489c9247b76743')
 shutil.copyfile('/tmp/task0773-state/before.sha256',R/'preserved-before.sha256')
 shutil.copyfile('/tmp/task0773-state/restored-check.txt',R/'preserved-restoration-check.txt')
 shutil.copyfile('/tmp/resume.py',R/'resume-driver.py')
 run('checker-merge-ancestor',['git','merge-base','--is-ancestor',state['main_sha'],'HEAD'])
 checker_paths=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',state['checker_approved_sha']],text=True).splitlines()
 state['checker_files']=checker_paths
 for p in checker_paths:
  assert P(p).read_bytes()==subprocess.check_output(['git','show',state['main_sha']+':'+p])
 run('uv-lock-check',[UV,'--config-file',CONFIG,'--cache-dir',CACHE,'lock','--check','--python',PY,'--no-python-downloads','--no-build'])
 run('supplement-checker',[PY,'-I','-B',str(S/'check-supplement.py'),'--check-lock','uv.lock'])
 lock=tomllib.loads(P('uv.lock').read_text()); project=tomllib.loads(P('pyproject.toml').read_text())
 state.update(external_distribution_count=len([p for p in lock['package'] if 'virtual' not in p['source']]),virtual_root_count=len([p for p in lock['package'] if 'virtual' in p['source']]),total_lock_entry_count=len(lock['package']),constraint_count=len(project['tool']['uv']['constraint-dependencies']))
 assert (state['external_distribution_count'],state['virtual_root_count'],state['total_lock_entry_count'],state['constraint_count'])==(54,1,55,39)
 base=[UV,'--config-file',CONFIG,'--cache-dir',CACHE,'sync','--frozen','--no-default-groups']
 tail=['--python',PY,'--no-python-downloads','--no-build']
 run('runtime-frozen-sync',base+tail)
 inventory_code="import importlib.metadata,json; print(json.dumps(sorted([dict(name=d.metadata['Name'],version=d.version) for d in importlib.metadata.distributions()],key=lambda x:x['name'].lower()),indent=2))"
 run('runtime-inventory',['/workspace/.venv/bin/python','-I','-B','-c',inventory_code])
 run('dev-test-frozen-sync',base+['--group','dev','--group','test']+tail)
 run('dev-test-inventory',['/workspace/.venv/bin/python','-I','-B','-c',inventory_code])
 assert sha('uv.lock')==expected
 state['first_lock_unchanged_after_syncs']=True; save()
except Exception:
 state['blocker']=traceback.format_exc();save();print(state['blocker'],flush=True);raise
