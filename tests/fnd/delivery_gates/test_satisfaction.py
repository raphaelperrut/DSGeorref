from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from tools.governance.delivery_gates.model import REGISTRY, SCHEMA, GateError, validate_schema
from tools.governance.delivery_gates.repository import GitRepository, WorkingRepository
from tools.governance.delivery_gates.satisfaction import require_satisfied
from tools.governance.delivery_gates.validation import ready_errors

from .fixture import GATE_ID, commit, delivery_fixture, git, write
from .signed_approval import install_test_verifier


@pytest.fixture
def delivered(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, dict[str, Any], str, str]:
    fixture = delivery_fixture(tmp_path / "repository")
    install_test_verifier(monkeypatch, fixture[0])
    return fixture


def assert_rejected(root: Path, message: str) -> None:
    base = git(root, "rev-parse", "HEAD")
    gate = WorkingRepository(root).json(REGISTRY)["gates"][0]
    with pytest.raises(GateError, match=message):
        require_satisfied(GitRepository(root, base), gate)


def test_completely_satisfied_gate_preserves_open_owner(delivered: tuple) -> None:
    root, _, _, _ = delivered
    before = (root / "docs/06-delivery/STORY_INDEX.csv").read_bytes()
    assert ready_errors(root, "TASK-0038", git(root, "rev-parse", "HEAD")) == []
    assert (root / "docs/06-delivery/STORY_INDEX.csv").read_bytes() == before
    assert b"STORY-0738,planned" in before


def test_receipt_definition_digest_mismatch(delivered: tuple) -> None:
    root, receipt, candidate, _ = delivered
    receipt["definition_sha256"] = "0" * 64
    write(root, f"evidence/delivery-gates/{GATE_ID}/{candidate}/integration-receipt.json", receipt)
    commit(root, "test: invalid receipt definition")
    assert_rejected(root, "definition digest mismatch")


def test_output_digest_mismatch(delivered: tuple) -> None:
    root, _, _, _ = delivered
    write(root, "src/frontend/package.json", {"tampered": True})
    commit(root, "test: changed accepted output")
    assert_rejected(root, "output digest mismatch")


@pytest.mark.parametrize("role", ["QA", "Reviewer", "ALL"])
def test_missing_independent_signed_approval(delivered: tuple, role: str) -> None:
    root, receipt, candidate, _ = delivered
    reference = receipt["daa_evidence"][0]
    bundle = json.loads((root / reference["path"]).read_text())
    bundle["attestations"] = [
        item for item in bundle["attestations"] if role != "ALL" and item["role"] != role
    ]
    receipt["daa_evidence"] = [write(root, reference["path"], bundle)]
    write(root, f"evidence/delivery-gates/{GATE_ID}/{candidate}/integration-receipt.json", receipt)
    commit(root, "test: missing approval")
    assert_rejected(root, "QA/Reviewer/DAA approval invalid")


def test_forged_daa_signature_rejected(delivered: tuple) -> None:
    root, receipt, candidate, _ = delivered
    reference = receipt["daa_evidence"][0]
    bundle = json.loads((root / reference["path"]).read_text())
    bundle["attestations"][0]["signature"]["value"] = "forged"
    receipt["daa_evidence"] = [write(root, reference["path"], bundle)]
    write(root, f"evidence/delivery-gates/{GATE_ID}/{candidate}/integration-receipt.json", receipt)
    commit(root, "test: forged approval")
    assert_rejected(root, "QA/Reviewer/DAA approval invalid")


def test_candidate_not_integrated(delivered: tuple) -> None:
    root, receipt, candidate, integration = delivered
    git(root, "switch", "-c", "unintegrated", integration + "^1")
    (root / "unrelated.txt").write_text("test candidate", encoding="utf-8")
    unrelated = commit(root, "test: unintegrated candidate")
    git(root, "switch", "main")
    old_root = root / f"evidence/delivery-gates/{GATE_ID}/{candidate}"
    new_prefix = f"evidence/delivery-gates/{GATE_ID}/{unrelated}"
    manifest = json.loads((root / receipt["acceptance_manifest"]["path"]).read_text())
    manifest["candidate_sha"] = unrelated
    receipt["acceptance_manifest"] = write(root, new_prefix + "/acceptance-manifest.json", manifest)
    write(root, new_prefix + "/integration-receipt.json", receipt)
    (old_root / "integration-receipt.json").unlink()
    commit(root, "test: receipt for unintegrated candidate")
    assert_rejected(root, "candidate not integrated")


def test_integration_outside_consumer_ancestry(delivered: tuple) -> None:
    root, receipt, candidate, integration = delivered
    git(root, "switch", "-c", "isolated", integration + "^2")
    write(root, f"evidence/delivery-gates/{GATE_ID}/{candidate}/integration-receipt.json", receipt)
    for reference in (receipt["human_integration_record"],):
        content = git(root, "show", "main:" + reference["path"])
        (root / reference["path"]).write_text(content + "\n", encoding="utf-8")
    commit(root, "test: receipt only on isolated branch")
    assert_rejected(root, "outside consumer ancestry")


def test_snapshot_missing_manifest_binding(delivered: tuple) -> None:
    root, receipt, candidate, _ = delivered
    path = receipt["task_envelope_snapshot"]["path"]
    snapshot = json.loads((root / path).read_text(encoding="utf-8"))
    del snapshot["delivery_gate_scope"]["acceptance_manifest_sha256"]
    receipt["task_envelope_snapshot"] = write(root, path, snapshot)
    write(root, f"evidence/delivery-gates/{GATE_ID}/{candidate}/integration-receipt.json", receipt)
    commit(root, "test: snapshot unbound")
    assert_rejected(root, "snapshot must bind manifest")


@pytest.mark.parametrize("kind", ["AcceptanceManifest", "IntegrationReceipt"])
def test_acceptance_schemas_closed_and_required(delivered: tuple, kind: str) -> None:
    root, receipt, _, _ = delivered
    schema = WorkingRepository(root).json(SCHEMA)
    document = (
        json.loads((root / receipt["acceptance_manifest"]["path"]).read_text())
        if kind == "AcceptanceManifest"
        else copy.deepcopy(receipt)
    )
    validate_schema(document, schema, kind)
    document["satisfied"] = True
    with pytest.raises(GateError, match="schema invalid"):
        validate_schema(document, schema, kind)
