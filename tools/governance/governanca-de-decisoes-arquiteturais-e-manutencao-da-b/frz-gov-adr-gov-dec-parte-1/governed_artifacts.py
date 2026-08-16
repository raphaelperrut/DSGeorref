from __future__ import annotations

import fnmatch
import hashlib
import re
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from canonical_json import CanonicalizationError, load_json_bytes


COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
FILE_SCOPE_POLICY_PATH = ".codex/policies/file-scopes.yaml"


@dataclass(frozen=True)
class GovernedArtifact:
    source_revision: str
    path: str
    content: bytes

    def json_object(self) -> dict[str, Any]:
        try:
            value = load_json_bytes(self.content)
        except CanonicalizationError as error:
            raise ValueError(f"governed artifact is not canonical JSON: {self.path}") from error
        if not isinstance(value, dict):
            raise ValueError(f"governed artifact must be a JSON object: {self.path}")
        return value


def git_blob(repository_root: Path, revision: str, path: str) -> bytes:
    if COMMIT_PATTERN.fullmatch(revision) is None:
        raise ValueError("artifact source_revision must be one full lowercase Git commit SHA")
    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts or "\\" in path:
        raise ValueError(f"artifact path is not repository-relative: {path!r}")
    resolved = subprocess.run(
        ["git", "-C", str(repository_root), "rev-parse", f"{revision}:{path}"],
        check=False,
        capture_output=True,
    )
    if resolved.returncode != 0:
        raise ValueError(f"governed artifact is missing at source revision: {path}")
    blob_id = resolved.stdout.decode("ascii").strip()
    completed = subprocess.run(
        ["git", "-C", str(repository_root), "cat-file", "blob", blob_id],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise ValueError(f"governed artifact blob is unreadable: {path}")
    return completed.stdout


def resolve_governed_artifact(
    repository_root: Path, reference: Mapping[str, Any]
) -> GovernedArtifact:
    path = reference.get("path")
    revision = reference.get("source_revision")
    expected_digest = reference.get("sha256")
    if not isinstance(path, str) or not isinstance(revision, str):
        raise ValueError("governed evidence reference lacks path/source_revision")
    if not isinstance(expected_digest, str):
        raise ValueError("governed evidence reference lacks sha256")
    content = git_blob(repository_root, revision, path)
    if hashlib.sha256(content).hexdigest() != expected_digest:
        raise ValueError(f"governed artifact hash mismatch: {path}")
    return GovernedArtifact(revision, path, content)


def revision_is_ancestor(
    repository_root: Path, ancestor: str, descendant: str
) -> bool:
    if COMMIT_PATTERN.fullmatch(ancestor) is None or COMMIT_PATTERN.fullmatch(descendant) is None:
        return False
    completed = subprocess.run(
        ["git", "-C", str(repository_root), "merge-base", "--is-ancestor", ancestor, descendant],
        check=False,
        capture_output=True,
    )
    return completed.returncode == 0


def revision_parent_count(repository_root: Path, revision: str) -> int:
    if COMMIT_PATTERN.fullmatch(revision) is None:
        return 0
    completed = subprocess.run(
        ["git", "-C", str(repository_root), "rev-list", "--parents", "-n", "1", revision],
        check=False,
        capture_output=True,
        encoding="ascii",
    )
    return max(0, len(completed.stdout.split()) - 1) if completed.returncode == 0 else 0


def role_authorizes_path(
    repository_root: Path,
    policy_revision: str,
    role: str,
    path: str,
) -> bool:
    patterns = _role_patterns(repository_root, policy_revision, role)
    if patterns is None:
        return False
    allow, deny = patterns
    authorized = any(fnmatch.fnmatchcase(path, pattern) for pattern in allow)
    denied = any(fnmatch.fnmatchcase(path, pattern) for pattern in deny)
    return authorized and not denied


def _role_patterns(
    repository_root: Path,
    policy_revision: str,
    role: str,
) -> tuple[list[str], list[str]] | None:
    try:
        policy = yaml.safe_load(
            git_blob(repository_root, policy_revision, FILE_SCOPE_POLICY_PATH).decode("utf-8")
        )
    except (UnicodeDecodeError, ValueError, yaml.YAMLError):
        return None
    rules = policy.get("rules") if isinstance(policy, dict) else None
    if not isinstance(rules, list):
        return None
    matches = [rule for rule in rules if isinstance(rule, dict) and rule.get("role") == role]
    if len(matches) != 1:
        return None
    allow, deny = matches[0].get("allow"), matches[0].get("deny", [])
    if not isinstance(allow, list) or not isinstance(deny, list):
        return None
    if not all(isinstance(pattern, str) and pattern for pattern in (*allow, *deny)):
        return None
    return allow, deny
