"""Resource decisions use current identity state and never confer execution rights."""

from dataclasses import replace
from importlib import import_module

import pytest
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied

from .conftest import ADAPTER, CONTRACT


@pytest.mark.parametrize("role", ["owner", "editor", "reviewer", "viewer"])
def test_role_project_operation_access(runtime, authorization, role):
    r = runtime
    project, other = uuid7(), uuid7()
    r.member(project, role)

    def check(action, kind, target):
        return authorization.check(r.issued.secret, "session", action, kind, target)

    assert check("project_member:list", "project", project)["allowed"]
    assert check("project_member:create", "project", project)["allowed"] is (role == "owner")
    assert not check("project_member:list", "project", other)["allowed"]
    assert not check("project_member:list", "account", r.account.id)["allowed"]
    assert check("token:create", "account", r.account.id)["allowed"]
    assert not check("token:create", "account", other)["allowed"]
    assert not check("instance:bootstrap", "account", r.account.id)["allowed"]
    assert not check("project_member:list", "project", "../private")["allowed"]
    assert not check("project_member:list", None, project)["allowed"]
    for kind in ("artifact", "artifact_path", "physical_path"):
        assert check("artifact_manifest:read", kind, other) == {
            "allowed": False,
            "policyVersion": "1.1.0",
            "reasonCode": "access_denied",
        }
    with pytest.raises(Denied, match="validation_failed"):
        check("unregistered", "project", project)


def test_each_use_rechecks_membership_credential_and_policy(runtime, authorization):
    r = runtime
    project = uuid7()
    r.member(project)

    def query():
        return authorization.check(
            r.issued.secret, "session", "project_member:create", "project", project
        )

    assert query()["allowed"]
    with r.uow() as store:
        store.update(
            "memberships",
            {"project_id": project, "account_id": r.account.id},
            {"role": "viewer", "revision": 2},
        )
    assert not query()["allowed"]
    r.tx.access.policy = replace(r.tx.access.policy, version="stale")
    with pytest.raises(Denied, match="internal_error"):
        query()
    r.tx.access.policy = replace(r.tx.access.policy, version="1.1.0")
    r.sessions.logout(r.issued.secret, "session", 1, "logout", r.browser())
    with pytest.raises(Denied, match="unauthorized"):
        query()


@pytest.mark.parametrize("exists", [False, None, "true"])
def test_project_authority_is_required(runtime, exists):
    r = runtime
    project = uuid7()
    r.member(project)
    service = import_module(ADAPTER).build_authorization(r.tx, lambda store, pid: exists, CONTRACT)
    if exists is False:
        assert not service.check(
            r.issued.secret, "session", "project_member:list", "project", project
        )["allowed"]
    else:
        with pytest.raises(Denied, match="internal_error"):
            service.check(r.issued.secret, "session", "project_member:list", "project", project)


def test_audit_is_durable_bounded_and_mandatory(runtime, authorization, monkeypatch):
    r = runtime
    assert authorization.check(r.issued.secret, "session", "token:create", "account", r.account.id)[
        "allowed"
    ]
    assert not authorization.check(r.issued.secret, "session", "token:create", "account", uuid7())[
        "allowed"
    ]
    with r.uow() as store:
        rows = store.rows("observations", {"action": "get_authorization_check"})
        assert {row["outcome"] for row in rows} == {"COMMITTED", "DENIED"}
        assert r.issued.secret not in str(rows)
        assert all(row["actor_id"] == r.account.id for row in rows)
        cls = type(store)

    def unavailable(*args, **kwargs):
        raise Denied("internal_error")

    monkeypatch.setattr(cls, "audit", unavailable)
    with pytest.raises(Denied, match="internal_error"):
        authorization.check(r.issued.secret, "session", "token:create", "account", r.account.id)


def test_missing_or_drifted_contract_fails_closed(runtime, tmp_path):
    build = import_module(ADAPTER).build_authorization
    with pytest.raises(Denied, match="internal_error"):
        build(runtime.tx, lambda store, pid: True, tmp_path / "absent")
    drift = tmp_path / "contract.json"
    drift.write_text(CONTRACT.read_text().replace('"1.0.0"', '"2.0.0"'))
    with pytest.raises(Denied, match="internal_error"):
        build(runtime.tx, lambda store, pid: True, drift)


def test_eligibility_and_database_failure_never_fall_back(runtime, authorization):
    r = runtime
    r.tx.eligibility = lambda store, operation, actor: False
    with pytest.raises(Denied, match="rate_limited"):
        authorization.check(r.issued.secret, "session", "token:create", "account", r.account.id)
    r.tx.access.uow = type(r.uow)("host=127.0.0.1 port=1 dbname=absent user=absent")
    with pytest.raises(Denied, match="internal_error"):
        authorization.check(r.issued.secret, "session", "token:create", "account", r.account.id)
