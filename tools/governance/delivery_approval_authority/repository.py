from __future__ import annotations

import hashlib
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .canonical import CanonicalizationError, load_json_object


COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
TRUST_ROOT = "contracts/assurance/delivery-approval-authority/trust"
MANIFEST_PATH = f"{TRUST_ROOT}/manifest.json"
PINNED_ANCHOR_PATH = (
    f"{TRUST_ROOT}/anchors/dsgeorref-daa-operational-roots-1.0.0.json"
)
PINNED_ANCHOR_SHA256 = "b5ef44d14070663a97d450761bde373a7b9d7fe150aed6fc20b6ca3bf13ae14f"


class GovernedTrustError(ValueError):
    """A repository/revision did not yield one unambiguous governed trust set."""


@dataclass(frozen=True)
class GovernedTrust:
    revision: str
    anchors: dict[str, Any]
    profile: dict[str, Any]
    digests: dict[str, str]


def _git(repository: Path, *arguments: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise GovernedTrustError("governed repository object is unavailable")
    return completed.stdout


def _validate_revision(repository: Path, revision: str) -> None:
    if COMMIT_PATTERN.fullmatch(revision) is None:
        raise GovernedTrustError("revision must be one full lowercase commit SHA")
    resolved = _git(repository, "rev-parse", "--verify", f"{revision}^{{commit}}")
    if resolved.decode("ascii").strip() != revision:
        raise GovernedTrustError("revision does not resolve exactly")


def runtime_governed_repository() -> tuple[Path, str]:
    """Resolve the repository and revision from the trusted verifier installation."""
    repository = Path(__file__).resolve().parents[3]
    revision = _git(repository, "rev-parse", "--verify", "HEAD^{commit}")
    decoded = revision.decode("ascii").strip()
    _validate_revision(repository, decoded)
    return repository, decoded


def _blob(repository: Path, revision: str, path: str) -> bytes:
    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts or "\\" in path:
        raise GovernedTrustError("governed path is not repository-relative")
    object_id = _git(repository, "rev-parse", f"{revision}:{path}").decode("ascii").strip()
    if re.fullmatch(r"[0-9a-f]{40,64}", object_id) is None:
        raise GovernedTrustError("governed path did not resolve to an object")
    return _git(repository, "cat-file", "blob", object_id)


def governed_json(repository: Path, revision: str, path: str) -> dict[str, Any]:
    try:
        return load_json_object(_blob(repository, revision, path))
    except CanonicalizationError as error:
        raise GovernedTrustError("governed artifact is not canonical JSON") from error


def _artifact(
    repository: Path,
    revision: str,
    reference: Any,
) -> tuple[dict[str, Any], str]:
    if not isinstance(reference, dict) or set(reference) != {"path", "sha256"}:
        raise GovernedTrustError("trust manifest reference is invalid")
    path, expected = reference.get("path"), reference.get("sha256")
    if not isinstance(path, str) or not path.startswith(f"{TRUST_ROOT}/"):
        raise GovernedTrustError("trust artifact is outside the governed trust root")
    if "/test-vectors/" in f"/{path}/" or not isinstance(expected, str):
        raise GovernedTrustError("conformance material cannot be operational trust")
    content = _blob(repository, revision, path)
    observed = hashlib.sha256(content).hexdigest()
    if not re.fullmatch(r"[0-9a-f]{64}", expected) or observed != expected:
        raise GovernedTrustError("governed trust digest mismatch")
    try:
        return load_json_object(content), observed
    except CanonicalizationError as error:
        raise GovernedTrustError("governed trust is not canonical JSON") from error


def resolve_governed_trust(repository: Path, revision: str) -> GovernedTrust:
    repository = repository.resolve(strict=True)
    _validate_revision(repository, revision)
    manifest = governed_json(repository, revision, MANIFEST_PATH)
    if set(manifest) != {"schema_version", "anchors", "profile"}:
        raise GovernedTrustError("trust manifest fields are invalid")
    if manifest.get("schema_version") != "1.0.0":
        raise GovernedTrustError("trust manifest version is unsupported")
    pinned_anchor = {"path": PINNED_ANCHOR_PATH, "sha256": PINNED_ANCHOR_SHA256}
    if manifest.get("anchors") != pinned_anchor:
        raise GovernedTrustError("trust anchor is not pinned by the operational verifier")
    anchors, anchor_digest = _artifact(repository, revision, manifest["anchors"])
    profile, profile_digest = _artifact(repository, revision, manifest["profile"])
    return GovernedTrust(
        revision=revision,
        anchors=anchors,
        profile=profile,
        digests={"anchors": anchor_digest, "profile": profile_digest},
    )


def governed_schema(repository: Path, revision: str, name: str) -> dict[str, Any]:
    allowed = {
        "anchors": "trust-anchor-set.schema.json",
        "profile": "trust-profile.schema.json",
        "binding": "role-binding.schema.json",
        "attestation": "approval-attestation.schema.json",
        "verdict": "verification-verdict.schema.json",
        "task": ".codex/tasks/TASK_ENVELOPE.schema.json",
    }
    if name not in allowed:
        raise GovernedTrustError("unknown governed schema")
    filename = allowed[name]
    contract_root = "contracts/assurance/delivery-approval-authority"
    path = filename if filename.startswith(".") else f"{contract_root}/{filename}"
    return governed_json(repository, revision, path)
