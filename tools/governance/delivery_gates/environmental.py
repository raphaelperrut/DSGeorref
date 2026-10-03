"""Narrow Stage A evaluator for immutable make-verify environmental evidence."""

from __future__ import annotations

import re
from typing import Any

from .model import parse, relative_path, require, sha256
from .repository import GitRepository

REASON = "FOUNDATION_INTEGRATION_SERVICES_UNAVAILABLE"
SOURCE = (
    "evidence/implementation/react-typescript-vite-design-system-cliente-openap/"
    "requirements-epic-fs1-run-parte-1/stage-a-license-review/make-verify.log"
)
FOUNDATION = "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_foundation.py"
FAILED_TEST = "test_walking_skeleton_end_to_end_and_vertical_slice_definition_of_done"


SUCCESS_MARKERS = (
    "All checks passed!",
    "Success: no issues found",
    "OpenAPI check: PASS",
    "OpenAPI diff: PASS",
    "Tests  17 passed (17)",
    "1 passed (1.9s)",
    "building client environment for production",
    "built in",
    "test:smoke",
    "1 passed (4.3s)",
    "55 passed",
    "VALIDATION PASS",
    '"status": "PASS"',
    "REQUIREMENTS REVIEW VALIDATION PASS",
    "DOMAIN DRIVEN DESIGN REVIEW PASS",
    '"open_architectural_decisions": 0',
    "SPECIFICATION REVIEW PASS",
    "SPRINT REVIEW PASS",
    "PYTHON ARCHITECTURE PASS",
    '"decision": "PASS"',
    "49 passed",
    '"findings": []',
)


def validate_log(content: bytes) -> None:
    """Require every preceding recipe, success markers, and only the known stop."""
    log = "\n".join(content.decode("utf-8").splitlines())
    require(log.startswith("COMMAND = make verify "), "make verify was not executed")
    boundary = re.search(r"^.* -m pytest .* " + re.escape(FOUNDATION) + r"$", log, re.M)
    require(boundary is not None, "foundation execution missing")
    before, after = log[: boundary.start()], log[boundary.end() :]
    require(
        not re.search(r"\b(?:fail(?:ed|ures)?|errors?|traceback)\b", before, re.I),
        "Stage A failure before environmental gate",
    )
    position = 0
    for marker in SUCCESS_MARKERS:
        found = before.find(marker, position)
        require(found >= 0, f"preceding Stage A success missing: {marker}")
        position = found + len(marker)
    require(after.count("FAILED ") == 1, "additional foundation failures")
    require(after.count("E       AssertionError:") == 1, "unexpected foundation error")
    require(
        'assert os.environ.get("FOUNDATION_INTEGRATION") == "1"' in after
        and "FOUNDATION_INTEGRATION=1 and the pinned PostgreSQL/RabbitMQ services are required"
        in after
        and "FAILED " + FOUNDATION + "::" + FAILED_TEST in after
        and re.search(r"^1 failed, 5 passed in [0-9.]+s$", after, re.M) is not None
        and after.rstrip().endswith("EXIT_CODE = 2"),
        "incompatible environmental stop",
    )


def validate_recipes(makefile: bytes, log: bytes) -> None:
    """Require the actual candidate Makefile recipe sequence through the stop."""
    sections = {}
    variables = {"PYTHON": ".venv/Scripts/python.exe", "PNPM": "pnpm.cmd"}
    current = ""
    for line in makefile.decode("utf-8").splitlines():
        assignment = re.fullmatch(r"([A-Z_]+) := (.+)", line)
        if assignment:
            variables[assignment[1]] = assignment[2]
        elif line and not line[0].isspace() and ":" in line:
            current = line.split(":", 1)[0]
            sections[current] = []
        elif line.startswith("\t"):
            sections[current].append(line.strip())
    recipes = sections["python-quality"] + sections["frontend-quality"] + sections["verify"]
    position = 0
    normalized = "\n".join(log.decode("utf-8").splitlines())
    for recipe in recipes:
        command = recipe
        for name, value in variables.items():
            command = command.replace("$(" + name + ")", value)
        require("$(" not in command, "unresolved candidate make variable")
        found = normalized.find(command + "\n", position)
        require(found >= 0, f"preceding make recipe missing: {command}")
        position = found + len(command)
        if command.endswith(FOUNDATION):
            break


def validate_environmental(
    repository: GitRepository,
    gate: dict[str, Any],
    manifest: dict[str, Any],
    check: dict[str, Any],
    content: bytes,
    evidence_root: str,
) -> None:
    require(
        gate["gate_id"] == "DG-TASK-0738-A" and check["check_id"] == "make-verify",
        "NONBLOCKING is unauthorized for gate/check",
    )
    require(
        check.get("classification") == "ENVIRONMENTAL"
        and check.get("reason_code") == REASON
        and type(check.get("raw_exit_code")) is int
        and check["raw_exit_code"] == 2,
        "incompatible environmental classification/reason/exit",
    )
    evidence = parse(content)
    require(
        set(evidence) == {"candidate_sha", "command", "raw_exit_code", "log"},
        "invalid environmental evidence fields",
    )
    require(
        evidence["candidate_sha"] == manifest["candidate_sha"]
        and evidence["command"]
        == ["make", "verify", "PYTHON=.venv/Scripts/python.exe", "PNPM=pnpm.cmd"]
        and type(evidence["raw_exit_code"]) is int
        and evidence["raw_exit_code"] == 2,
        "environmental evidence candidate/command/exit mismatch",
    )
    reference = evidence["log"]
    require(
        isinstance(reference, dict) and set(reference) == {"path", "sha256"},
        "invalid environmental log reference",
    )
    path = relative_path(reference["path"])
    require(path.startswith(evidence_root + "/"), "environmental log outside candidate root")
    log = repository.read(path)
    require(sha256(log) == reference["sha256"], "environmental log digest mismatch")
    require(
        log == repository.read(SOURCE, manifest["candidate_sha"]),
        "environmental log is not immutable candidate evidence",
    )
    validate_recipes(repository.read("Makefile", manifest["candidate_sha"]), log)
    validate_log(log)
