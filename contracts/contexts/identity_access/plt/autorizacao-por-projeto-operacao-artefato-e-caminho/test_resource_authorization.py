"""Executable decisions and compatibility for STORY-0046, without runtime claims."""

import copy
import hashlib
import json
import runpy
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ORACLE = runpy.run_path(str(HERE / "conformance.py"))
CONTRACT, POLICY, FREEZE, RULES = (
    ORACLE[name] for name in ("CONTRACT", "POLICY", "FREEZE", "RULES")
)
OPERATIONS = list(CONTRACT["operation_resources"])
PROJECT_OPERATIONS = [name for name in OPERATIONS if "projects" in name]


def snapshot(operation: str) -> dict[str, Any]:
    project = operation in PROJECT_OPERATIONS
    return {
        "account_id": "alice",
        "account_state": "active",
        "credential_state": "active",
        "policy_version": "1.1.0",
        "grant_current": True,
        "role": "owner",
        "membership_account_id": "alice",
        "membership_project_id": "project-a",
        "membership_revision": 2,
        "current_membership_revision": 2,
        "token_scopes": None,
        "token_project_id": None,
        "resource_type": "project" if project else "account",
        "resource_id": "project-a" if project else "alice",
        "project_id": "project-a" if project else None,
        "resource_exists": True,
    }


def facts(operation: str) -> dict[str, bool]:
    return dict.fromkeys(
        (guard["fact"] for guard in FREEZE["operations"][operation]["guards"]), True
    )


def decide(operation: str, subject: dict[str, Any], guards: dict[str, bool]) -> dict[str, Any]:
    result = ORACLE["decide"](operation, subject, guards)
    assert set(result) == {"allowed", "policyVersion", "reasonCode"}
    assert result["policyVersion"] == POLICY["version"]
    return result


@pytest.mark.parametrize("operation", OPERATIONS)
def test_epic_010_politica(operation: str) -> None:
    subject = snapshot(operation)
    assert decide(operation, subject, facts(operation))["allowed"] is True
    permission = POLICY["operations"][operation]["permission"]
    scoped = subject | {"token_scopes": [permission], "token_project_id": subject["project_id"]}
    assert decide(operation, scoped, facts(operation))["allowed"] is True
    assert not decide(operation, scoped | {"token_scopes": []}, facts(operation))["allowed"]


@pytest.mark.parametrize("operation", PROJECT_OPERATIONS)
@pytest.mark.parametrize("role", ["owner", "editor", "reviewer", "viewer", "administrator"])
def test_existing_role_grants(operation: str, role: str) -> None:
    expected = role in POLICY["project_roles"] and (
        operation == "get_projects_projectid_members" or role == "owner"
    )
    assert (
        decide(operation, snapshot(operation) | {"role": role}, facts(operation))["allowed"]
        is expected
    )


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize(
    "mutation",
    [
        {"account_id": ""},
        {"account_state": "inactive"},
        {"account_state": "locked"},
        {"credential_state": "revoked"},
        {"credential_state": "expired"},
        {"credential_state": "rotated"},
        {"policy_version": "stale"},
        {"grant_current": False},
        {"grant_current": "true"},
        {"resource_exists": False},
        {"resource_exists": "true"},
        {"resource_id": "another-resource"},
        {"resource_type": "physical_path"},
        {"token_scopes": "project_member:list"},
        {"token_scopes": []},
        {"token_scopes": ["unregistered:permission"]},
        {"token_project_id": "other-project"},
    ],
)
def test_identity_resource_and_scope_denials(operation: str, mutation: dict[str, Any]) -> None:
    assert not decide(operation, snapshot(operation) | mutation, facts(operation))["allowed"]


@pytest.mark.parametrize("operation", PROJECT_OPERATIONS)
@pytest.mark.parametrize(
    "mutation",
    [
        {"membership_project_id": None, "instance_administrator": True},
        {"membership_project_id": "project-b"},
        {"membership_account_id": "bob"},
        {"role": None, "client_role": "owner"},
        {"membership_revision": 1},
        {"membership_revision": True, "current_membership_revision": True},
        {"current_membership_revision": None},
        {"project_id": "project-b", "resource_id": "project-b"},
    ],
)
def test_no_cross_project_or_administrator_bypass(operation: str, mutation: dict[str, Any]) -> None:
    assert not decide(operation, snapshot(operation) | mutation, facts(operation))["allowed"]


@pytest.mark.parametrize("operation", OPERATIONS)
def test_missing_inputs_and_every_original_guard_deny(operation: str) -> None:
    subject, guards = snapshot(operation), facts(operation)
    required = {
        "account_id",
        "account_state",
        "credential_state",
        "policy_version",
        "grant_current",
        "token_scopes",
        "token_project_id",
        "resource_type",
        "resource_id",
        "resource_exists",
    }
    if operation in PROJECT_OPERATIONS:
        required |= {
            "role",
            "membership_account_id",
            "membership_project_id",
            "membership_revision",
            "current_membership_revision",
            "project_id",
        }
    for name in required:
        missing = subject.copy()
        del missing[name]
        assert not decide(operation, missing, guards)["allowed"], name
    for name in guards:
        for invalid in (False, None, "true"):
            assert not decide(operation, subject, guards | {name: invalid})["allowed"], name
        missing = guards.copy()
        del missing[name]
        assert not decide(operation, subject, missing)["allowed"], name
    assert not decide(operation, subject, guards | {"unknown_guard": True})["allowed"]


