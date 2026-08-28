from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from validation_types import Finding


FOUNDATION_REL = Path(
    "docs/03-engineering/contexts/engineering_governance/"
    "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/foundation-plan.json"
)
CONTRACT_ROOT_REL = Path(
    "contracts/contexts/engineering_governance/fnd/"
    "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r"
)
CONTRACT_REL = CONTRACT_ROOT_REL / "examples/monorepo-foundation.json"
CONTRACT_SCHEMA_REL = CONTRACT_ROOT_REL / "monorepo-foundation.schema.json"
TASK_REL = Path(".codex/tasks/TASK-0013.json")
TASK_SCHEMA_REL = Path(".codex/tasks/TASK_ENVELOPE.schema.json")
FOUNDATION_TEST_REL = Path(
    "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_foundation.py"
)
CONTRACT_TEST_REL = FOUNDATION_TEST_REL.with_name("test_foundation_contract.py")
FOUNDATION_VALIDATOR_REL = Path(
    "tools/governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/"
    "foundation_validation.py"
)
WORKFLOW_REL = Path(
    ".github/workflows/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r.yaml"
)
AUTOMATION_TEST_REL = FOUNDATION_TEST_REL.with_name("test_automation.py")

REQUIREMENT_TESTS = {
    "REQ-DEL-001": (
        FOUNDATION_TEST_REL,
        "test_walking_skeleton_end_to_end_and_vertical_slice_definition_of_done",
    ),
    "REQ-DEV-001": (
        FOUNDATION_TEST_REL,
        "test_host_container_ci_contract_and_no_implicit_downloads",
    ),
    "REQ-TOP-001": (CONTRACT_TEST_REL, "test_cli_api_semantic_contract"),
}
ACCEPTANCE_EVIDENCE = {
    f"AC-ISSUE-0123-{index:02d}": "test_epic_003_automacao" for index in range(1, 5)
}
EXPECTED_ALLOW_PATHS = [
    "tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**",
    (
        "tools/quality/contexts/engineering_governance/"
        "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**"
    ),
    ".github/workflows/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r.yaml",
]


def _finding(code: str, artifact: Path, detail: str) -> Finding:
    return Finding(code, artifact.as_posix(), detail)


def _load_json(root: Path, relative: Path, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return json.loads((root / relative).read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [_finding(code, relative, str(error))]


def _schema_findings(
    document: object,
    schema: object,
    artifact: Path,
    code: str,
) -> list[Finding]:
    if not isinstance(schema, dict):
        return [_finding("SCHEMA_INVALID", artifact, "schema must be a JSON object")]
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        return [_finding("SCHEMA_INVALID", artifact, error.message)]
    return [
        _finding(code, artifact, f"{error.json_path}: {error.message}")
        for error in Draft202012Validator(schema).iter_errors(document)
    ]


def _foundation_findings(root: Path) -> list[Finding]:
    if not (root / FOUNDATION_VALIDATOR_REL).is_file():
        detail = "mandatory foundation validator is missing"
        return [_finding("FOUNDATION_VALIDATOR_MISSING", FOUNDATION_VALIDATOR_REL, detail)]
    if any(not (root / relative).is_file() for relative in (FOUNDATION_REL, CONTRACT_REL)):
        return []
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(root / FOUNDATION_VALIDATOR_REL),
            "--foundation",
            str(root / FOUNDATION_REL),
            "--contract",
            str(root / CONTRACT_REL),
        ],
        cwd=root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError:
        detail = completed.stderr.strip() or completed.stdout.strip() or "no diagnostic output"
        return [_finding("FOUNDATION_VALIDATOR_FAILED", FOUNDATION_VALIDATOR_REL, detail)]
    if not isinstance(report, dict):
        return [_finding("FOUNDATION_VALIDATOR_FAILED", FOUNDATION_VALIDATOR_REL, str(report))]
    findings = report.get("findings")
    if completed.returncode == 0 and report.get("status") == "PASS" and findings == []:
        return []
    if not isinstance(findings, list):
        return [_finding("FOUNDATION_VALIDATOR_FAILED", FOUNDATION_VALIDATOR_REL, str(report))]
    if not findings:
        return [
            _finding(
                "FOUNDATION_VALIDATOR_FAILED",
                FOUNDATION_VALIDATOR_REL,
                f"exit={completed.returncode} status={report.get('status')!r}",
            )
        ]
    return [
        Finding(
            str(item.get("code", "FOUNDATION_VALIDATION_FAILED")),
            FOUNDATION_REL.as_posix(),
            f"{item.get('field', '$')}: {item.get('detail', 'validation failed')}",
        )
        for item in findings
        if isinstance(item, dict)
    ]


def _defined_functions(root: Path, relative: Path) -> tuple[set[str], list[Finding]]:
    try:
        source = (root / relative).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=relative.as_posix())
    except (OSError, UnicodeError, SyntaxError) as error:
        return set(), [_finding("TEST_SOURCE_INVALID", relative, str(error))]
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }, []


