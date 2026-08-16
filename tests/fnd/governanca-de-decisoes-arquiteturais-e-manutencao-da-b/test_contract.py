from __future__ import annotations

import copy
import csv
import json
import runpy
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "governanca-de-decisoes-arquiteturais-e-manutencao-da-b"
)
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"

PORTFOLIO_SCHEMA = CONTRACT_ROOT / "portfolio-snapshot.schema.json"
PORTFOLIO_EXAMPLE = CONTRACT_ROOT / "examples/portfolio-snapshot.json"
FORECAST_SCHEMA = CONTRACT_ROOT / "issue-forecast.schema.json"
FORECAST_EXAMPLE = CONTRACT_ROOT / "examples/issue-forecast.json"
BOUNDARIES_SCHEMA = CONTRACT_ROOT / "foundation-boundaries.schema.json"
BOUNDARIES_EXAMPLE = CONTRACT_ROOT / "examples/foundation-boundaries.json"
VALIDATOR_PATH = (
    ROOT
    / "tools/quality/contexts/engineering_governance"
    / "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/validator.py"
)

PUBLISHED_PATHS = {
    path.relative_to(ROOT).as_posix()
    for path in (
        MANIFEST_PATH,
        PORTFOLIO_SCHEMA,
        PORTFOLIO_EXAMPLE,
        FORECAST_SCHEMA,
        FORECAST_EXAMPLE,
        BOUNDARIES_SCHEMA,
        BOUNDARIES_EXAMPLE,
    )
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_manifest() -> dict[str, Any]:
    loaded = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _validator(schema_path: Path) -> Draft202012Validator:
    schema = _load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _assert_schema_rejects(
    validator: Draft202012Validator, instance: dict[str, Any]
) -> None:
    assert list(validator.iter_errors(instance)), "invalid instance was silently accepted"


def _assert_fails(check: Callable[[], None]) -> None:
    try:
        check()
    except AssertionError:
        return
    raise AssertionError("inconsistent contract data was silently accepted")


def _contract_entry(manifest: dict[str, Any], contract_id: str) -> dict[str, Any]:
    matches = [item for item in manifest["contracts"] if item["contract_id"] == contract_id]
    assert len(matches) == 1
    return matches[0]


def _validator_symbols() -> dict[str, Any]:
    sys.path.insert(0, str(VALIDATOR_PATH.parent))
    try:
        return runpy.run_path(str(VALIDATOR_PATH))
    finally:
        sys.path.pop(0)


def _synthetic_schema_pair(dialect: object) -> tuple[dict[str, Any], list[Any]]:
    symbols = _validator_symbols()
    validate_pairs = symbols["_validate_schema_pairs"]
    validator_globals = validate_pairs.__globals__
    validator_globals["EXPECTED_CONTRACTS"] = {
        "synthetic": {
            "schema": Path("synthetic.schema.json"),
            "example": Path("synthetic.example.json"),
        }
    }
    schema = {
        "$schema": dialect,
        "$id": "https://dsgeorref.local/contracts/synthetic/1.0.0",
        "type": "object",
    }

    def load_synthetic(path: Path, artifact: str) -> tuple[dict[str, Any], list[Any]]:
        del artifact
        return (schema if path.name == "synthetic.schema.json" else {}), []

    validator_globals["_load_json"] = load_synthetic
    return validate_pairs(ROOT)


def _assert_portfolio_semantics(snapshot: dict[str, Any]) -> None:
    reconciliations = snapshot["reconciliations"]
    stable_ids = [item["stable_id"] for item in reconciliations]
    github_sides = [
        (
            item["github_issue"]["repository"],
            item["github_issue"]["issue_number"],
            item["github_issue"]["node_id"],
        )
        for item in reconciliations
    ]
    assert len(stable_ids) == len(set(stable_ids))
    assert len(github_sides) == len(set(github_sides))
    assert all(
        item["stable_id"] == item["repository_issue"]["issue_id"]
        for item in reconciliations
    )
    assert all(item["status"] == "RECONCILED" for item in reconciliations)
    assert snapshot["reconciliation_summary"]["reconciled"] == len(reconciliations)
    assert snapshot["reconciliation_summary"]["unresolved"] == 0


def _assert_forecast_semantics(forecast: dict[str, Any]) -> None:
    interval = forecast["interval"]
    assert interval["minimum"] <= interval["mode"] <= interval["maximum"]
    assert forecast["variance"]["basis_snapshot_id"] == forecast["snapshot"]["snapshot_id"]
    assert forecast["variance"]["basis_snapshot_version"] == forecast["snapshot"][
        "snapshot_version"
    ]


def _assert_boundary_semantics(decision: dict[str, Any]) -> None:
    boundaries = decision["boundaries"]
    assert set(boundaries) == {"core", "api", "runners"}
    ids = [boundary["boundary_id"] for boundary in boundaries.values()]
    concerns = [boundary["concern"] for boundary in boundaries.values()]
    assert len(ids) == len(set(ids)) == 3
    assert len(concerns) == len(set(concerns)) == 3
    assert all(boundary["runtime_materialized"] is False for boundary in boundaries.values())


def _assert_manifest(manifest: dict[str, Any], *, require_files: bool = True) -> None:
    assert manifest["schema_version"] == "1.0.0"
    assert manifest["contract_version"] == "1.0.0"
    assert manifest["owner"] == "BC-001"
    assert manifest["compatibility"]["policy"] == "SEMVER"
    assert manifest["compatibility"]["breaking_change"] == "NEW_MAJOR_OR_REPLACEMENT_ADR"
    assert manifest["runtime"]["http"] == "NOT_APPLICABLE"
    assert manifest["runtime"]["persistence"] == "NOT_APPLICABLE"
    assert manifest["runtime"]["implementation"] == "NOT_INCLUDED"
    assert set(manifest["traceability"]["requirements"]) == {
        "REQ-ISM-004",
        "REQ-ISS-002",
        "REQ-SPRINT-001-004",
    }
    assert set(manifest["traceability"]["acceptance_criteria"]) == {
        "AC-ISSUE-0111-01",
        "AC-ISSUE-0111-02",
        "AC-ISSUE-0111-03",
        "AC-ISSUE-0111-04",
    }
    referenced = {
        item[key]
        for item in manifest["contracts"]
        for key in ("schema", "example")
    }
    assert referenced == PUBLISHED_PATHS - {MANIFEST_PATH.relative_to(ROOT).as_posix()}
    if require_files:
        assert all((ROOT / path).is_file() for path in referenced)


def test_versioned_issue_portfolio_catalog_github_reconciliation() -> None:
    manifest = _load_manifest()
    contract = _contract_entry(manifest, "portfolio-snapshot")
    assert contract["owner"] == "BC-001"
    assert contract["version"] == "1.0.0"
    assert contract["requirement"] == "REQ-ISM-004"
    assert "MISSING_RECONCILIATION_SIDE" in contract["failure_modes"]
    assert "INCONSISTENT_RECONCILIATION" in contract["failure_modes"]

    validator = _validator(PORTFOLIO_SCHEMA)
    snapshot = _load_json(PORTFOLIO_EXAMPLE)
    validator.validate(snapshot)
    _assert_portfolio_semantics(snapshot)

    reconciliation = snapshot["reconciliations"][0]
    assert reconciliation["stable_id"] == "ISSUE-0111"
    assert reconciliation["repository_issue"]["story_id"] == "STORY-0001"
    assert reconciliation["github_issue"]["issue_number"] == 111

    github_renumbered = copy.deepcopy(snapshot)
    github_renumbered["reconciliations"][0]["github_issue"]["issue_number"] = 9999
    validator.validate(github_renumbered)
    _assert_portfolio_semantics(github_renumbered)
    assert github_renumbered["reconciliations"][0]["stable_id"] == "ISSUE-0111"

    for field in ("schema_version", "snapshot_id", "reconciliations"):
        invalid = copy.deepcopy(snapshot)
        invalid.pop(field)
        _assert_schema_rejects(validator, invalid)

    missing_side = copy.deepcopy(snapshot)
    missing_side["reconciliations"][0].pop("github_issue")
    _assert_schema_rejects(validator, missing_side)

    unexpected = copy.deepcopy(snapshot)
    unexpected["fallback"] = "accept"
    _assert_schema_rejects(validator, unexpected)

    duplicate_github_side = copy.deepcopy(snapshot)
    duplicate = copy.deepcopy(duplicate_github_side["reconciliations"][0])
    duplicate["stable_id"] = "ISSUE-9999"
    duplicate["repository_issue"]["issue_id"] = "ISSUE-9999"
    duplicate_github_side["reconciliations"].append(duplicate)
    duplicate_github_side["reconciliation_summary"]["reconciled"] = 2
    _assert_fails(lambda: _assert_portfolio_semantics(duplicate_github_side))

    stable_id_mismatch = copy.deepcopy(snapshot)
    stable_id_mismatch["reconciliations"][0]["stable_id"] = "ISSUE-9999"
    _assert_fails(lambda: _assert_portfolio_semantics(stable_id_mismatch))


def test_issue_forecast_min_mode_max_confidence_and_snapshot_variance() -> None:
    manifest = _load_manifest()
    contract = _contract_entry(manifest, "issue-forecast")
    assert contract["owner"] == "BC-001"
    assert contract["version"] == "1.0.0"
    assert contract["requirement"] == "REQ-ISS-002"
    assert "INVALID_INTERVAL_ORDER" in contract["failure_modes"]
    assert "SNAPSHOT_VARIANCE_MISMATCH" in contract["failure_modes"]

    validator = _validator(FORECAST_SCHEMA)
    forecast = _load_json(FORECAST_EXAMPLE)
    validator.validate(forecast)
    _assert_forecast_semantics(forecast)

    for field in ("schema_version", "confidence", "snapshot", "variance"):
        invalid = copy.deepcopy(forecast)
        invalid.pop(field)
        _assert_schema_rejects(validator, invalid)

    minimum_above_mode = copy.deepcopy(forecast)
    minimum_above_mode["interval"]["minimum"] = 9
    minimum_above_mode["interval"]["mode"] = 8
    _assert_fails(lambda: _assert_forecast_semantics(minimum_above_mode))

    mode_above_maximum = copy.deepcopy(forecast)
    mode_above_maximum["interval"]["mode"] = 13
    mode_above_maximum["interval"]["maximum"] = 12
    _assert_fails(lambda: _assert_forecast_semantics(mode_above_maximum))

    snapshot_mismatch = copy.deepcopy(forecast)
    snapshot_mismatch["variance"]["basis_snapshot_id"] = "PORTFOLIO-SNAPSHOT-OTHER"
    _assert_fails(lambda: _assert_forecast_semantics(snapshot_mismatch))

    unexpected = copy.deepcopy(forecast)
    unexpected["central_estimate_only"] = True
    _assert_schema_rejects(validator, unexpected)


def test_sprint_zero_baseline_decision_04() -> None:
    manifest = _load_manifest()
    contract = _contract_entry(manifest, "foundation-boundaries")
    assert contract["owner"] == "BC-001"
    assert contract["version"] == "1.0.0"
    assert contract["requirement"] == "REQ-SPRINT-001-004"
    assert "BOUNDARY_MISSING" in contract["failure_modes"]
    assert "BOUNDARY_COLLAPSED" in contract["failure_modes"]

    validator = _validator(BOUNDARIES_SCHEMA)
    decision = _load_json(BOUNDARIES_EXAMPLE)
    validator.validate(decision)
    _assert_boundary_semantics(decision)

    for boundary in ("core", "api", "runners"):
        missing = copy.deepcopy(decision)
        missing["boundaries"].pop(boundary)
        _assert_schema_rejects(validator, missing)

    collapsed = copy.deepcopy(decision)
    collapsed["boundaries"]["api"]["boundary_id"] = collapsed["boundaries"]["core"][
        "boundary_id"
    ]
    _assert_fails(lambda: _assert_boundary_semantics(collapsed))

    materialized = copy.deepcopy(decision)
    materialized["boundaries"]["runners"]["runtime_materialized"] = True
    _assert_schema_rejects(validator, materialized)

    unexpected = copy.deepcopy(decision)
    unexpected["endpoint"] = "/governance"
    _assert_schema_rejects(validator, unexpected)


def test_rfc3339_leap_seconds_require_an_announced_utc_date() -> None:
    checker = _validator_symbols()["_story_format_checker"]()
    expected = {
        "2025-01-31T23:59:60Z": False,
        "2025-01-31T23:59:59Z": True,
        "1998-12-31T23:59:60Z": True,
        "1998-12-31T15:59:60.123-08:00": True,
        "2025-06-30T23:59:60Z": False,
    }
    first = {value: checker.conforms(value, "date-time") for value in expected}
    second = {value: checker.conforms(value, "date-time") for value in expected}
    assert first == expected
    assert second == first


def test_schema_dialect_failures_are_controlled_and_deterministic(capsys: Any) -> None:
    supported_examples, supported_findings = _synthetic_schema_pair(
        "https://json-schema.org/draft/2020-12/schema"
    )
    assert supported_examples == {"synthetic": {}}
    assert supported_findings == []

    for dialect in ("https://example.invalid/unknown-dialect", 202012):
        valid_examples, findings = _synthetic_schema_pair(dialect)
        repeated = _synthetic_schema_pair(dialect)
        assert "synthetic" not in valid_examples
        assert any(finding.code == "SCHEMA_DIALECT_INVALID" for finding in findings)
        assert (valid_examples, findings) == repeated

        symbols = _validator_symbols()
        main = symbols["main"]
        main.__globals__["validate"] = lambda repository_root: findings
        first_code = main([])
        first_output = capsys.readouterr()
        second_code = main([])
        second_output = capsys.readouterr()
        assert first_code == second_code == 1
        assert first_output == second_output
        assert "VALIDATION FAILED" in first_output.out
        assert "SCHEMA_DIALECT_INVALID" in first_output.out
        assert "VALIDATION PASS" not in first_output.out
        assert "Traceback" not in first_output.out + first_output.err


def test_epic_001_contrato() -> None:
    manifest = _load_manifest()
    _assert_manifest(manifest)
    assert manifest["identity"] == {
        "epic_id": "EPIC-001",
        "story_id": "STORY-0001",
        "issue_id": "ISSUE-0111",
        "task_id": "TASK-0001",
    }
    assert set(manifest["proof"]["tests"]) == {
        "test_versioned_issue_portfolio_catalog_github_reconciliation",
        "test_issue_forecast_min_mode_max_confidence_and_snapshot_variance",
        "test_sprint_zero_baseline_decision_04",
        "test_epic_001_contrato",
    }

    wrong_owner = copy.deepcopy(manifest)
    wrong_owner["owner"] = "BC-013"
    _assert_fails(lambda: _assert_manifest(wrong_owner))

    missing_reference = copy.deepcopy(manifest)
    missing_reference["contracts"][0]["schema"] = (
        CONTRACT_ROOT.relative_to(ROOT).as_posix() + "/missing.schema.json"
    )
    _assert_fails(lambda: _assert_manifest(missing_reference))

    with OWNERSHIP_PATH.open(encoding="utf-8", newline="") as ownership_file:
        rows = list(csv.DictReader(ownership_file))
    registered = {
        row["contract"]
        for row in rows
        if row["owner_context"] == "BC-001" and row["status"] == "VERSIONED"
    }
    assert PUBLISHED_PATHS <= registered
