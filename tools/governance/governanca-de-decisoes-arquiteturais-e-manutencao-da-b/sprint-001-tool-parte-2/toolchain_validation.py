from __future__ import annotations

import re
from pathlib import Path

from repository_surfaces import (
    WORKFLOW_PREFIX,
    executable_shell_lines,
    make_recipes,
    make_targets,
    revision_paths,
    workflow_commands,
    workflow_paths,
)
from runtime_validation import RUNTIME_GATES, validate_python_runtime
from slice_one import Finding, git_blob
from uv_validation import validate_uv_lock_baseline


SHELL_COMMAND_BOUNDARY = r"(?:^|&&|\|\||[;|&\n])\s*"
BYPASS_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_.-])(?:"
    r"(?:python(?:3)?\s+-m\s+)?(?:pytest|ruff|mypy)\b|"
    r"python(?:3)?\s+tools/validate_repository\.py\b)",
    re.MULTILINE,
)
MAKE_INVOCATION_PATTERN = re.compile(
    SHELL_COMMAND_BOUNDARY + r"make\s+([A-Za-z0-9][A-Za-z0-9_-]*)(?:\s|$)",
    re.MULTILINE,
)
REQUIRED_CI_TARGETS = frozenset({"verify"})
SUBSTANTIVE_COMMAND_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_.-])(?:"
    r"(?:python(?:3)?\s+-m\s+)?(?:pytest|ruff|mypy)\b|"
    r"python(?:3)?\s+tools/[A-Za-z0-9_./-]+\.py\b|"
    r"uv\s+(?:sync|run)\b)"
)
DELEGATED_MAKE_PATTERN = re.compile(
    r"(?:\$\(MAKE\)|make)\s+([A-Za-z0-9][A-Za-z0-9_-]*)\b"
)


def validate_make_ci_parity(
    repository_root: Path, source_revision: str
) -> list[Finding]:
    findings: list[Finding] = []
    try:
        paths = revision_paths(repository_root, source_revision)
        make_text = git_blob(repository_root, source_revision, "Makefile").decode(
            "utf-8"
        )
    except (UnicodeDecodeError, ValueError) as error:
        findings.append(Finding("MAKE_FACADE_INVALID", "Makefile", str(error)))
        return sorted(findings)
    targets = make_targets(make_text)
    recipes = make_recipes(make_text)
    governed_workflows = workflow_paths(paths)
    if not targets:
        findings.append(Finding("MAKE_FACADE_INVALID", "Makefile", "no targets found"))
    if not governed_workflows:
        findings.append(
            Finding("CI_WORKFLOW_INVALID", WORKFLOW_PREFIX, "no governed workflows found")
        )
    commands, command_findings = workflow_commands(
        repository_root, source_revision, paths
    )
    findings.extend(command_findings)
    executable_commands = [
        line for command in commands for line in executable_shell_lines(command)
    ]
    invoked = {
        match.group(1)
        for command in executable_commands
        for match in MAKE_INVOCATION_PATTERN.finditer(command)
    }
    for target in sorted(REQUIRED_CI_TARGETS - invoked):
        findings.append(
            Finding(
                "MAKE_CI_DIVERGENT",
                target,
                "CI does not invoke the normative Make façade",
            )
        )
    for target in sorted(invoked - set(targets)):
        findings.append(
            Finding("MAKE_TARGET_MISSING", target, "CI invokes an absent Make target")
        )
    for target in sorted(invoked & set(targets)):
        if not _substantive_target(target, recipes, set()):
            findings.append(
                Finding(
                    "MAKE_TARGET_NOT_SUBSTANTIVE",
                    target,
                    "CI target has no governed executable command",
                )
            )
    if any(BYPASS_PATTERN.search(command) for command in executable_commands):
        findings.append(
            Finding(
                "MAKE_CI_BYPASS",
                "$.workflow_paths",
                "direct quality command bypasses Make",
            )
        )
    return sorted(findings)


def _substantive_target(
    target: str,
    recipes: dict[str, tuple[str, ...]],
    visited: set[str],
) -> bool:
    if target in visited:
        return False
    visited.add(target)
    commands = [
        line
        for recipe in recipes.get(target, ())
        for line in executable_shell_lines(recipe)
    ]
    if any(SUBSTANTIVE_COMMAND_PATTERN.search(command) for command in commands):
        return True
    delegated = {
        match.group(1)
        for command in commands
        for match in DELEGATED_MAKE_PATTERN.finditer(command)
    }
    return any(_substantive_target(item, recipes, visited) for item in delegated)
