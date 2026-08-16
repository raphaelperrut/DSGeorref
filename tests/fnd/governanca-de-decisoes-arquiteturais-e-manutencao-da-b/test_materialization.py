from __future__ import annotations

import copy
import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = ROOT / (
    "tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "frz-gov-adr-gov-dec-parte-1"
)
sys.path.insert(0, str(MODULE_ROOT))

from baseline_lifecycle import (  # noqa: E402
    AppendOnlyRecordLedger,
    EvidenceArtifact,
    build_baseline,
    validate_baseline,
    validate_closure,
    validate_evidence_set,
    validate_reopening,
    validate_transition,
)
from canonical_json import canonical_json_bytes  # noqa: E402
from decision_governance import (  # noqa: E402
    DECISION_CLASSIFICATIONS,
    LOCAL_CLASSIFICATIONS,
    validate_adr_change_governance,
    validate_classification_before_identifier,
    validate_new_adr_eligibility,
)
from portfolio_validation import validate_snapshot_tombstone_delta_history  # noqa: E402
from sprint_validation import (  # noqa: E402
    derive_story_selection,
    minimum_sprint_scope,
    validate_graph_derived_selection,
    validate_minimum_sprint_scope,
)


def _revision(name: str = "HEAD") -> str:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", name],
        check=True,
        capture_output=True,
        encoding="ascii",
    )
    return completed.stdout.strip()


def _codes(findings: list[Any]) -> set[str]:
    return {finding.code for finding in findings}


def _reference(path: str, content: bytes) -> dict[str, str]:
    return {"path": path, "sha256": hashlib.sha256(content).hexdigest()}


def _baseline(revision: str | None = None, version: str = "1.0.0") -> dict[str, Any]:
    return build_baseline(
        ROOT,
        revision or _revision(),
        "FOUNDATION-BASELINE-CANONICAL",
        version,
    )


def test_foundation_baseline_digest_controlled_change_and_adr_supersession() -> None:
    current = _baseline()
    assert current == _baseline()
    assert validate_baseline(ROOT, current) == []
    assert current["coverage"] == sorted(current["coverage"], key=lambda row: row["path"])
    assert current["coverage"][0]["path"] == ".codex/roles/ROLE-003-tech-lead.md"
    assert any(row["path"] == ".codex/tasks/TASK-0688.json" for row in current["coverage"])

    predecessor = _baseline(_revision("origin/main"), "0.9.0")
    assert predecessor["baseline_digest"] != current["baseline_digest"]
    assert _codes(validate_transition(ROOT, predecessor, current, None)) == {
        "SUPERSESSION_REQUIRED"
    }
    supersession = {
        "schema_version": "1.0.0",
        "record_type": "FOUNDATION_BASELINE_SUPERSESSION",
        "supersession_id": "FOUNDATION-SUPERSESSION-CANONICAL-1",
        "predecessor": {
            key: predecessor[key]
            for key in ("baseline_id", "baseline_version", "baseline_digest")
        },
        "successor": {
            key: current[key]
            for key in ("baseline_id", "baseline_version", "baseline_digest")
        },
        "reason": "TASK-0688 coverage authority changed under reviewed reconciliation.",
        "authority": {"path": "evidence/authority.json", "sha256": "a" * 64},
        "recorded_at": "2026-08-16T18:00:00Z",
    }
    assert validate_transition(ROOT, predecessor, current, supersession) == []

    inconsistent = copy.deepcopy(current)
    inconsistent["coverage"] = list(reversed(inconsistent["coverage"]))
    assert {"COVERAGE_MISMATCH", "DIGEST_MISMATCH"} <= _codes(
        validate_baseline(ROOT, inconsistent)
    )
    ledger = AppendOnlyRecordLedger()
    ledger.append(predecessor)
    ledger.append(current)
    replacement = copy.deepcopy(current)
    replacement["baseline_digest"] = "b" * 64
    try:
        ledger.append(replacement)
    except ValueError as error:
        assert "silent replacement" in str(error)
    else:
        raise AssertionError("immutable record replacement was accepted")


