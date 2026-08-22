from __future__ import annotations

import base64
import copy
import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from tools.governance.delivery_approval_authority.canonical import canonical_json_bytes


SCOPE = "DSGEOREF-DELIVERY-APPROVAL-AUTHORITY-V1"
PROFILE_DOMAIN = "DSGEOREF-DELIVERY-APPROVAL-TRUST-PROFILE-V1"
BINDING_DOMAIN = "DSGEOREF-DELIVERY-APPROVAL-ROLE-BINDING-V1"
ATTESTATION_DOMAIN = "DSGEOREF-DELIVERY-APPROVAL-ATTESTATION-V1"
TRUST_ROOT = Path("contracts/assurance/delivery-approval-authority/trust")
ISSUER = "https://operational-test.invalid"


def _key(label: str) -> Ed25519PrivateKey:
    seed = hashlib.sha256(f"issue-0871-independent:{label}".encode()).digest()
    return Ed25519PrivateKey.from_private_bytes(seed)


def _encoded(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode()


def _public(key: Ed25519PrivateKey) -> str:
    return _encoded(key.public_key().public_bytes_raw())


def _sign(document: dict[str, Any], key: Ed25519PrivateKey, domain: str) -> None:
    projection = copy.deepcopy(document)
    projection["signature"]["value"] = ""
    message = domain.encode("ascii") + b"\x00" + canonical_json_bytes(projection)
    document["signature"]["value"] = _encoded(key.sign(message))


def _git(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _write_json(path: Path, document: dict[str, Any]) -> str:
    content = (json.dumps(document, indent=2) + "\n").encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return hashlib.sha256(content).hexdigest()


@dataclass
class GovernedFixture:
    repository: Path
    revision: str
    profile: dict[str, Any]
    anchors: dict[str, Any]
    private_keys: dict[str, Ed25519PrivateKey]
    task: dict[str, Any]
    candidate_sha: str
    evidence: dict[str, Any]


def _profile(keys: dict[str, Ed25519PrivateKey]) -> dict[str, Any]:
    records = [
        {
            "key_id": "issue-0871-binding",
            "algorithm": "Ed25519",
            "public_key": _public(keys["binding"]),
            "purpose": "DELIVERY_ROLE_BINDING",
            "trust_scope": SCOPE,
            "principal": None,
            "roles": ["Executor", "QA", "Reviewer"],
            "task_envelope_ids": ["TASK-0761"],
            "valid_from": "2026-08-22T00:00:00Z",
            "valid_until": "2026-08-23T00:00:00Z",
            "revoked_at": None,
        }
    ]
    for role in ("Executor", "QA", "Reviewer"):
        label = role.lower()
        records.append(
            {
                "key_id": f"issue-0871-{label}",
                "algorithm": "Ed25519",
                "public_key": _public(keys[label]),
                "purpose": "DELIVERY_APPROVAL_ATTESTATION",
                "trust_scope": SCOPE,
                "principal": {"issuer": ISSUER, "subject": f"principal-{label}"},
                "roles": [role],
                "task_envelope_ids": ["TASK-0761"],
                "valid_from": "2026-08-22T00:00:00Z",
                "valid_until": "2026-08-23T00:00:00Z",
                "revoked_at": None,
            }
        )
    profile = {
        "schema_version": "1.0.0",
        "profile_id": "issue-0871-independent-test",
        "profile_version": "1.0.0",
        "trust_scope": SCOPE,
        "canonicalization": "JCS-RFC8785-PROFILE-1",
        "hash_algorithm": "SHA-256",
        "signature_algorithm": "Ed25519",
        "valid_from": "2026-08-22T00:00:00Z",
        "valid_until": "2026-08-23T00:00:00Z",
        "identity_issuers": [
            {
                "issuer": ISSUER,
                "trust_scope": SCOPE,
                "valid_from": "2026-08-22T00:00:00Z",
                "valid_until": "2026-08-23T00:00:00Z",
                "revoked_at": None,
            }
        ],
        "keys": records,
        "signature": {
            "key_id": "issue-0871-root",
            "algorithm": "Ed25519",
            "message_profile": PROFILE_DOMAIN,
            "value": "",
        },
    }
    _sign(profile, keys["root"], PROFILE_DOMAIN)
    return profile


def _anchors(root: Ed25519PrivateKey) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "anchor_set_id": "issue-0871-independent-test-roots",
        "anchor_set_version": "1.0.0",
        "trust_scope": SCOPE,
        "anchors": [
            {
                "key_id": "issue-0871-root",
                "algorithm": "Ed25519",
                "public_key": _public(root),
                "purpose": "DELIVERY_TRUST_PROFILE_SIGNING",
                "trust_scope": SCOPE,
                "valid_from": "2026-08-22T00:00:00Z",
                "valid_until": "2026-08-23T00:00:00Z",
                "revoked_at": None,
            }
        ],
    }


def _binding(role: str, key: Ed25519PrivateKey) -> dict[str, Any]:
    label = role.lower()
    document = {
        "schema_version": "1.0.0",
        "binding_id": f"issue-0871-binding-{label}",
        "binding_version": "1.0.0",
        "trust_scope": SCOPE,
        "policy": {"profile_id": "issue-0871-independent-test", "profile_version": "1.0.0"},
        "principal": {"issuer": ISSUER, "subject": f"principal-{label}"},
        "accountable_subject": f"acct:issue-0871/{label}",
        "role": role,
        "task_envelope_ids": ["TASK-0761"],
        "valid_from": "2026-08-22T00:00:00Z",
        "valid_until": "2026-08-23T00:00:00Z",
        "revoked_at": None,
        "signature": {
            "key_id": "issue-0871-binding",
            "algorithm": "Ed25519",
            "message_profile": BINDING_DOMAIN,
            "value": "",
        },
    }
    _sign(document, key, BINDING_DOMAIN)
    return document


def _attestation(
    role: str,
    binding: dict[str, Any],
    task: dict[str, Any],
    candidate_sha: str,
    key: Ed25519PrivateKey,
) -> dict[str, Any]:
    label = role.lower()
    document = {
        "schema_version": "1.0.0",
        "attestation_id": f"issue-0871-attestation-{label}",
        "trust_scope": SCOPE,
        "policy": {"profile_id": "issue-0871-independent-test", "profile_version": "1.0.0"},
        "principal": {"issuer": ISSUER, "subject": f"principal-{label}"},
        "accountable_subject": f"acct:issue-0871/{label}",
        "role": role,
        "decision": "DELIVERED" if role == "Executor" else "APPROVE",
        "binding": {
            "binding_id": binding["binding_id"],
            "binding_version": binding["binding_version"],
            "digest_sha256": hashlib.sha256(canonical_json_bytes(binding)).hexdigest(),
        },
        "task_envelope": {
            "task_id": task["task_id"],
            "digest_sha256": hashlib.sha256(canonical_json_bytes(task)).hexdigest(),
        },
        "candidate_sha": candidate_sha,
        "issued_at": "2026-08-22T12:00:00Z",
        "signature": {
            "key_id": f"issue-0871-{label}",
            "algorithm": "Ed25519",
            "message_profile": ATTESTATION_DOMAIN,
            "value": "",
        },
    }
    _sign(document, key, ATTESTATION_DOMAIN)
    return document


def _commit_trust(repository: Path, anchors: dict[str, Any], profile: dict[str, Any]) -> str:
    anchor_path = TRUST_ROOT / "anchors/independent-test.json"
    profile_path = TRUST_ROOT / "profiles/independent-test.json"
    anchor_digest = _write_json(repository / anchor_path, anchors)
    profile_digest = _write_json(repository / profile_path, profile)
    manifest = {
        "schema_version": "1.0.0",
        "repository": "raphaelperrut/DSGeorref",
        "anchors": {"path": anchor_path.as_posix(), "sha256": anchor_digest},
        "profile": {"path": profile_path.as_posix(), "sha256": profile_digest},
    }
    _write_json(repository / TRUST_ROOT / "manifest.json", manifest)
    _git(repository, "add", TRUST_ROOT.as_posix())
    _git(repository, "commit", "-m", "test: governed operational trust revision")
    return _git(repository, "rev-parse", "HEAD")


def governed_fixture(source: Path, destination: Path) -> GovernedFixture:
    subprocess.run(
        ["git", "clone", "--quiet", "--no-hardlinks", str(source), str(destination)],
        check=True,
    )
    _git(destination, "config", "user.name", "ISSUE-0871 test")
    _git(destination, "config", "user.email", "issue-0871@test.invalid")
    keys = {label: _key(label) for label in ("root", "binding", "executor", "qa", "reviewer")}
    anchors, profile = _anchors(keys["root"]), _profile(keys)
    revision = _commit_trust(destination, anchors, profile)
    task = json.loads((destination / ".codex/tasks/TASK-0761.json").read_text())
    bindings = [_binding(role, keys["binding"]) for role in ("Executor", "QA", "Reviewer")]
    attestations = [
        _attestation(role, binding, task, revision, keys[role.lower()])
        for role, binding in zip(("Executor", "QA", "Reviewer"), bindings, strict=True)
    ]
    return GovernedFixture(
        destination,
        revision,
        profile,
        anchors,
        keys,
        task,
        revision,
        {"bindings": bindings, "attestations": attestations},
    )


def commit_profile(fixture: GovernedFixture) -> str:
    _sign(fixture.profile, fixture.private_keys["root"], PROFILE_DOMAIN)
    return _commit_trust(fixture.repository, fixture.anchors, fixture.profile)
