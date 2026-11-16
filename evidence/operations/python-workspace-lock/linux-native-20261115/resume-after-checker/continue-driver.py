import os,pathlib,subprocess,json,time,hashlib,tomllib,shutil,traceback,importlib.util
os.chdir('/workspace')
P=pathlib.Path
R=P('evidence/operations/python-workspace-lock/linux-native-20261115/resume-after-checker')
PY='/usr/local/bin/python3.12'; UV='/usr/local/bin/uv'
S=P('evidence/architecture/python-workspace-dependency-graph/supplement-http-runtime-v1')
CONFIG='/workspace/evidence/operations/python-workspace-lock/linux-native-20261115/composed/resolver-config.toml'
CACHE='/opt/dsgeorref-python-inputs/cache'
env=dict(PATH='/usr/local/bin:/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
sha=lambda p:hashlib.sha256(P(p).read_bytes()).hexdigest()
expected='bd70e02748e7f09b5ca7fd544862f3b7d1deec30365a65c66552795839ce5cf2'
state=json.loads((R/'results.json').read_text())
def save(): (R/'results.json').write_text(json.dumps(state,indent=2)+'\n')
def run(name,args,cwd='/workspace',environment=env,required=True):
 print(name,flush=True)
 with (R/(name+'.log')).open('w') as log:
  start=time.time(); proc=subprocess.run(args,cwd=cwd,env=environment,stdout=log,stderr=subprocess.STDOUT)
 data=dict(name=name,args=args,cwd=cwd,environment=environment,exit_code=proc.returncode,elapsed_seconds=round(time.time()-start,3))
 with (R/'commands.jsonl').open('a') as f:f.write(json.dumps(data)+'\n')
 state[name]='PASS' if proc.returncode==0 else 'FAIL'; save()
 print((R/(name+'.log')).read_text()[-4500:],flush=True)
 if required: assert proc.returncode==0,name
 return proc.returncode
try:
 shutil.copyfile('/tmp/continue.py',R/'continue-driver.py')
 spec=importlib.util.spec_from_file_location('checker',S/'check-supplement.py'); checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
 old,delta,packages=checker.composition()
 changed={p['name'] for p in delta['packages']}
 edges=[e for e in old['active_edges'] if e['parent'] not in changed and e['parent'] in packages]+delta['affected_edges']
 project=tomllib.loads(P('pyproject.toml').read_text()); lock=tomllib.loads(P('uv.lock').read_text())
 external={p['name']:p['version'] for p in lock['package'] if 'virtual' not in p['source']}
 norm=lambda n:__import__('re').sub('[-_.]+','-',n).lower()
 inventory={}
 for group in ['runtime','dev-test']:
  actual={norm(p['name']):p['version'] for p in json.loads((R/(group+'-inventory.log')).read_text())}
  reached={norm(r.split('==')[0].split('[')[0]) for r in project['project']['dependencies']}
  if group=='dev-test':
   reached|={norm(r.split('==')[0].split('[')[0]) for roots in project['dependency-groups'].values() for r in roots}
  while True:
   nxt=reached|{e['child'] for e in edges if e['parent'] in reached}
   if nxt==reached:break
   reached=nxt
  authorized={n:packages[n]['version'] for n in reached}
  assert actual==authorized=={n:external[n] for n in reached},(group,actual,authorized)
  inventory[group]=dict(count=len(actual),authorized=authorized,installed=actual,match=True)
 assert len(inventory['dev-test']['installed'])==54
 assert P('pyproject.toml').read_bytes()==(S/'supplement-pyproject-proposed.toml').read_bytes()
 (R/'inventory-match.json').write_text(json.dumps(dict(graph_plus_supplement_to_pyproject_to_lock_to_install='PASS',groups=inventory,roots=project['project']['dependencies'],dependency_groups=project['dependency-groups'],constraints=project['tool']['uv']['constraint-dependencies'],active_edges=edges),indent=2)+'\n')
 state['install_inventory_match']='PASS';save()
 second=P('/tmp/task0773-second'); assert not second.exists()
 run('second-clone',['git','-c','core.autocrlf=false','clone','--no-hardlinks','--no-checkout','/workspace',str(second)])
 run('second-checkout',['git','-c','core.autocrlf=false','checkout','--detach',state['merge_head']],cwd=str(second))
 assert not subprocess.check_output(['git','status','--porcelain'],cwd=second)
 assert not (second/'uv.lock').exists()
 run('second-checker-ancestor',['git','merge-base','--is-ancestor',state['main_sha'],'HEAD'],cwd=str(second))
 shutil.copyfile(second/S/'supplement-pyproject-proposed.toml',second/'pyproject.toml')
 assert sha(second/'pyproject.toml')==sha('pyproject.toml')
 config2=second/'resolver-config.toml';shutil.copyfile(CONFIG,config2)
 assert sha(config2)==sha(CONFIG)
 secondcache='/tmp/task0773-second-cache';assert not P(secondcache).exists()
 state['second_inputs']=dict(head=state['merge_head'],lock_absent_before_resolution=True,cache_empty_before_resolution=True,pyproject_sha256=sha(second/'pyproject.toml'),config_sha256=sha(config2),registry='file:///opt/dsgeorref-python-inputs/simple',python=PY,uv=UV)
 save()
 run('second-lock',[UV,'--config-file',str(config2),'--cache-dir',secondcache,'lock','--python',PY,'--no-python-downloads','--no-build'],cwd=str(second))
 state['second_lock_sha256']=sha(second/'uv.lock');assert state['second_lock_sha256']==expected
 state['lock_reproducible']='YES';save()
 run('second-lock-checker',[PY,'-I','-B',str(S/'check-supplement.py'),'--check-lock','uv.lock'],cwd=str(second))
 shutil.copyfile(second/'uv.lock',R/'second-uv.lock')
 cachefiles={p.relative_to(CACHE).as_posix():sha(p) for p in P(CACHE).rglob('*') if p.is_file() and not p.is_symlink()}
 (R/'cache-files-before-offline.json').write_text(json.dumps(cachefiles,indent=2)+'\n')
 state['cache_file_count']=len(cachefiles);save()
 offlineenv=env|{'UV_PROJECT_ENVIRONMENT':'/tmp/task0773-offline-env'}
 assert not P(offlineenv['UV_PROJECT_ENVIRONMENT']).exists()
 base=[UV,'--config-file',CONFIG,'--cache-dir',CACHE,'sync','--frozen','--offline','--no-default-groups']
 tail=['--python',PY,'--no-python-downloads','--no-build']
 run('offline-runtime-frozen-sync',base+tail,environment=offlineenv)
 run('offline-dev-test-frozen-sync',base+['--group','dev','--group','test']+tail,environment=offlineenv)
 code="import importlib.metadata,json; print(json.dumps(sorted([dict(name=d.metadata['Name'],version=d.version) for d in importlib.metadata.distributions()],key=lambda x:x['name'].lower()),indent=2))"
 run('offline-inventory',['/tmp/task0773-offline-env/bin/python','-I','-B','-c',code])
 actual={norm(p['name']):p['version'] for p in json.loads((R/'offline-inventory.log').read_text())}
 assert actual==external
 state.update(offline_frozen_sync='PASS',network_fallback_used='NO',offline_fresh_environment_inventory_match=True)
 assert sha('uv.lock')==expected;save()
 run('ruff-version',['/workspace/.venv/bin/python','-m','ruff','--version'])
 verifyenv=env|{'PATH':'/workspace/.venv/bin:/usr/local/bin:/usr/bin:/bin','VIRTUAL_ENV':'/workspace/.venv'}
 result=run('make-verify',['make','verify','PYTHON=/workspace/.venv/bin/python'],environment=verifyenv,required=False)
 state['make_verify_exit_code']=result;save()
except Exception:
 state['blocker']=traceback.format_exc();save();print(state['blocker'],flush=True);raise
