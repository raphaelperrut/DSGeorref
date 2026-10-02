"""Target authorization regression against a copy of the approved PostgreSQL schema."""

import json
import os
from dataclasses import asdict

import psycopg
import pytest
from conftest import ORIGIN, Runtime, synthetic_profile
from dsgeorref.contexts.identity_access.adapters.local_identity.crypto import ArgonPasswords
from dsgeorref.contexts.identity_access.adapters.local_identity.postgres import PostgresUnitOfWork
from dsgeorref.contexts.identity_access.application.local_identity.access import Access
from dsgeorref.contexts.identity_access.application.local_identity.accounts import LocalAccounts
from dsgeorref.contexts.identity_access.application.local_identity.sessions import Sessions
from dsgeorref.contexts.identity_access.application.local_identity.tokens import Tokens
from dsgeorref.contexts.identity_access.application.local_identity.transactions import (
    IdentityTransactions,
)
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import (
    digest,
    opaque,
    uuid7,
)
from dsgeorref.contexts.identity_access.domain.local_identity.models import Account
from dsgeorref.contexts.identity_access.domain.local_identity.policy import (
    PUBLIC_ACTIONS,
    AuthorizationPolicy,
)
from dsgeorref.contexts.identity_access.domain.local_identity.web import WebPolicy
from test_requirements import (
    rejected,
)
from test_requirements import (
    test_req_auth_impl_004 as test_req_auth_impl_004,
)
from test_requirements import (
    test_req_auth_impl_006 as test_req_auth_impl_006,
)
from test_requirements import (
    test_req_dbschema_003 as test_req_dbschema_003,
)


@pytest.fixture
def runtime():
    dsn = os.environ["IDENTITY_H1_TEST_DSN"]
    with psycopg.connect(dsn) as connection:
        assert connection.info.dbname == "local_identity_h1_validation"
        assert connection.execute(
            "SELECT version_num FROM identity.alembic_version"
        ).fetchone() == ("local_identity_v1",)
        password_hash = connection.execute(
            "SELECT password_hash FROM identity.accounts WHERE administrator LIMIT 1"
        ).fetchone()[0]
    profile = synthetic_profile()
    account = Account(uuid7(), "revoke-test-" + opaque(), password_hash, digest(opaque()))
    policy = AuthorizationPolicy(
        "synthetic-policy-only",
        {account.id: PUBLIC_ACTIONS},
        {"owner": PUBLIC_ACTIONS, "viewer": frozenset({"project_member:list"})},
        frozenset({"instance:bootstrap"}),
        frozenset({"session:create", "oidc:callback"}),
    )
    uow = PostgresUnitOfWork(dsn)
    access = Access(uow, policy, profile)
    tx = IdentityTransactions(
        access, ArgonPasswords(profile), WebPolicy(ORIGIN), lambda *args: True, opaque().encode()
    )
    # Seed only the subject/session needed by this regression; no bootstrap or migration.
    with uow() as store:
        store.insert("accounts", asdict(account))
        issued = tx.session(store, account.id)
    return Runtime(
        uow, access, tx, LocalAccounts(tx), Sessions(tx), Tokens(tx), account, issued, "", dsn
    )


def test_revoke_requires_target_project_permission(runtime, record_property):
    r = runtime
    project_a, project_b = uuid7(), uuid7()
    r.member(project_a)
    r.member(project_b)

    def issue(project, scopes):
        return r.tokens.issue(r.issued.secret, "session", scopes, opaque(), r.browser(), project)

    target = issue(project_b, ["project_member:list"])
    caller_a = issue(project_a, ["project_member:list"])
    manager_a = issue(project_a, ["token:create"])
    manager_b = issue(project_b, ["token:create"])
    with r.uow() as store:
        before = store.get("tokens", {"id": target.token.id})
        store.update(
            "memberships",
            {"project_id": project_b, "account_id": r.account.id},
            {"role": "viewer", "revision": 2},
        )

    evidence = []

    def denied(secret, kind, scenario):
        rejected(
            "forbidden",
            lambda: r.tokens.revoke(
                secret, kind, target.token.id, r.browser() if kind == "session" else None
            ),
        )
        with r.uow() as store:
            assert store.get("tokens", {"id": target.token.id}) == before
            assert not store.rows(
                "observations", {"action": "revoke", "target_id": target.token.id}
            )
        evidence.append(
            {
                "scenario": scenario,
                "expected": "forbidden; target unchanged",
                "observed": "forbidden; complete persisted row unchanged; no committed revoke",
            }
        )

    denied(caller_a.secret, "pat", "A list-only PAT; B central permission denied; same owner")
    denied(r.issued.secret, "session", "session owner; B central permission denied")
    with r.uow() as store:
        store.update(
            "memberships",
            {"project_id": project_b, "account_id": r.account.id},
            {"role": "owner", "revision": 3},
        )
    denied(
        manager_a.secret,
        "pat",
        "A token:create PAT; B central role allows; caller project mismatch",
    )
    denied(target.secret, "pat", "B list-only PAT; target owned; required action absent")
    r.tokens.revoke(manager_b.secret, "pat", target.token.id, None)
    with r.uow() as store:
        after = store.get("tokens", {"id": target.token.id})
        assert after == {**before, "state": "revoked", "revision": before["revision"] + 1}
        assert (
            len(store.rows("observations", {"action": "revoke", "target_id": target.token.id})) == 1
        )
    rejected("unauthorized", lambda: r.access.authenticate(pat=target.secret))
    evidence.append(
        {
            "scenario": "B token:create PAT; matching target project and owner",
            "expected": "revoked; revision +1; subsequent use denied",
            "observed": "revoked; revision +1; one committed audit; unauthorized",
        }
    )
    record_property("runtime_regression", json.dumps(evidence))
