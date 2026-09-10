from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = ROOT / (
    "tools/governance/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/sprint-001-parte-2"
)
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
    "sprint-001-parte-2/foundation-policy.json"
)
HANDOFF_PATH = POLICY_PATH.with_name("README.md")
VALIDATOR_PATH = MODULE_ROOT / "foundation_validation.py"
sys.path.insert(0, str(MODULE_ROOT))

from foundation_expectations import (  # noqa: E402
    EVIDENCE_PATH,
    EXPECTED_CAPABILITY_SCOPE,
    EXPECTED_CLOSURE_POLICY,
    EXPECTED_CUTOVER_POLICY,
    EXPECTED_REQUIREMENTS,
    EXPECTED_TEST_TARGETS,
)
from foundation_validation import (  # noqa: E402
    canonical_json_sha256,
    load_policy,
    validate_policy,
)


def _policy() -> dict[str, object]:
    loaded = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _codes(policy: object) -> set[str]:
    return {finding.code for finding in validate_policy(policy, ROOT)}


def test_completion_policy_covers_closure_and_cutover() -> None:
    policy = load_policy(POLICY_PATH, ROOT)
    assert policy["slice"]["requirement_ids"] == EXPECTED_REQUIREMENTS
    assert policy["sprint_closure"] == EXPECTED_CLOSURE_POLICY
    assert policy["first_slice_cutover"] == EXPECTED_CUTOVER_POLICY
    assert policy["contract"]["change"] == "NONE"


def test_completion_policy_binds_canonical_checkpoints() -> None:
    policy = load_policy(POLICY_PATH, ROOT)
    assert list(policy["requirement_evidence"]) == EXPECTED_REQUIREMENTS
    for requirement, (path, test_id) in EXPECTED_TEST_TARGETS.items():
        assert policy["requirement_evidence"][requirement] == {
            "test_path": path,
            "test_id": test_id,
            "checkpoint": f"{path}::{test_id}",
        }


def test_completion_policy_rejects_fallback_and_missing_proofs() -> None:
    assert "POLICY_STRUCTURE_INVALID" in _codes([])

    silent = copy.deepcopy(_policy())
    silent["failure_policy"]["silent_fallback"] = True
    assert "FAILURE_POLICY_INVALID" in _codes(silent)

    calendar = copy.deepcopy(_policy())
    calendar["sprint_closure"]["calendar_fallback"] = True
    assert "SPRINT_CLOSURE_POLICY_INVALID" in _codes(calendar)

    no_gate = copy.deepcopy(_policy())
    no_gate["first_slice_cutover"]["foundation_gate"] = "OPTIONAL"
    assert "CUTOVER_POLICY_INVALID" in _codes(no_gate)

    no_authorization = copy.deepcopy(_policy())
    no_authorization["first_slice_cutover"]["first_slice_authorization"] = "ABSENT"
    assert "CUTOVER_POLICY_INVALID" in _codes(no_authorization)


def test_completion_policy_rejects_checkpoint_scope_and_contract_drift() -> None:
    redirected = copy.deepcopy(_policy())
    redirected["requirement_evidence"][EXPECTED_REQUIREMENTS[0]] = redirected[
        "requirement_evidence"
    ][EXPECTED_REQUIREMENTS[1]]
    assert "CHECKPOINT_INVALID" in _codes(redirected)

    expanded = copy.deepcopy(_policy())
    expanded["write_scope"].append("src/**")
    assert "WRITE_SCOPE_INVALID" in _codes(expanded)

    drifted = copy.deepcopy(_policy())
    drifted["contract"]["sha256"] = "0" * 64
    assert "CONTRACT_BINDING_INVALID" in _codes(drifted)


def test_completion_evidence_is_canonical_and_immutable() -> None:
    policy = load_policy(POLICY_PATH, ROOT)
    evidence = json.loads((ROOT / EVIDENCE_PATH).read_text(encoding="utf-8"))
    assert evidence["payload_sha256"] == canonical_json_sha256(evidence["payload"])
    assert evidence["payload"]["requirements"] == EXPECTED_REQUIREMENTS
    assert policy["evidence_set"]["immutable"] is True


def test_completion_validator_cli_is_deterministic_and_fails_closed() -> None:
    command = [
        sys.executable,
        str(VALIDATOR_PATH),
        "--policy",
        str(POLICY_PATH),
        "--repository-root",
        str(ROOT),
    ]
    first = subprocess.run(command, check=False, capture_output=True, text=True)
    second = subprocess.run(command, check=False, capture_output=True, text=True)
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert json.loads(first.stdout)["status"] == "PASS"

    missing = POLICY_PATH.with_name("missing-policy.json")
    failed = subprocess.run(
        [*command[:3], str(missing), *command[4:]],
        check=False,
        capture_output=True,
        text=True,
    )
    assert failed.returncode == 2
    report = json.loads(failed.stdout)
    assert report["status"] == "FAIL"
    assert report["findings"][0]["code"] == "POLICY_UNREADABLE"


def test_completion_handoff_records_contract_risk_and_rollback() -> None:
    handoff = HANDOFF_PATH.read_text(encoding="utf-8")
    for heading in ("## Contract impact", "## Risks and limitations", "## Rollback"):
        assert heading in handoff
    assert "No frozen contract was changed" in handoff
    assert "Independent QA" in handoff
    assert "Reviewer" in handoff
    assert "does not grant a real" in handoff
    assert _policy()["write_scope"] == EXPECTED_CAPABILITY_SCOPE
