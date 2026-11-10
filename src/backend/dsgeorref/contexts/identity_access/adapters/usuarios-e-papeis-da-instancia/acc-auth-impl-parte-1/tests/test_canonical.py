"""Canonical requirements reuse real identity services with the approved grants."""

from dataclasses import asdict, replace

import pytest
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest, uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Account, Denied
from test_requirements import (
    test_req_auth_impl_001 as test_req_auth_impl_001,
)
from test_requirements import (
    test_req_auth_impl_0010 as test_req_auth_impl_0010,
)
from test_requirements import (
    test_req_auth_impl_002 as test_req_auth_impl_002,
)
from test_requirements import (
    test_req_auth_impl_003 as test_req_auth_impl_003,
)
from test_requirements import (
    test_req_auth_impl_005 as test_req_auth_impl_005,
)
from test_requirements import (
    test_req_auth_impl_006 as test_req_auth_impl_006,
)
from test_requirements import (
    test_req_auth_impl_008 as test_req_auth_impl_008,
)
from test_requirements import (
    test_req_auth_impl_009 as test_req_auth_impl_009,
)


def target(runtime):
    account = Account(uuid7(), "target", runtime.account.password_hash, digest("synthetic-kit"))
    with runtime.uow() as store:
        store.insert("accounts", asdict(account))
    return account


@pytest.mark.parametrize("role", ["owner", "editor", "reviewer", "viewer"])
def test_role_project_operation_access(runtime, members, role):
    r = runtime
    project, other = uuid7(), uuid7()
    r.member(project, role)
    account = target(r)
    assert members.list(r.issued.secret, "session", project)[0].role == role
    if role == "owner":
        added = members.add(
            r.issued.secret, "session", project, account.id, "viewer", "add", r.browser()
        )
        assert added.role == "viewer"
        assert (
            members.add(
                r.issued.secret, "session", project, account.id, "viewer", "add", r.browser()
            )
            == added
        )
        with r.uow() as store:
            assert store.get(
                "memberships", {"project_id": project, "account_id": account.id}
            ) == asdict(added)
    else:
        with pytest.raises(Denied, match="forbidden"):
            members.add(
                r.issued.secret, "session", project, account.id, "viewer", "add", r.browser()
            )
    # Even the installation administrator must have a current project membership.
    with pytest.raises(Denied, match="forbidden"):
        members.list(r.issued.secret, "session", other)


def test_req_auth_impl_004(runtime):
    r = runtime
    project = uuid7()
    r.member(project)
    issued = r.tokens.issue(
        r.issued.secret, "session", ["project_member:list"], "pat", r.browser(), project
    )
    assert r.access.authenticate(pat=issued.secret).credential.id == issued.token.id
    with r.uow() as store:
        row = store.get("tokens", {"id": issued.token.id})
        assert row["secret_hash"] == digest(issued.secret) and issued.secret not in str(row)
        store.update(
            "memberships",
            {"project_id": project, "account_id": r.account.id},
            {"role": "viewer", "revision": 2},
        )
        stranger = target_account = replace(
            r.account, id=uuid7(), username="stranger", administrator=False
        )
        store.insert("accounts", asdict(target_account))
        foreign = r.tx.session(store, stranger.id)
    with pytest.raises(Denied, match="forbidden"):
        r.tokens.revoke(foreign.secret, "session", issued.token.id, r.browser(foreign))
    r.tokens.revoke(r.issued.secret, "session", issued.token.id, r.browser())
    with pytest.raises(Denied, match="unauthorized"):
        r.access.authenticate(pat=issued.secret)
    with r.uow() as store:
        assert store.get("tokens", {"id": issued.token.id})["state"] == "revoked"
