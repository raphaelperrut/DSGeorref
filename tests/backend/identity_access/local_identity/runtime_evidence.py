"""Disposable PostgreSQL rehearsal through application services, without HTTP/UI."""

import hashlib
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, replace
from datetime import timedelta
from pathlib import Path

import psycopg
from conftest import ORIGIN, PASSWORD, synthetic_profile
from dsgeorref.contexts.identity_access.adapters.local_identity.crypto import ArgonPasswords
from dsgeorref.contexts.identity_access.adapters.local_identity.migration import migrate
from dsgeorref.contexts.identity_access.adapters.local_identity.postgres import (
    TABLES,
    PostgresUnitOfWork,
)
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
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from dsgeorref.contexts.identity_access.domain.local_identity.policy import (
    PUBLIC_ACTIONS,
    AuthorizationPolicy,
)
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance, WebPolicy
from sqlalchemy.exc import DBAPIError

ROOT = Path(__file__).resolve().parents[4]
OUTPUT = (
    ROOT
    / "evidence/implementation/contas-locais-bootstrap-unico-sessoes-tokens-e-ada"
    / "auth-impl-dbschema-parte-1"
)
DSN = os.environ["IDENTITY_TEST_DSN"]
MIGRATION_DSN = "postgresql+psycopg://auth_test@127.0.0.1:55482/local_identity_validation"
PG_BIN = Path("C:/Program Files/PostgreSQL/16/bin")


def psql(sql):
    with psycopg.connect(DSN) as connection:
        assert connection.info.dbname == "local_identity_validation"
        return (
            connection.execute(sql).fetchall()
            if sql.lstrip().startswith("SELECT")
            else connection.execute(sql)
        )


def clear_fixture():
    psql("""TRUNCATE identity.accounts,identity.bootstrap,identity.memberships,
      identity.oidc_links,identity.sessions,identity.tokens,identity.requests,
      identity.oidc_transactions,identity.ceremonies,identity.observations CASCADE""")
    psql("INSERT INTO identity.bootstrap VALUES (true,'available',NULL,1)")


def denied(expected, action):
    try:
        action()
    except Denied as error:
        assert error.code == expected, error.code
        return error.code
    raise AssertionError("operation unexpectedly succeeded")


def snapshot():
    rows = {}
    with psycopg.connect(DSN) as connection:
        for table in TABLES:
            # All identifiers are the closed BC-002 table catalog, never external input.
            rows[table] = [
                row[0]
                for row in connection.execute(
                    f"SELECT to_jsonb(t)::text FROM identity.{table} t ORDER BY to_jsonb(t)::text"
                )
            ]
    encoded = json.dumps(rows, sort_keys=True).encode()
    return rows, hashlib.sha256(encoded).hexdigest()


