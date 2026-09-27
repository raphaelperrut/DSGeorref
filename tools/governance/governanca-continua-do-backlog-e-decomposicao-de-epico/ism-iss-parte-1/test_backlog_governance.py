from __future__ import annotations

import copy
import csv
import importlib.util
import sys
from functools import cache
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

ROOT = Path(__file__).resolve().parents[4]
MODULE_ROOT = Path(__file__).resolve().parent
KNOWN_SOURCES = {
    "ADR-008",
    "REQ-ISM-001",
    "REQ-ISM-002",
    "REQ-ISM-003",
    "REQ-ISM-007",
}
KNOWN_EVIDENCE = {"focused-tests"}
POLICY_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "governanca-continua-do-backlog-e-decomposicao-de-epico/"
    "ism-iss-parte-1/foundation-policy.json"
)
DOMAIN_PATH = POLICY_PATH.with_name("domain-taxonomy.json")


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


POLICY = _load_module("policy_validation", MODULE_ROOT / "policy_validation.py")
VALIDATION = _load_module("backlog_validation", MODULE_ROOT / "backlog_validation.py")
DOMAIN = _load_module("domain_taxonomy", MODULE_ROOT / "domain_taxonomy.py")


@cache
def _policy() -> dict[str, Any]:
    return cast(dict[str, Any], POLICY.load_policy(POLICY_PATH))


@cache
def _domains() -> set[str]:
    return cast(set[str], DOMAIN.load_canonical_domains(DOMAIN_PATH, ROOT))


def _policy_codes(policy: object) -> set[str]:
    return {finding.code for finding in POLICY.validate_policy(policy)}


def _finding_codes(findings: list[Any]) -> set[str]:
    return {finding.code for finding in findings}


def _delivery_rows(name: str) -> list[dict[str, str]]:
    with (ROOT / "docs/06-delivery" / name).open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _work_item() -> dict[str, Any]:
    return {
        "stable_id": "ISSUE-0001",
        "title": "Cross-domain backlog item",
        "github_number": 101,
        "primary_domain": "FND",
        "affected_domains": ["GEO"],
        "references": {
            "adrs": ["ADR-008"],
            "requirements": ["REQ-ISM-001"],
            "risks": [],
            "gates": [],
        },
        "local_decision": None,
    }


def _epic() -> dict[str, Any]:
    return {
        "outcome": "A verifiable backlog-governance foundation is executable.",
        "closure_evidence": ["focused-tests"],
        "epic_issue": "ISSUE-0002",
        "slices": [
            {
                "stable_id": "STORY-0001",
                "requirement_ids": ["REQ-ISM-001", "REQ-ISM-002"],
                "write_scope": "tools/governance/backlog-foundation/**",
                "integration_sequence": 1,
            },
            {
                "stable_id": "STORY-0002",
                "requirement_ids": ["REQ-ISM-003"],
                "write_scope": "docs/03-engineering/backlog-foundation/**",
                "integration_sequence": 2,
            },
        ],
        "acceptance_evidence": [
            {
                "criterion": "Each assigned requirement has evidence.",
                "sources": ["ADR-008", "REQ-ISM-007"],
                "evidence": "focused-tests",
            }
        ],
    }