def _evidence_findings(root: Path, plan: object, contract: object) -> list[Finding]:
    findings: list[Finding] = []
    raw_plan_evidence = plan.get("requirement_evidence") if isinstance(plan, dict) else None
    raw_contract_requirements = (
        contract.get("requirement_ids") if isinstance(contract, dict) else None
    )
    plan_evidence = raw_plan_evidence if isinstance(raw_plan_evidence, dict) else {}
    contract_requirements = (
        raw_contract_requirements if isinstance(raw_contract_requirements, list) else []
    )
    declared = set(plan_evidence) | set(contract_requirements)
    expected = set(REQUIREMENT_TESTS)
    if declared != expected:
        findings.append(
            _finding(
                "REQUIREMENT_EVIDENCE_INVALID",
                FOUNDATION_REL,
                f"expected requirement evidence {sorted(expected)!r}, found {sorted(declared)!r}",
            )
        )
    for requirement, (relative, function_name) in REQUIREMENT_TESTS.items():
        functions, source_findings = _defined_functions(root, relative)
        findings.extend(source_findings)
        if function_name not in functions:
            findings.append(
                _finding(
                    "REQUIREMENT_TEST_MISSING",
                    relative,
                    f"{requirement} requires {function_name}",
                )
            )
    return findings


def _task_findings(task: object) -> list[Finding]:
    if not isinstance(task, dict):
        return [_finding("TASK_CONTROL_INVALID", TASK_REL, "TaskEnvelope must be an object")]
    expected = {
        "task_id": "TASK-0013",
        "issue_id": "ISSUE-0123",
        "story_id": "STORY-0013",
        "epic_id": "EPIC-003",
        "role": "DevOps",
        "acceptance_criterion_ids": list(ACCEPTANCE_EVIDENCE),
        "tests": ["test_epic_003_automacao"],
        "allow_paths": EXPECTED_ALLOW_PATHS,
    }
    findings = [
        _finding("TASK_CONTROL_INVALID", TASK_REL, f"{field}: expected {value!r}")
        for field, value in expected.items()
        if task.get(field) != value
    ]
    phase_review = task.get("phase_f_review")
    phase_files = phase_review.get("files") if isinstance(phase_review, dict) else None
    scope_matches = isinstance(phase_files, dict) and phase_files.get(
        "allow_paths"
    ) == task.get("allow_paths")
    if not scope_matches:
        findings.append(
            _finding(
                "TASK_SCOPE_DRIFT",
                TASK_REL,
                "allow_paths must match phase_f_review.files.allow_paths",
            )
        )
    return findings


def _workflow_findings(root: Path) -> list[Finding]:
    try:
        workflow_text = (root / WORKFLOW_REL).read_text(encoding="utf-8")
        workflow = yaml.safe_load(workflow_text)
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return [_finding("WORKFLOW_INVALID", WORKFLOW_REL, str(error))]
    if not isinstance(workflow, dict):
        return [_finding("WORKFLOW_INVALID", WORKFLOW_REL, "workflow must be an object")]
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        return [_finding("WORKFLOW_INVALID", WORKFLOW_REL, "jobs must be an object")]
    commands: list[str] = []
    for job in jobs.values():
        if not isinstance(job, dict) or not isinstance(job.get("steps"), list):
            return [_finding("WORKFLOW_INVALID", WORKFLOW_REL, "each job requires steps")]
        commands.extend(
            step["run"]
            for step in job["steps"]
            if isinstance(step, dict) and isinstance(step.get("run"), str)
        )
    checks = {
        "validator dry-run": any(
            "tools/quality/contexts/engineering_governance/"
            "monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/validator.py" in command
            and "--dry-run" in command
            for command in commands
        ),
        "focused acceptance test": any(
            AUTOMATION_TEST_REL.as_posix() in command
            and "test_epic_003_automacao" in command
            for command in commands
        ),
        "pinned Python": "python-version: '3.12.13'" in workflow_text,
        "read-only permissions": "contents: read" in workflow_text,
    }
    return [
        _finding("WORKFLOW_INVALID", WORKFLOW_REL, f"missing {name}")
        for name, passed in checks.items()
        if not passed
    ]


def validate_repository(root: Path) -> list[Finding]:
    resolved = root.resolve()
    plan, findings = _load_json(resolved, FOUNDATION_REL, "FOUNDATION_UNREADABLE")
    contract, contract_findings = _load_json(resolved, CONTRACT_REL, "CONTRACT_UNREADABLE")
    contract_schema, schema_findings = _load_json(
        resolved, CONTRACT_SCHEMA_REL, "CONTRACT_SCHEMA_UNREADABLE"
    )
    task, task_findings = _load_json(resolved, TASK_REL, "TASK_UNREADABLE")
    task_schema, task_schema_findings = _load_json(
        resolved, TASK_SCHEMA_REL, "TASK_SCHEMA_UNREADABLE"
    )
    findings.extend(contract_findings + schema_findings + task_findings + task_schema_findings)
    if contract is not None and contract_schema is not None:
        findings.extend(
            _schema_findings(contract, contract_schema, CONTRACT_REL, "CONTRACT_SCHEMA_INVALID")
        )
    if task is not None and task_schema is not None:
        findings.extend(_schema_findings(task, task_schema, TASK_REL, "TASK_SCHEMA_INVALID"))
        findings.extend(_task_findings(task))
    if plan is not None and contract is not None:
        findings.extend(_evidence_findings(resolved, plan, contract))
    findings.extend(_foundation_findings(resolved))
    findings.extend(_workflow_findings(resolved))
    return sorted(set(findings))
