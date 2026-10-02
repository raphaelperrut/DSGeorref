"""Offline contract interpreter; never a backend, authorization service or provider adapter."""

from __future__ import annotations

import csv
import hashlib
import json
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any, cast

import yaml
from jsonschema import Draft202012Validator, FormatChecker

SECURITY_FACTS = {
    "authority_ready",
    "policy_ready",
    "audit_ready",
    "fallback_disabled",
    "permission_granted",
}
TERMINAL = {
    "bootstrap": {"completed"},
    "session": {"revoked", "expired", "rotated"},
    "pat": {"revoked", "expired"},
    "oidc_callback": {"consumed", "failed"},
    "oidc_link": {"revoked"},
}


class ContractViolation(ValueError):
    """Reject an incomplete, unknown or inconsistent conformance input."""


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def validate_contract(contract: dict[str, Any], schema: dict[str, Any]) -> None:
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(contract)
    for name, machine in contract["machines"].items():
        states = set(machine["states"])
        if machine["initial"] not in states:
            raise ContractViolation("unknown initial state")
        seen = set()
        for edge in machine["transitions"]:
            key = (edge["from"], edge["event"])
            required = set(edge["requires"])
            valid = edge["from"] in states and edge["to"] in states and key not in seen
            valid = valid and edge["from"] not in TERMINAL.get(name, set())
            valid = valid and SECURITY_FACTS | {"commit_ready"} <= required
            if not valid:
                raise ContractViolation("invalid/ambiguous transition or missing server guard")
            seen.add(key)
    for operation in contract["operations"].values():
        names = [gate["fact"] for gate in operation["guards"]]
        if len(names) != len(set(names)) or not set(names) >= SECURITY_FACTS:
            raise ContractViolation("operation lacks unique server-side guards")
        if any(gate["error"] not in operation["errors"] for gate in operation["guards"]):
            raise ContractViolation("unpublished HTTP error")


def decide_operation(
    contract: dict[str, Any], operation_id: str, facts: dict[str, bool]
) -> dict[str, Any]:
    """Evaluate ordered declarative guards; facts model trusted server port results only."""
    operation = contract["operations"].get(operation_id)
    if operation is None:
        raise ContractViolation("unknown operation; no action allowed")
    expected = {gate["fact"] for gate in operation["guards"]}
    if set(facts) != expected or any(type(value) is not bool for value in facts.values()):
        return {"allowed": False, "status": 500, "code": "internal_error", "effects": []}
    for gate in operation["guards"]:
        if not facts[gate["fact"]]:
            code = gate["error"]
            return {
                "allowed": False,
                "status": operation["errors"][code],
                "code": code,
                "effects": [],
            }
    return {
        "allowed": True,
        "status": operation["success_status"],
        "code": None,
        "effects": ["contract_action"],
    }


def next_state(
    contract: dict[str, Any], machine_id: str, state: str, event: str, facts: dict[str, bool]
) -> str:
    """Interpret one graph edge without persistence or any side effects."""
    machine = contract["machines"].get(machine_id)
    if machine is None or state not in machine["states"]:
        raise ContractViolation("unknown state/machine")
    matching = [e for e in machine["transitions"] if (e["from"], e["event"]) == (state, event)]
    if len(matching) != 1:
        raise ContractViolation("unknown/invalid transition")
    edge = matching[0]
    if set(facts) != set(edge["requires"]) or any(value is not True for value in facts.values()):
        raise ContractViolation("missing/denied server-side transition guard")
    return str(edge["to"])