def _closure_fixture() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, EvidenceArtifact],
]:
    baseline = _baseline()
    candidate, merged = _revision(), _revision("origin/main")
    proof_names = (
        "IMPLEMENTATION_AND_MANDATORY_TESTS",
        "ARTIFACTS_AND_CONTRACTS_SYNCHRONIZED",
        "MIGRATIONS_AND_ROLLBACK_APPLICABILITY",
        "APPLICABLE_INVARIANTS",
        "ACCEPTANCE_CRITERIA",
        "QA_APPROVAL",
        "REVIEWER_APPROVAL",
        "DOCUMENTATION_AND_TRACEABILITY",
        "HUMAN_MERGE",
        "APPLICABLE_CTO_CONTROLS",
        "SPRINT_EVIDENCE_SET",
        "FOUNDATION_CHECKS",
        "NETWORK_AUTHENTICATION_APPLICABILITY",
        "SECURE_ROOTS",
        "DIAGNOSTIC_FLOW",
        "FIRST_SLICE_AUTHORIZATION",
        "G1_FOUNDATION_GATE_RESULT",
    )
    artifacts: dict[str, EvidenceArtifact] = {}
    proofs: dict[str, Any] = {}
    for name in proof_names:
        path = f"evidence/proofs/{name.lower()}.json"
        content = canonical_json_bytes({"proof": name})
        artifacts[path] = EvidenceArtifact(
            content,
            reviewed_candidate_commit=candidate,
            merged_commit=merged if name == "HUMAN_MERGE" else None,
        )
        proofs[name] = {"result": "PASS", "artifact": _reference(path, content)}
    evidence_set = {
        "schema_version": "1.0.0",
        "record_type": "FOUNDATION_CLOSURE_EVIDENCE_SET",
        "evidence_set_id": "FOUNDATION-CLOSURE-EVIDENCE-CANONICAL-1",
        "baseline": {
            key: baseline[key]
            for key in ("baseline_id", "baseline_version", "baseline_digest")
        },
        "reviewed_candidate_commit": candidate,
        "merged_commit": merged,
        "proofs": proofs,
    }
    evidence_bytes = canonical_json_bytes(evidence_set)
    authority_bytes = canonical_json_bytes({"authority": "ADR-057"})
    artifacts["evidence/closure-set.json"] = EvidenceArtifact(evidence_bytes)
    artifacts["evidence/closure-authority.json"] = EvidenceArtifact(authority_bytes)
    closure = {
        "schema_version": "1.0.0",
        "record_type": "FOUNDATION_CLOSURE",
        "closure_id": "FOUNDATION-CLOSURE-CANONICAL-1",
        "baseline": evidence_set["baseline"],
        "evidence_set_id": evidence_set["evidence_set_id"],
        "evidence_set": _reference("evidence/closure-set.json", evidence_bytes),
        "closure_authority": _reference(
            "evidence/closure-authority.json", authority_bytes
        ),
        "closed_at": "2026-08-16T18:30:00Z",
    }
    return baseline, evidence_set, closure, artifacts


def test_foundation_closure_evidence_set_and_material_reopening_criteria() -> None:
    baseline, evidence_set, closure, artifacts = _closure_fixture()
    assert validate_evidence_set(ROOT, evidence_set, baseline, artifacts) == []
    assert validate_closure(ROOT, closure, evidence_set, baseline, artifacts) == []

    incomplete = copy.deepcopy(evidence_set)
    incomplete["proofs"].pop("QA_APPROVAL")
    assert "SCHEMA_INVALID" in _codes(
        validate_evidence_set(ROOT, incomplete, baseline, artifacts)
    )
    wrong_link = copy.deepcopy(artifacts)
    first_path = evidence_set["proofs"]["FOUNDATION_CHECKS"]["artifact"]["path"]
    wrong_link[first_path] = EvidenceArtifact(wrong_link[first_path].content, "f" * 40)
    assert "COMMIT_LINK_MISMATCH" in _codes(
        validate_evidence_set(ROOT, evidence_set, baseline, wrong_link)
    )

    closure_bytes = canonical_json_bytes(closure)
    trigger_bytes = canonical_json_bytes({"trigger": "covered source changed"})
    authority_bytes = canonical_json_bytes({"authority": "Project Owner"})
    artifacts["evidence/prior-closure.json"] = EvidenceArtifact(closure_bytes)
    artifacts["evidence/material-trigger.json"] = EvidenceArtifact(trigger_bytes)
    artifacts["evidence/reopening-authority.json"] = EvidenceArtifact(authority_bytes)
    reopening = {
        "schema_version": "1.0.0",
        "record_type": "FOUNDATION_REOPENING",
        "reopening_id": "FOUNDATION-REOPENING-CANONICAL-1",
        "prior_closure_id": closure["closure_id"],
        "prior_closure": _reference("evidence/prior-closure.json", closure_bytes),
        "prior_baseline": closure["baseline"],
        "material_trigger": {
            "kind": "COVERED_SOURCE_DIGEST_CHANGED",
            "evidence": _reference("evidence/material-trigger.json", trigger_bytes),
        },
        "new_candidate_id": "FOUNDATION-CANDIDATE-CANONICAL-2",
        "new_evidence_set_id": "FOUNDATION-CLOSURE-EVIDENCE-CANONICAL-2",
        "authority": _reference("evidence/reopening-authority.json", authority_bytes),
        "reopened_at": "2026-08-16T19:00:00Z",
    }
    ledger = AppendOnlyRecordLedger()
    ledger.append(evidence_set)
    ledger.append(closure)
    assert validate_reopening(
        ROOT, reopening, closure, baseline, evidence_set, artifacts, ledger
    ) == []
    mutated_evidence = copy.deepcopy(evidence_set)
    mutated_evidence["merged_commit"] = "e" * 40
    assert "HISTORY_NOT_PRESERVED" in _codes(
        validate_reopening(
            ROOT, reopening, closure, baseline, mutated_evidence, artifacts, ledger
        )
    )


