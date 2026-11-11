"""Offline resource contract oracle; not a runtime authorization service or locator."""

import json
import runpy
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
CONTRACT = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
POLICY = json.loads((HERE / CONTRACT["policy_ref"]).read_text(encoding="utf-8"))
FREEZE_DIR = (HERE / CONTRACT["freeze_ref"]).parent
FREEZE = json.loads((FREEZE_DIR / "contract.json").read_text(encoding="utf-8"))
RULES = runpy.run_path(str(FREEZE_DIR / "conformance.py"))


def resource_bound(snapshot: dict[str, Any]) -> bool:
    """Evaluate logical ownership only; an identifier or matching path grants nothing."""
    kind = snapshot.get("resource_type")
    resource_id = snapshot.get("resource_id")
    if not isinstance(resource_id, str) or not resource_id:
        return False
    if snapshot.get("resource_exists") is not True:
        return False
    if kind == "account":
        return resource_id == snapshot.get("account_id")
    if kind == "project":
        return resource_id == snapshot.get("project_id")
    if kind not in {"artifact", "artifact_path"}:
        return False
    manifest = snapshot.get("manifest")
    if not isinstance(manifest, dict):
        return False
    if not snapshot.get("project_id") or manifest.get("project_id") != snapshot["project_id"]:
        return False
    if manifest.get("publication", {}).get("status") != "PUBLISHED":
        return False
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        return False
    matches = [a for a in artifacts if isinstance(a, dict) and a.get("artifact_id") == resource_id]
    if len(matches) != 1:
        return False
    return kind == "artifact" or (
        isinstance(snapshot.get("relative_path"), str)
        and snapshot["relative_path"] == matches[0].get("relative_path")
    )


def current_subject(snapshot: dict[str, Any]) -> bool:
    """Unknown states, absent scope selection and stale policy all deny."""
    return (
        isinstance(snapshot.get("account_id"), str)
        and bool(snapshot["account_id"])
        and snapshot.get("account_state") == "active"
        and snapshot.get("credential_state") == "active"
        and snapshot.get("policy_version") == POLICY["version"]
        and snapshot.get("grant_current") is True
        and "token_scopes" in snapshot
        and "token_project_id" in snapshot
    )


def current_grant(operation: str, snapshot: dict[str, Any]) -> bool:
    """Read the single existing grant authority; no local permission table."""
    row = POLICY["operations"][operation]
    permission = row["permission"]
    project = None
    if row["grant_source"] == "central_policy":
        grant = permission in POLICY["self_service_grants"]
    elif row["grant_source"] == "project_membership":
        project = snapshot.get("project_id")
        revision = snapshot.get("membership_revision")
        grant = (
            bool(project)
            and project == snapshot.get("membership_project_id")
            and snapshot.get("account_id") == snapshot.get("membership_account_id")
            and type(revision) is int
            and revision > 0
            and type(snapshot.get("current_membership_revision")) is int
            and revision == snapshot["current_membership_revision"]
            and permission in POLICY["project_role_grants"].get(snapshot.get("role"), [])
        )
    else:
        return False
    scopes = snapshot["token_scopes"]
    if scopes is None:
        return grant and snapshot["token_project_id"] is None
    return (
        grant
        and isinstance(scopes, list)
        and bool(scopes)
        and all(isinstance(scope, str) for scope in scopes)
        and permission in scopes
        and project == snapshot["token_project_id"]
    )


def decide(operation: str, snapshot: dict[str, Any], facts: dict[str, bool]) -> dict[str, Any]:
    """Conjoin trusted snapshot predicates and ALL original guards; emit existing DTO."""
    expected_kind = CONTRACT["operation_resources"].get(operation)
    allowed = False
    if (
        expected_kind is not None
        and snapshot.get("resource_type") == expected_kind
        and current_subject(snapshot)
        and resource_bound(snapshot)
    ):
        evaluated = facts.copy()
        evaluated["permission_granted"] = facts.get("permission_granted") is True and current_grant(
            operation, snapshot
        )
        # Missing facts must not be fabricated, even when a predicate was derived.
        if "permission_granted" in facts:
            allowed = RULES["decide_operation"](FREEZE, operation, evaluated)["allowed"]
    return {
        "allowed": allowed,
        "policyVersion": POLICY["version"],
        "reasonCode": CONTRACT["decision"]["allow_reason" if allowed else "deny_reason"],
    }