def test_resource_binding_does_not_grant_artifact_or_path_access() -> None:
    manifest = json.loads(
        (ROOT / "contracts/artifacts/examples/artifact-set-manifest-2.0.0.json").read_text()
    )
    schema = json.loads((ROOT / CONTRACT["artifact_boundary"]["manifest_schema"]).read_text())
    Draft202012Validator(schema).validate(manifest)
    artifact = manifest["artifacts"][0]
    subject = snapshot(PROJECT_OPERATIONS[0]) | {
        "resource_type": "artifact_path",
        "resource_id": artifact["artifact_id"],
        "project_id": manifest["project_id"],
        "relative_path": artifact["relative_path"],
        "manifest": manifest,
    }
    assert ORACLE["resource_bound"](subject)
    assert ORACLE["resource_bound"](subject | {"resource_type": "artifact"})
    for mutation in (
        {"project_id": "other-project"},
        {"resource_id": "absent"},
        {"relative_path": artifact["relative_path"] + "/child"},
        {"relative_path": "../secret"},
        {"relative_path": "C:\\internal\\secret"},
        {"resource_exists": False},
        {"manifest": None},
        {"resource_type": "physical_path"},
    ):
        assert not ORACLE["resource_bound"](subject | mutation)
    unpublished = copy.deepcopy(manifest)
    unpublished["publication"]["status"] = "STAGING"
    assert not ORACLE["resource_bound"](subject | {"manifest": unpublished})
    for role in [*POLICY["project_roles"], "instance_administrator"]:
        denied = decide(CONTRACT["artifact_boundary"]["operation"], subject | {"role": role}, {})
        assert denied == {"allowed": False, "policyVersion": "1.1.0", "reasonCode": "access_denied"}
        assert "secret" not in json.dumps(denied)
    assert not decide("unknown-operation", subject, {})["allowed"]


def test_existing_transitions_and_invalidation() -> None:
    for name in CONTRACT["transitions"]["delegate_machines"]:
        for edge in FREEZE["machines"][name]["transitions"]:
            guards = dict.fromkeys(edge["requires"], True)
            args = (FREEZE, name, edge["from"], edge["event"])
            assert RULES["next_state"](*args, guards) == edge["to"]
            for fact in guards:
                with pytest.raises(RULES["ContractViolation"]):
                    RULES["next_state"](*args, guards | {fact: False})
    for machine, state, event in (
        ("session", "revoked", "CriarSessao"),
        ("pat", "expired", "EmitirToken"),
        ("account", "unknown", "activate"),
        ("membership", "active", "revoke"),
    ):
        with pytest.raises(RULES["ContractViolation"]):
            RULES["next_state"](FREEZE, machine, state, event, {})
    operation = PROJECT_OPERATIONS[0]
    subject = snapshot(operation)
    assert decide(operation, subject, facts(operation))["allowed"]
    for mutation in ({"current_membership_revision": 3}, {"credential_state": "revoked"}):
        assert not decide(operation, subject | mutation, facts(operation))["allowed"]


def test_req_auth_impl_007() -> None:
    # Reuse the existing state/evidence proof; never implement another throttle engine.
    upstream = runpy.run_path(
        str(HERE.parent / "usuarios-e-papeis-da-instancia/test_instance_policy.py")
    )
    upstream["test_req_auth_impl_007"]()
    assert CONTRACT["throttling"]["requirement"] == POLICY["throttling"]["requirement"]
    operation = "get_projects_projectid_members"
    for state in FREEZE["machines"]["throttle"]["states"]:
        guards = facts(operation) | {
            "throttle_open": state in POLICY["throttling"]["eligible_states"]
        }
        assert decide(operation, snapshot(operation), guards)["allowed"] is (state == "open")
        assert not decide(operation, snapshot(operation) | {"role": None}, guards)["allowed"]


def test_contract_compatibility() -> None:
    for source, digest in CONTRACT["source_sha256"].items():
        assert (
            hashlib.sha256((HERE / source).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
            == digest
        )
    assert CONTRACT["contract_version"] == "1.0.0"
    assert CONTRACT["policy_version"] == POLICY["version"] == "1.1.0"
    assert CONTRACT["runtime_implemented"] is False
    assert CONTRACT["default_decision"] == POLICY["default_decision"] == "deny"
    assert set(OPERATIONS) | set(CONTRACT["authentication_exceptions"]) == set(POLICY["operations"])
    catalog = json.loads((ROOT / "contracts/http/OPERATION_CATALOG.json").read_text())
    rows = {row["operation_id"]: row for row in catalog["operations"]}
    openapi = yaml.safe_load((ROOT / "contracts/http/openapi.yaml").read_text())
    for operation, row in POLICY["operations"].items():
        assert row["permission"] == rows[operation]["permission"]
        frozen = FREEZE["operations"][operation]
        http = openapi["paths"][frozen["path"]][frozen["method"].lower()]
        assert http["operationId"] == operation
        assert http["x-required-permission"] == row["permission"]
    boundary = CONTRACT["artifact_boundary"]
    assert rows[boundary["operation"]]["permission"] == boundary["permission"]
    assert all(
        boundary["permission"] not in grants for grants in POLICY["project_role_grants"].values()
    )
    assert boundary["permission"] not in POLICY["self_service_grants"]
    for operation in CONTRACT["authentication_exceptions"]:
        assert not decide(operation, snapshot(OPERATIONS[0]), {})["allowed"]
