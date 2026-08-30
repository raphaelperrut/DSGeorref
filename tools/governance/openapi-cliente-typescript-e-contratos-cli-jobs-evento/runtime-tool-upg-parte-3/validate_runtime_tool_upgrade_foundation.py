from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

CHECKPOINT_NAME = "runtime-tool-upgrade-foundation-checkpoint.json"
CONSOLIDATION = {
    "path": (
        "contracts/contexts/engineering_governance/fnd/"
        "openapi-cliente-typescript-e-contratos-cli-jobs-evento/"
        "consolidacao/examples/slice-consolidation.json"
    ),
    "sha256": "d585db2b6d62a807ed55aa2d5c150329a721363ab63ca5a53eb9fb47d4bb0ce3",
}
EXPECTED_DEPENDENCY = {
    "consolidation": CONSOLIDATION,
    "eligible_story": "STORY-0705",
    "required_state": "READY_FOR_INDEPENDENT_REVIEW",
}
EXPECTED_BINDINGS = {
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
    "http_api": {
        "path": "contracts/http/openapi.yaml",
        "sha256": "0f236a4937a5226b1c57cf8c6731750153b5d4cd9d6381c88a6bd2fceca30d52",
    },
    "version_and_rollback": {
        "path": "contracts/operations/version-and-rollback-matrix.yaml",
        "sha256": "511a2d613773cae3b59edb96a9c065d0a03eee390a0e65b36321a306c4c28a96",
    },
    "queue_policy": {
        "path": "contracts/operations/lock-and-queue-policy.yaml",
        "sha256": "3b4c2760dc570e3b570db17b236a9e226e58b62eb3b9586f712aaa60b01a8131",
    },
}
REQUIREMENT_TESTS = {
    "REQ-RUNTIME-006": "test_runtime_decision_6",
    "REQ-RUNTIME-007": "test_runtime_decision_7",
    "REQ-TOOL-005": "test_model_boundary_architecture",
    "REQ-UPG-005": (
        "test_phased_rollout_limited_mixed_version_window_drain_"
        "and_long_job_pinning"
    ),
}
EXPECTED_CONTROLS: dict[str, Any] = {
    "browser_boundary": {
        "surface": "PUBLISHED_HTTP_CONTRACT_ONLY",
        "host_paths": "PROHIBITED",
        "broker_payloads": "PROHIBITED",
        "direct_persistence": "PROHIBITED",
        "violation": "REJECT",
    },
    "authorized_selection": {
        "roots": "AUTHORIZED_REGISTERED_ONLY",
        "root_identifier": "OPAQUE_UUID",
        "entry_identifier": "OPAQUE_STRING",
        "absolute_host_path": "REJECT",
        "unknown_root_or_entry": "REJECT",
    },
    "model_boundaries": {
        "domain_models": "SEPARATE",
        "transport_models": "SEPARATE_HTTP_ADAPTER_ONLY",
        "persistence_models": "SEPARATE_ADAPTER_ONLY",
        "mapping": "EXPLICIT_TRANSPORT_DOMAIN_PERSISTENCE",
        "shared_boundary_model": "REJECT",
    },
    "upgrade_rollout": {
        "mixed_version_window": "ONE_UPGRADE_OPERATION",
        "writers": "SINGLE_VERSION",
        "writer_drain": "EXPLICIT_REQUIRED_BEFORE_CUTOVER",
        "long_jobs": "PINNED_TO_COMPATIBLE_VERSION_UNTIL_COMPLETION",
        "incompatible_or_unpinned": "REJECT",
    },
}

def load_document(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    loaded = json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
    if not isinstance(loaded, dict):
        raise ValueError(f"{path}: expected an object")
    return loaded

def _mismatch(
    errors: list[str], label: str, actual: object, expected: object
) -> None:
    if actual != expected:
        rendered_expected = (
            repr(sorted(expected)) if isinstance(expected, set) else repr(expected)
        )
        rendered_actual = (
            repr(sorted(actual)) if isinstance(actual, set) else repr(actual)
        )
        errors.append(f"{label}: expected {rendered_expected}, got {rendered_actual}")

def _bound_document(
    root: Path,
    label: str,
    descriptor: dict[str, str],
    errors: list[str],
) -> dict[str, Any] | None:
    path = (root / descriptor["path"]).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        errors.append(f"{label}: path escapes repository root")
        return None
    try:
        content = path.read_bytes().replace(b"\r\n", b"\n")
    except OSError as exc:
        errors.append(f"{label}: binding is unreadable: {exc}")
        return None
    if hashlib.sha256(content).hexdigest() != descriptor["sha256"]:
        errors.append(f"{label}: sha256 mismatch")
        return None
    try:
        return load_document(path)
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        yaml.YAMLError,
        ValueError,
    ) as exc:
        errors.append(f"{label}: binding is invalid: {exc}")
        return None

