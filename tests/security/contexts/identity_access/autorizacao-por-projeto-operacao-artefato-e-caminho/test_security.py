"""Adversarial checks of the existing authority; no alternative policy or I/O."""

from dataclasses import replace
from datetime import timedelta
from importlib import import_module

import pytest
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest, uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied

from .conftest import ADAPTER, CONTRACT


def test_epic_010_seguranca_happy_path(runtime, authorization):
    r = runtime
    project = uuid7()
    r.member(project)
    assert authorization.tx is r.tx
    assert authorization.check(
        r.issued.secret, "session", "project_member:list", "project", project
    ) == {"allowed": True, "policyVersion": "1.1.0", "reasonCode": "granted"}
    with r.uow() as store:
        rows = store.rows("observations", {"action": "get_authorization_check"})
        assert len(rows) == 1
        row = rows[0]
        assert row["actor_id"] == r.account.id and row["target_id"] == project
        assert row["outcome"] == "COMMITTED" and row["policy_version"] == "1.1.0"
        assert row["correlation_id"].version == 7 and row["observed_at"] is not None


@pytest.mark.parametrize(
    "case",
    [
        "cross_project",
        "other_account",
        "artifact",
        "artifact_path",
        "physical_path",
        "traversal",
        "url",
        "missing_type",
        "unexpected_type",
        "unknown_action",
    ],
)
def test_epic_010_seguranca_negative_paths(runtime, authorization, case):
    r = runtime
    project = uuid7()
    r.member(project)
    action, kind, target = "project_member:list", "project", project
    if case == "cross_project":
        target = uuid7()
    elif case == "other_account":
        action, kind, target = "token:create", "account", uuid7()
    elif case in {"artifact", "artifact_path", "physical_path"}:
        action, kind = "artifact_manifest:read", case
    elif case in {"traversal", "url"}:
        target = "../private-synthetic" if case == "traversal" else "https://example.test/private"
    elif case == "missing_type":
        kind = None
    elif case == "unexpected_type":
        kind = {"project": True}
    elif case == "unknown_action":
        action = "unregistered-synthetic"
    if case == "unknown_action":
        with pytest.raises(Denied) as rejected:
            authorization.check(r.issued.secret, "session", action, kind, target)
        assert rejected.value.code == "validation_failed"
    else:
        assert authorization.check(r.issued.secret, "session", action, kind, target) == {
            "allowed": False,
            "policyVersion": "1.1.0",
            "reasonCode": "access_denied",
        }
    with r.uow() as store:
        rows = store.rows("observations", {"action": "get_authorization_check"})
        assert len(rows) == 1 and rows[0]["outcome"] == "DENIED"
        assert rows[0]["reason_code"] in {"access_denied", "validation_failed"}
        assert "private-synthetic" not in str(rows) and "example.test" not in str(rows)


@pytest.mark.parametrize("response", [None, "true", 1, {}, []])
def test_unexpected_project_authority_fails_closed(runtime, response):
    r = runtime
    project = uuid7()
    r.member(project)
    service = import_module(ADAPTER).build_authorization(
        r.tx, lambda store, target: response, CONTRACT
    )
    with pytest.raises(Denied) as rejected:
        service.check(r.issued.secret, "session", "project_member:list", "project", project)
    assert rejected.value.code == "internal_error"
    with r.uow() as store:
        rows = store.rows("observations", {"action": "get_authorization_check"})
        assert len(rows) == 1 and rows[0]["outcome"] == "DENIED"


@pytest.mark.parametrize("response", [False, None, "true", 1])
def test_abuse_eligibility_is_conjunctive(runtime, authorization, response):
    r = runtime
    r.tx.eligibility = lambda store, operation, actor: response
    with pytest.raises(Denied) as rejected:
        authorization.check(r.issued.secret, "session", "token:create", "account", r.account.id)
    assert rejected.value.code == "rate_limited"
    with r.uow() as store:
        rows = store.rows("observations", {"action": "get_authorization_check"})
        assert len(rows) == 1 and rows[0]["outcome"] == "DENIED"


@pytest.mark.parametrize("change", ["membership", "account", "expired", "revoked", "policy"])
def test_previous_allow_never_survives_authority_change(
    runtime, authorization, change, monkeypatch
):
    r = runtime
    project = uuid7()
    r.member(project)

    def query():
        return authorization.check(
            r.issued.secret, "session", "project_member:create", "project", project
        )

    assert query()["allowed"] is True
    with r.uow() as store:
        if change == "membership":
            store.update(
                "memberships",
                {"project_id": project, "account_id": r.account.id},
                {"role": "viewer", "revision": 2},
            )
        elif change == "account":
            store.update("accounts", {"id": r.account.id}, {"state": "inactive", "revision": 2})
        elif change == "expired":
            # Advance the trusted clock; credential identity/expiry remain immutable.
            monkeypatch.setattr(
                type(store), "now", lambda store: r.issued.session.expires_at + timedelta(seconds=1)
            )
        elif change == "revoked":
            store.update(
                "sessions", {"id": r.issued.session.id}, {"state": "revoked", "revision": 2}
            )
    if change == "membership":
        assert query()["allowed"] is False
    else:
        if change == "policy":
            r.tx.access.policy = replace(r.tx.access.policy, version="stale")
        with pytest.raises(Denied) as rejected:
            query()
        assert rejected.value.code == ("internal_error" if change == "policy" else "unauthorized")


def test_query_permission_does_not_expand_pat_scope(runtime, authorization):
    r = runtime
    pat = r.tokens.issue(
        r.issued.secret, "session", ["authorization:check"], "security-query-only", r.browser()
    )
    assert (
        authorization.check(pat.secret, "pat", "authorization:check", "account", r.account.id)[
            "allowed"
        ]
        is True
    )
    assert (
        authorization.check(pat.secret, "pat", "token:create", "account", r.account.id)["allowed"]
        is False
    )


def test_persisted_secret_minimization_and_audit_allowlist(runtime, authorization, caplog, capsys):
    r = runtime
    sentinel = "synthetic-invalid-credential-only"
    with pytest.raises(Denied) as rejected:
        authorization.check(sentinel, "session", "token:create", "account", r.account.id)
    assert rejected.value.code == "unauthorized"
    authorization.check(r.issued.secret, "session", "token:create", "account", r.account.id)
    with r.uow() as store:
        session = store.get("sessions", {"id": r.issued.session.id})
        assert session["secret_hash"] == digest(r.issued.secret)
        rows = store.rows("observations", {"action": "get_authorization_check"})
        assert len(rows) == 2
        assert all(
            set(row)
            == {
                "id",
                "actor_id",
                "action",
                "target_id",
                "outcome",
                "policy_version",
                "correlation_id",
                "observed_at",
                "reason_code",
            }
            for row in rows
        )
    captured = capsys.readouterr()
    output = str(rows) + caplog.text + captured.out + captured.err + str(rejected.value)
    assert all(
        value not in output
        for value in (
            sentinel,
            r.issued.secret,
            r.issued.csrf,
            r.recovery,
            r.account.password_hash,
            session["secret_hash"],
            session["csrf_hash"],
        )
    )
