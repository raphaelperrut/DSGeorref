from __future__ import annotations

import copy
import hashlib
import inspect
import json
import subprocess
from pathlib import Path

import pytest

from tools.governance.delivery_approval_authority import verify_delivery_approval
from tools.governance.delivery_approval_authority.canonical import canonical_json_bytes
from tools.governance.delivery_approval_authority.repository import (
    PINNED_ANCHOR_SHA256,
    GovernedTrust,
    GovernedTrustError,
    resolve_governed_trust,
    runtime_governed_repository,
)
from tools.governance.delivery_approval_authority.schemas import SchemaSet
from tools.governance.delivery_approval_authority.verifier import OperationalVerifier

from .fixture import (
    ATTESTATION_DOMAIN,
    TRUST_ROOT,
    GovernedFixture,
    _git,
    _sign,
    _write_json,
    governed_fixture,
)


ROOT = Path(__file__).resolve().parents[3]
VERIFICATION_TIME = "2026-08-22T12:30:00Z"


def _fixture(tmp_path: Path) -> GovernedFixture:
    return governed_fixture(ROOT, tmp_path / "governed-repository")


def _verify_core(
    fixture: GovernedFixture,
    evidence: object,
) -> dict[str, object]:
    trust = GovernedTrust(
        revision=fixture.revision,
        anchors=fixture.anchors,
        profile=fixture.profile,
        digests={},
    )
    verifier = OperationalVerifier(trust, SchemaSet(fixture.repository, fixture.revision))
    return verifier.verify(
        evidence=evidence,
        task_envelope=fixture.task,
        candidate_sha=fixture.candidate_sha,
        verification_time=VERIFICATION_TIME,
    )


def _assert_fail(verdict: dict[str, object], code: str) -> None:
    assert verdict["status"] == "FAIL"
    assert verdict["code"] == code
    assert verdict["validated_roles"] == []
    assert verdict["accountable_subjects"] == {"Executor": [], "QA": [], "Reviewer": []}


def test_delivery_approval_operational_verifier(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    verdict = _verify_core(fixture, fixture.evidence)
    assert verdict["status"] == "PASS"
    assert verdict["code"] == "APPROVAL_AUTHORITY_VERIFIED"
    assert set(verdict["validated_roles"]) == {"Executor", "QA", "Reviewer"}

    parameters = inspect.signature(verify_delivery_approval).parameters
    forbidden = {
        "repository",
        "revision",
        "verifier",
        "trust_profile",
        "anchors",
        "issuer",
        "key",
        "policy",
    }
    assert forbidden.isdisjoint(parameters)
    governed = verify_delivery_approval(
        task_envelope=fixture.task,
        expected_candidate_sha=fixture.candidate_sha,
        verification_time=VERIFICATION_TIME,
        evidence={"bindings": [], "attestations": []},
    )
    assert governed["profile"] == {
        "profile_id": "dsgeorref-daa-operational",
        "profile_version": "1.0.0",
    }
    assert governed["code"] == "APPROVAL_MISSING"
    package_source = (ROOT / "tools/governance/delivery_approval_authority").glob("*.py")
    combined = "\n".join(path.read_text() for path in package_source)
    assert "test_delivery_approval_authority_contract" not in combined
    assert "tests." not in combined


def test_delivery_approval_governed_trust_resolution(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    repository, revision = runtime_governed_repository()
    assert repository == ROOT
    trust = resolve_governed_trust(repository, revision)
    assert trust.digests["anchors"] == PINNED_ANCHOR_SHA256

    with pytest.raises(GovernedTrustError, match="not pinned"):
        resolve_governed_trust(fixture.repository, fixture.revision)


def test_delivery_approval_rejects_caller_and_conformance_trust(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    suite_path = fixture.repository / (
        "contracts/assurance/delivery-approval-authority/test-vectors/conformance-suite.json"
    )
    suite = json.loads(suite_path.read_text())
    injected = copy.deepcopy(fixture.evidence)
    injected["trust_profile"] = suite["trusted_configuration"]["trust_profile"]
    _assert_fail(_verify_core(fixture, injected), "SCHEMA_INVALID")

    with pytest.raises(TypeError, match="repository"):
        verify_delivery_approval(
            repository=fixture.repository,  # type: ignore[call-arg]
            task_envelope=fixture.task,
            expected_candidate_sha=fixture.candidate_sha,
            verification_time=VERIFICATION_TIME,
            evidence=fixture.evidence,
        )

    copied = tmp_path / "conformance-copy"
    subprocess.run(["git", "clone", "--quiet", str(ROOT), str(copied)], check=True)
    _git(copied, "config", "user.name", "ISSUE-0871 sentinel")
    _git(copied, "config", "user.email", "issue-0871-sentinel@test.invalid")
    suite_path = copied / (
        "contracts/assurance/delivery-approval-authority/test-vectors/conformance-suite.json"
    )
    suite = json.loads(suite_path.read_text())
    manifest_path = copied / TRUST_ROOT / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    anchor_path = copied / manifest["anchors"]["path"]
    profile_path = copied / manifest["profile"]["path"]
    trusted = suite["trusted_configuration"]
    manifest["anchors"]["sha256"] = _write_json(anchor_path, trusted["trust_anchors"])
    manifest["profile"]["sha256"] = _write_json(profile_path, trusted["trust_profile"])
    _write_json(manifest_path, manifest)
    _git(copied, "add", TRUST_ROOT.as_posix())
    _git(copied, "commit", "-m", "test: copy conformance material into operational trust")
    copied_revision = _git(copied, "rev-parse", "HEAD")
    with pytest.raises(GovernedTrustError, match="not pinned"):
        resolve_governed_trust(copied, copied_revision)


def test_delivery_approval_operational_fail_closed(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)

    unknown_issuer = copy.deepcopy(fixture.evidence)
    qa = unknown_issuer["attestations"][1]
    qa["principal"]["issuer"] = "https://caller.invalid"
    _sign(qa, fixture.private_keys["qa"], ATTESTATION_DOMAIN)
    _assert_fail(_verify_core(fixture, unknown_issuer), "ISSUER_UNTRUSTED")

    unknown_key = copy.deepcopy(fixture.evidence)
    unknown_key["attestations"][1]["signature"]["key_id"] = "caller-key"
    _assert_fail(_verify_core(fixture, unknown_key), "SIGNER_UNKNOWN")

    wrong_scope = copy.deepcopy(fixture.evidence)
    wrong_scope["attestations"][1]["trust_scope"] = "SPEC-001-PROMPT-BUNDLE-V1"
    _assert_fail(_verify_core(fixture, wrong_scope), "TRUST_SCOPE_INVALID")

    invalid_signature = copy.deepcopy(fixture.evidence)
    invalid_signature["attestations"][1]["signature"]["value"] = "A" * 86
    _assert_fail(_verify_core(fixture, invalid_signature), "SIGNATURE_INVALID")

    qa_key = next(key for key in fixture.profile["keys"] if key["key_id"] == "issue-0871-qa")
    qa_key["revoked_at"] = "2026-08-22T12:15:00Z"
    profile_domain = "DSGEOREF-DELIVERY-APPROVAL-TRUST-PROFILE-V1"
    _sign(fixture.profile, fixture.private_keys["root"], profile_domain)
    _assert_fail(_verify_core(fixture, fixture.evidence), "REVOKED")

    assert hashlib.sha256(canonical_json_bytes(fixture.task)).hexdigest() == (
        fixture.evidence["attestations"][0]["task_envelope"]["digest_sha256"]
    )
