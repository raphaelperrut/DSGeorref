"""Durability, deferred commit failures and the existing Alembic rollback guard."""

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from threading import Event

import psycopg
import pytest
from dsgeorref.contexts.identity_access.adapters.local_identity.migration import migrate
from dsgeorref.contexts.identity_access.adapters.local_identity.oidc import ValidatingOidcProvider
from dsgeorref.contexts.identity_access.application.local_identity.federation import Federation
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest, uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from oidc_fixture import SignedProvider, config
from sqlalchemy.exc import DBAPIError
from test_canonical import target


@contextmanager
def reject_commit(dsn, action):
    assert action in {"MembershipChanged", "rotate", "revoke", "link"}
    with psycopg.connect(dsn) as connection:
        connection.execute("""CREATE FUNCTION identity.reject_candidate() RETURNS trigger
          LANGUAGE plpgsql AS $$ BEGIN
          IF NEW.outcome='COMMITTED' AND NEW.action = TG_ARGV[0] THEN
            RAISE EXCEPTION 'synthetic deferred commit failure';
          END IF; RETURN NEW; END $$""")
        connection.execute(
            """CREATE CONSTRAINT TRIGGER reject_candidate
          AFTER INSERT ON identity.observations DEFERRABLE INITIALLY DEFERRED
          FOR EACH ROW EXECUTE FUNCTION identity.reject_candidate(%s)"""
            % ("'" + action + "'")
        )
    try:
        yield
    finally:
        with psycopg.connect(dsn) as connection:
            connection.execute("DROP TRIGGER reject_candidate ON identity.observations")
            connection.execute("DROP FUNCTION identity.reject_candidate()")


def test_membership_commit_failure_rolls_back_idempotency_and_event(runtime, members):
    r = runtime
    project, account = uuid7(), target(r)
    r.member(project)
    with reject_commit(r.dsn, "MembershipChanged"), pytest.raises(Denied, match="internal_error"):
        members.add(r.issued.secret, "session", project, account.id, "viewer", "fail", r.browser())
    with r.uow() as store:
        assert store.get("memberships", {"project_id": project, "account_id": account.id}) is None
        assert not store.rows("requests", {"operation": "post_projects_projectid_members"})
        assert not store.rows("observations", {"action": "MembershipChanged"})
    # Retrying the same key succeeds after rollback; no poisoned idempotency record.
    assert (
        members.add(
            r.issued.secret, "session", project, account.id, "viewer", "fail", r.browser()
        ).account_id
        == account.id
    )


def test_rotation_and_revocation_commit_failure_leave_credentials_unchanged(runtime):
    r = runtime
    token = r.tokens.issue(r.issued.secret, "session", ["authorization:check"], "pat", r.browser())
    for action, call in (
        ("rotate", lambda: r.sessions.rotate(r.issued.secret, 1, r.browser())),
        (
            "revoke",
            lambda: r.tokens.revoke(r.issued.secret, "session", token.token.id, r.browser()),
        ),
    ):
        with reject_commit(r.dsn, action), pytest.raises(Denied, match="internal_error"):
            call()
    with r.uow() as store:
        assert len(store.rows("sessions", {"account_id": r.account.id})) == 1
        assert store.get("sessions", {"id": r.issued.session.id})["state"] == "active"
        assert store.get("tokens", {"id": token.token.id})["state"] == "active"
        assert not store.rows("observations", {"action": "rotate", "outcome": "COMMITTED"})
        assert not store.rows("observations", {"action": "revoke", "outcome": "COMMITTED"})


def test_link_commit_failure_exposes_no_link_or_session(runtime):
    r = runtime
    transport = SignedProvider("pending")
    federation = Federation(r.tx, ValidatingOidcProvider(config(), transport))
    state, transport.nonce = federation.begin("browser", r.browser(), r.issued.secret)
    with reject_commit(r.dsn, "link"), pytest.raises(Denied, match="internal_error"):
        federation.callback(state, "browser", "code")
    with r.uow() as store:
        assert not store.rows("oidc_links", {"account_id": r.account.id})
        assert len(store.rows("sessions", {"account_id": r.account.id})) == 1
        assert not store.rows("observations", {"action": "link"})
        assert store.get("oidc_transactions", {"state_hash": digest(state)})["state"] == "failed"
        attempt = store.get(
            "requests",
            {
                "operation": "get_auth_oidc_callback",
                "principal_id": r.account.id,
                "key_hash": digest(state),
            },
        )
        assert attempt is not None and attempt["outcome_id"] is None
    with pytest.raises(Denied, match="oidc_state_invalid"):
        federation.callback(state, "browser", "new-code")
    state, transport.nonce = federation.begin("browser", r.browser(), r.issued.secret)
    issued, linked = federation.callback(state, "browser", "fresh-code")
    assert linked and r.access.authenticate(session=issued.secret).account.id == r.account.id