def validate_boundary(evidence: dict[str, Any], schema: dict[str, Any], kind: str) -> None:
    if kind not in {"oidc", "throttle"}:
        raise ContractViolation("unknown evidence DTO")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.evolve(schema=schema["$defs"][kind]).validate(evidence)
    if kind == "oidc":
        identity, config = evidence["identity"], evidence["config"]
        valid = identity["issuer"] == config["issuer"]
        valid = valid and identity["audience"] == config["clientId"]
        valid = valid and _time(identity["expiresAt"]) > _time(identity["validatedAt"])
        if not valid:
            raise ContractViolation("issuer/audience/expiry mismatch")
    else:
        _validate_throttle(evidence)


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _validate_throttle(evidence: dict[str, Any]) -> None:
    before, after = evidence["before"], evidence["after"]
    if evidence["reason"] in {"authority_unavailable", "policy_unavailable"} and before != after:
        raise ContractViolation("failed authority/policy changed authoritative state")
    now = _time(evidence["observedAt"])
    for snapshot in (before, after):
        if _time(snapshot["windowEndsAt"]) <= _time(snapshot["windowStartedAt"]):
            raise ContractViolation("invalid throttle window")
        blocked = snapshot["blockedUntil"]
        if snapshot["state"] != "open" and blocked is None:
            raise ContractViolation("throttle denial lacks observable expiry")
    same_window = after["windowStartedAt"] == before["windowStartedAt"]
    if _time(after["windowStartedAt"]) < _time(before["windowStartedAt"]):
        raise ContractViolation("authoritative window regressed")
    if same_window and after["failureCount"] < before["failureCount"]:
        raise ContractViolation("counter reset without a new authoritative window")
    if (
        before["state"] != "open"
        and after["state"] == "open"
        and _time(before["blockedUntil"]) > now
    ):
        raise ContractViolation("release before authoritative deadline")
    if after["revision"] < before["revision"]:
        raise ContractViolation("throttle revision regressed")
    if before != after and after["revision"] == before["revision"]:
        raise ContractViolation("changed state without authoritative revision")
    if evidence["decision"] == "ALLOW":
        if after["state"] != "open" or evidence["reason"] != "eligible":
            raise ContractViolation("throttled/unknown decision permitted")
        if after["blockedUntil"] is not None and _time(after["blockedUntil"]) > now:
            raise ContractViolation("unexpired block permitted")
    elif evidence["reason"] == "eligible":
        raise ContractViolation("inconsistent denial reason")
    for reason, state in (("rate_limited", "limited"), ("account_locked", "locked")):
        if evidence["reason"] == reason and after["state"] != state:
            raise ContractViolation("denial has no corresponding authoritative state")


def check_sources(contract: dict[str, Any], root: Path) -> None:
    for relative, expected in contract["sources"].items():
        actual = hashlib.sha256((root / relative).read_text(encoding="utf-8").encode()).hexdigest()
        if actual != expected:
            raise ContractViolation(f"source drift: {relative}")


def check_http(contract: dict[str, Any], root: Path) -> None:
    """Compare only TASK-0036 operations against existing canonical HTTP surfaces."""
    api = read_http_api(root)
    catalog = read_json(root / "contracts/http/OPERATION_CATALOG.json")["operations"]
    with (root / "contracts/http/API_CONTRACT_INDEX.csv").open(encoding="utf-8", newline="") as f:
        index = list(csv.DictReader(f))
    terms = {"Obrigatória": "required", "Não aplicável": "not-applicable"}
    for key, frozen in contract["operations"].items():
        entries = [row for row in catalog if row["operation_id"] == key]
        indexed = [row for row in index if row["operation_id"] == key]
        if len(entries) != 1 or len(indexed) != 1:
            raise ContractViolation("missing/duplicate HTTP source operation")
        row = entries[0]
        op = api["paths"][frozen["path"]][frozen["method"].lower()]
        _check_http_metadata(key, frozen, row, indexed[0], op, terms)
        lines = (root / row["contract_file"]).read_text(encoding="utf-8").splitlines()
        required_lines = {
            f"# {key} — {frozen['method']} {frozen['path']}",
            f"- **Idempotência:** `{row['idempotency']}`",
            f"- **Permissão:** `{row['permission']}`",
            f"- **Success status:** `{row['success_status']}`",
        }
        if not required_lines <= set(lines):
            raise ContractViolation("specific HTTP contract drift")