def test_adr_governance_overlap() -> None:
    assert validate_new_adr_eligibility(
        "NEW_ADR",
        "NEW_ADR",
        boundary_independent=True,
        durable_impact=True,
        high_reversal_cost=True,
    ) == []
    for local_classification in sorted(LOCAL_CLASSIFICATIONS):
        findings = validate_new_adr_eligibility(
            "NEW_ADR",
            local_classification,
            boundary_independent=True,
            durable_impact=True,
            high_reversal_cost=True,
        )
        assert "ARTIFICIAL_ADR_PROMOTION" in _codes(findings)
    assert validate_adr_change_governance(
        overlapping_adr_ids=("ADR-006",),
        superseded_adr_ids=("ADR-006",),
        declared_normative_owner="ADR-040",
        expected_normative_owner="ADR-040",
        owner_approved=True,
    ) == []
    rejected = validate_adr_change_governance(
        overlapping_adr_ids=("ADR-006",),
        superseded_adr_ids=(),
        declared_normative_owner="ADR-999",
        expected_normative_owner="ADR-040",
        owner_approved=False,
    )
    assert _codes(rejected) == {
        "ADR_OVERLAP_UNRESOLVED",
        "NORMATIVE_OWNER_INVALID",
        "OWNER_GATE_REQUIRED",
    }


def test_req_gov_dec_001() -> None:
    assert DECISION_CLASSIFICATIONS == {
        "NEW_ADR",
        "REFINE_EXISTING",
        "APPLICATION_PROFILE",
        "BENCHMARK_PROFILE",
        "ISSUE_DETAIL",
    }
    for classification in DECISION_CLASSIFICATIONS:
        assert validate_classification_before_identifier(classification, None) == []
    early = validate_classification_before_identifier(None, "ADR-999")
    assert _codes(early) == {"CLASSIFICATION_REQUIRED", "IDENTIFIER_ALLOCATED_EARLY"}
    assert _codes(validate_classification_before_identifier("LOCAL_NOTE", None)) == {
        "CLASSIFICATION_INVALID"
    }


def test_req_gov_dec_002() -> None:
    for values in ((False, True, True), (True, False, True), (True, True, False)):
        findings = validate_new_adr_eligibility(
            "NEW_ADR",
            "NEW_ADR",
            boundary_independent=values[0],
            durable_impact=values[1],
            high_reversal_cost=values[2],
        )
        assert _codes(findings) == {"NEW_ADR_INELIGIBLE"}


def test_portfolio_snapshot_tombstone_approved_delta() -> None:
    snapshot = {"snapshot": "PORTFOLIO-1", "items": ["ISSUE-0111", "ISSUE-0798"]}
    assert validate_snapshot_tombstone_delta_history(
        (("PORTFOLIO-1", snapshot),),
        previous_item_ids=("ISSUE-0111", "ISSUE-0798"),
        current_item_ids=("ISSUE-0798",),
        tombstoned_item_ids=("ISSUE-0111",),
        applied_delta_ids=("DELTA-1",),
        approved_delta_ids=("DELTA-1",),
    ) == []
    mutated = {"snapshot": "PORTFOLIO-1", "items": ["ISSUE-0798"]}
    findings = validate_snapshot_tombstone_delta_history(
        (("PORTFOLIO-1", snapshot), ("PORTFOLIO-1", mutated)),
        previous_item_ids=("ISSUE-0111", "ISSUE-0798"),
        current_item_ids=("ISSUE-0798",),
        tombstoned_item_ids=(),
        applied_delta_ids=("DELTA-UNAPPROVED",),
        approved_delta_ids=(),
    )
    assert _codes(findings) == {
        "SNAPSHOT_MUTATED",
        "TOMBSTONE_REQUIRED",
        "DELTA_NOT_APPROVED",
    }


def test_sprint_zero_baseline_decision_01() -> None:
    expected = minimum_sprint_scope(ROOT)
    assert len(expected) == 7
    assert expected[-1] == "SprintEvidenceSet machine-readable"
    assert validate_minimum_sprint_scope(ROOT, expected) == []
    assert _codes(validate_minimum_sprint_scope(ROOT, expected[:-1])) == {
        "SPRINT_MINIMUM_SCOPE_MISMATCH"
    }
    assert _codes(validate_minimum_sprint_scope(ROOT, tuple(reversed(expected)))) == {
        "SPRINT_MINIMUM_SCOPE_MISMATCH"
    }


def test_sprint_zero_baseline_decision_02() -> None:
    expected = derive_story_selection(ROOT, ("STORY-0688",))
    assert expected == ("STORY-0001", "STORY-0688")
    assert expected == derive_story_selection(ROOT, ("STORY-0688",))
    assert validate_graph_derived_selection(ROOT, ("STORY-0688",), expected) == []
    parallel = {
        "STORY-0692",
        "STORY-0693",
        "STORY-0754",
        "STORY-0757",
        "STORY-0758",
    }
    assert parallel.isdisjoint(expected)
    rejected = validate_graph_derived_selection(
        ROOT, ("STORY-0688",), (*expected, "STORY-0692")
    )
    assert _codes(rejected) == {"SPRINT_SELECTION_NON_CANONICAL"}
