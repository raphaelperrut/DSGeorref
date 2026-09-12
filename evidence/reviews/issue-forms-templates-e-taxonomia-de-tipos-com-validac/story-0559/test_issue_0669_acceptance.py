"""Executable final-review evidence for ISSUE-0669."""

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
SLUG = "issue-forms-templates-e-taxonomia-de-tipos-com-validac"
REVIEW_EVIDENCE = Path(__file__).with_name("REVIEW_EVIDENCE.json")
EXPECTED_CANDIDATE = "a3f0364ecedac56cde0dd76787970b987c8de41b"
EXPECTED_MERGE = "6e3748dfd26f89b6345b6b2442091602420530bd"
EXPECTED_AC_IDS = [f"AC-ISSUE-0669-{index:02d}" for index in range(1, 5)]
EXPECTED_TESTS = [
    "test_epic_090_aceite_happy_path",
    "test_epic_090_aceite_negative_paths",
]
EXPECTED_REQUIREMENTS = {
    "REQ-GOV-002": (
        f"tools/governance/{SLUG}/test_repository_integration.py::"
        "test_epic_090_integracao"
    )
}

CONTRACT_SUITE = f"tests/fnd/{SLUG}/test_contract.py"
FOUNDATION_SUITE = f"tests/fnd/{SLUG}/test_foundation.py"
AUTOMATION_SUITE = f"tests/fnd/{SLUG}/test_automation.py"
INTEGRATION_SUITE = f"tools/governance/{SLUG}/test_repository_integration.py"


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
    for checkpoint in EXPECTED_REQUIREMENTS.values():
        path, separator, test_name = checkpoint.partition("::")
        assert separator and test_name
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"), path)
        names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert test_name in names


def _assert_review_evidence(evidence: Mapping[str, Any]) -> None:
    assert evidence.get("issue_id") == "ISSUE-0669"
    assert evidence.get("reviewed_issue_id") == "ISSUE-0668"
    assert evidence.get("reviewed_pull_request") == 959
    assert evidence.get("candidate_sha") == EXPECTED_CANDIDATE
    assert evidence.get("merge_sha") == EXPECTED_MERGE
    assert evidence.get("candidate_tree") == _git_rev_parse(
        f"{EXPECTED_CANDIDATE}^{{tree}}"
    )
    assert evidence.get("candidate_tree") == _git_rev_parse(f"{EXPECTED_MERGE}^{{tree}}")
    assert evidence.get("acceptance_criteria") == EXPECTED_AC_IDS
    assert evidence.get("acceptance_tests") == EXPECTED_TESTS
    assert evidence.get("requirements_evidence") == EXPECTED_REQUIREMENTS
    assert evidence.get("implicit_approval") is False
    assert evidence.get("self_approval") is False
    assert evidence.get("contract_impact") == "NONE"
    assert evidence.get("migration_required") is False
    assert evidence.get("task_envelope_change") == "NOT_NEEDED"
    assert evidence.get("new_prerequisite_created") is False
    assert evidence.get("architectural_risk_open") == "NONE"

    hosted = evidence.get("hosted_validation")
    assert isinstance(hosted, Mapping)
    assert hosted.get("pull_request") == 959
    assert hosted.get("head_sha") == EXPECTED_CANDIDATE
    assert hosted.get("conclusion") == "SUCCESS"
    runs = hosted.get("runs")
    assert isinstance(runs, list)
    assert {run.get("workflow") for run in runs if isinstance(run, Mapping)} == {
        "epic-090-issue-form-governance",
        "epic-090-issue-form-controls",
        "foundation-ci",
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
    assert reviewer.get("authority") == "ROLE-011"
    assert qa.get("authority") == "GITHUB_ACTIONS"
    assert reviewer.get("authority") != qa.get("authority")
    assert reviewer.get("decision") == qa.get("decision") == "PASS"
    assert reviewer.get("candidate_sha") == qa.get("candidate_sha") == EXPECTED_CANDIDATE
    assert reviewer.get("evidence_paths") == qa.get("evidence_paths")
    assert reviewer.get("residual_risk_ids") == qa.get("residual_risk_ids")

    risks = evidence.get("residual_risks")
    assert isinstance(risks, list)
    risk_ids = {risk.get("id") for risk in risks if isinstance(risk, Mapping)}
    assert risk_ids == set(reviewer.get("residual_risk_ids", []))

    task = json.loads((ROOT / ".codex/tasks/TASK-0559.json").read_text(encoding="utf-8"))
    assert task["dependencies"] == ["STORY-0558"]
    assert task["acceptance_criterion_ids"] == EXPECTED_AC_IDS
    assert task["tests"] == EXPECTED_TESTS
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    review_path = REVIEW_EVIDENCE.relative_to(ROOT).as_posix()
    assert review_path.startswith(task["allow_paths"][0].removesuffix("**"))


def test_epic_090_aceite_happy_path() -> None:
    """Prove candidate lineage, public controls, and requirement evidence."""

    _assert_review_evidence(_load_evidence())
    _assert_requirement_checkpoints_exist()
    _run_pytest(
        f"{CONTRACT_SUITE}::test_epic_090_contrato",
        f"{CONTRACT_SUITE}::test_issue_taxonomy_and_required_fields_are_complete",
        f"{FOUNDATION_SUITE}::test_issue_form_required_acceptance_risk_test_rollback_fields",
        f"{FOUNDATION_SUITE}::test_epic_090_fundacao",
        f"{INTEGRATION_SUITE}::test_epic_090_integracao",
    )


def test_epic_090_aceite_negative_paths() -> None:
    """Prove fail-closed controls and reject ambiguous review coordination."""

    _run_pytest(
        f"{CONTRACT_SUITE}::test_contract_rejects_missing_field_unknown_type_and_bypasses",
        f"{CONTRACT_SUITE}::test_contract_rejects_absent_required_sections",
        f"{FOUNDATION_SUITE}::test_required_field_and_unknown_type_fail_closed",
        f"{AUTOMATION_SUITE}::test_epic_090_automacao",
        f"{INTEGRATION_SUITE}::test_integration_rejects_failed_or_malformed_foundation_report",
        f"{INTEGRATION_SUITE}::test_integration_rejects_failed_or_permissive_automation_report",
        f"{INTEGRATION_SUITE}::test_integration_converts_predecessor_timeout_to_fail_closed_report",
        f"{INTEGRATION_SUITE}::test_integration_rejects_task_identity_scope_and_phase_f_drift",
        f"{INTEGRATION_SUITE}::test_integration_control_plane_has_no_cross_module_import_or_rule_copy",
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

    missing_qa = copy.deepcopy(_load_evidence())
    missing_qa["coordination"][1]["decision"] = "PENDING"
    with pytest.raises(AssertionError):
        _assert_review_evidence(missing_qa)

    shared_authority = copy.deepcopy(_load_evidence())
    shared_authority["coordination"][1]["authority"] = "ROLE-011"
    with pytest.raises(AssertionError):
        _assert_review_evidence(shared_authority)
