from __future__ import annotations

import re
import subprocess
from collections.abc import Mapping
from pathlib import Path

import yaml

from slice_one import COMMIT_PATTERN, Finding, git_blob


WORKFLOW_PREFIX = ".github/workflows/"
ACTION_PREFIX = ".github/actions/"
WORKFLOW_SUFFIXES = (".yml", ".yaml")


def revision_paths(repository_root: Path, revision: str) -> tuple[str, ...]:
    if COMMIT_PATTERN.fullmatch(revision) is None:
        raise ValueError("one full lowercase Git commit SHA is required")
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(repository_root),
            "ls-tree",
            "-r",
            "--name-only",
            "-z",
            revision,
        ],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise ValueError("repository revision cannot be enumerated")
    return tuple(
        sorted(
            item.decode("utf-8")
            for item in completed.stdout.split(b"\0")
            if item
        )
    )


def python_capabilities(paths: tuple[str, ...]) -> tuple[str, ...]:
    capabilities = {
        parts[1]
        for path in paths
        if path.startswith("src/") and path.endswith(".py")
        and len(parts := path.split("/")) >= 3
    }
    return tuple(sorted(capabilities))


def workflow_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        path
        for path in paths
        if path.startswith(WORKFLOW_PREFIX) and path.endswith(WORKFLOW_SUFFIXES)
    )


def ci_command_surface_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        path
        for path in paths
        if path.endswith(WORKFLOW_SUFFIXES)
        and (
            path.startswith(WORKFLOW_PREFIX)
            or path.startswith(ACTION_PREFIX)
        )
    )


def make_targets(make_text: str) -> tuple[str, ...]:
    targets = {
        match.group(1)
        for match in re.finditer(r"(?m)^([A-Za-z0-9][A-Za-z0-9_-]*)\s*:", make_text)
    }
    return tuple(sorted(targets))


def make_recipes(make_text: str) -> dict[str, tuple[str, ...]]:
    recipes: dict[str, list[str]] = {}
    current: tuple[str, ...] = ()
    for line in make_text.splitlines():
        match = re.match(
            r"^([A-Za-z0-9][A-Za-z0-9_-]*(?:\s+[A-Za-z0-9][A-Za-z0-9_-]*)*)\s*:",
            line,
        )
        if match:
            current = tuple(match.group(1).split())
            for target in current:
                recipes.setdefault(target, [])
            continue
        if line.startswith("\t") and current:
            for target in current:
                recipes[target].append(line[1:])
        elif line and not line[0].isspace():
            current = ()
    return {target: tuple(lines) for target, lines in sorted(recipes.items())}


def executable_shell_lines(surface: str) -> tuple[str, ...]:
    joined = re.sub(r"\\\r?\n\s*", " ", surface)
    executable: list[str] = []
    for line in joined.splitlines():
        command = _strip_shell_comment(line).strip()
        if command:
            executable.append(command)
    return tuple(executable)


def _strip_shell_comment(line: str) -> str:
    single = False
    double = False
    escaped = False
    for index, character in enumerate(line):
        if escaped:
            escaped = False
            continue
        if character == "\\" and not single:
            escaped = True
        elif character == "'" and not double:
            single = not single
        elif character == '"' and not single:
            double = not double
        elif character == "#" and not single and not double:
            return line[:index]
    return line


def workflow_commands(
    repository_root: Path,
    revision: str,
    paths: tuple[str, ...],
) -> tuple[list[str], list[Finding]]:
    commands: list[str] = []
    findings: list[Finding] = []
    for path in ci_command_surface_paths(paths):
        try:
            text = git_blob(repository_root, revision, path).decode("utf-8")
            document = yaml.safe_load(text)
        except (UnicodeDecodeError, ValueError, yaml.YAMLError) as error:
            findings.append(Finding("CI_WORKFLOW_INVALID", path, str(error)))
            continue
        _collect_run_commands(document, path, commands, findings)
    return commands, findings


def _collect_run_commands(
    value: object,
    workflow_path: str,
    commands: list[str],
    findings: list[Finding],
) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key == "run":
                if isinstance(item, str):
                    commands.append(item)
                else:
                    findings.append(
                        Finding(
                            "CI_WORKFLOW_INVALID",
                            workflow_path,
                            "run value must be a string",
                        )
                    )
            else:
                _collect_run_commands(item, workflow_path, commands, findings)
    elif isinstance(value, list):
        for item in value:
            _collect_run_commands(item, workflow_path, commands, findings)
