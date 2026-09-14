"""Executable final-review evidence for ISSUE-0679."""

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
SLUG = "fechamento-da-sprint-001-e-autorizacao-da-primeira-fat"
REVIEW_EVIDENCE = Path(__file__).with_name("REVIEW_EVIDENCE.json")
EXPECTED_CANDIDATE = "97fc405d81b5fb6ab1ff802bf351e17845b2272e"
EXPECTED_MERGE = "ae5ae1818f8438a8fac1822baf1ff4e2995788cb"
EXPECTED_AC_IDS = [f"AC-ISSUE-0679-{index:02d}" for index in range(1, 5)]
EXPECTED_TESTS = [
    "test_epic_092_aceite_happy_path",
    "test_epic_092_aceite_negative_paths",
]

CONTRACT_SUITE = f"tests/fnd/{SLUG}/test_contract.py"
FOUNDATION_SUITE = f"tests/fnd/{SLUG}/test_sprint_001_foundation.py"
AUTOMATION_SUITE = f"tests/fnd/{SLUG}/test_automation.py"
INTEGRATION_SUITE = f"tests/fnd/{SLUG}/test_integration.py"
INTEGRATION_CHECKPOINT = f"{INTEGRATION_SUITE}::test_epic_092_integracao"
EXPECTED_REQUIREMENTS = {
    "REQ-DEV-001": (
        "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/"
        "test_foundation.py::test_host_container_ci_contract_and_no_implicit_downloads"
    ),
    "REQ-EPIC-001": (
        "tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
        "test_contract.py::test_executable_foundation_gate_clean_room_end_to_end"
    ),
    "REQ-FRZ-001": (
        "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "test_materialization.py::"
        "test_foundation_baseline_digest_controlled_change_and_adr_supersession"
    ),
    "REQ-FRZ-002": (
        "tests/fnd/migrations-ci-secret-dependency-scan-e-telemetria-mini/"
        "test_bex_epic_frz_part_2.py::"
        "test_sprint_zero_authorization_and_functional_foundation_gate_blocking"
    ),
    "REQ-FRZ-003": (
        "tests/fnd/ruleset-de-main-checks-unicos-codeowners-politica-de-b/"
        "test_main_ruleset_foundation.py::"
        "test_issue_adr_decision_package_impact_boundary_and_no_silent_divergence"
    ),
    "REQ-FRZ-004": (
        "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "test_materialization.py::"
        "test_foundation_closure_evidence_set_and_material_reopening_criteria"
    ),
    "REQ-GOV-005": (
        "tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "test_materialization.py::test_sprint_zero_baseline_decision_09"
    ),
    "REQ-TST-001": (
        "tests/fnd/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/"
        "test_foundation.py::test_corpus_license_hash_split_and_access_integrity"
    ),
}
INTEGRATED_REQUIREMENTS = {
    "REQ-DEV-001",
    "REQ-FRZ-001",
    "REQ-FRZ-002",
    "REQ-FRZ-003",
    "REQ-FRZ-004",
    "REQ-GOV-005",
}


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


