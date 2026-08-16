from __future__ import annotations

import fnmatch
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from canonical_json import CanonicalizationError, load_json_bytes
from foundation_validation_types import Finding


FILE_SCOPE_POLICY_PATH = ".codex/policies/file-scopes.yaml"


def _git_bytes(repository_root: Path, revision: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(repository_root), "show", f"{revision}:{path}"],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise ValueError(f"repository path is unavailable at {revision}: {path}")
    return completed.stdout


def _changed_paths(repository_root: Path, start: str, end: str) -> tuple[str, ...]:
    completed = subprocess.run(
        ["git", "-C", str(repository_root), "diff", "--name-only", f"{start}..{end}"],
        check=False,
        capture_output=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise ValueError(f"cannot resolve effective diff {start}..{end}")
    paths = tuple(line for line in completed.stdout.splitlines() if line)
    if len(paths) != len(set(paths)):
        raise ValueError("effective diff contains duplicate paths")
    return paths


def _is_ancestor(repository_root: Path, ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(repository_root), "merge-base", "--is-ancestor", ancestor, descendant],
        check=False,
        capture_output=True,
    )
    return completed.returncode == 0


def _matches(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def _task_at_revision(
    repository_root: Path, revision: str, task_envelope_path: str
) -> dict[str, Any]:
    try:
        task = load_json_bytes(_git_bytes(repository_root, revision, task_envelope_path))
    except (CanonicalizationError, ValueError) as error:
        raise ValueError(f"invalid TaskEnvelope authority: {error}") from error
    if not isinstance(task, dict):
        raise ValueError("TaskEnvelope authority must be a JSON object")
    return task


def _role_scope_at_revision(
    repository_root: Path, revision: str, role: object
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if not isinstance(role, str) or not role:
        raise ValueError("TaskEnvelope has no authoritative role")
    try:
        policy = yaml.safe_load(
            _git_bytes(repository_root, revision, FILE_SCOPE_POLICY_PATH).decode("utf-8")
        )
    except (UnicodeDecodeError, yaml.YAMLError, ValueError) as error:
        raise ValueError(f"invalid file-scope policy: {error}") from error
    rules = policy.get("rules") if isinstance(policy, dict) else None
    if not isinstance(rules, list):
        raise ValueError("file-scope policy has no rules")
    matches = [rule for rule in rules if isinstance(rule, dict) and rule.get("role") == role]
    if len(matches) != 1:
        raise ValueError(f"file-scope policy must define exactly one role rule: {role}")
    allow, deny = matches[0].get("allow"), matches[0].get("deny", [])
    return _validated_patterns(allow, "role allow"), _validated_patterns(deny, "role deny")


def _validated_patterns(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{label} scope is not an array")
    if not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{label} scope contains an invalid pattern")
    return tuple(value)


def _scope_authorities(
    repository_root: Path,
    base_revision: str,
    authority_checkpoint: str,
    candidate_revision: str,
    task_envelope_path: str,
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...], tuple[str, ...], tuple[str, ...], set[str], bool]:
    task = _task_at_revision(repository_root, authority_checkpoint, task_envelope_path)
    checkpoint_task = _git_bytes(repository_root, authority_checkpoint, task_envelope_path)
    candidate_task = _git_bytes(repository_root, candidate_revision, task_envelope_path)
    role_allow, role_deny = _role_scope_at_revision(
        repository_root, authority_checkpoint, task.get("role")
    )
    task_allow = _validated_patterns(task.get("allow_paths"), "TaskEnvelope allow")
    task_deny = _validated_patterns(task.get("deny_paths"), "TaskEnvelope deny")
    effective_paths = _changed_paths(repository_root, base_revision, candidate_revision)
    checkpoint_paths = set(
        _changed_paths(repository_root, base_revision, authority_checkpoint)
    )
    frozen = checkpoint_task == candidate_task
    return task_allow, task_deny, role_allow, role_deny, effective_paths, checkpoint_paths, frozen


def _effective_path_findings(
    effective_paths: tuple[str, ...],
    task_allow: tuple[str, ...],
    task_deny: tuple[str, ...],
    task_envelope_path: str,
    control_plane_authorized: bool,
) -> list[Finding]:
    findings: list[Finding] = []
    for path in effective_paths:
        if _matches(path, task_deny):
            findings.append(Finding("DENIED_PATH_CHANGED", path, "path matches deny_paths"))
        elif _matches(path, task_allow):
            continue
        elif path == task_envelope_path and control_plane_authorized:
            continue
        else:
            findings.append(
                Finding(
                    "PATH_OUTSIDE_EFFECTIVE_SCOPE",
                    path,
                    "path is neither TaskEnvelope-authorized nor a frozen control-plane mutation",
                )
            )
    return findings


def _task_path_findings(task_envelope_path: str) -> list[Finding]:
    pure = PurePosixPath(task_envelope_path)
    valid = (
        not pure.is_absolute()
        and ".." not in pure.parts
        and pure.parent == PurePosixPath(".codex/tasks")
        and pure.name.startswith("TASK-")
        and pure.suffix == ".json"
    )
    if valid:
        return []
    return [
        Finding(
            "TASK_ENVELOPE_PATH_INVALID",
            "task_envelope_path",
            "control-plane authority is limited to one repository TaskEnvelope",
        )
    ]


def _checkpoint_findings(
    repository_root: Path,
    base_revision: str,
    authority_checkpoint: str,
    candidate_revision: str,
) -> list[Finding]:
    findings: list[Finding] = []
    if not _is_ancestor(repository_root, base_revision, authority_checkpoint):
        findings.append(
            Finding("CHECKPOINT_INVALID", "authority_checkpoint", "checkpoint is not based on base")
        )
    if not _is_ancestor(repository_root, authority_checkpoint, candidate_revision):
        findings.append(
            Finding(
                "CHECKPOINT_INVALID",
                "candidate_revision",
                "candidate does not preserve the authority checkpoint in history",
            )
        )
    return findings


def validate_effective_task_scope(
    repository_root: Path,
    *,
    base_revision: str,
    authority_checkpoint: str,
    candidate_revision: str,
    task_envelope_path: str,
) -> list[Finding]:
    findings = _task_path_findings(task_envelope_path)
    findings.extend(
        _checkpoint_findings(
            repository_root, base_revision, authority_checkpoint, candidate_revision
        )
    )
    if findings:
        return sorted(findings)
    try:
        (
            task_allow,
            task_deny,
            role_allow,
            role_deny,
            effective_paths,
            checkpoint_paths,
            frozen,
        ) = _scope_authorities(
            repository_root,
            base_revision,
            authority_checkpoint,
            candidate_revision,
            task_envelope_path,
        )
    except ValueError as error:
        return [Finding("SCOPE_AUTHORITY_INVALID", "$", str(error))]

    task_control_plane_authorized = (
        task_envelope_path in checkpoint_paths
        and frozen
        and _matches(task_envelope_path, role_allow)
        and not _matches(task_envelope_path, role_deny)
    )
    findings.extend(
        _effective_path_findings(
            effective_paths,
            task_allow,
            task_deny,
            task_envelope_path,
            task_control_plane_authorized,
        )
    )
    if task_envelope_path in effective_paths and not task_control_plane_authorized:
        findings.append(
            Finding(
                "TASK_CONTROL_PLANE_UNAUTHORIZED",
                task_envelope_path,
                "TaskEnvelope mutation lacks frozen checkpoint and role-policy authority",
            )
        )
    return sorted(set(findings))
