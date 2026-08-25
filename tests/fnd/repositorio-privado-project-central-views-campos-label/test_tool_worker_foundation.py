from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
from functools import cache
from pathlib import Path
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / (
    "tools/governance/repositorio-privado-project-central-views-campos-label/"
    "sprint-001-tool-worker-parte-8/foundation_validation.py"
)
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "sprint-001-tool-worker-parte-8/foundation-policy.json"
)
MODULE_NAME = "tool_worker_foundation_validation"
_validator_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
if _validator_spec is None or _validator_spec.loader is None:
    raise ImportError(f"cannot load validator from {MODULE_PATH}")
_validator = importlib.util.module_from_spec(_validator_spec)
sys.modules[MODULE_NAME] = _validator
_validator_spec.loader.exec_module(_validator)

FoundationValidationError = _validator.FoundationValidationError
load_policy = _validator.load_policy
validate_policy = _validator.validate_policy


@cache
def _policy() -> dict[str, Any]:
    return load_policy(POLICY_PATH, ROOT)


def _codes(policy: object) -> set[str]:
    return {finding.code for finding in validate_policy(policy, ROOT)}


def _worker_control(name: str) -> dict[str, Any]:
    return _policy()["controls"]["worker"][name]


def test_model_boundary_architecture() -> None:
    boundaries = _policy()["controls"]["model_boundaries"]
    assert boundaries == {
        "domain": "SEPARATE",
        "transport": "SEPARATE",
        "persistence": "SEPARATE",
        "cross_layer_model_reuse": "REJECT",
    }
    invalid = copy.deepcopy(_policy())
    invalid["controls"]["model_boundaries"]["transport"] = "DOMAIN_MODEL"
    assert "MODEL_BOUNDARY_INVALID" in _codes(invalid)


def test_req_worker_002() -> None:
    queue = _worker_control("queue")
    assert queue["classes"] == ["interactive", "batch", "ai-gpu", "maintenance"]
    assert queue["dynamic_per_job"] == "REJECT"

    dynamic = copy.deepcopy(_policy())
    dynamic["controls"]["worker"]["queue"]["dynamic_per_job"] = "ALLOW"
    assert "QUEUE_POLICY_INVALID" in _codes(dynamic)


def test_req_worker_003() -> None:
    ack_prefetch = _worker_control("ack_prefetch")
    assert ack_prefetch == {
        "ack": "AFTER_AUTHORITATIVE_COMMIT",
        "initial_prefetch": 1,
        "promotion_owner": "BP-004",
        "premature_ack": "REJECT",
    }

    premature = copy.deepcopy(_policy())
    premature["controls"]["worker"]["ack_prefetch"]["ack"] = "BEFORE_COMMIT"
    assert "ACK_PREFETCH_POLICY_INVALID" in _codes(premature)


def test_req_worker_004() -> None:
    isolation = _worker_control("isolation")
    assert isolation == {
        "pool": "PREFORK",
        "process_isolation": "REQUIRED",
        "recycling": "REQUIRED",
        "missing_isolation_or_recycling": "REJECT",
    }

    unsafe = copy.deepcopy(_policy())
    unsafe["controls"]["worker"]["isolation"]["recycling"] = "OPTIONAL"
    assert "WORKER_ISOLATION_INVALID" in _codes(unsafe)


def test_req_worker_005() -> None:
    leases = _worker_control("leases")
    assert leases == {
        "authority": "PostgreSQL",
        "fencing_token": "REQUIRED",
        "expiration": "VERIFIABLE",
        "stale_owner_commit_or_publish": "REJECT",
    }

    stale_owner = copy.deepcopy(_policy())
    stale_owner["controls"]["worker"]["leases"]["stale_owner_commit_or_publish"] = "ALLOW"
    assert "FENCING_POLICY_INVALID" in _codes(stale_owner)


def test_req_worker_006() -> None:
    retry = _worker_control("retry")
    assert retry == {
        "taxonomy": "CLASSIFIED_TECHNICAL_ONLY",
        "poison_message": "AUDITABLE_QUARANTINE",
        "unclassified_or_unquarantined": "REJECT",
    }

    unclassified = copy.deepcopy(_policy())
    unclassified["controls"]["worker"]["retry"]["taxonomy"] = "UNCLASSIFIED"
    assert "RETRY_POLICY_INVALID" in _codes(unclassified)

    no_quarantine = copy.deepcopy(_policy())
    no_quarantine["controls"]["worker"]["retry"]["poison_message"] = "DROP"
    assert "RETRY_POLICY_INVALID" in _codes(no_quarantine)