def _validate_dependency(
    checkpoint: dict[str, Any], root: Path, errors: list[str]
) -> None:
    dependency = checkpoint.get("dependency")
    _mismatch(errors, "dependency", dependency, EXPECTED_DEPENDENCY)
    if dependency != EXPECTED_DEPENDENCY:
        return
    consolidation = _bound_document(
        root, "dependency.consolidation", CONSOLIDATION, errors
    )
    if consolidation is None:
        return
    _mismatch(errors, "dependency.status", consolidation.get("status"), "FROZEN")
    gate = consolidation.get("review_gate")
    if not isinstance(gate, dict):
        errors.append("dependency.review_gate: expected an object")
        return
    _mismatch(
        errors,
        "dependency.required_state",
        gate.get("candidate_state"),
        EXPECTED_DEPENDENCY["required_state"],
    )
    eligible = gate.get("eligible_dependents")
    if not isinstance(eligible, list) or "STORY-0705" not in eligible:
        errors.append("dependency.eligible_story: STORY-0705 is not eligible")


def _validate_http_binding(api: dict[str, Any], errors: list[str]) -> None:
    paths = api.get("paths")
    schemas = api.get("components", {}).get("schemas", {})
    if not isinstance(paths, dict) or not isinstance(schemas, dict):
        errors.append("canonical_bindings.http_api: paths or schemas are missing")
        return
    operations = {
        "/workspace/roots": "get",
        "/workspace/entries": "get",
        "/admin/drain": "post",
        "/admin/upgrades": "post",
    }
    for path, method in operations.items():
        operation = paths.get(path, {}).get(method, {})
        _mismatch(
            errors,
            f"canonical_bindings.http_api.{path}",
            operation.get("x-contract-status"),
            "FROZEN",
        )
    expected_fields = {
        "WorkspaceRoot": {"rootId", "name", "readOnly", "capabilities"},
        "WorkspaceEntry": {
            "entryId", "rootId", "parentId", "name", "kind",
            "sizeBytes", "mediaType",
        },
    }
    for schema_name, fields in expected_fields.items():
        schema = schemas.get(schema_name, {})
        _mismatch(
            errors,
            f"canonical_bindings.http_api.{schema_name}.fields",
            set(schema.get("properties", {})),
            fields,
        )
        _mismatch(
            errors,
            f"canonical_bindings.http_api.{schema_name}.additionalProperties",
            schema.get("additionalProperties"),
            False,
        )
    root_id = (
        schemas.get("WorkspaceRoot", {}).get("properties", {}).get("rootId", {})
    )
    _mismatch(
        errors,
        "canonical_bindings.http_api.rootId.type",
        root_id.get("type"),
        "string",
    )
    _mismatch(
        errors,
        "canonical_bindings.http_api.rootId.format",
        root_id.get("format"),
        "uuid",
    )


