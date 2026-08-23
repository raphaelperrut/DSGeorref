from __future__ import annotations

import fnmatch
import re
import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from repository_surfaces import (
    executable_shell_lines,
    revision_paths,
    workflow_commands,
)
from slice_one import Finding, git_blob


def validate_uv_lock_baseline(
    repository_root: Path, source_revision: str
) -> list[Finding]:
    try:
        paths = revision_paths(repository_root, source_revision)
        root_text = git_blob(
            repository_root, source_revision, "pyproject.toml"
        ).decode("utf-8")
        lock_text = git_blob(repository_root, source_revision, "uv.lock").decode(
            "utf-8"
        )
        make_text = git_blob(
            repository_root, source_revision, "Makefile"
        ).decode("utf-8")
    except (UnicodeDecodeError, ValueError) as error:
        return [Finding("UV_LOCK_MISSING", source_revision, str(error))]
    projects, findings = _workspace_projects(
        repository_root, source_revision, paths, root_text
    )
    findings.extend(_lock_findings(lock_text, projects))
    commands, command_findings = workflow_commands(
        repository_root, source_revision, paths
    )
    findings.extend(command_findings)
    findings.extend(_uv_command_findings([make_text, *commands]))
    return sorted(findings)


def _workspace_projects(
    repository_root: Path,
    revision: str,
    paths: tuple[str, ...],
    root_text: str,
) -> tuple[list[tuple[str, Mapping[str, Any]]], list[Finding]]:
    try:
        root = tomllib.loads(root_text)
    except tomllib.TOMLDecodeError as error:
        return [], [Finding("UV_WORKSPACE_INVALID", "pyproject.toml", str(error))]
    workspace = root.get("tool", {}).get("uv", {}).get("workspace")
    members = workspace.get("members") if isinstance(workspace, Mapping) else None
    if not isinstance(members, list) or not members or not all(
        isinstance(item, str) and item for item in members
    ):
        return [], [
            Finding(
                "UV_WORKSPACE_INVALID",
                "pyproject.toml",
                "[tool.uv.workspace] members are required",
            )
        ]
    projects: list[tuple[str, Mapping[str, Any]]] = [(".", root)]
    findings: list[Finding] = []
    child_manifests = tuple(
        path for path in paths if path != "pyproject.toml" and path.endswith("/pyproject.toml")
    )
    for pattern in members:
        matched = [
            path
            for path in child_manifests
            if fnmatch.fnmatch(path.removesuffix("/pyproject.toml"), pattern)
        ]
        if not matched:
            findings.append(
                Finding(
                    "UV_WORKSPACE_INVALID",
                    "pyproject.toml",
                    f"workspace member pattern has no governed manifest: {pattern}",
                )
            )
        for path in matched:
            try:
                document = tomllib.loads(
                    git_blob(repository_root, revision, path).decode("utf-8")
                )
            except (UnicodeDecodeError, ValueError, tomllib.TOMLDecodeError) as error:
                findings.append(Finding("UV_WORKSPACE_INVALID", path, str(error)))
                continue
            project_path = path.removesuffix("/pyproject.toml")
            if all(existing_path != project_path for existing_path, _ in projects):
                projects.append((project_path, document))
    return projects, findings


def _lock_findings(
    lock_text: str, projects: list[tuple[str, Mapping[str, Any]]]
) -> list[Finding]:
    try:
        lock = tomllib.loads(lock_text)
    except tomllib.TOMLDecodeError as error:
        return [Finding("UV_LOCK_DIVERGENT", "uv.lock", str(error))]
    packages = lock.get("package")
    if not isinstance(lock.get("version"), int) or not isinstance(
        lock.get("revision"), int
    ) or not isinstance(packages, list):
        return [
            Finding(
                "UV_LOCK_DIVERGENT",
                "uv.lock",
                "lock metadata and package inventory are required",
            )
        ]
    findings: list[Finding] = []
    for project_path, document in projects:
        project = document.get("project")
        if not isinstance(project, Mapping):
            continue
        name, version = project.get("name"), project.get("version")
        matches = [
            package
            for package in packages
            if isinstance(package, Mapping)
            and package.get("name") == name
            and package.get("version") == version
        ]
        expected_source = "." if project_path == "." else project_path
        matches = [
            package
            for package in matches
            if isinstance(package.get("source"), Mapping)
            and expected_source
            in {
                package["source"].get("virtual"),
                package["source"].get("editable"),
            }
        ]
        if len(matches) != 1:
            findings.append(
                Finding(
                    "UV_LOCK_DIVERGENT",
                    project_path,
                    "workspace project identity is absent or ambiguous in uv.lock",
                )
            )
            continue
        declared = _dependency_names(project.get("dependencies", []))
        locked = _locked_dependency_names(matches[0].get("dependencies", []))
        if declared != locked:
            findings.append(
                Finding(
                    "UV_LOCK_DIVERGENT",
                    project_path,
                    "direct dependency inventory differs from uv.lock",
                )
            )
    return findings


def _dependency_names(value: object) -> set[str]:
    if not isinstance(value, list):
        return set()
    names: set[str] = set()
    for dependency in value:
        if isinstance(dependency, str) and (
            match := re.match(r"[A-Za-z0-9][A-Za-z0-9._-]*", dependency)
        ):
            names.add(_normalized_name(match.group(0)))
    return names


def _locked_dependency_names(value: object) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {
        _normalized_name(str(item["name"]))
        for item in value
        if isinstance(item, Mapping) and isinstance(item.get("name"), str)
    }


def _normalized_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def _uv_command_findings(surfaces: list[str]) -> list[Finding]:
    commands = [
        match.group(0)
        for surface in surfaces
        for line in executable_shell_lines(surface)
        for match in re.finditer(r"uv\s+sync\b[^;&|]*", line)
    ]
    if not commands:
        return [Finding("UV_SYNC_COMMAND_INVALID", "repository", "uv sync is absent")]
    findings: list[Finding] = []
    if any("--frozen" not in command.split() for command in commands):
        findings.append(Finding("UV_NOT_FROZEN", "repository", "every uv sync must be frozen"))
    forbidden = {"--upgrade", "--refresh", "--reinstall"}
    if any(forbidden & set(command.split()) for command in commands):
        findings.append(Finding("UV_IMPLICIT_LOCK_UPDATE", "repository", "lock-changing option found"))
    return findings
