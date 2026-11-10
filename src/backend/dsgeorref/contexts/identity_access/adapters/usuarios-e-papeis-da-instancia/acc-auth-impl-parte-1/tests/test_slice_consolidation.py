"""STORY-0042 integration against the published BC-002 instance policy."""

import pytest
from dsgeorref.contexts.identity_access.adapters.local_identity.oidc import ValidatingOidcProvider
from dsgeorref.contexts.identity_access.application.local_identity.federation import Federation
from dsgeorref.contexts.identity_access.application.local_identity.recovery import (
    AdministrativeRecovery,
)
from dsgeorref.contexts.identity_access.domain.local_identity.credentials import uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from oidc_fixture import SignedProvider, config


def test_story_0042_slice_consolidation(runtime, members):
    project, other_project = uuid7(), uuid7()
    runtime.member(project, "owner")
    runtime.member(other_project, "owner")
    transport = SignedProvider("pending")
    federation = Federation(runtime.tx, ValidatingOidcProvider(config(), transport))

    state, transport.nonce = federation.begin("browser", runtime.browser(), runtime.issued.secret)
    federated, linked = federation.callback(state, "browser", "signed-code")
    assert linked
    expected_members = members.list(runtime.issued.secret, "session", project)
    assert [(row.account_id, row.role) for row in expected_members] == [
        (runtime.account.id, "owner")
    ]
    assert members.list(federated.secret, "session", project) == expected_members

    pat = runtime.tokens.issue(
        federated.secret,
        "session",
        ["project_member:list"],
        "project-pat",
        runtime.browser(federated),
        project,
    )
    assert members.list(pat.secret, "pat", project) == expected_members
    with pytest.raises(Denied, match=r"^forbidden$"):
        members.list(pat.secret, "pat", other_project)

    recovery = AdministrativeRecovery(
        runtime.tx, lambda account, ceremony: account == runtime.account.id
    )
    assert (
        recovery.recover(
            runtime.account.id, runtime.recovery, "rotated-password-for-tests-only", uuid7()
        )
        != runtime.recovery
    )

    for secret, kind in (
        (runtime.issued.secret, "session"),
        (federated.secret, "session"),
        (pat.secret, "pat"),
    ):
        with pytest.raises(Denied, match=r"^unauthorized$"):
            members.list(secret, kind, project)

    recovered = runtime.accounts.login(
        runtime.account.username, "rotated-password-for-tests-only", "recovered", runtime.browser()
    )
    assert members.list(recovered.secret, "session", project) == expected_members
