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

SLUG = "fechamento-da-sprint-001-e-autorizacao-da-primeira-fat"
ROOT = Path(__file__).resolve().parents[5]
TASK_REL = Path(".codex/tasks/TASK-0567.json")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
TEST_REL = Path(f"tests/fnd/{SLUG}/test_automation.py")
QUALITY_REL = Path(f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py")
EVIDENCE_REL = Path("evidence/operations/epic-092/story-0567/validation.json")
FOUNDATION_REL = Path(f"tools/governance/{SLUG}/foundation_validation.py")

CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_PYTHON_SHA = "5fda3b95a4ea91299a34e894583c3862153e4b97"
REQUIRED_TEST = "test_epic_092_automacao"
REQUIREMENT_EVIDENCE = {
    "REQ-DEV-001": "test_host_container_ci_contract_and_no_implicit_downloads",
    "REQ-FRZ-001": "test_foundation_baseline_digest_controlled_change_and_adr_supersession",
    "REQ-FRZ-002": "test_sprint_zero_authorization_and_functional_foundation_gate_blocking",
    "REQ-FRZ-003": "test_issue_adr_decision_package_impact_boundary_and_no_silent_divergence",
    "REQ-FRZ-004": "test_foundation_closure_evidence_set_and_material_reopening_criteria",
    "REQ-GOV-005": "test_sprint_zero_baseline_decision_09",
}
ACCEPTANCE_EVIDENCE = {
    f"AC-ISSUE-0677-{index:02d}": REQUIRED_TEST for index in range(1, 5)
}
EXPECTED_ALLOW_PATHS = [
    TASK_REL.as_posix(),
    f"tests/fnd/{SLUG}/**",
    f"tools/quality/contexts/engineering_governance/{SLUG}/**",
    WORKFLOW_REL.as_posix(),
    "evidence/operations/epic-092/story-0567/**",
]
EVIDENCE_FIELDS = {
    "schema_version",
    "issue",
    "story",
    "status",
    "candidate_state",
    "foundation_issue",
    "required_test",
    "requirement_evidence",
    "acceptance_evidence",
    "authorization_claim",
    "destructive_actions",
    "migration",
    "rollback",
}


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


def _load_document(
    root: Path, relative: Path, *, yaml_document: bool = False
) -> tuple[object, list[Finding]]:
    try:
        content = (root / relative).read_text(encoding="utf-8")
        return (yaml.safe_load(content) if yaml_document else json.loads(content)), []
    except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError) as error:
        return None, [
            _finding(
                "DOCUMENT_UNREADABLE",
                relative,
                str(error),
                f"Restore a valid document at {relative.as_posix()}.",
            )
        ]


def _task_findings(root: Path) -> list[Finding]:
    task, findings = _load_document(root, TASK_REL)
    if not isinstance(task, dict):
        findings.append(
            _finding(
                "TASK_CONTROL_INVALID",
                TASK_REL,
                "TaskEnvelope must be a JSON object",
                "Restore TASK-0567 with the approved ISSUE-0677 controls.",
            )
        )
        return findings
    expected: dict[str, object] = {
        "task_id": "TASK-0567",
        "issue_id": "ISSUE-0677",
        "story_id": "STORY-0567",
        "epic_id": "EPIC-092",
        "role": "DevOps",
        "dependencies": ["STORY-0565"],
        "tests": [REQUIRED_TEST],
        "acceptance_criterion_ids": list(ACCEPTANCE_EVIDENCE),
        "allow_paths": EXPECTED_ALLOW_PATHS,
    }
    drifted = [field for field, value in expected.items() if task.get(field) != value]
    if drifted:
        findings.append(
            _finding(
                "TASK_CONTROL_INVALID",
                TASK_REL,
                f"governed fields drifted: {', '.join(drifted)}",
                "Restore the approved identity, scope, dependency, test, and AC IDs.",
            )
        )
    phase_f = task.get("phase_f_review")
    files = phase_f.get("files") if isinstance(phase_f, Mapping) else None
    phase_paths = files.get("allow_paths") if isinstance(files, Mapping) else None
    if phase_paths != task.get("allow_paths"):
        findings.append(
            _finding(
                "TASK_SCOPE_DRIFT",
                TASK_REL,
                "phase_f_review.files.allow_paths differs from allow_paths",
                "Keep both TaskEnvelope allow-path lists identical.",
            )
        )
    return findings


