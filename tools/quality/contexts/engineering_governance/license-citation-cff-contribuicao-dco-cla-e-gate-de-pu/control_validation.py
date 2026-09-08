from __future__ import annotations

import ast
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from jsonschema.exceptions import SchemaError  # type: ignore[import-untyped]

SLUG = "license-citation-cff-contribuicao-dco-cla-e-gate-de-pu"
TASK_REL = Path(".codex/tasks/TASK-0033.json")
TASK_SCHEMA_REL = Path(".codex/tasks/TASK_ENVELOPE.schema.json")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
TEST_REL = Path(f"tests/fnd/{SLUG}/test_automation.py")
QUALITY_REL = Path(f"tools/quality/contexts/engineering_governance/{SLUG}")
FOUNDATION_VALIDATOR_REL = Path(f"tools/governance/{SLUG}/foundation_validation.py")
CONTRACT_ROOT_REL = Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}")
CONTRACT_SCHEMA_REL = CONTRACT_ROOT_REL / "license-publication-governance.schema.json"
CONTRACT_EXAMPLE_REL = CONTRACT_ROOT_REL / "examples/license-publication-governance.json"

EXPECTED_REQUIREMENTS = ["REQ-CIT-001", "REQ-EPIC-042", "REQ-OSS-001", "REQ-PUB-002"]
EXPECTED_ACCEPTANCE_IDS = [f"AC-ISSUE-0143-{index:02d}" for index in range(1, 5)]
EXPECTED_ALLOW_PATHS = [
    TASK_REL.as_posix(),
    f"tests/fnd/{SLUG}/**",
    f"tools/quality/contexts/engineering_governance/{SLUG}/**",
    WORKFLOW_REL.as_posix(),
    "evidence/operations/epic-007/story-0033/**",
]
EXPECTED_DENY_PATHS = ["src/geo/**", "src/ai/**", "src/**/epic-*", "src/**/issue-*"]
EXPECTED_BLOCKERS = [
    "DCO_AUTOMATED_CHECK",
    "DEPENDENCY_INVENTORY_AND_SBOM",
    "LEGAL_REVIEW_BEFORE_G6",
    "SECURITY_LICENSE_RESTORE_COMPATIBILITY_SCIENTIFIC_GATES",
]
CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_PYTHON_SHA = "5fda3b95a4ea91299a34e894583c3862153e4b97"


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    artifact: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"artifact": self.artifact, "code": self.code, "detail": self.detail}


def _finding(code: str, artifact: Path, detail: str) -> Finding:
    return Finding(code=code, artifact=artifact.as_posix(), detail=detail)


