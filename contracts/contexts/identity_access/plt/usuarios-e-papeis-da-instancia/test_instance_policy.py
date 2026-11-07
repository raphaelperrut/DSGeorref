"""Conformance of the instance policy against the existing BC-002 freeze."""

import json
import runpy
from pathlib import Path
from typing import Any

import pytest

HERE = Path(__file__).resolve().parent
FREEZE = HERE.parent / "contas-locais-bootstrap-unico-sessoes-tokens-e-adapter"
POLICY = json.loads((HERE / "policy.json").read_text(encoding="utf-8"))
CONTRACT = json.loads((FREEZE / "contract.json").read_text(encoding="utf-8"))
RULES = runpy.run_path(str(FREEZE / "conformance.py"))


@pytest.fixture
def context() -> dict[str, Any]:
    """Synthetic server snapshot for contract evaluation, without production I/O."""
    return {
        "account_id": "alice",
        "target_account_id": "alice",
        "account_state": "active",
        "credential_state": "active",
        "project_id": "project-a",
        "membership_project_id": "project-a",
        "membership_account_id": "alice",
        "role": "owner",
        "grant_current": True,
        "target_role": "viewer",
        "token_scopes": None,
        "token_project_id": None,
    }


def decision(operation: str, context: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    """Interpret the published grant table and delegate consequences to the freeze."""
    row = POLICY["operations"][operation]
    action, source = row["permission"], row["grant_source"]
    account = context.get("account_id")
    active = bool(account) and context.get("account_state") == "active"
    principal_valid = active and context.get("credential_state") == "active"
    if source == "central_policy":
        grant = action in POLICY["self_service_grants"] and account == context.get(
            "target_account_id"
        )
    elif source == "project_membership":
        grant = (
            bool(context.get("project_id"))
            and context.get("project_id") == context.get("membership_project_id")
            and account == context.get("membership_account_id")
            and action in POLICY["project_role_grants"].get(context.get("role"), [])
        )
    else:
        grant = context.get(source) is True
    grant = grant and context.get("grant_current") is True
    scopes = context.get("token_scopes")
    if scopes is not None:
        project = context.get("project_id") if source == "project_membership" else None
        grant = grant and action in scopes and project == context.get("token_project_id")
    guards = CONTRACT["operations"][operation]["guards"]
    facts = dict.fromkeys((guard["fact"] for guard in guards), True) | overrides
    if "principal_valid" in facts:
        facts["principal_valid"] = principal_valid and facts["principal_valid"] is True
    if "account_active" in facts:
        facts["account_active"] = active and facts["account_active"] is True
    if "role_registered" in facts:
        facts["role_registered"] = (
            context.get("target_role") in POLICY["project_roles"]
            and facts["role_registered"] is True
        )
    facts["permission_granted"] = grant and facts["permission_granted"] is True
    return RULES["decide_operation"](CONTRACT, operation, facts)


def assert_denied(result: dict[str, Any]) -> None:
    assert result["allowed"] is False
    assert result["effects"] == []
    assert result["status"] >= 400


def test_epic_009_politica() -> None:
    assert POLICY["default_decision"] == "deny"
    assert POLICY["project_roles"] == CONTRACT["policies"]["authorization"]["roles"]
    assert POLICY["role_grant_rule"] == "explicit_grant_for_current_membership"
    assert POLICY["instance_grant_rule"] == "explicit_grant_for_account"
    assert POLICY["self_service_target"] == "authenticated_account"
    assert POLICY["administrator_project_bypass"] is False
    assert POLICY["grant_must_be_current"] is True
    assert POLICY["self_service_grants"] == [
        "session:revoke",
        "token:create",
        "authorization:check",
    ]
    assert POLICY["project_role_grants"] == {
        "owner": ["project_member:list", "project_member:create"],
        "editor": ["project_member:list"],
        "reviewer": ["project_member:list"],
        "viewer": ["project_member:list"],
    }
    operations = POLICY["operations"]
    assert set(operations) == set(CONTRACT["operations"])
    assert {key: row["grant_source"] for key, row in operations.items()} == {
        "post_auth_bootstrap": "installation_capability",
        "post_auth_session": "authentication_policy",
        "get_auth_oidc_callback": "authentication_policy",
        "delete_auth_session": "central_policy",
        "post_auth_tokens": "central_policy",
        "get_projects_projectid_members": "project_membership",
        "post_projects_projectid_members": "project_membership",
        "get_authorization_check": "central_policy",
    }
    for key, row in operations.items():
        frozen = CONTRACT["operations"][key]
        assert row["permission"] == frozen["permission"]
        facts = dict.fromkeys((guard["fact"] for guard in frozen["guards"]), True)
        for guard in frozen["guards"]:
            missing = facts.copy()
            del missing[guard["fact"]]
            denied = RULES["decide_operation"](CONTRACT, key, missing)
            assert denied["allowed"] is False
            assert denied["effects"] == []
            rejected = RULES["decide_operation"](CONTRACT, key, facts | {guard["fact"]: False})
            assert rejected["code"] == guard["error"]
            assert rejected["status"] == frozen["errors"][guard["error"]]
            assert rejected["effects"] == []


def test_account_transition_guards() -> None:
    assert POLICY["account_machine"] == "account"
    machine = CONTRACT["machines"]["account"]
    assert set(machine["states"]) == {"absent", "active", "inactive", "locked"}
    assert {(edge["from"], edge["event"], edge["to"]) for edge in machine["transitions"]} == {
        ("absent", "create", "active"),
        ("active", "deactivate", "inactive"),
        ("locked", "deactivate", "inactive"),
        ("inactive", "activate", "active"),
        ("active", "lock", "locked"),
        ("locked", "unlock", "active"),
    }
    for edge in machine["transitions"]:
        facts = dict.fromkeys(edge["requires"], True)
        step = (CONTRACT, "account", edge["from"], edge["event"])
        assert RULES["next_state"](*step, facts) == edge["to"]
        for guard in edge["requires"]:
            with pytest.raises(RULES["ContractViolation"]):
                RULES["next_state"](*step, facts | {guard: False})


def test_req_auth_impl_007() -> None:
    throttle = POLICY["throttling"]
    assert throttle["requirement"] == CONTRACT["requirement"] == "REQ-AUTH-IMPL-007"
    assert throttle["evidence"] == CONTRACT["policies"]["throttling"]["evidence_schema"]
    assert throttle["machine"] == "throttle"
    assert throttle["eligible_states"] == ["open"]
    assert set(CONTRACT["machines"]["throttle"]["states"]) == {"open", "limited", "locked"}
    examples = json.loads((FREEZE / "examples.json").read_text(encoding="utf-8"))
    boundary = json.loads((FREEZE / "boundary-evidence.schema.json").read_text(encoding="utf-8"))
    observations = examples["throttle_observations"]
    assert observations
    for observation in observations:
        RULES["validate_boundary"](observation, boundary, throttle["machine"])


@pytest.mark.parametrize("role", ["owner", "editor", "reviewer", "viewer"])
@pytest.mark.parametrize(
    "operation", ["get_projects_projectid_members", "post_projects_projectid_members"]
)
def test_project_role_matrix(role: str, operation: str, context: dict[str, Any]) -> None:
    result = decision(operation, context | {"role": role})
    expected = operation == "get_projects_projectid_members" or role == "owner"
    assert result["allowed"] is expected
    if not expected:
        assert_denied(result)


@pytest.mark.parametrize("target_role", ["owner", "editor", "reviewer", "viewer"])
def test_owner_adds_existing_account(target_role: str, context: dict[str, Any]) -> None:
    result = decision(
        "post_projects_projectid_members",
        context | {"target_account_id": "bob", "target_role": target_role},
    )
    assert result["allowed"] is True
    assert_denied(decision("post_projects_projectid_members", context, target_account_exists=False))
    assert_denied(decision("post_projects_projectid_members", context | {"target_role": "unknown"}))


@pytest.mark.parametrize(
    "operation", ["delete_auth_session", "post_auth_tokens", "get_authorization_check"]
)
@pytest.mark.parametrize(
    "role", ["owner", "editor", "reviewer", "viewer", "instance_administrator"]
)
def test_self_service_is_own_account_only(
    operation: str, role: str, context: dict[str, Any]
) -> None:
    own = context | {"role": role}
    assert decision(operation, own)["allowed"] is True
    assert_denied(decision(operation, own | {"target_account_id": "bob"}))


@pytest.mark.parametrize(
    "operation", ["get_projects_projectid_members", "post_projects_projectid_members"]
)
@pytest.mark.parametrize(
    "mutation",
    [
        {"project_id": "project-b"},
        {"membership_account_id": "bob"},
        {"membership_project_id": None, "instance_administrator": True},
        {"role": "unknown"},
        {"role": None, "client_role": "owner"},
        {"grant_current": False},
        {"grant_current": "true"},
        {"token_scopes": [], "token_project_id": "project-a"},
        {
            "token_scopes": ["project_member:list", "project_member:create"],
            "token_project_id": "project-b",
        },
    ],
)
def test_project_grants_fail_closed(
    operation: str, mutation: dict[str, Any], context: dict[str, Any]
) -> None:
    assert_denied(decision(operation, context | mutation))


@pytest.mark.parametrize(
    "operation",
    [
        "delete_auth_session",
        "post_auth_tokens",
        "get_authorization_check",
        "get_projects_projectid_members",
        "post_projects_projectid_members",
    ],
)
@pytest.mark.parametrize(
    "mutation",
    [
        {"account_id": None},
        {"account_state": "inactive"},
        {"account_state": "locked"},
        {"credential_state": "revoked"},
        {"credential_state": "expired"},
        {"grant_current": False},
    ],
)
def test_current_identity_and_grant_required(
    operation: str, mutation: dict[str, Any], context: dict[str, Any]
) -> None:
    assert_denied(decision(operation, context | mutation))


PROTECTIVE_GUARDS = [
    (operation, guard["fact"])
    for operation, row in CONTRACT["operations"].items()
    for guard in row["guards"]
    if guard["fact"]
    in {
        "authority_ready",
        "policy_ready",
        "audit_ready",
        "fallback_disabled",
        "throttle_open",
        "provenance_valid",
        "commit_ready",
        "scope_subset",
        "expiry_valid",
        "role_registered",
    }
]


@pytest.mark.parametrize(("operation", "guard"), PROTECTIVE_GUARDS)
def test_matrix_cannot_bypass_frozen_guards(
    operation: str, guard: str, context: dict[str, Any]
) -> None:
    authorized = context | {"installation_capability": True, "authentication_policy": True}
    assert decision(operation, authorized)["allowed"] is True
    assert_denied(decision(operation, authorized, **{guard: False}))


@pytest.mark.parametrize(
    "operation", ["post_auth_bootstrap", "post_auth_session", "get_auth_oidc_callback"]
)
@pytest.mark.parametrize(
    "role", ["owner", "editor", "reviewer", "viewer", "instance_administrator"]
)
def test_authentication_has_no_role_grant(
    operation: str, role: str, context: dict[str, Any]
) -> None:
    assert_denied(decision(operation, context | {"role": role}))


@pytest.mark.parametrize(
    "operation",
    [
        "get_projects_projectid_members",
        "post_projects_projectid_members",
        "delete_auth_session",
        "post_auth_tokens",
        "get_authorization_check",
    ],
)
def test_pat_with_eligible_scope(operation: str, context: dict[str, Any]) -> None:
    action = POLICY["operations"][operation]["permission"]
    project = context["project_id"] if "projects" in operation else None
    assert (
        decision(operation, context | {"token_scopes": [action], "token_project_id": project})[
            "allowed"
        ]
        is True
    )
    assert_denied(decision(operation, context | {"token_scopes": [], "token_project_id": project}))