def test_canonical_domain_taxonomy_primary_and_affected_domains(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert {"FND", "GEO"} <= _domains()
    assert VALIDATION.validate_work_item(_work_item(), _domains(), KNOWN_SOURCES) == []
    unknown = copy.deepcopy(_work_item())
    unknown["affected_domains"] = ["UNKNOWN"]
    assert "DOMAIN_UNKNOWN" in _finding_codes(
        VALIDATION.validate_work_item(unknown, _domains(), KNOWN_SOURCES)
    )
    duplicate = copy.deepcopy(_work_item())
    duplicate["affected_domains"] = ["GEO", "GEO"]
    assert "DOMAIN_TAXONOMY_INVALID" in _finding_codes(
        VALIDATION.validate_work_item(duplicate, _domains(), KNOWN_SOURCES)
    )
    monkeypatch.setattr(DOMAIN, "_index_domains", lambda path: {"XXX"})
    with pytest.raises(ValueError, match="registry diverges"):
        DOMAIN.load_canonical_domains(DOMAIN_PATH, ROOT)


def test_work_package_epics_outcome_evidence_and_closure() -> None:
    assert VALIDATION.validate_epic(_epic(), KNOWN_SOURCES, KNOWN_EVIDENCE) == []
    missing = copy.deepcopy(_epic())
    missing["outcome"] = ""
    missing["closure_evidence"] = []
    assert {
        "EPIC_OUTCOME_MISSING",
        "EPIC_CLOSURE_EVIDENCE_MISSING",
    } <= _finding_codes(VALIDATION.validate_epic(missing, KNOWN_SOURCES, KNOWN_EVIDENCE))
    unresolved = copy.deepcopy(_epic())
    unresolved["closure_evidence"] = ["unpublished-proof"]
    assert "EPIC_CLOSURE_EVIDENCE_MISSING" in _finding_codes(
        VALIDATION.validate_epic(unresolved, KNOWN_SOURCES, KNOWN_EVIDENCE)
    )


def test_thin_vertical_integrable_slices_and_pr_sequence() -> None:
    policy = _policy()["controls"]["vertical_slices"]
    assert policy["maximum_requirements"] == 10
    invalid = copy.deepcopy(_epic())
    invalid["slices"][0]["requirement_ids"] = [f"REQ-{index}" for index in range(11)]
    invalid["slices"][1]["integration_sequence"] = 4
    assert {"SLICE_TOO_LARGE", "SLICE_SEQUENCE_INVALID"} <= _finding_codes(
        VALIDATION.validate_epic(invalid, KNOWN_SOURCES, KNOWN_EVIDENCE)
    )
    duplicated = copy.deepcopy(_epic())
    duplicated["slices"][1]["stable_id"] = duplicated["slices"][0]["stable_id"]
    assert "SLICE_INVALID" in _finding_codes(
        VALIDATION.validate_epic(duplicated, KNOWN_SOURCES, KNOWN_EVIDENCE)
    )


def test_stable_portfolio_ids_independent_github_numbers_titles() -> None:
    before = _work_item()
    after = copy.deepcopy(before)
    after["github_number"] = 202
    after["title"] = "Renamed GitHub issue"
    assert VALIDATION.validate_identity_update(before, after) == []
    after["stable_id"] = "ISSUE-0002"
    assert _finding_codes(VALIDATION.validate_identity_update(before, after)) == {
        "STABLE_ID_CHANGED"
    }
    assert _finding_codes(VALIDATION.validate_identity_update({}, {})) == {"STABLE_ID_INVALID"}


def test_req_ism_007() -> None:
    assert VALIDATION.validate_epic(_epic(), KNOWN_SOURCES, KNOWN_EVIDENCE) == []
    unresolved = copy.deepcopy(_epic())
    unresolved["acceptance_evidence"][0]["sources"] = ["REQ-ISM-999"]
    assert "ACCEPTANCE_EVIDENCE_INVALID" in _finding_codes(
        VALIDATION.validate_epic(unresolved, KNOWN_SOURCES, KNOWN_EVIDENCE)
    )


def test_single_primary_cross_domain_issue_contracts() -> None:
    control = _policy()["controls"]["cross_domain_work"]
    assert control == {
        "issue_identity": "SINGLE",
        "primary_domain_count": 1,
        "affected_domains": "REQUIRED_WHEN_CROSS_DOMAIN",
        "duplicate_issue": "REJECT",
    }
    duplicated = copy.deepcopy(_work_item())
    duplicated["affected_domains"] = ["GEO", "GEO"]
    assert "DOMAIN_TAXONOMY_INVALID" in _finding_codes(
        VALIDATION.validate_work_item(duplicated, _domains(), KNOWN_SOURCES)
    )
    cross_domain_copy = copy.deepcopy(_work_item())
    cross_domain_copy["primary_domain"] = "GEO"
    cross_domain_copy["affected_domains"] = ["FND"]
    assert "DUPLICATE_ISSUE" in _finding_codes(
        VALIDATION.validate_issue_set([_work_item(), cross_domain_copy], _domains(), KNOWN_SOURCES)
    )


def test_req_ism_009() -> None:
    spike = {
        "question": "Does the proposed decomposition integrate?",
        "budget": "one focused experiment",
        "evidence": "recorded result",
        "exit_decision": "accept or reject the decomposition",
    }
    assert VALIDATION.validate_spike(spike) == []
    incomplete = copy.deepcopy(spike)
    incomplete["exit_decision"] = ""
    assert _finding_codes(VALIDATION.validate_spike(incomplete)) == {"SPIKE_INVALID"}


def test_all_work_packages_have_parent_issue_and_slice_skeleton() -> None:
    assert VALIDATION.validate_epic(_epic(), KNOWN_SOURCES, KNOWN_EVIDENCE) == []
    incomplete = copy.deepcopy(_epic())
    incomplete["epic_issue"] = ""
    incomplete["slices"] = []
    assert {"EPIC_ISSUE_MISSING", "SLICE_SKELETON_MISSING"} <= _finding_codes(
        VALIDATION.validate_epic(incomplete, KNOWN_SOURCES, KNOWN_EVIDENCE)
    )
    epics = _delivery_rows("EPIC_INDEX.csv")
    stories = _delivery_rows("STORY_INDEX.csv")
    epic_ids = {row["epic_id"] for row in epics}
    story_parents = {row["epic_id"] for row in stories}
    assert len(epics) == len(epic_ids)
    assert epic_ids == story_parents
    assert all(row["issue_id"].startswith("ISSUE-") for row in epics)
    assert all(row["story_id"] and row["issue_id"] and row["task_id"] for row in stories)


def test_no_orphan_issue_without_adr_or_local_decision_justification() -> None:
    governed = _work_item()
    assert VALIDATION.validate_work_item(governed, _domains(), KNOWN_SOURCES) == []
    orphan = copy.deepcopy(governed)
    orphan["references"] = {"adrs": [], "requirements": [], "risks": [], "gates": []}
    assert "ORPHAN_ISSUE" in _finding_codes(
        VALIDATION.validate_work_item(orphan, _domains(), KNOWN_SOURCES)
    )
    orphan["local_decision"] = {"justification": "Local reversible choice", "reversible": True}
    assert VALIDATION.validate_work_item(orphan, _domains(), KNOWN_SOURCES) == []
    orphan["local_decision"]["reversible"] = False
    assert {"LOCAL_DECISION_INVALID", "ORPHAN_ISSUE"} <= _finding_codes(
        VALIDATION.validate_work_item(orphan, _domains(), KNOWN_SOURCES)
    )
    stories = _delivery_rows("STORY_INDEX.csv")
    assert all(row["governing_adrs"] or row["requirements"] for row in stories)


def test_policy_rejects_unknown_missing_and_unreadable_input(tmp_path: Path) -> None:
    assert POLICY.validate_policy(_policy()) == []
    unknown = copy.deepcopy(_policy())
    unknown["fallback"] = "ALLOW"
    assert "POLICY_STRUCTURE_INVALID" in _policy_codes(unknown)
    missing = copy.deepcopy(_policy())
    del missing["controls"]["baseline_history"]
    assert "BASELINE_HISTORY_INVALID" in _policy_codes(missing)
    with pytest.raises(POLICY.PolicyValidationError, match="POLICY_UNREADABLE"):
        POLICY.load_policy(tmp_path / "missing.json")
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"owner":"BC-001","owner":"BC-002"}', encoding="utf-8")
    with pytest.raises(POLICY.PolicyValidationError, match="duplicate JSON key"):
        POLICY.load_policy(duplicate)
    non_finite = tmp_path / "non-finite.json"
    non_finite.write_text('{"value":NaN}', encoding="utf-8")
    with pytest.raises(POLICY.PolicyValidationError, match="non-finite JSON constant"):
        POLICY.load_policy(non_finite)
