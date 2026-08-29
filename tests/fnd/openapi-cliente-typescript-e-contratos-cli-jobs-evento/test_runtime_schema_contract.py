from __future__ import annotations

import copy
import csv
import json
import re
from functools import cache
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "openapi-cliente-typescript-e-contratos-cli-jobs-evento"
    / "runtime-scm-tool-parte-2"
)
SCHEMA_PATH = CONTRACT_ROOT / "runtime-schema-conformance.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/runtime-schema-conformance.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
REGISTRY_PATH = CONTRACT_ROOT / "schema-compatibility-checkpoint.json"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0702.json"
OPENAPI_PATH = ROOT / "contracts/http/openapi.yaml"
JOB_EVENT_PATH = ROOT / "contracts/events/job-event.schema.json"
ARTIFACT_MANIFEST_PATH = ROOT / "contracts/artifacts/artifact-set-manifest.schema.json"
PROCESSING_PLAN_PATH = ROOT / "contracts/domain/processing-plan.schema.json"
QUALITY_REPORT_PATH = ROOT / "contracts/domain/quality-report.schema.json"
FAILURE_DIAGNOSTIC_PATH = ROOT / "contracts/domain/failure-diagnostic.schema.json"
FOUNDATION_PROFILE_PATH = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "openapi-cliente-typescript-e-contratos-cli-jobs-evento"
    / "crs-dbschema-epic-parte-1/examples/contract-foundation.json"
)

REQUIREMENT_TESTS = {
    "REQ-RUNTIME-008": "test_runtime_decision_8",
    "REQ-SCM-001": (
        "test_versioned_schema_registry_reader_writer_compatibility_window_"
        "and_unknown_major_rejection"
    ),
    "REQ-TOOL-003": "test_fastapi_openapi_contract",
    "REQ-TOP-001": "cli_api_semantic_contract",
    "REQ-UX-002": "test_no_duplicate_modes_processing_plan_roundtrip",
}


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


@cache
def _validator() -> Draft202012Validator:
    schema = _load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


@cache
def _profile() -> dict[str, Any]:
    profile = _load_json(EXAMPLE_PATH)
    _validator().validate(profile)
    return profile


def _assert_rejected(profile: dict[str, Any]) -> None:
    assert list(_validator().iter_errors(profile)), "invalid profile was silently accepted"


def _assert_control_rejected(control: str, field: str, value: object) -> None:
    invalid = copy.deepcopy(_profile())
    invalid["controls"][control][field] = value
    _assert_rejected(invalid)


def _manifest_entry(requirement: str) -> dict[str, Any]:
    manifest = _load_yaml(MANIFEST_PATH)
    entries = [item for item in manifest["requirements"] if item["id"] == requirement]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["test"] == REQUIREMENT_TESTS[requirement]
    assert entry["failure_modes"]
    return entry


@cache
def _registry() -> dict[str, Any]:
    return _load_json(REGISTRY_PATH)


def _registry_entry(contract: str) -> dict[str, Any]:
    entries = [item for item in _registry()["entries"] if item["contract"] == contract]
    assert len(entries) == 1
    return entries[0]


def _require_registered_major(contract: str, major: int) -> None:
    entry = _registry_entry(contract)
    if major not in entry["reader"]["supported_majors"]:
        raise ValueError("UNKNOWN_SCHEMA_MAJOR")


def _semver_from_schema_id(schema: dict[str, Any]) -> str:
    schema_id = schema.get("$id")
    assert isinstance(schema_id, str)
    version = schema_id.rstrip("/").rsplit("/", maxsplit=1)[-1]
    major, minor, patch = version.split(".")
    assert all(component.isdigit() for component in (major, minor, patch))
    return version


def _openapi_major(openapi: dict[str, Any]) -> int:
    server_urls = [server["url"] for server in openapi["servers"]]
    matches = [re.fullmatch(r"/api/v(\d+)", url) for url in server_urls]
    assert all(matches), "OpenAPI server URL must identify its API major"
    majors = {int(match.group(1)) for match in matches if match is not None}
    assert len(majors) == 1
    return majors.pop()


def test_runtime_decision_8() -> None:
    control = _profile()["controls"]["surface_semantics"]
    foundation = _load_json(FOUNDATION_PROFILE_PATH)["controls"][
        "application_boundaries"
    ]
    assert control["application_services"] == foundation["application_services"]
    assert control["cli"] == foundation["surfaces"]["cli"]
    assert control["api"] == foundation["surfaces"]["api"]
    assert control["frontend"] == "PUBLISHED_CONTRACT_CONSUMER"
    assert control["semantic_equivalence"] == "REQUIRED"
    assert control["surface_specific_business_rule"] == "REJECT"
    _manifest_entry("REQ-RUNTIME-008")
    _assert_control_rejected("surface_semantics", "semantic_equivalence", "BEST_EFFORT")


