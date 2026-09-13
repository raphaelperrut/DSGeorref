from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[3]
SLUG = "ruleset-de-main-checks-unicos-codeowners-politica-de-b"
TOOL_ROOT = ROOT / "tools/governance" / SLUG
TOOL_PATH = TOOL_ROOT / "foundation_validation.py"


def _load_tool() -> ModuleType:
    sys.path.insert(0, str(TOOL_ROOT))
    spec = importlib.util.spec_from_file_location("main_ruleset_foundation_validation", TOOL_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TOOL = _load_tool()


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _valid_bypass_record(candidate_sha: str, verdict_ref: str) -> dict[str, str]:
    return {
        "event_id": "bypass-event-001",
        "ruleset_id": "DSGEOREF-MAIN",
        "protected_branch": "main",
        "candidate_sha": candidate_sha,
        "actor_subject": "authorized-maintainer",
        "reason": "documented emergency recovery",
        "occurred_at": "2026-09-12T12:00:00Z",
        "delivery_approval_verdict_ref": verdict_ref,
    }


def test_epic_091_fundacao() -> None:
    report = TOOL.validate_foundation(ROOT)
    assert report["decision"] == "PASS"
    assert report["live_ruleset_enforcement"] == "NOT_ASSERTED_BY_FOUNDATION"
    assert report["required_checks"] == ["verify-foundation"]
    assert set(report["requirement_evidence"]) == {
        "REQ-FRZ-003",
        "REQ-GOV-004",
        "REQ-ISS-003",
        "REQ-ISS-006",
        "REQ-PUB-002",
    }
    assert report["acceptance_evidence"] == dict.fromkeys(
        TOOL.EXPECTED_AC_IDS, "test_epic_091_fundacao"
    )

    checkpoint = TOOL.validate_checkpoint(ROOT)
    command = checkpoint["reproducible_command"]
    assert command == checkpoint["local_command"] == checkpoint["ci_command"]
    assert TOOL.validate_ci_integration(ROOT)["command"] == command

    completed = subprocess.run(
        [sys.executable, "-X", "utf8", str(TOOL_PATH)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["decision"] == "PASS"


def test_issue_adr_decision_package_impact_boundary_and_no_silent_divergence() -> None:
    checkpoint = TOOL.validate_checkpoint(ROOT)
    task = _load_json(TOOL.TASK_PATH)
    contract = TOOL.validate_contract(ROOT)
    assert checkpoint["requirement_evidence"]["REQ-FRZ-003"] == (
        "test_issue_adr_decision_package_impact_boundary_and_no_silent_divergence"
    )

    divergent = copy.deepcopy(checkpoint)
    divergent["requirement_evidence"]["REQ-FRZ-003"] = "implicit-local-decision"
    with pytest.raises(TOOL.FoundationValidationError, match="requirement evidence diverges"):
        TOOL._validate_checkpoint_document(divergent, task=task, contract=contract)


def test_no_orphan_issue_without_adr_or_local_decision_justification() -> None:
    checkpoint = TOOL.validate_checkpoint(ROOT)
    task = _load_json(TOOL.TASK_PATH)
    contract = TOOL.validate_contract(ROOT)
    assert set(task["governing_adrs"]) == {
        "ADR-003",
        "ADR-006",
        "ADR-007",
        "ADR-008",
        "ADR-016",
        "ADR-057",
    }
    assert set(checkpoint["requirement_evidence"]) == {
        item["requirement_id"] for item in contract["requirement_evidence"]
    }

    orphaned = copy.deepcopy(checkpoint)
    del orphaned["requirement_evidence"]["REQ-ISS-003"]
    with pytest.raises(TOOL.FoundationValidationError, match="requirement evidence diverges"):
        TOOL._validate_checkpoint_document(orphaned, task=task, contract=contract)


def test_registry_codeowners_and_ruleset_reject_drift_fail_closed() -> None:
    contract = TOOL.validate_contract(ROOT)
    registry = _load_json(TOOL.REGISTRY_PATH)
    ruleset = _load_json(TOOL.RULESET_PATH)

    duplicate = copy.deepcopy(registry)
    duplicate["required_checks"].append(copy.deepcopy(duplicate["required_checks"][0]))
    with pytest.raises(TOOL.FoundationValidationError, match="duplicate required check context"):
        TOOL.validate_required_check_registry(duplicate, ROOT)

    stale_ruleset = copy.deepcopy(ruleset)
    stale_ruleset["branch_policy"]["direct_push"] = "ALLOW"
    with pytest.raises(TOOL.FoundationValidationError, match="branch policy diverges"):
        TOOL.validate_ruleset(
            stale_ruleset,
            contract=contract,
            required_contexts=["verify-foundation"],
        )

    with pytest.raises(TOOL.FoundationValidationError, match="global CODEOWNERS coverage missing"):
        TOOL.validate_codeowners("/src/ @maintainer\n")


def test_bypass_proof_requires_exact_sha_authority_and_complete_evidence() -> None:
    candidate_sha = "a" * 40
    verdict_ref = "delivery-approval-verdict-001"
    record = _valid_bypass_record(candidate_sha, verdict_ref)
    TOOL.validate_bypass_record(
        record,
        ruleset_id="DSGEOREF-MAIN",
        candidate_sha=candidate_sha,
        delivery_approval_verdict_ref=verdict_ref,
    )

    stale = copy.deepcopy(record)
    stale["candidate_sha"] = "b" * 40
    with pytest.raises(TOOL.FoundationValidationError, match="candidate SHA is stale"):
        TOOL.validate_bypass_record(
            stale,
            ruleset_id="DSGEOREF-MAIN",
            candidate_sha=candidate_sha,
            delivery_approval_verdict_ref=verdict_ref,
        )

    missing = copy.deepcopy(record)
    del missing["reason"]
    with pytest.raises(TOOL.FoundationValidationError, match="fields are incomplete"):
        TOOL.validate_bypass_record(
            missing,
            ruleset_id="DSGEOREF-MAIN",
            candidate_sha=candidate_sha,
            delivery_approval_verdict_ref=verdict_ref,
        )

    assert TOOL.main(["--repository-root", str(ROOT), "--bypass-record", "missing.json"]) == 1
