"""Verify acceptance content and the DAA-bound owner snapshot."""

from __future__ import annotations

import copy
from typing import Any

from jsonschema import Draft202012Validator
from tools.governance.delivery_approval_authority.crypto import digest

from .model import TASK_SCHEMA, definition_digest, relative_path, require, sha256, validate_schema
from .planning import authorized_output, unique_ids
from .repository import GitRepository


def read_evidence(
    repository: GitRepository, reference: dict[str, str], evidence_root: str
) -> bytes:
    path = relative_path(reference["path"])
    require(path.startswith(evidence_root + "/"), "evidence outside gate/candidate root")
    content = repository.read(path)
    require(sha256(content) == reference["sha256"], f"evidence digest mismatch: {path}")
    return content


def validate_outputs(
    repository: GitRepository,
    gate: dict[str, Any],
    manifest: dict[str, Any],
    task: dict[str, Any],
    integration: str,
) -> None:
    outputs = manifest["outputs"]
    unique_ids(outputs, "output_id")
    paths = [output["path"] for output in outputs]
    require(len(paths) == len(set(paths)), "duplicate accepted output path")
    registered = {item["output_id"]: item["path"] for item in gate["required_outputs"]}
    accepted = {item["output_id"]: item["path"] for item in outputs}
    require(
        all(accepted.get(key) == path for key, path in registered.items()),
        "required outputs missing or replaced",
    )
    for output in outputs:
        path = relative_path(output["path"])
        require(authorized_output(path, task), f"output outside owner write scope: {path}")
        for revision in (manifest["candidate_sha"], integration, repository.revision):
            require(
                sha256(repository.read(path, revision)) == output["sha256"],
                f"output digest mismatch at {revision}: {path}",
            )


def validate_checks(
    repository: GitRepository, gate: dict[str, Any], manifest: dict[str, Any], evidence_root: str
) -> None:
    unique_ids(manifest["checks"], "check_id")
    expected = {item["check_id"]: item["reference"] for item in gate["acceptance_checks"]}
    observed = {item["check_id"]: item["reference"] for item in manifest["checks"]}
    require(observed == expected, "acceptance checks missing or incompatible")
    for check in manifest["checks"]:
        require(check["result"] == "PASS", f"check did not PASS: {check['check_id']}")
        require(bool(read_evidence(repository, check, evidence_root)), "empty check evidence")


def validate_manifest(
    repository: GitRepository,
    gate: dict[str, Any],
    schema: dict[str, Any],
    manifest: dict[str, Any],
    integration: str,
) -> dict[str, Any]:
    validate_schema(manifest, schema, "AcceptanceManifest")
    require(
        manifest["gate_id"] == gate["gate_id"]
        and manifest["definition_sha256"] == definition_digest(gate),
        "manifest definition digest mismatch",
    )
    candidate = manifest["candidate_sha"]
    candidate_gate = repository.json("docs/06-delivery/DELIVERY_GATES.json", candidate)
    require(gate in candidate_gate["gates"], "candidate definition is not canonical")
    task = repository.json(f".codex/tasks/{gate['owner_task_id']}.json", candidate)
    Draft202012Validator(repository.json(TASK_SCHEMA)).validate(task)
    require(
        digest(task) == manifest["owner_task_envelope_sha256"],
        "owner origin TaskEnvelope digest mismatch",
    )
    require(
        task["task_id"] == gate["owner_task_id"] and task["story_id"] == gate["owner_story_id"],
        "manifest owner mismatch",
    )
    require(
        task.get("delivery_gate_scope")
        == {"gate_id": gate["gate_id"], "definition_sha256": definition_digest(gate)},
        "origin scope missing, incompatible or already accepted",
    )
    root = f"evidence/delivery-gates/{gate['gate_id']}/{candidate}"
    validate_outputs(repository, gate, manifest, task, integration)
    validate_checks(repository, gate, manifest, root)
    return task


def validate_snapshot(
    repository: GitRepository, snapshot: dict[str, Any], task: dict[str, Any], manifest_bytes: bytes
) -> None:
    Draft202012Validator(repository.json(TASK_SCHEMA)).validate(snapshot)
    expected = copy.deepcopy(task)
    expected["delivery_gate_scope"]["acceptance_manifest_sha256"] = sha256(manifest_bytes)
    require(snapshot == expected, "acceptance snapshot must bind manifest without owner drift")