def _workflow_findings(root: Path) -> list[Finding]:
    workflow, findings = _load_document(root, WORKFLOW_REL, yaml_document=True)
    if not isinstance(workflow, dict):
        findings.append(
            _finding(
                "WORKFLOW_INVALID",
                WORKFLOW_REL,
                "workflow must be a YAML object",
                "Restore the ISSUE-0677 workflow.",
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
    raw = (root / WORKFLOW_REL).read_text(encoding="utf-8")
    checks = {
        "read-only permissions": workflow.get("permissions") == {"contents": "read"},
        "pinned checkout": f"actions/checkout@{CHECKOUT_SHA}" in uses,
        "pinned Python": f"actions/setup-python@{SETUP_PYTHON_SHA}" in uses,
        "Python 3.12.13": "python-version: '3.12.13'" in raw,
        "validator dry-run": any(
            QUALITY_REL.as_posix() in command
            and "--dry-run" in command
            and "--candidate-sha" in command
            for command in commands
        ),
        "focused acceptance test": any(
            TEST_REL.as_posix() in command and REQUIRED_TEST in command
            for command in commands
        ),
        "fail closed": "continue-on-error: true" not in raw,
    }
    findings.extend(
        _finding(
            "WORKFLOW_INVALID",
            WORKFLOW_REL,
            f"missing {name}",
            f"Restore the required {name} control in the ISSUE-0677 workflow.",
        )
        for name, passed in checks.items()
        if not passed
    )
    return findings


def _evidence_findings(root: Path) -> list[Finding]:
    evidence, findings = _load_document(root, EVIDENCE_REL)
    expected: dict[str, object] = {
        "schema_version": "1.0.0",
        "issue": "ISSUE-0677",
        "story": "STORY-0567",
        "status": "PASS",
        "candidate_state": "READY_FOR_INDEPENDENT_REVIEW",
        "foundation_issue": "ISSUE-0676",
        "required_test": REQUIRED_TEST,
        "requirement_evidence": REQUIREMENT_EVIDENCE,
        "acceptance_evidence": ACCEPTANCE_EVIDENCE,
        "authorization_claim": "NOT_ASSERTED_BY_AUTOMATION",
        "destructive_actions": 0,
        "migration": "NOT_APPLICABLE",
        "rollback": "REVERT_COMMIT",
    }
    invalid = not isinstance(evidence, dict) or set(evidence) != EVIDENCE_FIELDS
    invalid = invalid or any(
        isinstance(evidence, dict) and evidence.get(key) != value
        for key, value in expected.items()
    )
    if invalid:
        findings.append(
            _finding(
                "EVIDENCE_INVALID",
                EVIDENCE_REL,
                "versioned evidence is absent, incomplete, or contradictory",
                "Restore exact ISSUE-0677 requirement and acceptance evidence.",
            )
        )
    return findings


def _test_findings(root: Path) -> list[Finding]:
    try:
        tree = ast.parse((root / TEST_REL).read_text(encoding="utf-8"))
        tests = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    except (OSError, UnicodeError, SyntaxError) as error:
        return [
            _finding(
                "TEST_SOURCE_INVALID",
                TEST_REL,
                str(error),
                "Restore valid ISSUE-0677 test source.",
            )
        ]
    if REQUIRED_TEST in tests:
        return []
    return [
        _finding(
            "REQUIRED_TEST_MISSING",
            TEST_REL,
            REQUIRED_TEST,
            f"Restore {REQUIRED_TEST} in {TEST_REL.as_posix()}.",
        )
    ]


def _foundation_findings(root: Path, candidate_sha: str | None) -> list[Finding]:
    if not candidate_sha:
        return [
            _finding(
                "CANDIDATE_SHA_REQUIRED",
                FOUNDATION_REL,
                "candidate SHA was not provided",
                "Pass --candidate-sha with the exact commit under validation.",
            )
        ]
    command = [
        sys.executable,
        "-B",
        str(root / FOUNDATION_REL),
        "--repository-root",
        str(root),
        "--candidate-sha",
        candidate_sha,
    ]
    environment = os.environ.copy()
    environment.update(
        {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"}
    )
    try:
        completed = subprocess.run(
            command, cwd=root, env=environment, check=False, capture_output=True, text=True
        )
        report = json.loads(completed.stdout)
    except (OSError, json.JSONDecodeError) as error:
        return [
            _finding(
                "FOUNDATION_REPORT_INVALID",
                FOUNDATION_REL,
                str(error),
                "Restore and run the ISSUE-0676 executable foundation validator.",
            )
        ]
    expected = {
        "decision": "PASS",
        "issue_id": "ISSUE-0676",
        "reviewable_state": "READY_FOR_INDEPENDENT_REVIEW",
        "authorization_claim": "NOT_ASSERTED_BY_FOUNDATION",
    }
    invalid = (
        completed.returncode != 0
        or completed.stderr != ""
        or not isinstance(report, dict)
        or any(report.get(key) != value for key, value in expected.items())
        or (
            isinstance(report, dict)
            and {
                key: value.rsplit("::", 1)[-1]
                for key, value in report.get("requirement_evidence", {}).items()
            }
            != REQUIREMENT_EVIDENCE
        )
    )
    if not invalid:
        return []
    detail = report.get("error") if isinstance(report, dict) else None
    return [
        _finding(
            "FOUNDATION_VALIDATION_FAILED",
            FOUNDATION_REL,
            str(detail or completed.stderr or "foundation report fields diverged"),
            "Repair the ISSUE-0676 foundation evidence for this exact candidate SHA.",
        )
    ]


def validate(root: Path, candidate_sha: str | None) -> list[Finding]:
    repository_root = root.resolve()
    findings = _task_findings(repository_root)
    findings.extend(_workflow_findings(repository_root))
    findings.extend(_evidence_findings(repository_root))
    findings.extend(_test_findings(repository_root))
    if not findings:
        findings.extend(_foundation_findings(repository_root, candidate_sha))
    return sorted(set(findings))


def _report(
    findings: list[Finding], *, candidate_sha: str | None, dry_run: bool
) -> dict[str, Any]:
    return {
        "acceptance_evidence": ACCEPTANCE_EVIDENCE,
        "authorization_claim": "NOT_ASSERTED_BY_AUTOMATION",
        "automation": "EPIC-092_SPRINT_001_CLOSURE_CONTROLS",
        "candidate_sha": candidate_sha,
        "candidate_state": "BLOCKED" if findings else "READY_FOR_INDEPENDENT_REVIEW",
        "destructive_actions": 0,
        "findings": [finding.as_dict() for finding in findings],
        "foundation_issue": "ISSUE-0676",
        "issue": "ISSUE-0677",
        "mode": "DRY_RUN" if dry_run else "READ_ONLY",
        "requirement_evidence": REQUIREMENT_EVIDENCE,
        "status": "FAIL" if findings else "PASS",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0677 sprint closure controls.")
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--candidate-sha")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        findings = validate(args.repository_root, args.candidate_sha)
    except Exception as error:  # CLI boundary is deliberately fail-closed.
        findings = [
            _finding(
                "VALIDATOR_INTERNAL_ERROR",
                Path("."),
                str(error),
                "Inspect the complete checkout and retry the ISSUE-0677 validator.",
            )
        ]
    print(json.dumps(_report(findings, candidate_sha=args.candidate_sha, dry_run=args.dry_run), sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