def run():
    clear_fixture()
    policy = AuthorizationPolicy(
        "synthetic-policy-only",
        {},
        {"owner": PUBLIC_ACTIONS, "viewer": frozenset({"project_member:list"})},
        frozenset({"instance:bootstrap"}),
        frozenset({"session:create"}),
    )
    profile, uow = synthetic_profile(), PostgresUnitOfWork(DSN)
    access = Access(uow, policy, profile)
    tx = IdentityTransactions(
        access,
        ArgonPasswords(profile),
        WebPolicy(ORIGIN),
        lambda store, operation, actor: True,
        opaque().encode(),
    )
    accounts, sessions, tokens = LocalAccounts(tx), Sessions(tx), Tokens(tx)
    request = Provenance(ORIGIN, "same-origin")
    report = {
        "profile": "synthetic fixture only; no BP-003 promotion or production readiness claim",
        "boundary": "application services -> private BC-002 UoW -> PostgreSQL 16.1",
        "migration_apply": "Alembic local_identity_v1; transactional additive DDL; PASS",
    }
    # Inject an actual deferred commit failure, beyond a mocked repository failure.
    psql("""CREATE FUNCTION identity.fail_commit() RETURNS trigger LANGUAGE plpgsql AS $$
      BEGIN RAISE EXCEPTION 'synthetic deferred commit failure'; END $$;
      CREATE CONSTRAINT TRIGGER inject_commit_failure AFTER INSERT ON identity.observations
      DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION identity.fail_commit()""")
    denied("internal_error", lambda: accounts.bootstrap("admin", PASSWORD, "failed", request))
    assert psql("SELECT count(*) FROM identity.accounts")[0][0] == 0
    assert psql("SELECT count(*) FROM identity.sessions")[0][0] == 0
    assert psql("SELECT count(*) FROM identity.requests")[0][0] == 0
    assert psql("SELECT state FROM identity.bootstrap")[0][0] == "available"
    psql(
        "DROP TRIGGER inject_commit_failure ON identity.observations; "
        "DROP FUNCTION identity.fail_commit()"
    )
    report["deferred_commit_failure"] = (
        "commit rejected -> no account/session/idempotency/audit success -> observed; "
        "bootstrap available"
    )

    def bootstrap(key):
        try:
            return accounts.bootstrap("admin", PASSWORD, key, request)
        except Denied as error:
            return error.code

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = list(executor.map(bootstrap, ("racer-one", "racer-two")))
    winner = next(result for result in outcomes if isinstance(result, tuple))
    assert outcomes.count("bootstrap_already_completed") == 1
    account, issued, kit = winner
    policy.account_grants[account.id] = PUBLIC_ACTIONS
    browser = Provenance(ORIGIN, "same-origin", issued.csrf)
    assert psql("SELECT count(*) FROM identity.accounts")[0][0] == 1
    report["bootstrap_concurrency"] = (
        "two transactions -> exactly one winner -> one account/session, "
        "loser bootstrap_already_completed"
    )
    project, other = uuid7(), uuid7()
    with uow() as store:
        store.insert(
            "memberships",
            {"project_id": project, "account_id": account.id, "role": "owner", "revision": 1},
        )
    pat = tokens.issue(
        issued.secret, "session", ["project_member:create"], "scoped", browser, project
    )
    assert access.authenticate(pat=pat.secret).credential.id == pat.token.id
    with uow() as store:
        principal = access.load(store, pat.secret, "pat")
        denied(
            "forbidden", lambda: access.enforce(store, principal, "project_member:create", other)
        )
    report["project_scope"] = (
        "scoped PAT -> same project allowed / other denied -> observed allowed / forbidden"
    )
    with uow() as store:
        expired = replace(
            pat.token,
            id=uuid7(),
            secret_hash=digest("expired-runtime-pat"),
            expires_at=store.now() - timedelta(seconds=1),
        )
        store.insert("tokens", asdict(expired))
    denied("unauthorized", lambda: access.authenticate(pat="expired-runtime-pat"))
    assert psql(f"SELECT state FROM identity.tokens WHERE id='{expired.id}'")[0][0] == "expired"
    report["expiry"] = "server expiry elapsed -> denied and state expired -> unauthorized / expired"
    subprocess.run(
        [
            str(PG_BIN / "pg_ctl.exe"),
            "-D",
            str(ROOT / "workdir/auth-postgres"),
            "-l",
            str(ROOT / "workdir/auth-postgres/server.log"),
            "-m",
            "fast",
            "-w",
            "restart",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=30,
    )
    assert access.authenticate(session=issued.secret).account.id == account.id
    assert access.authenticate(pat=pat.secret).credential.id == pat.token.id
    report["restart"] = (
        "PostgreSQL restart -> durable sessions/tokens/bootstrap -> same identities valid; "
        "bootstrap completed"
    )
    tokens.revoke(issued.secret, "session", pat.token.id, browser)
    denied("unauthorized", lambda: access.authenticate(pat=pat.secret))
    rotated = sessions.rotate(issued.secret, 1, browser)
    denied("unauthorized", lambda: access.authenticate(session=issued.secret))
    sessions.logout(
        rotated.secret,
        "session",
        1,
        "runtime-logout",
        Provenance(ORIGIN, "same-origin", rotated.csrf),
    )
    denied("unauthorized", lambda: access.authenticate(session=rotated.secret))
    report["revocation_rotation_logout"] = (
        "revoke/rotate/logout -> old credential denied, terminal state persisted -> "
        "revoked/rotated/revoked + unauthorized"
    )
    data, before = snapshot()
    raw = json.dumps(data)
    secrets = (PASSWORD, kit, issued.secret, issued.csrf, pat.secret, rotated.secret, rotated.csrf)
    assert all(secret not in raw for secret in secrets)
    assert "$argon2id$" in raw and digest(pat.secret) in raw
    report["secret_at_rest"] = (
        "all BC-002 tables inspected -> no raw password/kit/session/CSRF/PAT -> absent; "
        "Argon2id and SHA-256 only"
    )
    constraints = psql("""SELECT c.relname,p.conname,pg_get_constraintdef(p.oid)
      FROM pg_constraint p JOIN pg_class c ON c.oid=p.conrelid
      WHERE p.connamespace='identity'::regnamespace ORDER BY c.relname,p.conname""")
    OUTPUT.joinpath("schema-constraints.json").write_text(
        json.dumps(constraints, indent=2), encoding="utf-8"
    )
    report["constraints"] = (
        f"{len(constraints)} schema constraints inspected; composite project/account FK, "
        "uniqueness, states, hashes and timestamptz"
    )
    backup = ROOT / "workdir/identity-validation-backup.sql"
    subprocess.run(
        [
            str(PG_BIN / "pg_dump.exe"),
            "-h",
            "127.0.0.1",
            "-p",
            "55482",
            "-U",
            "auth_test",
            "--no-owner",
            "-f",
            str(backup),
            "local_identity_validation",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=30,
    )
    assert all(secret not in backup.read_text(encoding="utf-8") for secret in secrets)
    try:
        migrate(MIGRATION_DSN, "downgrade")
    except DBAPIError as error:
        assert "nonempty identity requires coordinated restore" in str(error)
    else:
        raise AssertionError("destructive rollback of initialized installation was allowed")
    assert snapshot()[1] == before
    report["populated_rollback_guard"] = (
        "initialized identity -> refuse destructive downgrade -> refused, same data digest"
    )
    clear_fixture()
    migrate(MIGRATION_DSN, "downgrade")
    assert (
        psql(
            "SELECT count(*) FROM pg_tables WHERE schemaname='identity' "
            "AND tablename<>'alembic_version'"
        )[0][0]
        == 0
    )
    assert psql("SELECT count(*) FROM identity.alembic_version")[0][0] == 0
    migrate(MIGRATION_DSN, "upgrade")
    assert psql("SELECT version_num FROM identity.alembic_version")[0][0] == "local_identity_v1"
    psql("DROP SCHEMA identity CASCADE")
    subprocess.run(
        [
            str(PG_BIN / "psql.exe"),
            "-h",
            "127.0.0.1",
            "-p",
            "55482",
            "-U",
            "auth_test",
            "-d",
            "local_identity_validation",
            "-v",
            "ON_ERROR_STOP=1",
            "-f",
            str(backup),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=30,
    )
    assert snapshot()[1] == before
    report["migration_rollback"] = (
        "empty downgrade -> base/no capability tables -> observed; reapply head -> observed; "
        "populated backup restored -> identical SHA-256"
    )
    report["restored_data_sha256"] = before
    report["final_state"] = (
        "local_identity_v1 restored; bootstrap completed; synthetic data preserved; "
        "no production deployment"
    )
    OUTPUT.joinpath("runtime-evidence.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()
