from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


CHECKPOINT_NAME = "runtime-foundation-checkpoint.json"
REQUIREMENT_TESTS = {
    "REQ-RUN-002": "test_req_run_002",
    "REQ-RUN-003": "test_req_run_003",
    "REQ-RUN-004": "test_req_run_004",
    "REQ-RUN-005": "test_req_run_005",
    "REQ-RUN-007": "test_req_run_007",
    "REQ-RUN-009": "test_req_run_009",
    "REQ-RUNTIME-001": "test_runtime_decision_1",
    "REQ-RUNTIME-002": "test_runtime_decision_2",
    "REQ-RUNTIME-003": "test_runtime_decision_3",
    "REQ-RUNTIME-004": "test_runtime_decision_4",
}
EXPECTED_CONTRACTS = {
    "foundation_profile": {
        "path": (
            "contracts/contexts/engineering_governance/fnd/"
            "openapi-cliente-typescript-e-contratos-cli-jobs-evento/"
            "crs-dbschema-epic-parte-1/examples/contract-foundation.json"
        ),
        "sha256": "414a1510f7e3d403ad16d22dafce67356049108953d7b071d2e1f1249a99f387",
    },
    "runtime_profile": {
        "path": (
            "contracts/contexts/engineering_governance/fnd/"
            "openapi-cliente-typescript-e-contratos-cli-jobs-evento/"
            "runtime-scm-tool-parte-2/examples/runtime-schema-conformance.json"
        ),
        "sha256": "e2effa4efbc5e224c5714b2ba8efeed5df39e9e8aebcf003ffd9929830ee38b4",
    },
}
EXPECTED_CONTROLS: dict[str, Any] = {
    "application_boundaries": {
        "namespace": "dsgeorref",
        "application_services": "SHARED",
        "surfaces": {
            "cli": "THIN_ADAPTER",
            "api": "THIN_ADAPTER",
            "worker": "THIN_ADAPTER",
        },
    },
    "domain_io_boundary": {
        "domain_core": "SYNCHRONOUS",
        "asynchronous_io": "BOUNDARIES_ONLY",
        "asynchronous_domain_core": "REJECT",
    },
    "composition": {
        "composition_roots": "EXPLICIT",
        "dependency_injection": "CONSTRUCTOR",
        "implicit_composition": "REJECT",
    },
    "settings": {
        "typing": "TYPED",
        "sources": "STRATIFIED",
        "required_values": "FAIL_CLOSED",
        "missing_required_value": "REJECT",
    },
    "command_transactions": {
        "unit_of_work": "EXPLICIT",
        "transactions": "SHORT",
        "implicit_or_long_transaction": "REJECT",
    },
    "repeatable_mutations": {
        "idempotency": "PERSISTENT",
        "volatile_idempotency": "REJECT",
    },
    "logging": {
        "envelope": "STRUCTURED",
        "correlation_ids": "REQUIRED",
        "redaction": "CENTRALIZED",
        "uncorrelated_or_unredacted": "REJECT",
    },
    "domain_errors": {
        "typed": "REQUIRED",
        "mapping": "VERSIONED_PROBLEM_DETAILS",
        "schema": "contracts/errors/problem-details.schema.json",
        "unmapped_error": "REJECT",
    },
    "state_authority": {
        "system_of_record": "POSTGRESQL_POSTGIS",
        "broker": "TRANSPORT_ONLY",
        "logs": "DERIVED_NOT_AUTHORITATIVE",
        "filesystem": "BINARY_STORAGE_NOT_STATE_AUTHORITY",
    },
}


def load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return loaded


def _record_mismatch(
    errors: list[str], label: str, actual: object, expected: object
) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")


def _validate_dependency(
    checkpoint: dict[str, Any], root: Path, errors: list[str]
) -> None:
    expected = {
        "consolidation": (
            "contracts/contexts/engineering_governance/fnd/"
            "openapi-cliente-typescript-e-contratos-cli-jobs-evento/"
            "consolidacao/examples/slice-consolidation.json"
        ),
        "eligible_story": "STORY-0704",
        "required_state": "READY_FOR_INDEPENDENT_REVIEW",
    }
    dependency = checkpoint.get("dependency")
    _record_mismatch(errors, "dependency", dependency, expected)
    if dependency != expected:
        return
    consolidation = load_json(root / expected["consolidation"])
    gate = consolidation.get("review_gate", {})
    if gate.get("candidate_state") != expected["required_state"]:
        errors.append("dependency.required_state: consolidation is not review-ready")
    if expected["eligible_story"] not in gate.get("eligible_dependents", []):
        errors.append("dependency.eligible_story: story is not eligible")


