"""Fail-closed mutations of attributable, previously executed Stage A evidence."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest
from tools.governance.delivery_gates.acceptance import validate_checks
from tools.governance.delivery_gates.environmental import REASON, SOURCE
from tools.governance.delivery_gates.model import REGISTRY, SCHEMA, GateError, validate_schema
from tools.governance.delivery_gates.repository import GitRepository, WorkingRepository

from .fixture import ROOT, commit, git, write


def evaluate(tmp_path: Path, mutation: str = "valid") -> None:
    root = tmp_path / "environmental"
    root.mkdir()
    git(root, "init", "--quiet", "-b", "main")
    git(root, "config", "core.longpaths", "true")
    git(root, "config", "core.autocrlf", "false")
    git(root, "config", "user.name", "environmental evidence test")
    git(root, "config", "user.email", "test@test.invalid")
    original = (ROOT / SOURCE).read_bytes()
    changes = {
        "frontend": (b"Tests  17 passed (17)", b"Tests  16 passed, 1 FAILED"),
        "openapi": (b"OpenAPI check: PASS", b"OpenAPI check: FAIL"),
        "license": (b'"decision": "PASS"', b'"decision": "FAIL"'),
        "repository": (b"VALIDATION PASS", b"VALIDATION FAIL"),
        "code": (b"All checks passed!", b"Traceback: code failure"),
        "no-command": (b"COMMAND = make verify", b"COMMAND = echo verify"),
        "extra-failure": (b"1 failed, 5 passed", b"2 failed, 4 passed"),
        "missing-success": (b"OpenAPI diff: PASS", b"OpenAPI diff: no result"),
    }
    log = original.replace(*changes[mutation]) if mutation in changes else original
    destination = root / SOURCE
    destination.parent.mkdir(parents=True)
    destination.write_bytes(log)
    (root / "Makefile").write_bytes((ROOT / "Makefile").read_bytes())
    candidate = commit(root, "test: attributable candidate log mutation")
    prefix = f"evidence/delivery-gates/DG-TASK-0738-A/{candidate}"
    log_ref = write(root, prefix + "/log.json", {})
    (root / log_ref["path"]).write_bytes(log)
    from tools.governance.delivery_gates.model import sha256

    log_ref["sha256"] = sha256(log)
    evidence = {
        "candidate_sha": candidate,
        "command": ["make", "verify", "PYTHON=.venv/Scripts/python.exe", "PNPM=pnpm.cmd"],
        "raw_exit_code": 2,
        "log": log_ref,
    }
    if mutation == "evidence-exit":
        evidence["raw_exit_code"] = 1
    if mutation == "candidate":
        evidence["candidate_sha"] = "0" * 40
    gate = copy.deepcopy(WorkingRepository(ROOT).json(REGISTRY)["gates"][0])
    checks = []
    for check in gate["acceptance_checks"]:
        ref = write(root, prefix + "/" + check["check_id"] + ".json", evidence)
        checks.append({**check, **ref, "result": "PASS"})
    selected = next(check for check in checks if check["check_id"] == "make-verify")
    selected.update(
        result="NONBLOCKING", classification="ENVIRONMENTAL", reason_code=REASON, raw_exit_code=2
    )
    fields = {"reason": "reason_code", "classification-missing": "classification"}
    if mutation == "reason":
        selected[fields[mutation]] = "UNRECOGNIZED"
    if mutation == "classification-missing":
        del selected[fields[mutation]]
    if mutation == "classification":
        selected["classification"] = "FUNCTIONAL"
    if mutation == "exit":
        selected["raw_exit_code"] = 1
    if mutation == "other-check":
        other = checks[0]
        other.update(
            {
                key: selected[key]
                for key in ("result", "classification", "reason_code", "raw_exit_code")
            }
        )
    if mutation == "unknown-check":
        selected["check_id"] = "unknown"
    if mutation == "other-gate":
        gate["gate_id"] = "DG-TASK-0738-B"
    if mutation == "empty":
        (root / selected["path"]).write_bytes(b"")
        selected["sha256"] = sha256(b"")
    if mutation == "missing":
        (root / selected["path"]).unlink()
    if mutation in {"PASS", "FAIL"}:
        for key in ("classification", "raw_exit_code", "reason_code"):
            del selected[key]
        selected["result"] = mutation
    commit(root, "test: acceptance evidence mutation")
    schema = WorkingRepository(ROOT).json(SCHEMA)
    for check in checks:
        validate_schema(check, schema, "CheckEvidence")
    repository = GitRepository(root, git(root, "rev-parse", "HEAD"))
    validate_checks(repository, gate, {"candidate_sha": candidate, "checks": checks}, prefix)


@pytest.mark.parametrize("mutation", ["PASS", "valid"])
def test_valid_results(tmp_path: Path, mutation: str) -> None:
    evaluate(tmp_path, mutation)


@pytest.mark.parametrize(
    "mutation",
    [
        "FAIL",
        "missing",
        "empty",
        "other-check",
        "unknown-check",
        "other-gate",
        "frontend",
        "openapi",
        "license",
        "repository",
        "code",
        "reason",
        "classification-missing",
        "classification",
        "exit",
        "evidence-exit",
        "candidate",
        "no-command",
        "extra-failure",
        "missing-success",
    ],
)
def test_environmental_fail_closed(tmp_path: Path, mutation: str) -> None:
    with pytest.raises(GateError):
        evaluate(tmp_path, mutation)
