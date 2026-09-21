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
    PINNED_V2_ANCHOR_SHA256,
    GovernedTrust,
    GovernedTrustError,
    resolve_governed_trust,
    runtime_governed_repository,
)
from tools.governance.delivery_approval_authority.schemas import SchemaSet
from tools.governance.delivery_approval_authority.verifier import OperationalVerifier

from .fixture import (
    ATTESTATION_DOMAIN,
    ATTESTATION_DOMAIN_V2,
    TRUST_ROOT,
    GovernedFixture,
    _git,
    _sign,
    _write_json,
    governed_fixture,
    solo_governed_fixture,
)


ROOT = Path(__file__).resolve().parents[3]
VERIFICATION_TIME = "2026-08-22T12:30:00Z"
V2_VERIFICATION_TIME = "2026-09-21T00:00:00Z"


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


def _solo_fixture(tmp_path: Path) -> GovernedFixture:
    return solo_governed_fixture(ROOT, tmp_path / "solo-governed-repository")


def _verify_solo_core(
    fixture: GovernedFixture,
    evidence: object,
) -> dict[str, object]:
    trust = GovernedTrust(
        revision=fixture.revision,
        anchors=fixture.anchors,
        profile=fixture.profile,
        digests={},
        contract_version="2.0.0",
    )
    verifier = OperationalVerifier(trust, SchemaSet(fixture.repository, fixture.revision))
    return verifier.verify(
        evidence=evidence,
        task_envelope=fixture.task,
        candidate_sha=fixture.candidate_sha,
        verification_time="2026-09-20T12:30:00Z",
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
        verification_time=V2_VERIFICATION_TIME,
        evidence={"bindings": [], "attestations": []},
    )
    assert governed["profile"] == {
        "profile_id": "dsgeorref-daa-operational",
        "profile_version": "2.0.0",
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
    assert trust.digests["anchors"] == PINNED_V2_ANCHOR_SHA256
    assert trust.contract_version == "2.0.0"
    assert PINNED_ANCHOR_SHA256 == (
        "b5ef44d14070663a97d450761bde373a7b9d7fe150aed6fc20b6ca3bf13ae14f"
    )

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


def test_solo_delivery_approval_verifies_ordered_functional_chain(tmp_path: Path) -> None:
    fixture = _solo_fixture(tmp_path)
    result = _verify_solo_core(fixture, fixture.evidence)
    assert result["status"] == "PASS"
    assert result["code"] == "APPROVAL_AUTHORITY_VERIFIED"
    assert result["governance_mode"] == "SOLO_FUNCTIONAL_SEGREGATION_V1"
    assert result["personal_independence"] == "ABSENT_DECLARED"
    assert result["formal_decision"] == "PASS"
    assert result["validated_roles"] == ["Executor", "QA", "Reviewer", "Project Owner"]
    assert len(result["functional_sessions"]) == 4
    subjects = result["accountable_subjects"]
    assert {tuple(values) for values in subjects.values()} == {
        ("acct:issue-0974/solo-principal",)
    }


def test_solo_delivery_approval_no_go_is_authenticated_fail(tmp_path: Path) -> None:
    fixture = _solo_fixture(tmp_path)
    evidence = copy.deepcopy(fixture.evidence)
    owner = evidence["attestations"][-1]
    owner["decision"] = "NO_GO"
    _sign(owner, fixture.private_keys["project-owner"], ATTESTATION_DOMAIN_V2)
    result = _verify_solo_core(fixture, evidence)
    assert result["status"] == "FAIL"
    assert result["code"] == "OWNER_NO_GO"
    assert result["formal_decision"] == "NO_GO"
    assert result["validated_roles"] == []


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("owner-missing", "APPROVAL_MISSING"),
        ("predecessor-mismatch", "PREDECESSOR_MISMATCH"),
        ("sequence-mismatch", "SESSION_SEQUENCE_INVALID"),
        ("candidate-mismatch", "CANDIDATE_SHA_MISMATCH"),
        ("personal-independence-claim", "SCHEMA_INVALID"),
    ],
)
def test_solo_delivery_approval_fails_closed(
    tmp_path: Path,
    mutation: str,
    expected_code: str,
) -> None:
    fixture = _solo_fixture(tmp_path)
    evidence = copy.deepcopy(fixture.evidence)
    if mutation == "owner-missing":
        evidence["attestations"].pop()
    elif mutation == "predecessor-mismatch":
        reviewer = evidence["attestations"][2]
        reviewer["functional_session"]["predecessor_attestation_digest_sha256"] = "0" * 64
        _sign(reviewer, fixture.private_keys["reviewer"], ATTESTATION_DOMAIN_V2)
    elif mutation == "sequence-mismatch":
        qa = evidence["attestations"][1]
        qa["functional_session"]["sequence"] = 3
        _sign(qa, fixture.private_keys["qa"], ATTESTATION_DOMAIN_V2)
    elif mutation == "candidate-mismatch":
        qa = evidence["attestations"][1]
        qa["candidate_sha"] = "f" * 40
        _sign(qa, fixture.private_keys["qa"], ATTESTATION_DOMAIN_V2)
    elif mutation == "personal-independence-claim":
        qa = evidence["attestations"][1]
        qa["personal_independence"] = "PRESENT"
        _sign(qa, fixture.private_keys["qa"], ATTESTATION_DOMAIN_V2)
    result = _verify_solo_core(fixture, evidence)
    assert result["status"] == "FAIL"
    assert result["code"] == expected_code
    assert result["formal_decision"] is None
    assert result["validated_roles"] == []
