"""Synthetic profiles for a disposable PostgreSQL database, never production policy."""

import os
from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

import psycopg
import pytest
from dsgeorref.contexts.identity_access.adapters.local_identity.crypto import ArgonPasswords
from dsgeorref.contexts.identity_access.adapters.local_identity.migration import migrate
from dsgeorref.contexts.identity_access.adapters.local_identity.postgres import PostgresUnitOfWork
from dsgeorref.contexts.identity_access.application.local_identity.access import Access
from dsgeorref.contexts.identity_access.application.local_identity.accounts import LocalAccounts
from dsgeorref.contexts.identity_access.application.local_identity.sessions import Sessions
from dsgeorref.contexts.identity_access.application.local_identity.tokens import Tokens
from dsgeorref.contexts.identity_access.application.local_identity.transactions import (
    IdentityTransactions,
)
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import opaque
from dsgeorref.contexts.identity_access.domain.local_identity.models import Account, IssuedSession
from dsgeorref.contexts.identity_access.domain.local_identity.policy import (
    PUBLIC_ACTIONS,
    AuthorizationPolicy,
    SecurityProfile,
)
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance, WebPolicy
from sqlalchemy.engine import make_url

PASSWORD = "synthetic-password-for-tests-only"
ORIGIN = "https://identity.example.test"


def synthetic_profile() -> SecurityProfile:
    return SecurityProfile(
        "synthetic-test-only",
        "BP-003",
        True,
        1024,
        1,
        1,
        1,
        12,
        256,
        timedelta(minutes=30),
        timedelta(minutes=10),
        timedelta(hours=1),
        timedelta(minutes=2),
        2.0,
    )


@dataclass
class Runtime:
    uow: PostgresUnitOfWork
    access: Access
    tx: IdentityTransactions
    accounts: LocalAccounts
    sessions: Sessions
    tokens: Tokens
    account: Account
    issued: IssuedSession
    recovery: str
    dsn: str

    def browser(self, issued: IssuedSession | None = None) -> Provenance:
        return Provenance(ORIGIN, "same-origin", (issued or self.issued).csrf)

    def member(self, project: UUID, role: str = "owner") -> None:
        with self.uow() as store:
            store.insert(
                "memberships",
                {"project_id": project, "account_id": self.account.id, "role": role, "revision": 1},
            )


@pytest.fixture(scope="session")
def database():
    dsn = os.environ["IDENTITY_TEST_DSN"]
    migration_dsn = os.environ.get(
        "IDENTITY_MIGRATION_DSN",
        "postgresql+psycopg://auth_test@127.0.0.1:55482/local_identity_validation",
    )
    # Explicitly require the private validation database before destructive fixture cleanup.
    with psycopg.connect(dsn) as connection:
        assert connection.info.dbname in {"local_identity_validation", "identity_slice2_validation"}
        assert make_url(migration_dsn).database == connection.info.dbname
    migrate(migration_dsn, "upgrade")
    yield dsn


@pytest.fixture
def runtime(database):
    with psycopg.connect(database) as connection:
        connection.execute("""TRUNCATE identity.accounts,identity.bootstrap,identity.memberships,
          identity.oidc_links,identity.sessions,identity.tokens,identity.requests,
          identity.oidc_transactions,identity.ceremonies,identity.observations CASCADE""")
        connection.execute("INSERT INTO identity.bootstrap VALUES (true,'available',NULL,1)")
    profile = synthetic_profile()
    policy = AuthorizationPolicy(
        "synthetic-policy-only",
        {},
        {"owner": PUBLIC_ACTIONS, "viewer": frozenset({"project_member:list"})},
        frozenset({"instance:bootstrap"}),
        frozenset({"session:create", "oidc:callback"}),
    )
    uow = PostgresUnitOfWork(database)
    access = Access(uow, policy, profile)
    # Fake upstream eligibility port only; no assertion of implemented REQ-AUTH-IMPL-007.
    tx = IdentityTransactions(
        access,
        ArgonPasswords(profile),
        WebPolicy(ORIGIN),
        lambda store, operation, actor: True,
        opaque().encode(),
    )
    accounts = LocalAccounts(tx)
    account, issued, recovery = accounts.bootstrap(
        "admin", PASSWORD, "bootstrap", Provenance(ORIGIN, "same-origin")
    )
    policy.account_grants[account.id] = PUBLIC_ACTIONS
    return Runtime(
        uow, access, tx, accounts, Sessions(tx), Tokens(tx), account, issued, recovery, database
    )
