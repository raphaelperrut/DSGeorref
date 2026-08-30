from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


CHECKPOINT_NAME = "foundation-checkpoint.json"
REQUIREMENT_TESTS = {
    "REQ-ARTLAYOUT-010": "test_req_artlayout_0010",
    "REQ-DBSCHEMA-002": "test_req_dbschema_002",
    "REQ-DBSCHEMA-004": "test_req_dbschema_004",
    "REQ-FS1-002": "test_first_functional_slice_decision_02",
    "REQ-FS1-003": "test_first_functional_slice_decision_03",
    "REQ-FS1-005": "test_first_functional_slice_decision_05",
    "REQ-FS1-007": "test_first_functional_slice_decision_07",
    "REQ-FS1-008": "test_first_functional_slice_decision_08",
    "REQ-FS1-009": "test_first_functional_slice_decision_09",
    "REQ-FS1-010": "test_first_functional_slice_decision_10",
}
EXPECTED_CONTRACTS = {
    "artifact_kind_registry": "contracts/artifacts/artifact-kind-registry.yaml",
    "artifact_set_manifest": "contracts/artifacts/artifact-set-manifest.schema.json",
    "failure_diagnostic": "contracts/domain/failure-diagnostic.schema.json",
    "processing_plan": "contracts/domain/processing-plan.schema.json",
    "quality_report": "contracts/domain/quality-report.schema.json",
}
EXPECTED_CONTROLS: dict[str, Any] = {
    "artifact_serving": {
        "authorization": "REQUIRED",
        "locator_resolution": "SAFE_REGISTERED_ROOT_ONLY",
        "unauthorized_or_unsafe": "REJECT",
    },
    "identity": {
        "logical_id": "UUIDV7_APPLICATION_GENERATED",
        "stable": True,
        "ordered_when_required": True,
        "invalid_id": "REJECT",
    },
    "time_and_concurrency": {
        "timestamp": "TIMESTAMPTZ",
        "locking": "OPTIMISTIC_REVISION_OR_EXPLICIT_LOCK",
        "concurrency_policy": "EXPLICIT",
        "implicit_last_write_wins": "REJECT",
    },
    "local_inputs": {
        "source": "LOCAL_AUTHORIZED_REGISTERED_ROOT",
        "locator": "RELATIVE_OPAQUE",
        "root_escape": "REJECT",
    },
    "ingestion": {
        "originals": "IMMUTABLE",
        "sha256": "REQUIRED",
        "source_identity": "REQUIRED",
        "metadata": "REQUIRED",
        "invalid_or_incomplete": "REJECT",
    },
    "classic_pipeline": {
        "execution_order": "CLASSIC_BEFORE_OPTIONAL_AI",
        "deterministic": True,
        "replaceable": True,
        "correspondence_audit": "REQUIRED",
        "untracked_correspondence": "REJECT",
    },
    "sgv": {
        "mandatory": True,
        "verdicts": ["accepted", "reviewable", "rejected"],
        "hard_gate_override": "PROHIBITED",
        "missing_invalid_or_inconsistent_metric": "REJECT",
    },
    "artifact_set": {
        "immutable": True,
        "required_kinds": ["COG_RASTER", "PROVENANCE_MANIFEST", "QUALITY_REPORT"],
        "manifest": "REQUIRED",
        "lineage": "REQUIRED",
        "root_digest": "SHA256",
        "publication": "ATOMIC_AFTER_SGV_ACCEPTED",
        "partial_or_nonaccepted": "REJECT",
    },
    "shared_core": {
        "application_services": "SHARED",
        "surfaces": ["REST", "CLI", "DIRECT_RUNNER", "CELERY"],
        "semantic_equivalence": "REQUIRED",
        "surface_specific_rule": "REJECT",
    },
    "promotion": {
        "corpus": "VERSIONED_STRATIFIED_INITIAL_CORPUS",
        "dimensions": ["FALSE_ACCEPTANCE", "QUALITY", "RUNTIME", "SECURITY"],
        "evidence": "REQUIRED",
        "failed_or_missing_dimension": "REJECT",
    },
}


def load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return loaded


def _expect(errors: list[str], label: str, actual: object, expected: object) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")


