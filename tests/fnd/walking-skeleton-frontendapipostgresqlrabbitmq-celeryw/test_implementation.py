from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = ROOT / (
    "tools/governance/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
    "del-ism-sprint-001-parte-1"
)
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
    "del-ism-sprint-001-parte-1/foundation-policy.json"
)
HANDOFF_PATH = POLICY_PATH.with_name("README.md")
VALIDATOR_PATH = MODULE_ROOT / "foundation_validation.py"
sys.path.insert(0, str(MODULE_ROOT))

from foundation_expectations import (  # noqa: E402
    EXPECTED_CAPABILITY_SCOPE,
    EXPECTED_REQUIREMENTS,
)
from foundation_validation import (  # noqa: E402
    load_policy,
    validate_policy,
)


def _policy() -> dict[str, object]:
    loaded = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _codes(policy: object) -> set[str]:
    return {finding.code for finding in validate_policy(policy, ROOT)}


def test_private_operational_baseline_scope_cpu_only_clean_install() -> None:
    policy = load_policy(POLICY_PATH, ROOT)
    assert policy["private_baseline"] == {
        "visibility": "PRIVATE",
        "installation": "CLEAN_REPOSITORY_PINNED",
        "compute": "CPU_ONLY",
        "flow": "APPROVED_WALKING_SKELETON",
        "evidence": "REPRODUCIBLE",
        "public_claims": False,
    }
    assert policy["ci_gate"] == {
        "mode": "PROGRESSIVE",
        "scope": "CAPABILITIES_PRESENT",
        "command": "make verify",
    }


def test_thin_vertical_integrable_slices_and_pr_sequence() -> None:
    policy = load_policy(POLICY_PATH, ROOT)
    assert policy["slice"] == {
        "number": 1,
        "total": 2,
        "dependency_story_ids": ["STORY-0534"],
        "requirement_ids": EXPECTED_REQUIREMENTS,
        "boundary": "CURRENT_SLICE_ONLY",
        "next_slice": "SEPARATE_AUTHORIZATION_REQUIRED",
    }
    assert policy["write_scope"][0] == ".codex/tasks/TASK-0752.json"
    assert policy["write_scope"][1:] == EXPECTED_CAPABILITY_SCOPE
    ticket_pattern = re.compile(r"\b(?:ISSUE|STORY|EPIC)-[0-9]{4}\b")
    assert all(
        ticket_pattern.search(path.read_text(encoding="utf-8")) is None
        for path in MODULE_ROOT.rglob("*.py")
    )


def test_materialization_covers_all_requirements_and_acceptance_criteria() -> None:
    policy = load_policy(POLICY_PATH, ROOT)
    assert list(policy["requirement_evidence"]) == EXPECTED_REQUIREMENTS
    assert policy["diagnostic_job"] == {
        "kind": "SYNTHETIC",
        "functional_georeferencing": False,
    }
    assert policy["contract"]["exercise"] == "ESSENTIAL_ONLY"
    assert policy["evidence_set"]["immutable"] is True
    assert policy["evidence_set"]["machine_readable"] is True


def test_materialization_rejects_drift_and_silent_fallback() -> None:
    silent = copy.deepcopy(_policy())
    silent["failure_policy"]["silent_fallback"] = True
    assert "FAILURE_POLICY_INVALID" in _codes(silent)

    drifted = copy.deepcopy(_policy())
    drifted["contract"]["sha256"] = "0" * 64
    assert "CONTRACT_BINDING_INVALID" in _codes(drifted)

    redirected = copy.deepcopy(_policy())
    redirected["requirement_evidence"]["REQ-DEL-002"] = redirected["requirement_evidence"][
        "REQ-ISM-003"
    ]
    assert "CHECKPOINT_INVALID" in _codes(redirected)

    expanded = copy.deepcopy(_policy())
    expanded["future_capability"] = "OUT_OF_SCOPE"
    assert "POLICY_STRUCTURE_INVALID" in _codes(expanded)


def test_validator_cli_is_deterministic_and_fails_closed() -> None:
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


def test_handoff_records_contract_risk_and_rollback() -> None:
    handoff = HANDOFF_PATH.read_text(encoding="utf-8")
    for heading in ("## Contract impact", "## Risks and limitations", "## Rollback"):
        assert heading in handoff
    assert "No frozen contract was changed" in handoff
    assert "independent QA" in handoff
    assert "Reviewer" in handoff
