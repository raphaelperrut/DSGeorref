"""Pytest entrypoints for TASK-0036 contract evidence; no production runtime required."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

BASE = Path(__file__).resolve().parent
ROOT = next(parent for parent in BASE.parents if (parent / ".codex/tasks/TASK-0036.json").is_file())
SPEC = importlib.util.spec_from_file_location("identity_auth_conformance", BASE / "conformance.py")
assert SPEC is not None and SPEC.loader is not None
RULES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RULES)
CONTRACT = RULES.read_json(BASE / "contract.json")
SCHEMA = RULES.read_json(BASE / "contract.schema.json")
BOUNDARY = RULES.read_json(BASE / "boundary-evidence.schema.json")
EXAMPLES = RULES.read_json(BASE / "examples.json")
DENIALS = [
    (op, gate["fact"], gate["error"])
    for op, row in CONTRACT["operations"].items()
    for gate in row["guards"]
]
EDGES = [
    (name, edge)
    for name, machine in CONTRACT["machines"].items()
    for edge in machine["transitions"]
]


def test_req_auth_impl_007() -> None:
    assert CONTRACT["requirement"] == "REQ-AUTH-IMPL-007"
    assert CONTRACT["policies"]["throttling"]["requirement"] == CONTRACT["requirement"]
    Draft202012Validator.check_schema(BOUNDARY)
    for observation in EXAMPLES["throttle_observations"]:
        RULES.validate_boundary(observation, BOUNDARY, "throttle")
    for op, row in CONTRACT["operations"].items():
        facts = {gate["fact"]: True for gate in row["guards"]}
        if "throttle_open" in facts:
            denied = RULES.decide_operation(CONTRACT, op, facts | {"throttle_open": False})
            assert denied["allowed"] is False and denied["effects"] == []
    for name, edge in EDGES:
        if name == "throttle":
            facts = dict.fromkeys(edge["requires"], True)
            with pytest.raises(RULES.ContractViolation):
                RULES.next_state(
                    CONTRACT, name, edge["from"], edge["event"], facts | {"authority_ready": False}
                )


def test_epic_008_politica() -> None:
    RULES.validate_contract(CONTRACT, SCHEMA)
    RULES.check_sources(CONTRACT, ROOT)
    for name, edge in EDGES:
        facts = dict.fromkeys(edge["requires"], True)
        assert RULES.next_state(CONTRACT, name, edge["from"], edge["event"], facts) == edge["to"]
    for op, row in CONTRACT["operations"].items():
        facts = {gate["fact"]: True for gate in row["guards"]}
        result = RULES.decide_operation(CONTRACT, op, facts)
        assert result["allowed"] is True and result["status"] == row["success_status"]
    edge = CONTRACT["machines"]["bootstrap"]["transitions"][0]
    facts = dict.fromkeys(edge["requires"], True)
    state = RULES.next_state(CONTRACT, "bootstrap", "available", "BootstrapAdmin", facts)
    assert state == "completed"
    with pytest.raises(RULES.ContractViolation):
        RULES.next_state(CONTRACT, "bootstrap", state, "BootstrapAdmin", facts)
    with pytest.raises(RULES.ContractViolation):
        RULES.next_state(
            CONTRACT, "bootstrap", "available", "BootstrapAdmin", facts | {"session_created": False}
        )
    assert CONTRACT["machines"]["bootstrap"]["initial"] == "available"


@pytest.mark.parametrize(("operation", "fact", "error"), DENIALS)
def test_every_server_guard_denies_without_success_effects(
    operation: str, fact: str, error: str
) -> None:
    row = CONTRACT["operations"][operation]
    facts = {gate["fact"]: True for gate in row["guards"]}
    result = RULES.decide_operation(CONTRACT, operation, facts | {fact: False})
    assert result == {
        "allowed": False,
        "status": row["errors"][error],
        "code": error,
        "effects": [],
    }
    assert row["errors"][error] >= 400
    missing = facts.copy()
    del missing[fact]
    for invalid in (missing, facts | {fact: "true"}, facts | {"client_role_admin": True}):
        assert RULES.decide_operation(CONTRACT, operation, invalid)["allowed"] is False


@pytest.mark.parametrize(("name", "edge"), EDGES)
def test_transition_fail_closed(name: str, edge: dict[str, Any]) -> None:
    facts = dict.fromkeys(edge["requires"], True)
    for guard in edge["requires"]:
        with pytest.raises(RULES.ContractViolation):
            RULES.next_state(CONTRACT, name, edge["from"], edge["event"], facts | {guard: False})
    for state, event in (("unknown", edge["event"]), (edge["from"], "unknown")):
        with pytest.raises(RULES.ContractViolation):
            RULES.next_state(CONTRACT, name, state, event, facts)
    with pytest.raises(RULES.ContractViolation):
        RULES.next_state(CONTRACT, name, edge["from"], edge["event"], {})


@pytest.mark.parametrize(
    "mutation",
    [
        "fallback",
        "authority",
        "runtime",
        "unknown_state",
        "no_permission",
        "reopen_bootstrap",
        "unknown_http_error",
    ],
)
def test_invalid_freeze_rejected(mutation: str) -> None:
    invalid = copy.deepcopy(CONTRACT)
    if mutation == "fallback":
        invalid["invariants"]["fallback"] = "LOCAL_ACCOUNT"
    elif mutation == "authority":
        invalid["invariants"]["authority"] = "Redis"
    elif mutation == "runtime":
        invalid["invariants"]["runtime_implemented"] = True
    elif mutation == "unknown_state":
        invalid["machines"]["account"]["initial"] = "unknown"
    elif mutation == "no_permission":
        gates = invalid["operations"]["post_auth_tokens"]["guards"]
        gates[:] = [gate for gate in gates if gate["fact"] != "permission_granted"]
    elif mutation == "reopen_bootstrap":
        edge = copy.deepcopy(invalid["machines"]["bootstrap"]["transitions"][0])
        edge.update({"from": "completed", "to": "available", "event": "reset"})
        invalid["machines"]["bootstrap"]["transitions"].append(edge)
    else:
        invalid["operations"]["post_auth_session"]["guards"][0]["error"] = "unknown"
    with pytest.raises((RULES.ContractViolation, ValidationError)):
        RULES.validate_contract(invalid, SCHEMA)


@pytest.mark.parametrize(
    ("section", "field", "value"),
    [
        ("config", "enabled", False),
        ("config", "issuer", "http://idp.example.test"),
        ("identity", "issuer", "https://different.example.test"),
        ("identity", "audience", "different-client"),
        ("identity", "signatureValidated", False),
        ("identity", "nonceValidated", False),
        ("identity", "stateValidated", False),
        ("identity", "expiresAt", "2026-10-01T12:00:00Z"),
        ("identity", "subject", ""),
        ("identity", "localFallback", True),
        ("identity", "roles", ["admin"]),
        ("config", "clientId", None),
    ],
)
def test_oidc_provider_config_and_result_fail_closed(section: str, field: str, value: Any) -> None:
    valid = EXAMPLES["oidc"]
    RULES.validate_boundary(valid, BOUNDARY, "oidc")
    invalid = copy.deepcopy(valid)
    invalid[section][field] = value
    with pytest.raises((RULES.ContractViolation, ValidationError)):
        RULES.validate_boundary(invalid, BOUNDARY, "oidc")
    missing = copy.deepcopy(valid)
    missing[section].pop(field, None)
    if field in valid[section]:
        with pytest.raises((RULES.ContractViolation, ValidationError)):
            RULES.validate_boundary(missing, BOUNDARY, "oidc")


@pytest.mark.parametrize(
    "mutation",
    [
        "allow_limited",
        "unknown_state",
        "missing_deadline",
        "missing_counter",
        "missing_policy",
        "secret",
        "revision",
        "unchanged_revision",
        "invalid_window",
        "bad_reason",
    ],
)
def test_throttling_evidence_rejects_invalid_or_unobservable_state(mutation: str) -> None:
    invalid = copy.deepcopy(EXAMPLES["throttle_observations"][0])
    if mutation == "allow_limited":
        invalid["decision"] = "ALLOW"
    elif mutation == "unknown_state":
        invalid["after"]["state"] = "unknown"
    elif mutation == "missing_deadline":
        invalid["after"]["blockedUntil"] = None
    elif mutation == "missing_counter":
        del invalid["after"]["failureCount"]
    elif mutation == "missing_policy":
        del invalid["policyVersion"]
    elif mutation == "secret":
        invalid["password"] = "synthetic-forbidden-field"
    elif mutation == "revision":
        invalid["after"]["revision"] = 0
    elif mutation == "unchanged_revision":
        invalid["after"]["revision"] = invalid["before"]["revision"]
    elif mutation == "invalid_window":
        invalid["after"]["windowEndsAt"] = invalid["after"]["windowStartedAt"]
    else:
        invalid["reason"] = "eligible"
    with pytest.raises((RULES.ContractViolation, ValidationError)):
        RULES.validate_boundary(invalid, BOUNDARY, "throttle")


def test_http_compatibility_and_shared_sources() -> None:
    RULES.check_http(CONTRACT, ROOT)
    for field, value in (
        ("permission", "invented:grant"),
        ("idempotency", "required"),
        ("success_status", 202),
    ):
        invalid = copy.deepcopy(CONTRACT)
        invalid["operations"]["get_projects_projectid_members"][field] = value
        with pytest.raises(RULES.ContractViolation):
            RULES.check_http(invalid, ROOT)
    task = RULES.read_json(ROOT / ".codex/tasks/TASK-0036.json")
    assert set(CONTRACT["operations"]) == set(task["phase_f_review"]["api"]["contracts"])


def test_published_http_response_and_error_shapes() -> None:
    api = RULES.read_http_api(ROOT)
    validator = Draft202012Validator(api, format_checker=FormatChecker())
    for operation, example in EXAMPLES["http_responses"].items():
        response = CONTRACT["operations"][operation]["response_schema"]
        validator.evolve(schema=api["components"]["schemas"][response]).validate(example)
        invalid = copy.deepcopy(example)
        invalid["unpublished_auth_state"] = "active"
        with pytest.raises(ValidationError):
            validator.evolve(schema=api["components"]["schemas"][response]).validate(invalid)
    problem = validator.evolve(schema=api["components"]["schemas"]["Problem"])
    for row in CONTRACT["operations"].values():
        for code, status in row["errors"].items():
            problem.validate(
                {
                    "type": f"https://dsgeorref.local/problems/{code}",
                    "title": code,
                    "status": status,
                    "code": code,
                }
            )


def test_canonical_audit_requires_commit_and_rejects_false_success() -> None:
    RULES.validate_audit(EXAMPLES["audit"], BOUNDARY, CONTRACT)
    denied = EXAMPLES["audit"] | {
        "outcome": "DENIED",
        "toState": "available",
        "committedAt": None,
        "domainEvent": None,
    }
    RULES.validate_audit(denied, BOUNDARY, CONTRACT)
    for patch in (
        {"committedAt": None},
        {"fromState": "unknown"},
        {"domainEvent": "TokenIssued"},
        {"outcome": "DENIED"},
        {"event": "reset"},
    ):
        with pytest.raises((RULES.ContractViolation, ValidationError)):
            RULES.validate_audit(EXAMPLES["audit"] | patch, BOUNDARY, CONTRACT)


def test_throttle_cannot_reset_counters_or_release_a_live_block() -> None:
    observation = copy.deepcopy(EXAMPLES["throttle_observations"][1])
    observation["after"]["failureCount"] = 0
    with pytest.raises(RULES.ContractViolation):
        RULES.validate_boundary(observation, BOUNDARY, "throttle")
    observation["after"].update({"state": "open", "failureCount": 1, "blockedUntil": None})
    observation.update({"decision": "ALLOW", "reason": "eligible"})
    with pytest.raises(RULES.ContractViolation):
        RULES.validate_boundary(observation, BOUNDARY, "throttle")


@pytest.mark.parametrize(
    ("machine", "state", "event"),
    [
        ("account", "active", "activate"),
        ("session", "revoked", "CriarSessao"),
        ("pat", "expired", "EmitirToken"),
        ("oidc_link", "revoked", "link"),
        ("oidc_callback", "consumed", "accept"),
        ("oidc_adapter", "disabled", "revalidate"),
    ],
)
def test_registered_event_in_wrong_state_is_denied(machine: str, state: str, event: str) -> None:
    with pytest.raises(RULES.ContractViolation):
        RULES.next_state(CONTRACT, machine, state, event, {})


def test_pat_plaintext_replay_and_failed_throttle_authority_are_denied() -> None:
    row = CONTRACT["operations"]["post_auth_tokens"]
    facts = {gate["fact"]: True for gate in row["guards"]}
    result = RULES.decide_operation(
        CONTRACT, "post_auth_tokens", facts | {"issuance_not_replayed": False}
    )
    assert result == {"allowed": False, "status": 409, "code": "conflict", "effects": []}
    invalid = copy.deepcopy(EXAMPLES["throttle_observations"][0])
    invalid["reason"] = "authority_unavailable"
    with pytest.raises(RULES.ContractViolation):
        RULES.validate_boundary(invalid, BOUNDARY, "throttle")
