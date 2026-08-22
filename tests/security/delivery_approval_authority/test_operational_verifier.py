from __future__ import annotations

import copy
import hashlib
import inspect
import json
from pathlib import Path

from tools.governance.delivery_approval_authority import verify_delivery_approval
from tools.governance.delivery_approval_authority.canonical import canonical_json_bytes

from .fixture import (
    ATTESTATION_DOMAIN,
    TRUST_ROOT,
    GovernedFixture,
    _git,
    _sign,
    commit_profile,
    governed_fixture,
)


ROOT = Path(__file__).resolve().parents[3]
VERIFICATION_TIME = "2026-08-22T12:30:00Z"


def _fixture(tmp_path: Path) -> GovernedFixture:
    return governed_fixture(ROOT, tmp_path / "governed-repository")


def _verify(
    fixture: GovernedFixture,
    evidence: object,
    *,
    revision: str | None = None,
) -> dict[str, object]:
    return verify_delivery_approval(
        repository=fixture.repository,
        revision=revision or fixture.revision,
        task_envelope=fixture.task,
        expected_candidate_sha=fixture.candidate_sha,
        verification_time=VERIFICATION_TIME,
        evidence=evidence,
    )


def _assert_fail(verdict: dict[str, object], code: str) -> None:
    assert verdict["status"] == "FAIL"
    assert verdict["code"] == code
    assert verdict["validated_roles"] == []
    assert verdict["accountable_subjects"] == {"Executor": [], "QA": [], "Reviewer": []}


def test_delivery_approval_operational_verifier(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    verdict = _verify(fixture, fixture.evidence)
    assert verdict["status"] == "PASS"
    assert verdict["code"] == "APPROVAL_AUTHORITY_VERIFIED"
    assert set(verdict["validated_roles"]) == {"Executor", "QA", "Reviewer"}

    parameters = inspect.signature(verify_delivery_approval).parameters
    forbidden = {"verifier", "trust_profile", "anchors", "issuer", "key", "policy"}
    assert forbidden.isdisjoint(parameters)
    package_source = (ROOT / "tools/governance/delivery_approval_authority").glob("*.py")
    combined = "\n".join(path.read_text() for path in package_source)
    assert "test_delivery_approval_authority_contract" not in combined
    assert "tests." not in combined


def test_delivery_approval_governed_trust_resolution(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    profile_path = fixture.repository / TRUST_ROOT / "profiles/independent-test.json"
    profile_path.write_text("{}\n")

    assert _verify(fixture, fixture.evidence)["status"] == "PASS"
    _git(fixture.repository, "add", profile_path.relative_to(fixture.repository).as_posix())
    _git(fixture.repository, "commit", "-m", "test: tamper governed profile")
    tampered_revision = _git(fixture.repository, "rev-parse", "HEAD")
    tampered = _verify(fixture, fixture.evidence, revision=tampered_revision)
    _assert_fail(tampered, "TRUST_ANCHOR_INVALID")
    assert _verify(fixture, fixture.evidence, revision=fixture.revision)["status"] == "PASS"
    _assert_fail(_verify(fixture, fixture.evidence, revision="f" * 40), "TRUST_ANCHOR_INVALID")


def test_delivery_approval_rejects_caller_and_conformance_trust(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    suite_path = fixture.repository / (
        "contracts/assurance/delivery-approval-authority/test-vectors/conformance-suite.json"
    )
    suite = json.loads(suite_path.read_text())
    injected = copy.deepcopy(fixture.evidence)
    injected["trust_profile"] = suite["trusted_configuration"]["trust_profile"]
    _assert_fail(_verify(fixture, injected), "SCHEMA_INVALID")

    manifest_path = fixture.repository / TRUST_ROOT / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["anchors"] = {
        "path": suite_path.relative_to(fixture.repository).as_posix(),
        "sha256": hashlib.sha256(suite_path.read_bytes()).hexdigest(),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    _git(fixture.repository, "add", manifest_path.relative_to(fixture.repository).as_posix())
    _git(fixture.repository, "commit", "-m", "test: attempt conformance trust promotion")
    revision = _git(fixture.repository, "rev-parse", "HEAD")
    _assert_fail(_verify(fixture, fixture.evidence, revision=revision), "TRUST_ANCHOR_INVALID")


def test_delivery_approval_operational_fail_closed(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)

    unknown_issuer = copy.deepcopy(fixture.evidence)
    qa = unknown_issuer["attestations"][1]
    qa["principal"]["issuer"] = "https://caller.invalid"
    _sign(qa, fixture.private_keys["qa"], ATTESTATION_DOMAIN)
    _assert_fail(_verify(fixture, unknown_issuer), "ISSUER_UNTRUSTED")

    unknown_key = copy.deepcopy(fixture.evidence)
    unknown_key["attestations"][1]["signature"]["key_id"] = "caller-key"
    _assert_fail(_verify(fixture, unknown_key), "SIGNER_UNKNOWN")

    wrong_scope = copy.deepcopy(fixture.evidence)
    wrong_scope["attestations"][1]["trust_scope"] = "SPEC-001-PROMPT-BUNDLE-V1"
    _assert_fail(_verify(fixture, wrong_scope), "TRUST_SCOPE_INVALID")

    invalid_signature = copy.deepcopy(fixture.evidence)
    invalid_signature["attestations"][1]["signature"]["value"] = "A" * 86
    _assert_fail(_verify(fixture, invalid_signature), "SIGNATURE_INVALID")

    qa_key = next(key for key in fixture.profile["keys"] if key["key_id"] == "issue-0871-qa")
    qa_key["revoked_at"] = "2026-08-22T12:15:00Z"
    revoked_revision = commit_profile(fixture)
    _assert_fail(_verify(fixture, fixture.evidence, revision=revoked_revision), "REVOKED")

    assert hashlib.sha256(canonical_json_bytes(fixture.task)).hexdigest() == (
        fixture.evidence["attestations"][0]["task_envelope"]["digest_sha256"]
    )
