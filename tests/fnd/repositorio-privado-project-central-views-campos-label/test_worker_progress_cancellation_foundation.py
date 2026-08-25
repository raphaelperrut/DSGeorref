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
    "worker-parte-9/foundation_validation.py"
)
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "worker-parte-9/foundation-policy.json"
)
MODULE_NAME = "worker_progress_cancellation_foundation_validation"
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


def test_req_worker_008() -> None:
    progress = _policy()["controls"]["progress"]
    assert progress == {
        "authority": "PostgreSQL",
        "granularity": "WORK_UNIT",
        "typed": "REQUIRED",
        "monotonic": "REQUIRED",
        "regression": "REJECT",
        "sse": "PERSISTED_PROGRESS_ONLY",
        "polling": "RECONCILIATION_REQUIRED",
        "transport_state_authority": "REJECT",
    }

    mutations = (
        ("monotonic", "OPTIONAL"),
        ("regression", "ALLOW"),
        ("polling", "OPTIONAL"),
        ("transport_state_authority", "ALLOW"),
    )
    for field, value in mutations:
        invalid = copy.deepcopy(_policy())
        invalid["controls"]["progress"][field] = value
        assert "PROGRESS_POLICY_INVALID" in _codes(invalid)


def test_req_worker_009() -> None:
    cancellation = _policy()["controls"]["cancellation"]
    assert cancellation == {
        "request_token": "PERSISTED",
        "mode": "COOPERATIVE",
        "application": "SAFE_POINTS_ONLY",
        "lease_validation": "REQUIRED_BEFORE_COMMIT_CHECKPOINT_OR_PUBLICATION",
        "publication": "ATOMIC_ONLY",
        "partial_result_current": "REJECT",
    }

    mutations = (
        ("request_token", "EPHEMERAL"),
        ("application", "ANY_POINT"),
        ("lease_validation", "OPTIONAL"),
        ("publication", "BEST_EFFORT"),
        ("partial_result_current", "ALLOW"),
    )
    for field, value in mutations:
        invalid = copy.deepcopy(_policy())
        invalid["controls"]["cancellation"][field] = value
        assert "CANCELLATION_POLICY_INVALID" in _codes(invalid)


def test_exact_requirement_registry_and_checkpoints() -> None:
    policy = _policy()
    assert policy["coverage"] == ["REQ-WORKER-008", "REQ-WORKER-009"]
    assert list(policy["requirements"]) == policy["coverage"]
    for evidence in policy["requirements"].values():
        assert evidence["authority_paths"]
        assert evidence["checkpoint"] == (
            f"{evidence['test_path']}::{evidence['test_id']}"
        )


def test_missing_requirement_reference_or_checkpoint_fails_closed() -> None:
    missing_requirement = copy.deepcopy(_policy())
    missing_requirement["requirements"].pop("REQ-WORKER-008")
    assert "REQUIREMENT_EVIDENCE_INVALID" in _codes(missing_requirement)

    missing_reference = copy.deepcopy(_policy())
    missing_reference["requirements"]["REQ-WORKER-009"]["authority_paths"][0] = (
        "docs/02-architecture/adrs/missing-authority.md"
    )
    assert "REFERENCE_INVALID" in _codes(missing_reference)

    missing_checkpoint = copy.deepcopy(_policy())
    missing_checkpoint["requirements"]["REQ-WORKER-008"]["checkpoint"] = (
        f"{__file__}::missing_test"
    )
    assert "CHECKPOINT_INVALID" in _codes(missing_checkpoint)


@pytest.mark.parametrize(
    "unsafe_reference",
    ("../outside.md", "C:\\outside.md", "README.md", "https://example.test/policy"),
)
def test_unsafe_or_out_of_domain_reference_is_rejected(
    unsafe_reference: str,
) -> None:
    invalid = copy.deepcopy(_policy())
    invalid["requirements"]["REQ-WORKER-008"]["authority_paths"][0] = unsafe_reference
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


def test_unknown_or_incomplete_configuration_fails_closed() -> None:
    unknown = copy.deepcopy(_policy())
    unknown["controls"]["progress"]["fallback"] = "BEST_EFFORT"
    assert "POLICY_STRUCTURE_INVALID" in _codes(unknown)

    incomplete = copy.deepcopy(_policy())
    incomplete["controls"]["cancellation"].pop("lease_validation")
    assert "CANCELLATION_POLICY_INVALID" in _codes(incomplete)

    fallback = copy.deepcopy(_policy())
    fallback["controls"]["failure_handling"]["silent_fallback"] = "ALLOW"
    assert "FAIL_CLOSED_POLICY_INVALID" in _codes(fallback)

    with pytest.raises(FoundationValidationError) as captured:
        load_policy(POLICY_PATH.parent / "missing-policy.json", ROOT)
    assert captured.value.findings[0].code == "POLICY_UNREADABLE"
