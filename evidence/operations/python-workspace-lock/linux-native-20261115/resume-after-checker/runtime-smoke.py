import sys,json,importlib.metadata
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
