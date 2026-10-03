"""Derive SATISFIED only from canonical integration and independent approval."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from tools.governance.delivery_approval_authority.api import verify_delivery_approval

from .acceptance import read_evidence, validate_manifest, validate_snapshot
from .model import SCHEMA, GateError, definition_digest, parse, require, validate_schema
from .repository import GitRepository


def validate_integration(
    repository: GitRepository, gate: dict[str, Any], receipt: dict[str, Any], candidate: str
) -> None:
    integration = receipt["integration_commit"]
    require(
        receipt["required_baseline_ref"] == gate["required_baseline_ref"],
        "receipt baseline mismatch",
    )
    baseline = repository.commit(gate["required_baseline_ref"])
    require(
        gate in repository.json("docs/06-delivery/DELIVERY_GATES.json", baseline)["gates"],
        "definition is not current on canonical baseline",
    )
    require(repository.ancestor(candidate, integration), "candidate not integrated")
    require(
        repository.ancestor(integration, repository.revision),
        "integration commit outside consumer ancestry",
    )
    mainline = repository.git("rev-list", "--first-parent", baseline).decode().splitlines()
    require(integration in mainline, "integration not in canonical baseline mainline")
    parents = repository.git("rev-list", "--parents", "-n", "1", integration).decode().split()[1:]
    require(
        len(parents) >= 2 and any(repository.ancestor(candidate, parent) for parent in parents[1:]),
        "candidate is not incorporated by a canonical Git merge",
    )


def validate_human_record(
    repository: GitRepository, receipt: dict[str, Any], candidate: str, evidence_root: str
) -> None:
    record = parse(read_evidence(repository, receipt["human_integration_record"], evidence_root))
    expected = {
        "proof_type": "HUMAN_MERGE",
        "authority_role": "Autoridade Humana",
        "result": "PASS",
        "reviewed_candidate_commit": candidate,
        "merged_commit": receipt["integration_commit"],
    }
    require(
        all(record.get(key) == value for key, value in expected.items()),
        "human integration record invalid or bound to another candidate",
    )


def validate_approval(
    repository: GitRepository,
    receipt: dict[str, Any],
    snapshot: dict[str, Any],
    candidate: str,
    evidence_root: str,
) -> None:
    evidence: dict[str, list[Any]] = {"bindings": [], "attestations": []}
    paths = [reference["path"] for reference in receipt["daa_evidence"]]
    require(len(paths) == len(set(paths)), "duplicate DAA evidence path")
    for reference in receipt["daa_evidence"]:
        bundle = parse(read_evidence(repository, reference, evidence_root))
        require(
            set(bundle) == set(evidence) and all(isinstance(bundle[key], list) for key in evidence),
            "invalid DAA bundle",
        )
        for key in evidence:
            evidence[key].extend(bundle[key])
    verdict = verify_delivery_approval(
        task_envelope=snapshot,
        expected_candidate_sha=candidate,
        verification_time=datetime.now(UTC).isoformat(),
        evidence=evidence,
    )
    require(
        verdict.get("status") == "PASS"
        and {"QA", "Reviewer"} <= set(verdict.get("validated_roles", [])),
        f"QA/Reviewer/DAA approval invalid: {verdict.get('code', 'INVALID')}",
    )


def validate_receipt(repository: GitRepository, gate: dict[str, Any], path: str) -> None:
    schema = repository.json(SCHEMA)
    receipt = repository.json(path)
    validate_schema(receipt, schema, "IntegrationReceipt")
    require(
        receipt["gate_id"] == gate["gate_id"]
        and receipt["definition_sha256"] == definition_digest(gate),
        "receipt definition digest mismatch",
    )
    manifest_path = receipt["acceptance_manifest"]["path"]
    prefix = f"evidence/delivery-gates/{gate['gate_id']}/"
    require(
        manifest_path.startswith(prefix) and manifest_path.endswith("/acceptance-manifest.json"),
        "noncanonical acceptance manifest path",
    )
    candidate = manifest_path[len(prefix) :].split("/")[0]
    repository.commit(candidate)
    evidence_root = prefix + candidate
    require(path == evidence_root + "/integration-receipt.json", "noncanonical receipt path")
    manifest_bytes = read_evidence(repository, receipt["acceptance_manifest"], evidence_root)
    manifest = parse(manifest_bytes)
    require(manifest.get("candidate_sha") == candidate, "manifest candidate/path mismatch")
    validate_integration(repository, gate, receipt, candidate)
    task = validate_manifest(repository, gate, schema, manifest, receipt["integration_commit"])
    snapshot_reference = receipt["task_envelope_snapshot"]
    require(
        snapshot_reference["path"] == evidence_root + "/task-envelope.acceptance.json",
        "noncanonical acceptance snapshot path",
    )
    snapshot = parse(read_evidence(repository, snapshot_reference, evidence_root))
    validate_snapshot(repository, snapshot, task, manifest_bytes)
    validate_human_record(repository, receipt, candidate, evidence_root)
    validate_approval(repository, receipt, snapshot, candidate, evidence_root)


def require_satisfied(repository: GitRepository, gate: dict[str, Any]) -> None:
    paths = sorted(
        path
        for path in repository.paths(f"evidence/delivery-gates/{gate['gate_id']}")
        if path.endswith("/integration-receipt.json")
    )
    require(bool(paths), f"{gate['gate_id']}: PENDING (no integrated acceptance receipt)")
    failures = []
    for path in paths:
        try:
            validate_receipt(repository, gate, path)
            return
        except (GateError, ValueError, KeyError, TypeError) as error:
            failures.append(str(error))
    raise GateError(f"{gate['gate_id']}: not SATISFIED: {'; '.join(failures)}")