def test_versioned_schema_registry_reader_writer_compatibility_window_and_unknown_major_rejection() -> None:
    control = _profile()["controls"]["schema_compatibility"]
    assert control["categories"] == [
        "DATABASE",
        "API",
        "EVENT",
        "MANIFEST",
        "ARTIFACT",
    ]
    assert control["reader_writer_matrix"] == "EXPLICIT_PER_CONTRACT"
    assert control["compatibility_window"] == "DECLARED_SUPPORTED_MAJORS"
    assert control["reader_policy"] == "REGISTERED_MAJOR_ONLY"
    assert control["writer_policy"] == "CURRENT_REGISTERED_MAJOR_ONLY"
    assert control["unknown_major"] == "REJECT"

    registry = _registry()
    assert registry["schema_version"] == "1.0.0"
    assert registry["checkpoint_version"] == "1.0.0"
    assert registry["status"] == "FROZEN"
    expected_contracts = {
        FOUNDATION_PROFILE_PATH.parent.parent / "contract-foundation.schema.json": "DATABASE",
        OPENAPI_PATH: "API",
        JOB_EVENT_PATH: "EVENT",
        ARTIFACT_MANIFEST_PATH: "MANIFEST",
        PROCESSING_PLAN_PATH: "ARTIFACT",
        QUALITY_REPORT_PATH: "ARTIFACT",
        FAILURE_DIAGNOSTIC_PATH: "ARTIFACT",
    }
    assert {
        ROOT / entry["contract"]: entry["category"] for entry in registry["entries"]
    } == expected_contracts

    registered_contracts = [entry["contract"] for entry in registry["entries"]]
    assert len(registered_contracts) == len(set(registered_contracts))
    for entry in registry["entries"]:
        contract_path = ROOT / entry["contract"]
        assert contract_path.is_file()
        contract = (
            _load_yaml(contract_path)
            if contract_path.suffix == ".yaml"
            else _load_json(contract_path)
        )
        contract_major = (
            _openapi_major(contract)
            if entry["category"] == "API"
            else int(_semver_from_schema_id(contract).split(".", maxsplit=1)[0])
        )
        writer_major = entry["writer"]["major"]
        supported_majors = entry["reader"]["supported_majors"]
        assert entry["reader"]["policy"] == "REGISTERED_MAJOR_ONLY"
        assert entry["writer"]["policy"] == "CURRENT_REGISTERED_MAJOR_ONLY"
        assert supported_majors == sorted(set(supported_majors))
        assert writer_major == contract_major
        compatibility_checkpoints = entry["reader"].get(
            "compatibility_checkpoints", {}
        )
        assert set(supported_majors) == {
            writer_major,
            *(int(major) for major in compatibility_checkpoints),
        }
        for major, checkpoint in compatibility_checkpoints.items():
            checkpoint_path = ROOT / checkpoint
            if entry["category"] == "API":
                assert contract_path == checkpoint_path == OPENAPI_PATH
                checkpoint_contract = _load_yaml(checkpoint_path)
                assert checkpoint_contract["openapi"] == "3.1.0"
                assert checkpoint_contract["info"]["title"] == "DSGeorref API"
                checkpoint_major = _openapi_major(checkpoint_contract)
            else:
                checkpoint_contract = _load_json(checkpoint_path)
                checkpoint_major = int(
                    _semver_from_schema_id(checkpoint_contract).split(".")[0]
                )
            assert checkpoint_major == int(major)
        _require_registered_major(entry["contract"], writer_major)
        with pytest.raises(ValueError, match="UNKNOWN_SCHEMA_MAJOR"):
            _require_registered_major(entry["contract"], max(supported_majors) + 1)

    for path in (PROCESSING_PLAN_PATH, QUALITY_REPORT_PATH, FAILURE_DIAGNOSTIC_PATH):
        schema = _load_json(path)
        Draft202012Validator.check_schema(schema)
        assert _semver_from_schema_id(schema) == "1.0.0"

    _manifest_entry("REQ-SCM-001")
    _assert_control_rejected("schema_compatibility", "unknown_major", "WARN")
    _assert_control_rejected("schema_compatibility", "compatibility_window", "IMPLICIT")


def test_fastapi_openapi_contract() -> None:
    control = _profile()["controls"]["http_adapter"]
    assert control["framework"] == "FASTAPI_PYDANTIC"
    assert control["transport_models"] == "HTTP_ADAPTER_ONLY"
    assert control["adapter_role"] == "THIN"
    assert control["mapping"] == "EXPLICIT_TRANSPORT_DOMAIN_PERSISTENCE"
    assert control["framework_outside_adapter"] == "REJECT"

    openapi = _load_yaml(OPENAPI_PATH)
    assert openapi["openapi"] == "3.1.0"
    assert openapi["info"]["version"]
    schemas = openapi["components"]["schemas"]
    assert {"ProcessingPlan", "QualityReport", "FailureDiagnostic"} <= set(schemas)

    _manifest_entry("REQ-TOOL-003")
    _assert_control_rejected("http_adapter", "adapter_role", "BUSINESS_LOGIC_ALLOWED")
    _assert_control_rejected("http_adapter", "framework_outside_adapter", "ALLOW")


