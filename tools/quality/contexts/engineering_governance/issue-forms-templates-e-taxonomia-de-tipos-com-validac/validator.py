from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

SLUG = "issue-forms-templates-e-taxonomia-de-tipos-com-validac"
TASK_REL = Path(".codex/tasks/TASK-0557.json")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
TEST_REL = Path(f"tests/fnd/{SLUG}/test_automation.py")
EVIDENCE_REL = Path("evidence/operations/epic-090/story-0557/validation.json")
QUALITY_REL = Path(f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py")
FOUNDATION_VALIDATOR_REL = Path(f"tools/governance/{SLUG}/validate_issue_forms.py")

CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_PYTHON_SHA = "5fda3b95a4ea91299a34e894583c3862153e4b97"
REQUIRED_TEST = "test_epic_090_automacao"
REQUIREMENT_EVIDENCE = {"REQ-GOV-002": REQUIRED_TEST}
ACCEPTANCE_EVIDENCE = {f"AC-ISSUE-0667-{index:02d}": REQUIRED_TEST for index in range(1, 5)}
EXPECTED_ALLOW_PATHS = [
    TASK_REL.as_posix(),
    f"tests/fnd/{SLUG}/**",
    f"tools/quality/contexts/engineering_governance/{SLUG}/**",
    WORKFLOW_REL.as_posix(),
    "evidence/operations/epic-090/story-0557/**",
]


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    artifact: str
    detail: str
    remediation: str

    def as_dict(self) -> dict[str, str]:
        return {
            "artifact": self.artifact,
            "code": self.code,
            "detail": self.detail,
            "remediation": self.remediation,
        }


def _finding(code: str, artifact: Path, detail: str, remediation: str) -> Finding:
    return Finding(code, artifact.as_posix(), detail, remediation)


def _load_json(root: Path, relative: Path, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return json.loads((root / relative).read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [
            _finding(code, relative, str(error), f"Restore valid JSON at {relative.as_posix()}.")
        ]


def _load_yaml(root: Path, relative: Path) -> tuple[object | None, list[Finding]]:
    try:
        return yaml.safe_load((root / relative).read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return None, [
            _finding(
                "WORKFLOW_INVALID",
                relative,
                str(error),
                f"Restore valid workflow YAML at {relative.as_posix()}.",
            )
        ]


def _task_findings(root: Path) -> list[Finding]:
    loaded, findings = _load_json(root, TASK_REL, "TASK_UNREADABLE")
    if not isinstance(loaded, dict):
        if loaded is not None:
            findings.append(
                _finding(
                    "TASK_CONTROL_INVALID",
                    TASK_REL,
                    "TaskEnvelope must be a JSON object",
                    "Restore TASK-0557 as an object with the approved issue identity and scope.",
                )
            )
        return findings

    expected: dict[str, object] = {
        "task_id": "TASK-0557",
        "issue_id": "ISSUE-0667",
        "story_id": "STORY-0557",
        "epic_id": "EPIC-090",
        "role": "DevOps",
        "dependencies": ["STORY-0555"],
        "tests": [REQUIRED_TEST],
        "acceptance_criterion_ids": list(ACCEPTANCE_EVIDENCE),
        "allow_paths": EXPECTED_ALLOW_PATHS,
    }
    drifted = [field for field, value in expected.items() if loaded.get(field) != value]
    if drifted:
        findings.append(
            _finding(
                "TASK_CONTROL_INVALID",
                TASK_REL,
                f"governed fields drifted: {', '.join(drifted)}",
                "Restore the approved ISSUE-0667 identity, dependency, test, AC IDs, "
                "and allow paths.",
            )
        )

    phase_f = loaded.get("phase_f_review")
    files = phase_f.get("files") if isinstance(phase_f, Mapping) else None
    phase_allow_paths = files.get("allow_paths") if isinstance(files, Mapping) else None
    if phase_allow_paths != loaded.get("allow_paths"):
        findings.append(
            _finding(
                "TASK_SCOPE_DRIFT",
                TASK_REL,
                "phase_f_review.files.allow_paths differs from allow_paths",
                "Keep both TaskEnvelope allow-path lists identical.",
            )
        )
    return findings


def _foundation_findings(root: Path) -> list[Finding]:
    command = [
        sys.executable,
        "-B",
        str(root / FOUNDATION_VALIDATOR_REL),
        "--repository-root",
        str(root),
    ]
    environment = os.environ.copy()
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"})
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        return [
            _finding(
                "FOUNDATION_VALIDATOR_UNAVAILABLE",
                FOUNDATION_VALIDATOR_REL,
                str(error),
                "Restore the ISSUE-0666 validator and a working Python runtime.",
            )
        ]

    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        return [
            _finding(
                "FOUNDATION_REPORT_INVALID",
                FOUNDATION_VALIDATOR_REL,
                f"non-JSON output: {error}",
                "Run the ISSUE-0666 validator directly and restore its JSON report contract.",
            )
        ]
    if not isinstance(report, dict):
        return [
            _finding(
                "FOUNDATION_REPORT_INVALID",
                FOUNDATION_VALIDATOR_REL,
                "report must be a JSON object",
                "Restore the ISSUE-0666 validator JSON report contract.",
            )
        ]

    upstream_findings = report.get("findings")
    if completed.returncode != 0 or report.get("status") != "PASS" or upstream_findings:
        if isinstance(upstream_findings, list) and upstream_findings:
            translated: list[Finding] = []
            for item in upstream_findings:
                if not isinstance(item, Mapping):
                    continue
                translated.append(
                    Finding(
                        str(item.get("code", "FOUNDATION_VALIDATION_FAILED")),
                        str(item.get("artifact", FOUNDATION_VALIDATOR_REL.as_posix())),
                        str(item.get("detail", "foundation validation failed")),
                        "Run the ISSUE-0666 validator directly and repair the reported artifact.",
                    )
                )
            if translated:
                return translated
        detail = (
            completed.stderr.strip()
            or f"exit={completed.returncode}, status={report.get('status')}"
        )
        return [
            _finding(
                "FOUNDATION_VALIDATION_FAILED",
                FOUNDATION_VALIDATOR_REL,
                detail,
                "Run the ISSUE-0666 validator directly and repair the reported failure.",
            )
        ]

    valid_report = (
        completed.stderr == ""
        and report.get("issue") == "ISSUE-0666"
        and report.get("failure_policy") == "FAIL_CLOSED"
        and isinstance(report.get("requirement_evidence"), dict)
        and "REQ-GOV-002" in report["requirement_evidence"]
    )
    if not valid_report:
        return [
            _finding(
                "FOUNDATION_REPORT_INVALID",
                FOUNDATION_VALIDATOR_REL,
                "missing issue identity, fail-closed policy, or REQ-GOV-002 evidence",
                "Restore the frozen ISSUE-0666 report fields consumed by this automation.",
            )
        ]
    return []


def _defined_tests(root: Path) -> tuple[set[str], list[Finding]]:
    try:
        source = (root / TEST_REL).read_text(encoding="utf-8")
        tree = ast.parse(source, TEST_REL.as_posix())
    except (OSError, UnicodeError, SyntaxError) as error:
        return set(), [
            _finding(
                "TEST_SOURCE_INVALID",
                TEST_REL,
                str(error),
                f"Restore valid Python test source at {TEST_REL.as_posix()}.",
            )
        ]
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }, []


def _workflow_findings(root: Path) -> list[Finding]:
    workflow, findings = _load_yaml(root, WORKFLOW_REL)
    if not isinstance(workflow, dict):
        if workflow is not None:
            findings.append(
                _finding(
                    "WORKFLOW_INVALID",
                    WORKFLOW_REL,
                    "workflow must be a YAML object",
                    "Restore the ISSUE-0667 workflow document.",
                )
            )
        return findings

    jobs = workflow.get("jobs")
    steps = [
        step
        for job in (jobs.values() if isinstance(jobs, Mapping) else [])
        if isinstance(job, Mapping)
        for step in job.get("steps", [])
        if isinstance(step, Mapping)
    ]
    uses = [step["uses"] for step in steps if isinstance(step.get("uses"), str)]
    commands = [step["run"] for step in steps if isinstance(step.get("run"), str)]
    text = (root / WORKFLOW_REL).read_text(encoding="utf-8")
    checks = {
        "read-only permissions": workflow.get("permissions") == {"contents": "read"},
        "pinned checkout": f"actions/checkout@{CHECKOUT_SHA}" in uses,
        "pinned Python": f"actions/setup-python@{SETUP_PYTHON_SHA}" in uses,
        "Python 3.12.13": "python-version: '3.12.13'" in text,
        "validator dry-run": any(
            QUALITY_REL.as_posix() in command and "--dry-run" in command for command in commands
        ),
        "focused acceptance test": any(
            TEST_REL.as_posix() in command and REQUIRED_TEST in command for command in commands
        ),
        "fail closed": "continue-on-error: true" not in text,
    }
    findings.extend(
        _finding(
            "WORKFLOW_INVALID",
            WORKFLOW_REL,
            f"missing {name}",
            f"Restore the required {name} control in the ISSUE-0667 workflow.",
        )
        for name, passed in checks.items()
        if not passed
    )
    return findings


def _evidence_findings(root: Path) -> list[Finding]:
    evidence, findings = _load_json(root, EVIDENCE_REL, "EVIDENCE_UNREADABLE")
    expected = {
        "issue": "ISSUE-0667",
        "story": "STORY-0557",
        "status": "PASS",
        "required_test": REQUIRED_TEST,
        "requirement_evidence": REQUIREMENT_EVIDENCE,
        "acceptance_evidence": ACCEPTANCE_EVIDENCE,
        "destructive_actions": 0,
    }
    if not isinstance(evidence, dict) or any(
        evidence.get(key) != value for key, value in expected.items()
    ):
        findings.append(
            _finding(
                "EVIDENCE_INVALID",
                EVIDENCE_REL,
                "candidate evidence is absent or does not cover ISSUE-0667",
                "Regenerate the versioned evidence from the focused ISSUE-0667 validation.",
            )
        )
    return findings


def validate(repository_root: Path) -> list[Finding]:
    root = repository_root.resolve()
    findings = _task_findings(root)
    findings.extend(_foundation_findings(root))
    findings.extend(_workflow_findings(root))
    tests, test_findings = _defined_tests(root)
    findings.extend(test_findings)
    if REQUIRED_TEST not in tests:
        findings.append(
            _finding(
                "REQUIRED_TEST_MISSING",
                TEST_REL,
                REQUIRED_TEST,
                f"Restore {REQUIRED_TEST} in {TEST_REL.as_posix()}.",
            )
        )
    findings.extend(_evidence_findings(root))
    return sorted(set(findings))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0667 Issue Form controls.")
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path(__file__).resolve().parents[5],
        help="Repository root containing the frozen ISSUE-0666 foundation.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Assert validation-only mode; no filesystem or repository state is changed.",
    )
    return parser


def _report(findings: list[Finding], *, dry_run: bool) -> dict[str, Any]:
    return {
        "acceptance_evidence": ACCEPTANCE_EVIDENCE,
        "automation": "EPIC-090_ISSUE_FORM_CONTROLS",
        "destructive_actions": 0,
        "findings": [finding.as_dict() for finding in findings],
        "issue": "ISSUE-0667",
        "mode": "DRY_RUN" if dry_run else "READ_ONLY",
        "requirement_evidence": REQUIREMENT_EVIDENCE,
        "status": "FAIL" if findings else "PASS",
    }


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        findings = validate(args.repository_root)
    except Exception as error:  # CLI boundary is fail-closed with an actionable report.
        findings = [
            _finding(
                "VALIDATOR_INTERNAL_ERROR",
                Path("."),
                str(error),
                "Run with --repository-root pointing to a complete checkout and inspect "
                "this error.",
            )
        ]
    print(json.dumps(_report(findings, dry_run=args.dry_run), sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