def _validate_contracts(
    checkpoint: dict[str, Any], root: Path, errors: list[str]
) -> None:
    contracts = checkpoint.get("canonical_contracts")
    _record_mismatch(errors, "canonical_contracts", contracts, EXPECTED_CONTRACTS)
    if contracts != EXPECTED_CONTRACTS:
        return
    for label, descriptor in contracts.items():
        path = root / descriptor["path"]
        if not path.is_file():
            errors.append(f"canonical_contracts.{label}: file is missing")
            continue
        canonical_bytes = path.read_bytes().replace(b"\r\n", b"\n")
        digest = hashlib.sha256(canonical_bytes).hexdigest()
        if digest != descriptor["sha256"]:
            errors.append(f"canonical_contracts.{label}: sha256 mismatch")
    if any(error.startswith("canonical_contracts.") for error in errors):
        return
    foundation = load_json(root / contracts["foundation_profile"]["path"])
    runtime = load_json(root / contracts["runtime_profile"]["path"])
    _record_mismatch(errors, "foundation.status", foundation.get("status"), "FROZEN")
    foundation_controls = foundation.get("controls", {})
    for name in ("application_boundaries", "domain_errors"):
        _record_mismatch(
            errors,
            f"controls.{name}.contract_binding",
            checkpoint["controls"].get(name),
            foundation_controls.get(name),
        )
    surface = runtime.get("controls", {}).get("surface_semantics", {})
    expected_surface = {
        "application_services": "SHARED",
        "cli": "THIN_ADAPTER",
        "api": "THIN_ADAPTER",
        "surface_specific_business_rule": "REJECT",
    }
    for field, expected in expected_surface.items():
        _record_mismatch(
            errors,
            f"runtime.surface_semantics.{field}",
            surface.get(field),
            expected,
        )
    error_schema = root / EXPECTED_CONTROLS["domain_errors"]["schema"]
    if not error_schema.is_file():
        errors.append("controls.domain_errors.schema: referenced schema is missing")


def validate_checkpoint(checkpoint: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    expected_keys = {
        "schema_version",
        "checkpoint_id",
        "owner",
        "dependency",
        "canonical_contracts",
        "requirements",
        "controls",
    }
    _record_mismatch(errors, "top-level fields", set(checkpoint), expected_keys)
    _record_mismatch(errors, "schema_version", checkpoint.get("schema_version"), "1.0.0")
    _record_mismatch(
        errors,
        "checkpoint_id",
        checkpoint.get("checkpoint_id"),
        "RUN-RUNTIME-FOUNDATION-CHECKPOINT",
    )
    _record_mismatch(errors, "owner", checkpoint.get("owner"), "BC-001")
    requirement_map = {
        item.get("id"): item.get("test")
        for item in checkpoint.get("requirements", [])
        if isinstance(item, dict)
    }
    _record_mismatch(errors, "requirements", requirement_map, REQUIREMENT_TESTS)
    controls = checkpoint.get("controls")
    if not isinstance(controls, dict):
        errors.append("controls: expected an object")
    else:
        _record_mismatch(errors, "controls fields", set(controls), set(EXPECTED_CONTROLS))
        for name, expected in EXPECTED_CONTROLS.items():
            _record_mismatch(errors, f"controls.{name}", controls.get(name), expected)
    _validate_dependency(checkpoint, root, errors)
    if isinstance(controls, dict):
        _validate_contracts(checkpoint, root, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the RUN/RUNTIME foundation")
    parser.add_argument(
        "checkpoint",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name(CHECKPOINT_NAME),
    )
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        checkpoint = load_json(args.checkpoint)
        errors = validate_checkpoint(checkpoint, args.repo_root.resolve())
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors = [f"checkpoint: unreadable or invalid: {exc}"]
    print(json.dumps({"status": "FAIL" if errors else "PASS", "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