def test_callback_replay_is_denied_before_failed_state_cleanup(runtime, monkeypatch):
    r = runtime
    transport = SignedProvider("pending")
    federation = Federation(r.tx, ValidatingOidcProvider(config(), transport))
    state, transport.nonce = federation.begin("browser", r.browser(), r.issued.secret)
    failed, release = Event(), Event()
    fail_callback = federation._fail_callback

    def delayed_cleanup(value):
        failed.set()
        assert release.wait(10)
        fail_callback(value)

    monkeypatch.setattr(federation, "_fail_callback", delayed_cleanup)
    with reject_commit(r.dsn, "link"), ThreadPoolExecutor(max_workers=1) as executor:
        first = executor.submit(federation.callback, state, "browser", "code")
        try:
            assert failed.wait(10)
            with pytest.raises(Denied, match="oidc_state_invalid"):
                federation.callback(state, "browser", "new-code")
            with r.uow() as store:
                assert store.get("oidc_transactions", {"state_hash": digest(state)})[
                    "state"
                ] == "pending"
                assert not store.rows("oidc_links", {"account_id": r.account.id})
                assert len(store.rows("sessions", {"account_id": r.account.id})) == 1
        finally:
            release.set()
        with pytest.raises(Denied, match="internal_error"):
            first.result(timeout=10)
    with r.uow() as store:
        assert store.get("oidc_transactions", {"state_hash": digest(state)})["state"] == "failed"


def test_callback_attempt_survives_unavailable_failed_state_cleanup(runtime, monkeypatch):
    r = runtime
    transport = SignedProvider("pending")
    federation = Federation(r.tx, ValidatingOidcProvider(config(), transport))
    state, transport.nonce = federation.begin("browser", r.browser(), r.issued.secret)

    def unavailable_cleanup(value):
        raise Denied("internal_error")

    monkeypatch.setattr(federation, "_fail_callback", unavailable_cleanup)
    with reject_commit(r.dsn, "link"), pytest.raises(Denied, match="internal_error"):
        federation.callback(state, "browser", "code")
    # A different server replay-signing key cannot turn the attempt into a fresh callback.
    monkeypatch.setattr(r.tx, "_replay_key", b"another-server-replay-key-value-32")
    with pytest.raises(Denied, match="oidc_state_invalid"):
        federation.callback(state, "browser", "new-code")
    with r.uow() as store:
        assert not store.rows("oidc_links", {"account_id": r.account.id})
        assert len(store.rows("sessions", {"account_id": r.account.id})) == 1


def test_concurrent_membership_replay_commits_exactly_once(runtime, members):
    r = runtime
    project, account = uuid7(), target(r)
    r.member(project)

    def add():
        return members.add(
            r.issued.secret, "session", project, account.id, "viewer", "concurrent", r.browser()
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        first, second = list(executor.map(lambda _: add(), range(2)))
    assert first == second
    with r.uow() as store:
        assert len(store.rows("memberships", {"project_id": project})) == 2
        assert len(store.rows("requests", {"operation": "post_projects_projectid_members"})) == 1
        assert len(store.rows("observations", {"action": "MembershipChanged"})) == 1


def test_existing_schema_populated_rollback_refuses_data_loss(runtime):
    r = runtime
    migration_dsn = os.environ["IDENTITY_MIGRATION_DSN"]
    with pytest.raises(DBAPIError, match="nonempty identity requires coordinated restore"):
        migrate(migration_dsn, "downgrade")
    assert r.access.authenticate(session=r.issued.secret).account.id == r.account.id
    with psycopg.connect(r.dsn) as connection:
        assert (
            connection.execute("SELECT version_num FROM identity.alembic_version").fetchone()[0]
            == "identity_link_binding_v2"
        )


def test_empty_schema_downgrade_and_reapply(database):
    with psycopg.connect(database) as connection:
        connection.execute("""TRUNCATE identity.accounts,identity.bootstrap,identity.memberships,
          identity.oidc_links,identity.sessions,identity.tokens,identity.requests,
          identity.oidc_transactions,identity.ceremonies,identity.observations CASCADE""")
    migration_dsn = os.environ["IDENTITY_MIGRATION_DSN"]
    migrate(migration_dsn, "downgrade")
    with psycopg.connect(database) as connection:
        assert connection.execute("SELECT to_regclass('identity.accounts')").fetchone()[0] is None
    migrate(migration_dsn, "upgrade")
    with psycopg.connect(database) as connection:
        assert (
            connection.execute("SELECT state FROM identity.bootstrap").fetchone()[0] == "available"
        )


@pytest.mark.skipif(
    not os.environ.get("IDENTITY_TEST_PGDATA"), reason="explicit disposable cluster required"
)
def test_restart_retains_membership_credentials_and_bootstrap(runtime, members):
    r = runtime
    project, account = uuid7(), target(r)
    r.member(project)
    added = members.add(
        r.issued.secret, "session", project, account.id, "viewer", "restart", r.browser()
    )
    token = r.tokens.issue(r.issued.secret, "session", ["authorization:check"], "pat", r.browser())
    data = Path(os.environ["IDENTITY_TEST_PGDATA"]).resolve()
    assert data.name == "instance-postgres-ready" and data.parent.name == "workdir"
    # Windows server descendants inherit pipe handles; use a file, not PIPE.
    with (data / "restart-command.log").open("wb") as output:
        subprocess.run(
            [
                os.environ["IDENTITY_TEST_PG_CTL"],
                "-D",
                str(data),
                "-l",
                str(data / "server.log"),
                "-m",
                "fast",
                "-w",
                "restart",
            ],
            check=True,
            stdout=output,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
    assert added in members.list(r.issued.secret, "session", project)
    assert r.access.authenticate(pat=token.secret).credential.id == token.token.id
    with r.uow() as store:
        assert store.get("bootstrap", {"singleton": True})["state"] == "completed"