def _validate_dependency(checkpoint: dict[str, Any], root: Path, errors: list[str]) -> None:
    dependency = checkpoint.get("dependency")
    expected = {
        "consolidation": (
            "contracts/contexts/engineering_governance/fnd/"
            "openapi-cliente-typescript-e-contratos-cli-jobs-evento/"
            "consolidacao/examples/slice-consolidation.json"
        ),
        "eligible_story": "STORY-0703",
        "required_state": "READY_FOR_INDEPENDENT_REVIEW",
    }
    _expect(errors, "dependency", dependency, expected)
    if not isinstance(dependency, dict):
        return
    dependency_path = root / str(dependency.get("consolidation", ""))
    if not dependency_path.is_file():
        errors.append("dependency.consolidation: canonical checkpoint is missing")
        return
    consolidation = load_json(dependency_path)
    gate = consolidation.get("review_gate", {})
    if gate.get("candidate_state") != dependency.get("required_state"):
        errors.append("dependency.required_state: consolidation is not review-ready")
    if dependency.get("eligible_story") not in gate.get("eligible_dependents", []):
        errors.append("dependency.eligible_story: story is not eligible in consolidation")


def _validate_contracts(checkpoint: dict[str, Any], root: Path, errors: list[str]) -> None:
    contracts = checkpoint.get("canonical_contracts")
    _expect(errors, "canonical_contracts", contracts, EXPECTED_CONTRACTS)
    if contracts != EXPECTED_CONTRACTS:
        return
    for label, relative in contracts.items():
        if not (root / relative).is_file():
            errors.append(f"canonical_contracts.{label}: file is missing")
    if errors:
        return

    plan = load_json(root / contracts["processing_plan"])
    required_plan = {
        "schema_version", "id", "project_id", "input_snapshot_id", "strategy",
        "quality_profile_id", "output_profile_id", "capabilities", "budgets", "digest",
    }
    if set(plan.get("required", [])) != required_plan:
        errors.append("canonical_contracts.processing_plan: required fields diverged")
    if plan.get("properties", {}).get("capabilities", {}).get("uniqueItems") is not True:
        errors.append("canonical_contracts.processing_plan: capabilities must be unique")

    quality = load_json(root / contracts["quality_report"])
    verdicts = quality.get("properties", {}).get("verdict", {}).get("enum")
    if verdicts != ["accepted", "reviewable", "rejected"]:
        errors.append("canonical_contracts.quality_report: SGV verdicts diverged")

    diagnostic = load_json(root / contracts["failure_diagnostic"])
    if set(diagnostic.get("required", [])) != {"code", "stage", "evidence", "remediations"}:
        errors.append("canonical_contracts.failure_diagnostic: required fields diverged")

    manifest = load_json(root / contracts["artifact_set_manifest"])
    required_manifest = {"artifacts", "lineage", "publication", "root_digest"}
    if not required_manifest <= set(manifest.get("required", [])):
        errors.append("canonical_contracts.artifact_set_manifest: publication proof is incomplete")
    publication = manifest.get("properties", {}).get("publication", {})
    status = publication.get("properties", {}).get("status", {}).get("const")
    if status != "PUBLISHED":
        errors.append("canonical_contracts.artifact_set_manifest: publication is not explicit")

    registry = yaml.safe_load((root / contracts["artifact_kind_registry"]).read_text(encoding="utf-8"))
    kinds = {item.get("kind") for item in registry.get("kinds", [])}
    required_kinds = set(EXPECTED_CONTROLS["artifact_set"]["required_kinds"])
    if not required_kinds <= kinds:
        errors.append("canonical_contracts.artifact_kind_registry: required kinds are missing")


def validate_checkpoint(checkpoint: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    expected_keys = {
        "schema_version", "checkpoint_id", "owner", "dependency",
        "canonical_contracts", "requirements", "controls",
    }
    _expect(errors, "top-level fields", set(checkpoint), expected_keys)
    _expect(errors, "schema_version", checkpoint.get("schema_version"), "1.0.0")
    _expect(
        errors,
        "checkpoint_id",
        checkpoint.get("checkpoint_id"),
        "FOUNDATION-MATERIALIZATION-CHECKPOINT",
    )
    _expect(errors, "owner", checkpoint.get("owner"), "BC-001")
    requirement_map = {
        item.get("id"): item.get("test")
        for item in checkpoint.get("requirements", [])
        if isinstance(item, dict)
    }
    _expect(errors, "requirements", requirement_map, REQUIREMENT_TESTS)
    controls = checkpoint.get("controls")
    if not isinstance(controls, dict):
        errors.append("controls: expected an object")
    else:
        _expect(errors, "controls fields", set(controls), set(EXPECTED_CONTROLS))
        for name, expected in EXPECTED_CONTROLS.items():
            _expect(errors, f"controls.{name}", controls.get(name), expected)
    _validate_dependency(checkpoint, root, errors)
    _validate_contracts(checkpoint, root, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the executable foundation checkpoint")
    parser.add_argument(
        "checkpoint",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name(CHECKPOINT_NAME),
    )
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate_checkpoint(load_json(args.checkpoint), args.repo_root.resolve())
    print(json.dumps({"status": "FAIL" if errors else "PASS", "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
