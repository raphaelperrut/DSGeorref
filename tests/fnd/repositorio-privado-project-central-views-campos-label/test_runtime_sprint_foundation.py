from __future__ import annotations

import copy
import importlib.util
import json
import sys
from functools import cache
from pathlib import Path
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / (
    "tools/governance/repositorio-privado-project-central-views-campos-label/"
    "runtime-sprint-001-parte-7/evidence_map_validation.py"
)
MAP_PATH = ROOT / (
    "docs/03-engineering/contexts/engineering_governance/"
    "repositorio-privado-project-central-views-campos-label/"
    "runtime-sprint-001-parte-7/foundation-evidence-map.json"
)
MODULE_NAME = "runtime_sprint_foundation_evidence_map_validation"
_validator_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
if _validator_spec is None or _validator_spec.loader is None:
    raise ImportError(f"cannot load validator from {MODULE_PATH}")
_validator = importlib.util.module_from_spec(_validator_spec)
sys.modules[MODULE_NAME] = _validator
_validator_spec.loader.exec_module(_validator)

EvidenceMapValidationError = _validator.EvidenceMapValidationError
load_evidence_map = _validator.load_evidence_map
validate_evidence_map = _validator.validate_evidence_map


@cache
def _evidence_map() -> dict[str, Any]:
    return load_evidence_map(MAP_PATH, ROOT)


def _codes(evidence_map: object) -> set[str]:
    return {
        finding.code
        for finding in validate_evidence_map(evidence_map, ROOT)
    }


def _load_json(relative_path: str) -> dict[str, Any]:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def test_runtime_decision_1() -> None:
    evidence = _evidence_map()["requirements"]["REQ-RUNTIME-001"]
    primitive = _load_json(evidence["primitive_path"])
    boundaries = primitive["controls"]["application_boundaries"]
    assert boundaries["namespace"] == "dsgeorref"
    assert boundaries["application_services"] == "SHARED"
    assert boundaries["surfaces"] == {
        "cli": "THIN_ADAPTER",
        "api": "THIN_ADAPTER",
        "worker": "THIN_ADAPTER",
    }
    assert evidence["test_id"] == "test_runtime_decision_1"


def test_runtime_decision_2() -> None:
    evidence = _evidence_map()["requirements"]["REQ-RUNTIME-002"]
    primitive = _load_json(evidence["primitive_path"])
    boundary = primitive["controls"]["domain_io_boundary"]
    assert boundary == {
        "domain_core": "SYNCHRONOUS",
        "asynchronous_io": "BOUNDARIES_ONLY",
        "asynchronous_domain_core": "REJECT",
    }
    assert evidence["test_id"] == "test_runtime_decision_2"


def test_missing_or_invalid_requirement_fails_closed() -> None:
    missing = copy.deepcopy(_evidence_map())
    missing["requirements"].pop("REQ-RUNTIME-001")
    assert "REQUIREMENT_EVIDENCE_INVALID" in _codes(missing)

    invalid = copy.deepcopy(_evidence_map())
    invalid["requirements"]["REQ-RUNTIME-001"] = "fallback"
    assert "REQUIREMENT_EVIDENCE_INVALID" in _codes(invalid)


def test_invalid_reference_has_no_fallback() -> None:
    invalid = copy.deepcopy(_evidence_map())
    invalid["requirements"]["REQ-RUNTIME-002"]["primitive_path"] = (
        "docs/missing-runtime-fallback.json"
    )
    assert "REFERENCE_INVALID" in _codes(invalid)

    with pytest.raises(EvidenceMapValidationError) as captured:
        load_evidence_map(MAP_PATH.parent / "missing-evidence-map.json", ROOT)
    assert captured.value.findings[0].code == "MAP_UNREADABLE"


def test_incomplete_coverage_is_rejected() -> None:
    incomplete = copy.deepcopy(_evidence_map())
    incomplete["coverage"].remove("REQ-SPRINT-001-009")
    assert "COVERAGE_INCOMPLETE" in _codes(incomplete)


def test_write_scope_is_stable_and_disjoint() -> None:
    scope = _evidence_map()["write_scope"]
    assert len(scope) == len(set(scope)) == 5

    overlapping = copy.deepcopy(_evidence_map())
    overlapping["write_scope"].append(
        "tools/governance/repositorio-privado-project-central-views-campos-label/"
        "runtime-sprint-001-parte-7/nested/**"
    )
    assert "WRITE_SCOPE_INVALID" in _codes(overlapping)
