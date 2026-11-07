"""Negative authorization and ownership cases against real PostgreSQL."""

from dataclasses import replace
from importlib import import_module

import pytest
from conftest import ADAPTER, APPLICATION, ORIGIN, POLICY, synthetic_profile
from dsgeorref.contexts.identity_access.adapters.local_identity.oidc import ValidatingOidcProvider
from dsgeorref.contexts.identity_access.application.local_identity.federation import Federation
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance, WebPolicy
from oidc_fixture import SignedProvider, config
from test_canonical import target


def test_rotation_owns_only_current_session(runtime):
    r = runtime
    with r.uow() as store:
        other = r.tx.session(store, r.account.id)
    with pytest.raises(Denied, match="forbidden"):
        r.sessions.rotate(r.issued.secret, 1, r.browser(other))
    rotated = r.sessions.rotate(r.issued.secret, 1, r.browser())
    assert r.access.authenticate(session=other.secret).credential.id == other.session.id
    assert r.access.authenticate(session=rotated.secret).credential.id == rotated.session.id
    with pytest.raises(Denied, match="unauthorized"):
        r.sessions.rotate(r.issued.secret, 1, r.browser())
    r.access.policy = replace(r.access.policy, authentication_actions=frozenset())
    with pytest.raises(Denied, match="forbidden"):
        r.sessions.rotate(rotated.secret, 1, r.browser(rotated))


def test_linking_and_unlinking_cannot_take_other_account(runtime):
    r = runtime
    stranger = target(r)
    with r.uow() as store:
        other = r.tx.session(store, stranger.id)
    transport = SignedProvider("pending")
    federation = Federation(r.tx, ValidatingOidcProvider(config(), transport))
    state, transport.nonce = federation.begin("browser", r.browser(other), other.secret)
    linked, _ = federation.callback(state, "browser", "code")
    with pytest.raises(Denied, match="identity_link_conflict"):
        federation.unlink(r.issued.secret, linked.session.oidc_link_id, r.browser())
    state, transport.nonce = federation.begin("browser", r.browser(), r.issued.secret)
    with pytest.raises(Denied, match="identity_link_conflict"):
        federation.callback(state, "browser", "code")
    assert r.access.authenticate(session=linked.secret).account.id == stranger.id
    r.access.policy = replace(r.access.policy, authentication_actions=frozenset())
    with pytest.raises(Denied, match="oidc_state_invalid"):
        federation.begin("browser", r.browser(), r.issued.secret)


@pytest.mark.parametrize("fault", ["csrf", "role", "target", "duplicate", "replay", "project"])
def test_membership_failure_has_no_partial_success(runtime, members, fault):
    r = runtime
    project, account = uuid7(), target(r)
    r.member(project)
    role, key, request = "viewer", "add", r.browser()
    if fault == "csrf":
        request = Provenance(ORIGIN, "same-origin", "wrong")
    if fault == "role":
        role = "instance_administrator"
    if fault == "target":
        account = replace(account, id=uuid7())
    if fault in {"duplicate", "replay"}:
        members.add(r.issued.secret, "session", project, account.id, role, key, request)
        role, key = ("editor", key) if fault == "replay" else (role, "new-key")
    if fault == "project":
        members = import_module(APPLICATION + ".memberships").Memberships(r.tx, lambda *args: False)
    with r.uow() as store:
        before = store.rows("memberships", {"project_id": project})
        requests = store.rows("requests", {"operation": "post_projects_projectid_members"})
    with pytest.raises(Denied):
        members.add(r.issued.secret, "session", project, account.id, role, key, request)
    with r.uow() as store:
        assert store.rows("memberships", {"project_id": project}) == before
        assert store.rows("requests", {"operation": "post_projects_projectid_members"}) == requests


def test_scope_revision_and_account_state_are_reread(runtime, members):
    r = runtime
    project = uuid7()
    r.member(project)
    token = r.tokens.issue(
        r.issued.secret, "session", ["project_member:create"], "pat", r.browser(), project
    )
    account = target(r)
    with pytest.raises(Denied, match="forbidden"):
        members.list(token.secret, "pat", project)
    with r.uow() as store:
        store.update(
            "memberships",
            {"project_id": project, "account_id": r.account.id},
            {"role": "viewer", "revision": 2},
        )
    with pytest.raises(Denied, match="forbidden"):
        members.add(token.secret, "pat", project, account.id, "viewer", "denied", None)
    with r.uow() as store:
        store.update("accounts", {"id": r.account.id}, {"state": "inactive", "revision": 2})
    with pytest.raises(Denied, match="unauthorized"):
        members.list(r.issued.secret, "session", project)


def test_missing_or_modified_policy_fails_closed(runtime, tmp_path):
    build = import_module(ADAPTER + ".runtime").build_transactions
    path = tmp_path / "policy.json"
    for content in (None, "{}", POLICY.read_text().replace('"deny"', '"allow"')):
        if content is not None:
            path.write_text(content)
        with pytest.raises(Denied, match="internal_error"):
            build(
                runtime.dsn,
                synthetic_profile(),
                WebPolicy(ORIGIN),
                lambda *args: True,
                b"x" * 32,
                path,
            )


def test_unavailable_throttle_or_project_authority_fails_closed(runtime, members):
    r = runtime
    project = uuid7()
    r.member(project)
    r.tx.eligibility = lambda *args: None
    with pytest.raises(Denied, match="rate_limited"):
        members.list(r.issued.secret, "session", project)
    unknown = import_module(APPLICATION + ".memberships").Memberships(r.tx, lambda *args: None)
    with pytest.raises(Denied, match="internal_error"):
        unknown.list(r.issued.secret, "session", project)