def test_req_worker_007() -> None:
    dispatch = _worker_control("dispatch")
    assert dispatch == {
        "authority": "SCHEDULER_AND_OUTBOX",
        "direct_fanout": "REJECT",
        "redelivery": "OUTBOX_RECONCILED",
    }

    bypass = copy.deepcopy(_policy())
    bypass["controls"]["worker"]["dispatch"]["direct_fanout"] = "ALLOW"
    assert "DISPATCH_POLICY_INVALID" in _codes(bypass)


def test_exact_requirement_coverage_and_checkpoints() -> None:
    policy = _policy()
    expected = {
        "REQ-SPRINT-001-010",
        "REQ-TOOL-001",
        "REQ-TOOL-002",
        "REQ-TOOL-005",
        "REQ-WORKER-002",
        "REQ-WORKER-003",
        "REQ-WORKER-004",
        "REQ-WORKER-005",
        "REQ-WORKER-006",
        "REQ-WORKER-007",
    }
    assert set(policy["coverage"]) == set(policy["requirements"]) == expected
    assert len(policy["coverage"]) == len(policy["requirements"]) == 10
    for evidence in policy["requirements"].values():
        assert evidence["checkpoint"] == f"{evidence['test_path']}::{evidence['test_id']}"


def test_missing_requirement_reference_or_checkpoint_fails_closed() -> None:
    missing_requirement = copy.deepcopy(_policy())
    missing_requirement["requirements"].pop("REQ-WORKER-005")
    assert "REQUIREMENT_EVIDENCE_INVALID" in _codes(missing_requirement)

    missing_reference = copy.deepcopy(_policy())
    missing_reference["requirements"]["REQ-WORKER-006"]["authority_path"] = (
        "contracts/operations/missing-policy.yaml"
    )
    assert "REFERENCE_INVALID" in _codes(missing_reference)

    missing_checkpoint = copy.deepcopy(_policy())
    missing_checkpoint["requirements"]["REQ-WORKER-007"]["checkpoint"] = (
        f"{__file__}::missing_test"
    )
    assert "CHECKPOINT_INVALID" in _codes(missing_checkpoint)


@pytest.mark.parametrize(
    "unsafe_reference",
    ["../outside.json", "C:\\outside.json", "README.md", "https://example.test/policy"],
)
def test_unsafe_or_out_of_domain_reference_is_rejected(unsafe_reference: str) -> None:
    invalid = copy.deepcopy(_policy())
    invalid["requirements"]["REQ-WORKER-002"]["authority_path"] = unsafe_reference
    assert "REFERENCE_INVALID" in _codes(invalid)


def test_scope_is_exact_disjoint_and_preserves_deny_paths() -> None:
    policy = _policy()
    scope = policy["write_scope"]
    task_path = next(path for path in scope if path.startswith(".codex/tasks/"))
    task = json.loads((ROOT / task_path).read_text(encoding="utf-8"))
    assert scope == task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    assert task["deny_paths"] == ["src/**/epic-*", "src/**/issue-*"]
    roots = [path.removesuffix("/**").rstrip("/") for path in scope]
    assert len(roots) == len(set(roots))
    assert not any(
        left.startswith(f"{right}/") or right.startswith(f"{left}/")
        for index, left in enumerate(roots)
        for right in roots[index + 1 :]
    )


def test_executable_code_has_no_ticket_identifiers() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert re.search(r"(?:TASK|ISSUE|STORY)-[0-9]{4}", source) is None


def test_incomplete_configuration_and_silent_fallback_are_rejected() -> None:
    incomplete = copy.deepcopy(_policy())
    incomplete["controls"]["worker"]["ack_prefetch"].pop("promotion_owner")
    assert "ACK_PREFETCH_POLICY_INVALID" in _codes(incomplete)

    fallback = copy.deepcopy(_policy())
    fallback["controls"]["failure_handling"]["silent_fallback"] = "ALLOW"
    assert "FAIL_CLOSED_POLICY_INVALID" in _codes(fallback)

    with pytest.raises(FoundationValidationError) as captured:
        load_policy(POLICY_PATH.parent / "missing-policy.json", ROOT)
    assert captured.value.findings[0].code == "POLICY_UNREADABLE"
