"""Disposable PostgreSQL fixtures exercising the approved instance policy."""

import importlib.util
import sys
from importlib import import_module
from pathlib import Path

import psycopg
import pytest

ROOT = next(
    path for path in Path(__file__).resolve().parents if (path / "pyproject.toml").is_file()
)
LEGACY = ROOT / "tests/backend/identity_access/local_identity"
sys.path.insert(0, str(LEGACY))
spec = importlib.util.spec_from_file_location("local_identity_fixtures", LEGACY / "conftest.py")
base = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = base
spec.loader.exec_module(base)
ORIGIN, PASSWORD, Runtime = base.ORIGIN, base.PASSWORD, base.Runtime
synthetic_profile = base.synthetic_profile
database = base.database
ADAPTER = (
    "dsgeorref.contexts.identity_access.adapters."
    "usuarios-e-papeis-da-instancia.acc-auth-impl-parte-1"
)
APPLICATION = (
    "dsgeorref.contexts.identity_access.application."
    "usuarios-e-papeis-da-instancia.acc-auth-impl-parte-1"
)
POLICY = ROOT / "contracts/contexts/identity_access/plt/usuarios-e-papeis-da-instancia/policy.json"


@pytest.fixture
def runtime(database):
    from dsgeorref.contexts.identity_access.application.local_identity.accounts import LocalAccounts
    from dsgeorref.contexts.identity_access.application.local_identity.sessions import Sessions
    from dsgeorref.contexts.identity_access.application.local_identity.tokens import Tokens
    from dsgeorref.contexts.identity_access.domain.local_identity.credentials import opaque
    from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance, WebPolicy

    with psycopg.connect(database) as connection:
        connection.execute("""TRUNCATE identity.accounts,identity.bootstrap,identity.memberships,
          identity.oidc_links,identity.sessions,identity.tokens,identity.requests,
          identity.oidc_transactions,identity.ceremonies,identity.observations,
          identity.throttle_buckets,identity.throttle_decisions CASCADE""")
        connection.execute("INSERT INTO identity.bootstrap VALUES (true,'available',NULL,1)")
    tx = import_module(ADAPTER + ".runtime").build_transactions(
        database,
        synthetic_profile(),
        WebPolicy(ORIGIN),
        lambda store, operation, actor: True,
        opaque().encode(),
        POLICY,
        installation_authorized=True,
    )
    accounts = LocalAccounts(tx)
    account, issued, recovery = accounts.bootstrap(
        "admin", PASSWORD, "bootstrap", Provenance(ORIGIN, "same-origin")
    )
    return Runtime(
        tx.access.uow,
        tx.access,
        tx,
        accounts,
        Sessions(tx),
        Tokens(tx),
        account,
        issued,
        recovery,
        database,
    )


@pytest.fixture
def members(runtime):
    # Synthetic project/eligibility ports only; no claim about upstream runtime gates.
    return import_module(APPLICATION + ".memberships").Memberships(
        runtime.tx, lambda store, project: True
    )
