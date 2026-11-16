import os,pathlib,subprocess,json,time,hashlib,sys,traceback
os.chdir('/workspace')
P=pathlib.Path;R=P('evidence/operations/python-workspace-lock/linux-native-20261115/resume-after-checker')
state=json.loads((R/'results.json').read_text())
env=dict(PATH='/workspace/.venv/bin:/usr/local/bin:/usr/bin:/bin',LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
def run(name,args,environment=env):
 print(name,flush=True); start=time.time()
 with (R/(name+'.log')).open('w') as log: result=subprocess.run(args,env=environment,stdout=log,stderr=subprocess.STDOUT)
 with (R/'commands.jsonl').open('a') as f:f.write(json.dumps(dict(name=name,args=args,cwd='/workspace',exit_code=result.returncode,elapsed_seconds=round(time.time()-start,3)))+'\n')
 state[name]='PASS' if result.returncode==0 else 'FAIL'
 (R/'results.json').write_text(json.dumps(state,indent=2)+'\n')
 print((R/(name+'.log')).read_text()[-6000:],flush=True)
 assert result.returncode==0,name
shutil=__import__('shutil');shutil.copyfile('/tmp/pertinent.py',R/'pertinent-driver.py')
try:
 run('metadata-audit',['/workspace/.venv/bin/python','-I','-B','evidence/architecture/python-workspace-dependency-graph/supplement-http-runtime-v1/check-supplement.py','--check-lock','uv.lock','--audit-metadata'])
 run('checker-regressions',['/workspace/.venv/bin/python','-I','-B','evidence/architecture/python-workspace-dependency-graph/supplement-http-runtime-v1/verify-checker.py'])
 run('pertinent-tests',['/workspace/.venv/bin/python','-X','utf8','-m','pytest','-q','-p','no:cacheprovider','--import-mode=importlib','tests/infra/native_stack/test_native_stack.py','tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/test_materialization.py::test_uv_lock_frozen'])
 smoke="""import sys,json,importlib.metadata
sys.path.insert(0,'/workspace/src/backend')
sys.path.insert(0,'/workspace/tests/backend/identity_access/local_identity')
from conftest import synthetic_profile,PASSWORD
from dsgeorref.contexts.identity_access.adapters.local_identity.crypto import ArgonPasswords
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
import psycopg,fastapi,uvicorn,pydantic,celery,sqlalchemy,alembic,jwt,cryptography
passwords=ArgonPasswords(synthetic_profile())
a,b=passwords.hash(PASSWORD),passwords.hash(PASSWORD)
assert a!=b and passwords.verify(PASSWORD,a)
assert not passwords.verify('incorrect-password',a)
try: passwords.verify(PASSWORD,'$argon2i$invalid')
except Denied as exc: assert exc.code=='internal_error'
else: raise AssertionError('invalid PHC accepted')
assert psycopg.pq.__impl__=='binary'
assert psycopg.pq.version()>0
print(json.dumps(dict(runtime_imports='PASS',credential_argon2id_roundtrip='PASS',incorrect_password_rejected=True,invalid_phc_fail_closed=True,psycopg_implementation=psycopg.pq.__impl__,libpq_version=psycopg.pq.version(),database_connection_tested=False,production_profile_tested=False,benchmark_executed=False),indent=2))
"""
 (R/'runtime-smoke.py').write_text(smoke)
 run('runtime-smoke',['/workspace/.venv/bin/python','-I','-B',str(R/'runtime-smoke.py')])
 state['make_verify_classification']='ENVIRONMENT_LIMITATION_PNPM_UNAVAILABLE; PYTHON_QUALITY_PASS; NOT_CANDIDATE_MATERIAL'
 state['make_verify_explanation']='Ruff 0.17.4, mypy 2.4.1 and Python architecture PASS. make verify exits 2 at frontend-quality because pnpm executable is absent (recipe error 127). Makefile, Python quality inputs and frontend files unchanged vs current main. No frontend, full technical-tests or integration-tests completion claim. No dependency or checker was changed to pass.'
 (R/'results.json').write_text(json.dumps(state,indent=2)+'\n')
except Exception:
 state['blocker']=traceback.format_exc();(R/'results.json').write_text(json.dumps(state,indent=2)+'\n');raise