def cli_api_semantic_contract() -> None:
    control = _profile()["controls"]["surface_semantics"]
    assert control["application_services"] == "SHARED"
    assert control["contract_source"] == OPENAPI_PATH.relative_to(ROOT).as_posix()
    assert control["cli"] == control["api"] == "THIN_ADAPTER"
    assert control["surface_specific_business_rule"] == "REJECT"


def test_cli_api_semantic_contract() -> None:
    cli_api_semantic_contract()
    _manifest_entry("REQ-TOP-001")
    _assert_control_rejected("surface_semantics", "cli", "ALTERNATIVE_USE_CASE")


def test_no_duplicate_modes_processing_plan_roundtrip() -> None:
    control = _profile()["controls"]["processing_plan_composition"]
    assert control["contract"] == PROCESSING_PLAN_PATH.relative_to(ROOT).as_posix()
    assert control["composition_field"] == "capabilities"
    assert control["capability_source"] == "VERSIONED_LOCAL_REGISTRY"
    assert control["capability_identity"] == "UNIQUE"
    assert control["duplicate_mode"] == "PROHIBITED"
    assert control["round_trip"] == "LOSSLESS_CANONICAL"
    assert all(value is False for value in control["gate_bypass"].values())

    schema = _load_json(PROCESSING_PLAN_PATH)
    validator = Draft202012Validator(schema)
    assert schema["properties"]["capabilities"]["uniqueItems"] is True
    plan = {
        "schema_version": "1.0.0",
        "id": "00000000-0000-0000-0000-000000000001",
        "project_id": "00000000-0000-0000-0000-000000000002",
        "input_snapshot_id": "00000000-0000-0000-0000-000000000003",
        "strategy": "contract-test",
        "quality_profile_id": "contract-test",
        "output_profile_id": "contract-test",
        "capabilities": [],
        "budgets": {},
        "digest": "0" * 64,
    }
    validator.validate(plan)
    encoded = json.dumps(plan, sort_keys=True, separators=(",", ":"))
    assert json.loads(encoded) == plan

    duplicated = copy.deepcopy(plan)
    duplicated["capabilities"] = ["contract-test", "contract-test"]
    assert list(validator.iter_errors(duplicated))

    _manifest_entry("REQ-UX-002")
    _assert_control_rejected("processing_plan_composition", "duplicate_mode", "ALLOW")


def test_contract_package_is_registered_and_envelope_is_contained() -> None:
    manifest = _load_yaml(MANIFEST_PATH)
    assert manifest["status"] == "FROZEN"
    assert manifest["contract_version"] == _profile()["profile_version"] == "1.0.0"
    assert {item["id"] for item in manifest["requirements"]} == set(REQUIREMENT_TESTS)
    assert manifest["proof"]["required_tests"] == list(REQUIREMENT_TESTS.values())
    assert manifest["contract"]["registry_checkpoint"] == REGISTRY_PATH.relative_to(
        ROOT
    ).as_posix()
    assert manifest["compatibility"]["checkpoint_version"] == _registry()[
        "checkpoint_version"
    ]

    published = {
        MANIFEST_PATH.relative_to(ROOT).as_posix(),
        SCHEMA_PATH.relative_to(ROOT).as_posix(),
        EXAMPLE_PATH.relative_to(ROOT).as_posix(),
        REGISTRY_PATH.relative_to(ROOT).as_posix(),
    }
    with OWNERSHIP_PATH.open(encoding="utf-8", newline="") as registry_file:
        registered = {
            row["contract"]
            for row in csv.DictReader(registry_file)
            if row["owner_context"] == "BC-001" and row["status"] == "VERSIONED"
        }
    assert published <= registered

    task = _load_json(TASK_PATH)
    allow_paths = set(task["allow_paths"])
    assert ".codex/tasks/TASK-0702.json" in allow_paths
    assert "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv" in allow_paths
    assert any(path.startswith("tests/fnd/openapi-") for path in allow_paths)
    assert any(path.startswith("evidence/implementation/openapi-") for path in allow_paths)


def test_profile_rejects_missing_unknown_or_permissive_control() -> None:
    missing = copy.deepcopy(_profile())
    del missing["controls"]["schema_compatibility"]
    _assert_rejected(missing)

    unknown = copy.deepcopy(_profile())
    unknown["controls"]["silent_fallback"] = {"enabled": True}
    _assert_rejected(unknown)

    permissive = copy.deepcopy(_profile())
    permissive["controls"]["processing_plan_composition"]["gate_bypass"][
        "scientific_gate"
    ] = True
    _assert_rejected(permissive)
