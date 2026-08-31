from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from validation_types import Finding


SLUG = "openapi-cliente-typescript-e-contratos-cli-jobs-evento"
TASK_REL = Path(".codex/tasks/TASK-0018.json")
TASK_SCHEMA_REL = Path(".codex/tasks/TASK_ENVELOPE.schema.json")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
AUTOMATION_TEST_REL = Path(f"tests/fnd/{SLUG}/test_automation.py")
ACCEPTANCE_EVIDENCE = {
    f"AC-ISSUE-0128-{index:02d}": "test_epic_004_automacao" for index in range(1, 5)
}
EXPECTED_ALLOW_PATHS = [
    f"tests/fnd/{SLUG}/**",
    f"tools/quality/contexts/engineering_governance/{SLUG}/**",
    f".github/workflows/{SLUG}.yaml",
]


def _finding(code: str, artifact: Path, detail: str) -> Finding:
    return Finding(code, artifact.as_posix(), detail)


def _load_json(root: Path, relative: Path, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return json.loads((root / relative).read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [_finding(code, relative, str(error))]


def _task_findings(root: Path) -> list[Finding]:
    task, findings = _load_json(root, TASK_REL, "TASK_UNREADABLE")
    schema, schema_findings = _load_json(root, TASK_SCHEMA_REL, "TASK_SCHEMA_UNREADABLE")
    findings.extend(schema_findings)
    if isinstance(schema, dict) and task is not None:
        try:
            Draft202012Validator.check_schema(schema)
            findings.extend(
                _finding("TASK_SCHEMA_INVALID", TASK_REL, f"{error.json_path}: {error.message}")
                for error in Draft202012Validator(schema).iter_errors(task)
            )
        except SchemaError as error:
            findings.append(_finding("TASK_SCHEMA_INVALID", TASK_SCHEMA_REL, error.message))
    if not isinstance(task, dict):
        return findings
    expected = {
        "task_id": "TASK-0018",
        "issue_id": "ISSUE-0128",
        "story_id": "STORY-0018",
        "epic_id": "EPIC-004",
        "role": "DevOps",
        "dependencies": ["STORY-0016"],
        "tests": ["test_epic_004_automacao"],
        "acceptance_criterion_ids": list(ACCEPTANCE_EVIDENCE),
        "allow_paths": EXPECTED_ALLOW_PATHS,
    }
    if any(task.get(field) != value for field, value in expected.items()):
        findings.append(
            _finding(
                "TASK_CONTROL_INVALID",
                TASK_REL,
                "identity, dependency, test, AC, or scope drift",
            )
        )
    review = task.get("phase_f_review")
    files = review.get("files") if isinstance(review, dict) else None
    if not isinstance(files, dict) or files.get("allow_paths") != task.get("allow_paths"):
        findings.append(_finding("TASK_SCOPE_DRIFT", TASK_REL, "Phase F allow_paths differ"))
    return findings


def _workflow_findings(root: Path) -> list[Finding]:
    try:
        text = (root / WORKFLOW_REL).read_text(encoding="utf-8")
        workflow = yaml.safe_load(text)
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return [_finding("WORKFLOW_INVALID", WORKFLOW_REL, str(error))]
    jobs = workflow.get("jobs") if isinstance(workflow, dict) else None
    commands = [
        step["run"]
        for job in (jobs or {}).values()
        if isinstance(job, dict)
        for step in job.get("steps", [])
        if isinstance(step, dict) and isinstance(step.get("run"), str)
    ]
    validator_rel = f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py"
    checks = {
        "validator dry-run": any(
            validator_rel in command and "--dry-run" in command for command in commands
        ),
        "focused acceptance test": any(
            AUTOMATION_TEST_REL.as_posix() in command
            and "test_epic_004_automacao" in command
            for command in commands
        ),
        "pinned Python": "python-version: '3.12.13'" in text,
        "read-only permissions": "contents: read" in text,
    }
    return [
        _finding("WORKFLOW_INVALID", WORKFLOW_REL, f"missing {name}")
        for name, passed in checks.items()
        if not passed
    ]


def validate_repository_controls(root: Path) -> list[Finding]:
    resolved = root.resolve()
    return sorted(set(_task_findings(resolved) + _workflow_findings(resolved)))