def _validate_binding_semantics(
    documents: dict[str, dict[str, Any]], errors: list[str]
) -> None:
    foundation = documents["foundation_profile"]
    runtime = documents["runtime_profile"]
    versioning = documents["version_and_rollback"]
    queue = documents["queue_policy"]
    _mismatch(errors, "foundation.status", foundation.get("status"), "FROZEN")
    _mismatch(errors, "runtime.status", runtime.get("status"), "FROZEN")
    _mismatch(errors, "versioning.status", versioning.get("status"), "FROZEN")
    _mismatch(errors, "queue_policy.status", queue.get("status"), "FROZEN")
    http_adapter = runtime.get("controls", {}).get("http_adapter", {})
    surface = runtime.get("controls", {}).get("surface_semantics", {})
    _mismatch(
        errors,
        "runtime.frontend",
        surface.get("frontend"),
        "PUBLISHED_CONTRACT_CONSUMER",
    )
    _mismatch(
        errors,
        "runtime.transport_models",
        http_adapter.get("transport_models"),
        "HTTP_ADAPTER_ONLY",
    )
    _mismatch(
        errors,
        "runtime.mapping",
        http_adapter.get("mapping"),
        "EXPLICIT_TRANSPORT_DOMAIN_PERSISTENCE",
    )
    forbidden = http_adapter.get("forbidden_direct_dependencies")
    _mismatch(
        errors,
        "runtime.forbidden_dependencies",
        forbidden,
        ["ORM", "FILESYSTEM", "BROKER", "GEOSPATIAL_ALGORITHM"],
    )
    _mismatch(
        errors,
        "foundation.application_services",
        foundation.get("controls", {})
        .get("application_boundaries", {})
        .get("application_services"),
        "SHARED",
    )
    _mismatch(
        errors,
        "versioning.mixed_versions",
        versioning.get("mixed_versions"),
        {
            "allowed_only_during_controlled_upgrade": True,
            "writers_single_version": True,
            "maximum_window": "one upgrade operation",
        },
    )
    broker = queue.get("broker", {})
    _mismatch(
        errors,
        "queue_policy.absolute_host_paths_forbidden",
        broker.get("absolute_host_paths_forbidden"),
        True,
    )
    _mismatch(
        errors,
        "queue_policy.binary_payloads_forbidden",
        broker.get("binary_payloads_forbidden"),
        True,
    )
    _validate_http_binding(documents["http_api"], errors)


def _validate_bindings(
    checkpoint: dict[str, Any], root: Path, errors: list[str]
) -> None:
    bindings = checkpoint.get("canonical_bindings")
    _mismatch(errors, "canonical_bindings", bindings, EXPECTED_BINDINGS)
    if bindings != EXPECTED_BINDINGS:
        return
    documents: dict[str, dict[str, Any]] = {}
    for label, descriptor in EXPECTED_BINDINGS.items():
        loaded = _bound_document(
            root, f"canonical_bindings.{label}", descriptor, errors
        )
        if loaded is not None:
            documents[label] = loaded
    if set(documents) == set(EXPECTED_BINDINGS):
        _validate_binding_semantics(documents, errors)


def validate_checkpoint(checkpoint: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    expected_keys = {
        "schema_version", "checkpoint_id", "owner", "dependency",
        "canonical_bindings", "requirements", "controls",
    }
    _mismatch(errors, "top-level fields", set(checkpoint), expected_keys)
    _mismatch(errors, "schema_version", checkpoint.get("schema_version"), "1.0.0")
    _mismatch(
        errors,
        "checkpoint_id",
        checkpoint.get("checkpoint_id"),
        "RUNTIME-TOOL-UPGRADE-FOUNDATION-CHECKPOINT",
    )
    _mismatch(errors, "owner", checkpoint.get("owner"), "BC-001")
    requirements = checkpoint.get("requirements")
    if not isinstance(requirements, list):
        errors.append("requirements: expected an array")
    else:
        requirement_map: dict[str, str] = {}
        invalid_entries = False
        for item in requirements:
            if not isinstance(item, dict) or set(item) != {"id", "test"}:
                invalid_entries = True
                continue
            requirement_id = item.get("id")
            test_name = item.get("test")
            if isinstance(requirement_id, str) and isinstance(test_name, str):
                requirement_map[requirement_id] = test_name
            else:
                invalid_entries = True
        _mismatch(errors, "requirements", requirement_map, REQUIREMENT_TESTS)
        if invalid_entries or len(requirements) != len(REQUIREMENT_TESTS):
            errors.append("requirements: duplicates or invalid entries are prohibited")
    controls = checkpoint.get("controls")
    if not isinstance(controls, dict):
        errors.append("controls: expected an object")
    else:
        _mismatch(errors, "controls fields", set(controls), set(EXPECTED_CONTROLS))
        for name, expected in EXPECTED_CONTROLS.items():
            _mismatch(errors, f"controls.{name}", controls.get(name), expected)
    _validate_dependency(checkpoint, root.resolve(), errors)
    _validate_bindings(checkpoint, root.resolve(), errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the RUNTIME/TOOL/UPG foundation checkpoint"
    )
    parser.add_argument(
        "checkpoint",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name(CHECKPOINT_NAME),
    )
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        checkpoint = load_document(args.checkpoint)
        errors = validate_checkpoint(checkpoint, args.repo_root)
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        yaml.YAMLError,
        ValueError,
    ) as exc:
        errors = [f"checkpoint: unreadable or invalid: {exc}"]
    result = {"status": "FAIL" if errors else "PASS", "errors": errors}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
