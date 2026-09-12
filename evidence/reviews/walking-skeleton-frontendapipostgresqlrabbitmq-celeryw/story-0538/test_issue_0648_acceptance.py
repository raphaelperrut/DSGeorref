"""Executable final-review evidence for ISSUE-0648.

The public entrypoints reuse the governed EPIC-086 checkpoints and bind the
review to the immutable ISSUE-0647 candidate. Runtime evidence that requires
PostgreSQL and RabbitMQ is taken only from the successful hosted gate for that
exact candidate SHA; it is never inferred from the read-only integration report.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[4]
SLUG = "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw"
REVIEW_EVIDENCE = Path(__file__).with_name("REVIEW_EVIDENCE.json")
EXPECTED_CANDIDATE = "94c073428be1e8bbe49d078767651ec9237594b7"
EXPECTED_MERGE = "21e7b73d3e6e75ab9d18eaf098e8ec22db7ffdc3"
EXPECTED_AC_IDS = [f"AC-ISSUE-0648-{index:02d}" for index in range(1, 5)]
EXPECTED_TESTS = [
    "test_epic_086_aceite_happy_path",
    "test_epic_086_aceite_negative_paths",
]
EXPECTED_REQUIREMENTS = {
    "REQ-DEL-001": (
        "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/"
        "test_foundation.py::"
        "test_walking_skeleton_end_to_end_and_vertical_slice_definition_of_done"
    ),
    "REQ-DEL-002": (
        f"tests/fnd/{SLUG}/test_implementation.py::"
        "test_private_operational_baseline_scope_cpu_only_clean_install"
    ),
    "REQ-EPIC-001": (
        f"tests/fnd/{SLUG}/test_contract.py::"
        "test_executable_foundation_gate_clean_room_end_to_end"
    ),
    "REQ-ISM-003": (
        f"tests/fnd/{SLUG}/test_implementation.py::"
        "test_thin_vertical_integrable_slices_and_pr_sequence"
    ),
    **{
        f"REQ-SPRINT-001-{index:03d}": (
            "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
            + (
                "test_contract.py::test_sprint_zero_baseline_decision_04"
                if index == 4
                else (
                    "test_materialization.py::"
                    f"test_sprint_zero_baseline_decision_{index:02d}"
                )
            )
        )
        for index in range(1, 11)
    },
}

CONTRACT_SUITE = f"tests/fnd/{SLUG}/test_contract.py"
IMPLEMENTATION_SUITE = f"tests/fnd/{SLUG}/test_implementation.py"
COMPLETION_SUITE = f"tests/fnd/{SLUG}/test_completion.py"
CONSOLIDATION_SUITE = f"tests/fnd/{SLUG}/test_slice_consolidation.py"
AUTOMATION_SUITE = f"tests/fnd/{SLUG}/test_automation.py"
INTEGRATION_SUITE = f"tools/governance/{SLUG}/test_repository_integration.py"
FOUNDATION_SUITE = (
    "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/"
    "test_foundation.py"
)
def _load_evidence() -> dict[str, Any]:
    loaded = json.loads(REVIEW_EVIDENCE.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_text(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def _candidate_blob(path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{EXPECTED_CANDIDATE}:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stderr.decode(errors="replace")
    return completed.stdout


def _git_rev_parse(revision: str) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", revision],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout.strip()


def _run_pytest(*nodes: str) -> None:
    environment = os.environ.copy()
    environment.update(
        {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"}
    )
    completed = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *nodes],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=240,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def _assert_requirement_checkpoints_exist() -> None:
    by_path: dict[str, set[str]] = {}
    for checkpoint in EXPECTED_REQUIREMENTS.values():
        path, separator, test_name = checkpoint.partition("::")
        assert separator and test_name
        by_path.setdefault(path, set()).add(test_name)
    for path, expected_names in by_path.items():
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"), path)
        actual_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert expected_names <= actual_names


def _assert_review_evidence(evidence: Mapping[str, Any]) -> None:
    assert evidence.get("issue_id") == "ISSUE-0648"
    assert evidence.get("reviewed_issue_id") == "ISSUE-0647"
    assert evidence.get("candidate_sha") == EXPECTED_CANDIDATE
    assert evidence.get("merge_sha") == EXPECTED_MERGE
    assert evidence.get("candidate_tree") == _git_rev_parse(f"{EXPECTED_CANDIDATE}^{{tree}}")
    assert evidence.get("candidate_tree") == _git_rev_parse(f"{EXPECTED_MERGE}^{{tree}}")
    assert evidence.get("acceptance_criteria") == EXPECTED_AC_IDS
    assert evidence.get("acceptance_tests") == EXPECTED_TESTS
    assert evidence.get("requirements_evidence") == EXPECTED_REQUIREMENTS
    assert evidence.get("implicit_approval") is False
    assert evidence.get("contract_impact") == "NONE"
    assert evidence.get("migration_required") is False

    hosted = evidence.get("hosted_validation")
    assert isinstance(hosted, Mapping)
    assert hosted.get("pull_request") == 954
    assert hosted.get("head_sha") == EXPECTED_CANDIDATE
    assert hosted.get("required_check") == "verify-foundation"
    assert hosted.get("services") == ["postgres:18.4", "rabbitmq:4.3.4"]
    assert hosted.get("conclusion") == "SUCCESS"

    gate = evidence.get("foundation_gate")
    assert gate == {
        "decision": "PENDING_PR_MERGE",
        "failure_mode": "FAIL_CLOSED",
        "first_functional_slice_authorized": False,
    }

    artifacts = evidence.get("candidate_artifacts")
    assert isinstance(artifacts, list) and artifacts
    for artifact in artifacts:
        assert isinstance(artifact, Mapping)
        path = artifact.get("path")
        digest = artifact.get("sha256")
        assert isinstance(path, str) and path
        assert isinstance(digest, str) and len(digest) == 64
        assert _sha256(_canonical_text(ROOT / path)) == digest
        assert _sha256(_candidate_blob(path)) == digest

    coordination = evidence.get("coordination")
    assert isinstance(coordination, list) and len(coordination) == 2
    by_role = {
        item.get("role"): item for item in coordination if isinstance(item, Mapping)
    }
    assert set(by_role) == {"QA", "Reviewer"}
    reviewer = by_role["Reviewer"]
    qa = by_role["QA"]
    assert reviewer.get("decision") == qa.get("decision") == "PASS"
    assert reviewer.get("candidate_sha") == qa.get("candidate_sha") == EXPECTED_CANDIDATE
    assert reviewer.get("evidence_paths") == qa.get("evidence_paths")
    assert reviewer.get("residual_risk_ids") == qa.get("residual_risk_ids")

    risks = evidence.get("residual_risks")
    assert isinstance(risks, list)
    risk_ids = {risk.get("id") for risk in risks if isinstance(risk, Mapping)}
    assert risk_ids == set(reviewer.get("residual_risk_ids", []))

    task = json.loads((ROOT / ".codex/tasks/TASK-0538.json").read_text(encoding="utf-8"))
    assert task["dependencies"] == ["STORY-0537"]
    assert task["acceptance_criterion_ids"] == EXPECTED_AC_IDS
    assert task["tests"] == EXPECTED_TESTS
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    review_path = REVIEW_EVIDENCE.relative_to(ROOT).as_posix()
    assert review_path.startswith(task["allow_paths"][0].removesuffix("**"))


def test_epic_086_aceite_happy_path() -> None:
    """Prove the candidate lineage, governed flow, and requirement evidence."""

    _assert_review_evidence(_load_evidence())
    _assert_requirement_checkpoints_exist()
    _run_pytest(
        f"{CONTRACT_SUITE}::test_epic_086_contrato",
        f"{CONTRACT_SUITE}::test_executable_foundation_gate_clean_room_end_to_end",
    )
    _run_pytest(
        f"{IMPLEMENTATION_SUITE}::test_private_operational_baseline_scope_cpu_only_clean_install",
        f"{IMPLEMENTATION_SUITE}::test_thin_vertical_integrable_slices_and_pr_sequence",
        f"{IMPLEMENTATION_SUITE}::test_materialization_covers_all_requirements_and_acceptance_criteria",
    )
    _run_pytest(
        f"{COMPLETION_SUITE}::test_completion_policy_covers_closure_and_cutover",
        f"{COMPLETION_SUITE}::test_completion_policy_binds_canonical_checkpoints",
        f"{COMPLETION_SUITE}::test_completion_evidence_is_canonical_and_immutable",
    )
    _run_pytest(f"{CONSOLIDATION_SUITE}::test_story_0535_slice_consolidation")
    _run_pytest(f"{AUTOMATION_SUITE}::test_epic_086_automacao")
    _run_pytest(f"{INTEGRATION_SUITE}::test_epic_086_integracao")
    _run_pytest(f"{FOUNDATION_SUITE}::test_host_container_ci_contract_and_no_implicit_downloads")


def test_epic_086_aceite_negative_paths() -> None:
    """Prove fail-closed controls and reject ambiguous review coordination."""

    _run_pytest(f"{CONTRACT_SUITE}::test_walking_skeleton_fail_closed_paths")
    _run_pytest(
        f"{IMPLEMENTATION_SUITE}::test_materialization_rejects_drift_and_silent_fallback",
        f"{IMPLEMENTATION_SUITE}::test_validator_cli_is_deterministic_and_fails_closed",
    )
    _run_pytest(
        f"{COMPLETION_SUITE}::test_completion_policy_rejects_fallback_and_missing_proofs",
        f"{COMPLETION_SUITE}::test_completion_policy_rejects_checkpoint_scope_and_contract_drift",
        f"{COMPLETION_SUITE}::test_completion_validator_cli_is_deterministic_and_fails_closed",
    )
    _run_pytest(
        f"{AUTOMATION_SUITE}::test_gate_rejects_silent_fallback_without_substitution",
        f"{AUTOMATION_SUITE}::test_gate_rejects_non_mapping_contract_input",
        f"{AUTOMATION_SUITE}::test_gate_rejects_missing_contract_source_with_actionable_diagnostic",
        f"{AUTOMATION_SUITE}::test_cli_fails_closed_for_malformed_input",
    )
    _run_pytest(
        f"{INTEGRATION_SUITE}::test_integration_rejects_failed_consolidation_checkpoint",
        f"{INTEGRATION_SUITE}::test_integration_rejects_failed_malformed_or_permissive_automation",
        f"{INTEGRATION_SUITE}::test_integration_rejects_task_identity_scope_and_phase_f_drift",
        f"{INTEGRATION_SUITE}::test_integration_converts_predecessor_timeout_to_fail_closed_result",
        f"{INTEGRATION_SUITE}::test_integration_has_no_cross_module_import_or_rule_copy",
    )

    sha_mismatch = copy.deepcopy(_load_evidence())
    sha_mismatch["coordination"][1]["candidate_sha"] = "0" * 40
    with pytest.raises(AssertionError):
        _assert_review_evidence(sha_mismatch)

    digest_mismatch = copy.deepcopy(_load_evidence())
    digest_mismatch["candidate_artifacts"][0]["sha256"] = "0" * 64
    with pytest.raises(AssertionError):
        _assert_review_evidence(digest_mismatch)

    implicit_approval = copy.deepcopy(_load_evidence())
    implicit_approval["implicit_approval"] = True
    with pytest.raises(AssertionError):
        _assert_review_evidence(implicit_approval)

    missing_qa_approval = copy.deepcopy(_load_evidence())
    missing_qa_approval["coordination"][1]["decision"] = "PENDING"
    with pytest.raises(AssertionError):
        _assert_review_evidence(missing_qa_approval)
