from __future__ import annotations

import copy
import csv
import json
from functools import cache
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = (
    ROOT
    / "contracts/contexts/engineering_governance/fnd"
    / "migrations-ci-secret-dependency-scan-e-telemetria-mini"
    / "aie-bex-epic-parte-1"
)
SCHEMA_PATH = CONTRACT_ROOT / "contract-foundation.schema.json"
EXAMPLE_PATH = CONTRACT_ROOT / "examples/contract-foundation.json"
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
TASK_PATH = ROOT / ".codex/tasks/TASK-0706.json"
FAILURE_DIAGNOSTIC_PATH = ROOT / "contracts/domain/failure-diagnostic.schema.json"
ATTEMPT_PATH = ROOT / "contracts/domain/attempt.schema.json"
JOB_PATH = ROOT / "contracts/domain/job.schema.json"
PROCESSING_PLAN_PATH = ROOT / "contracts/domain/processing-plan.schema.json"
READINESS_PATH = ROOT / "contracts/http/operations/get_admin_readiness.md"
VERSION_MATRIX_PATH = ROOT / "contracts/operations/version-and-rollback-matrix.yaml"
VENDOR_EXIT_PATH = ROOT / "contracts/operations/vendor-exit-matrix.csv"

REQUIREMENT_TESTS = {
    "REQ-AIE-001": "test_ai_escalation_decision_01",
    "REQ-AIE-005": "test_ai_escalation_decision_05",
    "REQ-BEX-003": "test_batch_execution_decision_03",
    "REQ-BEX-005": "test_batch_execution_decision_05",
    "REQ-EPIC-012": "migration_upgrade_rollback",
    "REQ-FS1-001": "test_first_functional_slice_decision_01",
    "REQ-FS1-004": "test_first_functional_slice_decision_04",
    "REQ-INS-003": (
        "test_installation_evidence_set_synthetic_canary_offline_readiness_"
        "and_failure_codes"
    ),
    "REQ-ISS-007": "test_acceptance_evidence_derivation_and_contract_change_review",
    "REQ-OBS-002": "test_opentelemetry_context_propagation_exporter_outage",
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


def test_ai_escalation_decision_01() -> None:
    control = _profile()["controls"]["ai_escalation"]
    diagnostic = _load_json(FAILURE_DIAGNOSTIC_PATH)
    assert {"code", "stage", "evidence", "remediations"} <= set(
        diagnostic["required"]
    )
    assert control["failure_classification"] == "TYPED_VERSIONED"
    assert control["neural_eligibility"] == "VERSIONED_EXPLICIT_DECISION"
    assert control["classic_evidence"] == "REQUIRED"
    assert "ELIGIBILITY_BYPASS" in _manifest_entry("REQ-AIE-001")["failure_modes"]
    _assert_control_rejected("ai_escalation", "unclassified_failure", "ALLOW")
    _assert_control_rejected("ai_escalation", "eligibility_bypass", "ALLOW")


def test_ai_escalation_decision_05() -> None:
    control = _profile()["controls"]["canonical_reuse"]
    assert control["checkpoints"] == "CANONICAL_ONLY"
    assert control["artifacts"] == "CANONICAL_ONLY"
    assert control["compatibility_evidence"] == "REQUIRED_BEFORE_REUSE"
    assert control["digest_verification"] == "REQUIRED"
    _assert_control_rejected("canonical_reuse", "incompatible_reuse", "WARN")


def test_batch_execution_decision_03() -> None:
    control = _profile()["controls"]["batch_execution"]
    job = _load_json(JOB_PATH)
    assert "partially_succeeded" in job["properties"]["state"]["enum"]
    assert control["image_verdicts"] == "PRESERVE_EACH_IMAGE"
    assert control["partial_success_state"] == "partially_succeeded"
    _assert_control_rejected("batch_execution", "missing_image_verdict", "IGNORE")
    _assert_control_rejected("batch_execution", "aggregate_overwrite", "ALLOW")


def test_batch_execution_decision_05() -> None:
    control = _profile()["controls"]["retry_boundary"]
    attempt = _load_json(ATTEMPT_PATH)
    assert "plan_digest" in attempt["required"]
    assert control["technical_retry"] == "DISTINCT_FROM_ALGORITHMIC_ATTEMPT"
    assert control["algorithmic_attempt"] == "NEW_VERSIONED_ATTEMPT"
    assert control["processing_plan_digest"] == "REQUIRED"
    _assert_control_rejected("retry_boundary", "ambiguous_retry", "ALLOW")


def migration_upgrade_rollback() -> None:
    control = _profile()["controls"]["schema_migrations"]
    matrix = _load_yaml(VERSION_MATRIX_PATH)
    assert control["authority"] == "POSTGRESQL"
    assert control["evolution"] == "VERSIONED_MIGRATIONS_ONLY"
    assert control["flow"] == "EXPAND_MIGRATE_CONTRACT"
    assert matrix["migration_rules"] == [
        "no implicit migration on restart",
        "backup preflight",
        "readiness and smoke evidence",
        "rollback decision before contract phase",
    ]
    _assert_control_rejected("schema_migrations", "implicit_restart_migration", "ALLOW")
    _assert_control_rejected("schema_migrations", "failed_cutover", "CONTINUE")


def test_migration_upgrade_rollback() -> None:
    migration_upgrade_rollback()
    _manifest_entry("REQ-EPIC-012")


def test_first_functional_slice_decision_01() -> None:
    control = _profile()["controls"]["first_functional_slice"]
    assert control == {
        "input_scope": "EXACTLY_ONE_IMAGE",
        "execution": "END_TO_END",
        "contract_shape": "BATCH_COMPATIBLE",
        "scope_expansion": "REJECT",
    }
    _assert_control_rejected("first_functional_slice", "input_scope", "UNBOUNDED_BATCH")


def test_first_functional_slice_decision_04() -> None:
    control = _profile()["controls"]["processing_plan"]
    processing_plan = _load_json(PROCESSING_PLAN_PATH)
    required = set(processing_plan["required"])
    assert {"schema_version", "strategy", "quality_profile_id", "output_profile_id"} <= required
    assert {"capabilities", "budgets", "digest"} <= required
    assert control["persistence"] == "REQUIRED"
    assert control["authority"] == "POSTGRESQL"
    assert control["immutability"] == "REQUIRED"
    assert control["versioning"] == "SCHEMA_AND_DIGEST"
    _assert_control_rejected("processing_plan", "invalid_plan", "PERSIST_WITH_WARNING")


def test_installation_evidence_set_synthetic_canary_offline_readiness_and_failure_codes() -> None:
    control = _profile()["controls"]["installation_readiness"]
    readiness_contract = READINESS_PATH.read_text(encoding="utf-8")
    assert "GET /admin/readiness" in readiness_contract
    assert control["ready_requires"] == "ALL_STAGE_EVIDENCE_AND_SYNTHETIC_CANARY"
    assert control["offline_evidence"] == "REQUIRED"
    assert control["failure_codes"] == "TYPED_REQUIRED"
    assert control["missing_or_stale_evidence"] == "NOT_READY"
    assert control["failed_canary"] == "NOT_READY"
    _assert_control_rejected("installation_readiness", "silent_fallback", "ALLOW")


def test_acceptance_evidence_derivation_and_contract_change_review() -> None:
    control = _profile()["controls"]["acceptance_evidence"]
    assert control["source"] == "CONTRACTS"
    assert control["requirement_mapping"] == "EXPLICIT"
    assert control["contract_change"] == "EXPLICIT_ARCHITECT_REVIEW"
    assert set(REQUIREMENT_TESTS) == {
        item["id"] for item in _load_yaml(MANIFEST_PATH)["requirements"]
    }
    _assert_control_rejected("acceptance_evidence", "missing_evidence", "WARN")
    _assert_control_rejected("acceptance_evidence", "implicit_approval", "ALLOW")


def test_opentelemetry_context_propagation_exporter_outage() -> None:
    control = _profile()["controls"]["telemetry"]
    vendor_exit = VENDOR_EXIT_PATH.read_text(encoding="utf-8")
    assert "OpenTelemetry backend" in vendor_exit
    assert "OTLP/vendor-neutral collector" in vendor_exit
    assert control["protocol"] == "OPENTELEMETRY"
    assert control["backend"] == "REPLACEABLE"
    assert control["correlation_scope"] == "REQUEST_JOB_ATTEMPT_WORKER_ARTIFACT_SET"
    assert control["authority"] == "NON_AUTHORITATIVE"
    assert control["exporter_outage"] == "KEEP_LOCAL_MINIMUM_SIGNALS"
    _assert_control_rejected("telemetry", "missing_correlation", "IGNORE")
    _assert_control_rejected("telemetry", "telemetry_as_state_authority", "ALLOW")


def test_contract_package_is_registered_and_envelope_is_contained() -> None:
    manifest = _load_yaml(MANIFEST_PATH)
    assert manifest["status"] == "FROZEN"
    assert manifest["contract_version"] == _profile()["profile_version"] == "1.0.0"
    assert manifest["proof"]["required_tests"] == list(REQUIREMENT_TESTS.values())

    published = {
        MANIFEST_PATH.relative_to(ROOT).as_posix(),
        SCHEMA_PATH.relative_to(ROOT).as_posix(),
        EXAMPLE_PATH.relative_to(ROOT).as_posix(),
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
    assert ".codex/tasks/TASK-0706.json" in allow_paths
    assert "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv" in allow_paths
    assert any(path.startswith("tests/fnd/migrations-ci-") for path in allow_paths)
    assert any(path.startswith("evidence/implementation/migrations-ci-") for path in allow_paths)
    assert not any(path.startswith("src/") for path in allow_paths)


def test_profile_rejects_missing_or_unknown_control() -> None:
    missing = copy.deepcopy(_profile())
    del missing["controls"]["telemetry"]
    _assert_rejected(missing)

    unknown = copy.deepcopy(_profile())
    unknown["controls"]["silent_fallback"] = {"enabled": True}
    _assert_rejected(unknown)