def _candidate_changed_paths() -> set[str]:
    completed = subprocess.run(
        [
            "git",
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            EXPECTED_CANDIDATE,
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    return {line for line in completed.stdout.splitlines() if line}


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
        timeout=600,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def _assert_test_nodes_exist(nodes: Mapping[str, str]) -> None:
    for node in nodes.values():
        path, separator, test_name = node.partition("::")
        assert separator and test_name
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"), path)
        names = {
            item.name
            for item in ast.walk(tree)
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert test_name in names


def _assert_review_evidence(evidence: Mapping[str, Any]) -> None:
    assert evidence.get("issue_id") == "ISSUE-0679"
    assert evidence.get("reviewed_issue_id") == "ISSUE-0678"
    assert evidence.get("reviewed_pull_request") == 969
    assert evidence.get("candidate_sha") == EXPECTED_CANDIDATE
    assert evidence.get("merge_sha") == EXPECTED_MERGE
    assert evidence.get("candidate_tree") == _git_rev_parse(
        f"{EXPECTED_CANDIDATE}^{{tree}}"
    )
    assert evidence.get("candidate_tree") == _git_rev_parse(f"{EXPECTED_MERGE}^{{tree}}")
    assert evidence.get("acceptance_criteria") == EXPECTED_AC_IDS
    assert evidence.get("acceptance_tests") == EXPECTED_TESTS
    assert evidence.get("requirements_evidence") == EXPECTED_REQUIREMENTS
    assert evidence.get("integration_checkpoint") == INTEGRATION_CHECKPOINT
    assert evidence.get("implicit_approval") is False
    assert evidence.get("self_approval") is False
    assert evidence.get("authorization_claim") == "NOT_ASSERTED_BY_ISSUE_0679"
    assert evidence.get("contract_impact") == "NONE"
    assert evidence.get("migration_required") is False
    assert evidence.get("task_envelope_change") == "NOT_NEEDED"
    assert evidence.get("new_prerequisite_created") is False
    assert evidence.get("architectural_risk_open") == "NONE"

    integration_registry = json.loads(
        (
            ROOT
            / "docs/03-engineering/contexts/engineering_governance"
            / SLUG
            / "integration-evidence-registry.json"
        ).read_text(encoding="utf-8")
    )
    assert set(integration_registry["requirement_evidence"]) == INTEGRATED_REQUIREMENTS
    assert integration_registry["required_result"] == "READY_FOR_INDEPENDENT_REVIEW"
    assert integration_registry["authorization_claim"] == "NOT_ASSERTED_BY_INTEGRATION"

    hosted = evidence.get("hosted_validation")
    assert isinstance(hosted, Mapping)
    assert hosted.get("pull_request") == 969
    assert hosted.get("head_sha") == EXPECTED_CANDIDATE
    assert hosted.get("conclusion") == "SUCCESS"
    runs = hosted.get("runs")
    assert isinstance(runs, list) and len(runs) == 2
    assert {run.get("workflow") for run in runs if isinstance(run, Mapping)} == {
        "epic-092-sprint-001-closure-controls",
        "foundation-ci",
    }
    assert all(
        run.get("event") == "pull_request" for run in runs if isinstance(run, Mapping)
    )

    artifacts = evidence.get("candidate_artifacts")
    assert isinstance(artifacts, list) and artifacts
    artifact_paths = {
        artifact.get("path") for artifact in artifacts if isinstance(artifact, Mapping)
    }
    assert artifact_paths == _candidate_changed_paths()
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
    assert reviewer.get("residual_risk_ids") == qa.get("residual_risk_ids") == []
    assert evidence.get("residual_risks") == []

    task = json.loads((ROOT / ".codex/tasks/TASK-0569.json").read_text(encoding="utf-8"))
    assert task["dependencies"] == ["STORY-0568"]
    assert task["acceptance_criterion_ids"] == EXPECTED_AC_IDS
    assert task["tests"] == EXPECTED_TESTS
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    review_path = REVIEW_EVIDENCE.relative_to(ROOT).as_posix()
    assert review_path.startswith(task["allow_paths"][0].removesuffix("**"))


def test_epic_092_aceite_happy_path() -> None:
    """Prove exact candidate lineage, controls, and requirement evidence."""

    _assert_review_evidence(_load_evidence())
    _assert_test_nodes_exist(EXPECTED_REQUIREMENTS)
    _run_pytest(f"{CONTRACT_SUITE}::test_epic_092_contrato")
    _run_pytest(f"{FOUNDATION_SUITE}::test_epic_092_fundacao")
    _run_pytest(f"{AUTOMATION_SUITE}::test_epic_092_automacao")
    _run_pytest(INTEGRATION_CHECKPOINT)
    _run_pytest(EXPECTED_REQUIREMENTS["REQ-EPIC-001"])
    _run_pytest(EXPECTED_REQUIREMENTS["REQ-TST-001"])


def test_epic_092_aceite_negative_paths() -> None:
    """Prove fail-closed controls and reject ambiguous review coordination."""

    _run_pytest(
        f"{CONTRACT_SUITE}::test_contract_rejects_unsafe_or_ambiguous_authorization",
        f"{CONTRACT_SUITE}::test_contract_rejects_missing_proof_exit_condition_or_review_gate",
        f"{FOUNDATION_SUITE}::test_error_paths_are_fail_closed_without_silent_fallback",
    )
    _run_pytest(f"{AUTOMATION_SUITE}::test_epic_092_automacao")
    _run_pytest(INTEGRATION_CHECKPOINT)

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

    authorization_overclaim = copy.deepcopy(_load_evidence())
    authorization_overclaim["authorization_claim"] = (
        "AUTHORIZED_FOR_FIRST_FUNCTIONAL_SLICE"
    )
    with pytest.raises(AssertionError):
        _assert_review_evidence(authorization_overclaim)