def _check_http_metadata(
    key: str,
    frozen: dict[str, Any],
    row: dict[str, Any],
    indexed: dict[str, str],
    op: dict[str, Any],
    terms: dict[str, str],
) -> None:
    fields = (
        "method",
        "path",
        "permission",
        "success_status",
        "request_schema",
        "response_schema",
        "resource_schema",
    )
    valid = all(frozen[field] == row[field] for field in fields)
    valid = valid and all(str(row[f] or "") == indexed[f] for f in fields)
    valid = valid and op["operationId"] == key and op["x-bounded-context"] == "BC-002"
    valid = valid and op["x-contract-status"] == row["contract_status"] == "FROZEN"
    valid = valid and op["x-required-permission"] == frozen["permission"]
    valid = valid and terms.get(row["idempotency"]) == terms.get(indexed["idempotency"])
    valid = valid and terms.get(row["idempotency"]) == op["x-idempotency"] == frozen["idempotency"]
    valid = valid and op.get("security", []) == frozen["security"]
    valid = valid and op.get("parameters", []) == frozen["parameters"]
    errors = {
        code: int(status)
        for status, data in op["responses"].items()
        for code in data.get("content", {}).get("application/problem+json", {}).get("examples", {})
    }
    valid = valid and errors == frozen["errors"] and set(errors) == set(row["error_codes"])
    valid = valid and set(errors) == set(op["x-error-codes"])
    valid = valid and str(frozen["success_status"]) in op["responses"]
    request = op.get("requestBody", {}).get("content", {}).get("application/json", {})
    response = op["responses"].get(str(frozen["success_status"]), {}).get("content", {})
    request_ref = request.get("schema", {}).get("$ref")
    response_ref = response.get("application/json", {}).get("schema", {}).get("$ref")
    for field, ref in (("request_schema", request_ref), ("response_schema", response_ref)):
        expected = f"#/components/schemas/{frozen[field]}" if frozen[field] else None
        valid = valid and ref == expected
    if not valid:
        raise ContractViolation(f"HTTP metadata/error/idempotency drift: {key}")


def validate_audit(
    evidence: dict[str, Any], schema: dict[str, Any], contract: dict[str, Any]
) -> None:
    """Check a synthetic owner audit record against the declared transition graph."""
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.evolve(schema=schema["$defs"]["audit"]).validate(evidence)
    machine = contract["machines"][evidence["machine"]]
    if any(evidence[key] not in machine["states"] for key in ("fromState", "toState")):
        raise ContractViolation("audit has unknown state")
    if evidence["outcome"] == "DENIED":
        if (
            evidence["domainEvent"] is not None
            or evidence["committedAt"] is not None
            or evidence["fromState"] != evidence["toState"]
        ):
            raise ContractViolation("denied command emitted a success or state change")
        return
    edges = [
        e
        for e in machine["transitions"]
        if (e["from"], e["event"], e["to"])
        == (evidence["fromState"], evidence["event"], evidence["toState"])
    ]
    signals = {
        "BootstrapAdmin": "AdminBootstrapped",
        "CriarSessao": "SessionCreated",
        "RevogarSessao": "SessionRevoked",
        "EmitirToken": "TokenIssued",
    }
    if (
        len(edges) != 1
        or evidence["committedAt"] is None
        or evidence["domainEvent"] != signals.get(evidence["event"])
    ):
        raise ContractViolation("audit lacks valid committed transition/signal")


def read_http_api(root: Path) -> dict[str, Any]:
    """Type the external YAML boundary and reject a non-object document."""
    loader = cast(Callable[[str], object], yaml.safe_load)
    loaded = loader((root / "contracts/http/openapi.yaml").read_text(encoding="utf-8"))
    if not isinstance(loaded, dict) or not {"paths", "components"} <= set(loaded):
        raise ContractViolation("invalid HTTP document at YAML boundary")
    return cast(dict[str, Any], loaded)