def _load_json(root: Path, relative: Path, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return json.loads((root / relative).read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [_finding(code, relative, str(error))]


def _load_yaml(root: Path, relative: Path, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return yaml.safe_load((root / relative).read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return None, [_finding(code, relative, str(error))]


def _schema_findings(
    instance: object, schema: object, artifact: Path, code: str
) -> list[Finding]:
    if not isinstance(schema, dict):
        return [_finding(code, artifact, "schema object required")]
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        return [_finding(code, artifact, error.message)]
    return [
        _finding(code, artifact, f"{error.json_path}: {error.message}")
        for error in Draft202012Validator(schema).iter_errors(instance)
    ]


def _contract_findings(root: Path) -> list[Finding]:
    schema, findings = _load_json(root, CONTRACT_SCHEMA_REL, "CONTRACT_UNREADABLE")
    contract, errors = _load_json(root, CONTRACT_EXAMPLE_REL, "CONTRACT_UNREADABLE")
    findings.extend(errors)
    if schema is not None and contract is not None:
        findings.extend(
            _schema_findings(contract, schema, CONTRACT_EXAMPLE_REL, "CONTRACT_SCHEMA_INVALID")
        )
    if not isinstance(contract, dict):
        return findings
    failure = contract.get("failure_policy")
    publication = contract.get("publication_gate")
    contribution = contract.get("contribution_policy")
    valid = (
        contract.get("requirement_ids") == EXPECTED_REQUIREMENTS
        and isinstance(failure, dict)
        and failure.get("mode") == "FAIL_CLOSED"
        and failure.get("silent_fallback") is False
        and isinstance(publication, dict)
        and publication.get("decision") == "BLOCK_UNLESS_ALL_APPLICABLE_EVIDENCE_PASSES"
        and isinstance(contribution, dict)
        and contribution.get("origin_certification") == "DCO-1.1"
        and contribution.get("cla") == "NOT_REQUIRED_INITIAL_BASELINE"
    )
    if not valid:
        findings.append(
            _finding("CONTRACT_POLICY_INVALID", CONTRACT_EXAMPLE_REL, "frozen policy drift")
        )
    return findings


def _defined_tests(root: Path) -> tuple[set[str], list[Finding]]:
    try:
        source = (root / TEST_REL).read_text(encoding="utf-8")
        tree = ast.parse(source, TEST_REL.as_posix())
    except (OSError, UnicodeError, SyntaxError) as error:
        return set(), [_finding("TEST_SOURCE_INVALID", TEST_REL, str(error))]
    names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    return names, []


def _task_findings(root: Path) -> list[Finding]:
    task, findings = _load_json(root, TASK_REL, "TASK_UNREADABLE")
    schema, errors = _load_json(root, TASK_SCHEMA_REL, "TASK_SCHEMA_UNREADABLE")
    findings.extend(errors)
    if task is not None and schema is not None:
        findings.extend(_schema_findings(task, schema, TASK_REL, "TASK_SCHEMA_INVALID"))
    if not isinstance(task, dict):
        return findings
    expected = {
        "task_id": "TASK-0033",
        "issue_id": "ISSUE-0143",
        "story_id": "STORY-0033",
        "epic_id": "EPIC-007",
        "role": "DevOps",
        "dependencies": ["STORY-0031"],
        "tests": ["test_epic_007_automacao"],
        "acceptance_criterion_ids": EXPECTED_ACCEPTANCE_IDS,
        "allow_paths": EXPECTED_ALLOW_PATHS,
        "deny_paths": EXPECTED_DENY_PATHS,
    }
    if any(task.get(key) != value for key, value in expected.items()):
        findings.append(
            _finding("TASK_CONTROL_INVALID", TASK_REL, "identity, test, AC, or scope drift")
        )
    phase_f = task.get("phase_f_review")
    files = phase_f.get("files") if isinstance(phase_f, dict) else None
    scopes_match = (
        isinstance(files, dict)
        and files.get("allow_paths") == task.get("allow_paths")
        and files.get("deny_paths") == task.get("deny_paths")
    )
    if not scopes_match:
        findings.append(_finding("TASK_SCOPE_DRIFT", TASK_REL, "Phase F allow_paths differ"))
    review = phase_f.get("review") if isinstance(phase_f, dict) else None
    if not isinstance(review, dict) or review.get("required_roles") != ["QA", "Reviewer"]:
        findings.append(_finding("TASK_REVIEW_INVALID", TASK_REL, "independent review drift"))
    tests, test_errors = _defined_tests(root)
    findings.extend(test_errors)
    if "test_epic_007_automacao" not in tests:
        findings.append(_finding("REQUIRED_TEST_MISSING", TEST_REL, "test_epic_007_automacao"))
    return findings


def _foundation_command(root: Path, *arguments: str) -> subprocess.CompletedProcess[str] | None:
    command = [sys.executable, "-B", "-X", "utf8", str(root / FOUNDATION_VALIDATOR_REL)]
    try:
        return subprocess.run(
            [*command, *arguments],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def _command_report(completed: subprocess.CompletedProcess[str]) -> dict[str, Any] | None:
    output = completed.stdout if completed.stdout.strip() else completed.stderr
    try:
        report = json.loads(output)
    except json.JSONDecodeError:
        return None
    return report if isinstance(report, dict) else None


def _foundation_findings(root: Path, external_commit_range: str | None) -> list[Finding]:
    arguments = (
        ("--commit-range", external_commit_range)
        if external_commit_range is not None
        else ()
    )
    completed = _foundation_command(root, *arguments)
    if completed is None:
        return [
            _finding("FOUNDATION_EXECUTION_FAILED", FOUNDATION_VALIDATOR_REL, "execution failed")
        ]
    report = _command_report(completed)
    if completed.returncode != 0 or report is None or report.get("decision") != "PASS":
        detail = report.get("error") if isinstance(report, dict) else "invalid validator output"
        code = (
            "DCO_VALIDATION_FAILED"
            if external_commit_range is not None
            else "FOUNDATION_VALIDATION_FAILED"
        )
        return [_finding(code, FOUNDATION_VALIDATOR_REL, str(detail))]

    gated = _foundation_command(root, "--publication-gate")
    gated_report = _command_report(gated) if gated is not None else None
    valid_gate = (
        gated is not None
        and gated.returncode == 1
        and isinstance(gated_report, dict)
        and gated_report.get("decision") == "BLOCKED"
        and isinstance(gated_report.get("publication_gate"), dict)
        and gated_report["publication_gate"].get("blockers") == EXPECTED_BLOCKERS
    )
    if not valid_gate:
        return [
            _finding(
                "PUBLICATION_GATE_INVALID",
                FOUNDATION_VALIDATOR_REL,
                "gate must fail closed with the frozen incomplete-evidence blockers",
            )
        ]
    return []


def _workflow_findings(root: Path) -> list[Finding]:
    workflow, findings = _load_yaml(root, WORKFLOW_REL, "WORKFLOW_UNREADABLE")
    if not isinstance(workflow, dict):
        return findings
    jobs = workflow.get("jobs")
    job_values = jobs.values() if isinstance(jobs, dict) else []
    steps = [
        step
        for job in job_values
        if isinstance(job, dict)
        for step in job.get("steps", [])
        if isinstance(step, dict)
    ]
    uses = [step["uses"] for step in steps if isinstance(step.get("uses"), str)]
    commands = [step["run"] for step in steps if isinstance(step.get("run"), str)]
    checkout = next(
        (
            step
            for step in steps
            if str(step.get("uses", "")).startswith("actions/checkout@")
        ),
        {},
    )
    dco_steps = [step for step in steps if "--external-commit-range" in str(step.get("run", ""))]
    dco_valid = any(
        "$BASE_SHA..$HEAD_SHA" in str(step.get("run"))
        and "pull_request" in str(step.get("if", ""))
        and "fork" in str(step.get("if", ""))
        and step.get("env")
        == {
            "BASE_SHA": "${{ github.event.pull_request.base.sha }}",
            "HEAD_SHA": "${{ github.event.pull_request.head.sha }}",
        }
        for step in dco_steps
    )
    text = (root / WORKFLOW_REL).read_text(encoding="utf-8")
    checks = {
        "read-only permissions": workflow.get("permissions") == {"contents": "read"},
        "pinned checkout": f"actions/checkout@{CHECKOUT_SHA}" in uses,
        "full commit history": checkout.get("with", {}).get("fetch-depth") == 0,
        "pinned Python": f"actions/setup-python@{SETUP_PYTHON_SHA}" in uses,
        "Python 3.12.13": "python-version: '3.12.13'" in text,
        "validator dry-run": any(
            (QUALITY_REL / "validator.py").as_posix() in command and "--dry-run" in command
            for command in commands
        ),
        "external DCO range": dco_valid,
        "focused acceptance test": any(
            TEST_REL.as_posix() in command and "test_epic_007_automacao" in command
            for command in commands
        ),
        "fail closed": "continue-on-error: true" not in text,
        "no expression in shell": all("${{" not in command for command in commands),
        "no privileged PR trigger": "pull_request_target:" not in text,
    }
    findings.extend(
        _finding("WORKFLOW_INVALID", WORKFLOW_REL, f"missing {name}")
        for name, passed in checks.items()
        if not passed
    )
    return findings


def validate(root: Path, *, external_commit_range: str | None = None) -> list[Finding]:
    resolved = root.resolve()
    findings = _contract_findings(resolved)
    findings.extend(_task_findings(resolved))
    findings.extend(_workflow_findings(resolved))
    findings.extend(_foundation_findings(resolved, external_commit_range))
    return sorted(set(findings))
