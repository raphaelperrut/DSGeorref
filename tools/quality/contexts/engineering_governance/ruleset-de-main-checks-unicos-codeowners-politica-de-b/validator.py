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

SLUG = "ruleset-de-main-checks-unicos-codeowners-politica-de-b"
TASK_REL = Path(".codex/tasks/TASK-0562.json")
WORKFLOW_REL = Path(f".github/workflows/{SLUG}.yaml")
TEST_REL = Path(f"tests/fnd/{SLUG}/test_automation.py")
EVIDENCE_REL = Path("evidence/operations/epic-091/story-0562/validation.json")
QUALITY_REL = Path(f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py")
FOUNDATION_REL = Path(f"tools/governance/{SLUG}/foundation_validation.py")

CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_PYTHON_SHA = "5fda3b95a4ea91299a34e894583c3862153e4b97"
REQUIRED_TEST = "test_epic_091_automacao"
REQUIREMENT_IDS = ("REQ-FRZ-003", "REQ-GOV-004", "REQ-ISS-003", "REQ-ISS-006", "REQ-PUB-002")
REQUIREMENTS = dict.fromkeys(REQUIREMENT_IDS, REQUIRED_TEST)
ACCEPTANCE = {f"AC-ISSUE-0672-{index:02d}": REQUIRED_TEST for index in range(1, 5)}
FOUNDATION_EVIDENCE = {
    "REQ-FRZ-003": "test_issue_adr_decision_package_impact_boundary_and_no_silent_divergence",
    "REQ-GOV-004": "test_codex_issue_scope_required_pr_no_direct_main_or_automerge",
    "REQ-ISS-003": "test_no_orphan_issue_without_adr_or_local_decision_justification",
    "REQ-ISS-006": "test_idempotent_dry_run_managed_field_issue_sync",
    "REQ-PUB-002": "test_contribution_origin_dco_signoff_and_inbound_outbound_policy",
}
EXPECTED_ALLOW_PATHS = [
    TASK_REL.as_posix(),
    f"tests/fnd/{SLUG}/**",
    f"tools/quality/contexts/engineering_governance/{SLUG}/**",
    WORKFLOW_REL.as_posix(),
    "evidence/operations/epic-091/story-0562/**",
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


def _load(
    root: Path, relative: Path, *, yaml_document: bool = False
) -> tuple[object, list[Finding]]:
    try:
        text = (root / relative).read_text(encoding="utf-8")
        return (yaml.safe_load(text) if yaml_document else json.loads(text)), []
    except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError) as error:
        code = "WORKFLOW_INVALID" if yaml_document else "JSON_UNREADABLE"
        return None, [
            _finding(code, relative, str(error), f"Restore a valid document at {relative}.")
        ]


def _task_findings(root: Path) -> list[Finding]:
    task, findings = _load(root, TASK_REL)
    if not isinstance(task, dict):
        findings.append(
            _finding(
                "TASK_CONTROL_INVALID",
                TASK_REL,
                "TaskEnvelope must be a JSON object",
                "Restore TASK-0562 with the approved ISSUE-0672 identity and scope.",
            )
        )
        return findings
    expected: dict[str, object] = {
        "task_id": "TASK-0562",
        "issue_id": "ISSUE-0672",
        "story_id": "STORY-0562",
        "epic_id": "EPIC-091",
        "role": "DevOps",
        "dependencies": ["STORY-0560"],
        "tests": [REQUIRED_TEST],
        "acceptance_criterion_ids": list(ACCEPTANCE),
        "allow_paths": EXPECTED_ALLOW_PATHS,
    }
    drifted = [field for field, value in expected.items() if task.get(field) != value]
    if drifted:
        findings.append(
            _finding(
                "TASK_CONTROL_INVALID",
                TASK_REL,
                f"governed fields drifted: {', '.join(drifted)}",
                "Restore the approved identity, dependency, test, AC IDs, and allow paths.",
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


def _foundation_findings(
    root: Path,
    bypass_record: Path | None,
    candidate_sha: str | None,
    verdict_ref: str | None,
) -> list[Finding]:
    bypass_values = (bypass_record, candidate_sha, verdict_ref)
    if any(bypass_values) and not all(bypass_values):
        return [
            _finding(
                "BYPASS_EVIDENCE_INCOMPLETE",
                FOUNDATION_REL,
                "bypass record, candidate SHA, and delivery verdict must be provided together",
                "Provide all three bypass arguments or omit all three.",
            )
        ]
    command = [sys.executable, "-B", str(root / FOUNDATION_REL), "--repository-root", str(root)]
    if bypass_record is not None:
        command.extend(
            [
                "--bypass-record",
                str(bypass_record),
                "--candidate-sha",
                str(candidate_sha),
                "--delivery-approval-verdict-ref",
                str(verdict_ref),
            ]
        )
    environment = os.environ.copy()
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"})
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
                "Run the ISSUE-0671 validator directly and restore its JSON report.",
            )
        ]
    if not isinstance(report, dict):
        return [
            _finding(
                "FOUNDATION_REPORT_INVALID",
                FOUNDATION_REL,
                "foundation report must be a JSON object",
                "Restore the ISSUE-0671 validator JSON report contract.",
            )
        ]
    expected = {
        "decision": "PASS",
        "issue_id": "ISSUE-0671",
        "live_ruleset_enforcement": "NOT_ASSERTED_BY_FOUNDATION",
        "required_checks": ["verify-foundation"],
        "requirement_evidence": FOUNDATION_EVIDENCE,
    }
    invalid = (
        completed.returncode != 0
        or completed.stderr != ""
        or any(report.get(key) != value for key, value in expected.items())
    )
    if bypass_record is not None:
        invalid = invalid or report.get("bypass_evidence") != "PASS"
    if not invalid:
        return []
    detail = report.get("error")
    return [
        _finding(
            "BYPASS_VALIDATION_FAILED" if bypass_record else "FOUNDATION_VALIDATION_FAILED",
            FOUNDATION_REL,
            str(detail or completed.stderr or "foundation report fields diverged"),
            "Repair the reported artifact or provide exact SHA-bound authorized bypass evidence.",
        )
    ]


def _workflow_findings(root: Path) -> list[Finding]:
    workflow, findings = _load(root, WORKFLOW_REL, yaml_document=True)
    if not isinstance(workflow, dict):
        findings.append(
            _finding(
                "WORKFLOW_INVALID",
                WORKFLOW_REL,
                "workflow must be a YAML object",
                "Restore the ISSUE-0672 workflow document.",
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
            QUALITY_REL.as_posix() in command and "--dry-run" in command for command in commands
        ),
        "focused acceptance test": any(
            TEST_REL.as_posix() in command and REQUIRED_TEST in command for command in commands
        ),
        "fail closed": "continue-on-error: true" not in raw,
    }
    findings.extend(
        _finding(
            "WORKFLOW_INVALID",
            WORKFLOW_REL,
            f"missing {name}",
            f"Restore the required {name} control in the ISSUE-0672 workflow.",
        )
        for name, passed in checks.items()
        if not passed
    )
    return findings


def _repository_evidence_findings(root: Path) -> list[Finding]:
    evidence, findings = _load(root, EVIDENCE_REL)
    expected = {
        "issue": "ISSUE-0672",
        "story": "STORY-0562",
        "status": "PASS",
        "required_test": REQUIRED_TEST,
        "requirement_evidence": REQUIREMENTS,
        "acceptance_evidence": ACCEPTANCE,
        "destructive_actions": 0,
    }
    if not isinstance(evidence, dict) or any(
        evidence.get(key) != value for key, value in expected.items()
    ):
        findings.append(
            _finding(
                "EVIDENCE_INVALID",
                EVIDENCE_REL,
                "candidate evidence is absent or does not cover ISSUE-0672",
                "Regenerate evidence from the focused ISSUE-0672 validation.",
            )
        )
    return findings


def validate(
    root: Path,
    bypass_record: Path | None = None,
    candidate_sha: str | None = None,
    verdict_ref: str | None = None,
) -> list[Finding]:
    repository_root = root.resolve()
    findings = _task_findings(repository_root)
    findings.extend(
        _foundation_findings(repository_root, bypass_record, candidate_sha, verdict_ref)
    )
    findings.extend(_workflow_findings(repository_root))
    try:
        tree = ast.parse((repository_root / TEST_REL).read_text(encoding="utf-8"))
        tests = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    except (OSError, UnicodeError, SyntaxError) as error:
        tests = set()
        findings.append(
            _finding("TEST_SOURCE_INVALID", TEST_REL, str(error), "Restore valid test source.")
        )
    if REQUIRED_TEST not in tests:
        findings.append(
            _finding(
                "REQUIRED_TEST_MISSING",
                TEST_REL,
                REQUIRED_TEST,
                f"Restore {REQUIRED_TEST} in {TEST_REL}.",
            )
        )
    findings.extend(_repository_evidence_findings(repository_root))
    return sorted(set(findings))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0672 main-ruleset controls.")
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--bypass-record", type=Path)
    parser.add_argument("--candidate-sha")
    parser.add_argument("--delivery-approval-verdict-ref")
    args = parser.parse_args(argv)
    try:
        findings = validate(
            args.repository_root,
            args.bypass_record,
            args.candidate_sha,
            args.delivery_approval_verdict_ref,
        )
    except Exception as error:  # CLI boundary is deliberately fail-closed.
        findings = [
            _finding(
                "VALIDATOR_INTERNAL_ERROR",
                Path("."),
                str(error),
                "Inspect the error against a complete checkout and retry.",
            )
        ]
    report: dict[str, Any] = {
        "acceptance_evidence": ACCEPTANCE,
        "automation": "EPIC-091_MAIN_RULESET_CONTROLS",
        "bypass_evidence": (
            "VALIDATED"
            if args.bypass_record and not findings
            else "REJECTED"
            if args.bypass_record
            else "NOT_PRESENT"
        ),
        "destructive_actions": 0,
        "findings": [finding.as_dict() for finding in findings],
        "issue": "ISSUE-0672",
        "live_ruleset_enforcement": "NOT_ASSERTED_BY_AUTOMATION",
        "mode": "DRY_RUN" if args.dry_run else "READ_ONLY",
        "requirement_evidence": REQUIREMENTS,
        "status": "FAIL" if findings else "PASS",
    }
    print(json.dumps(report, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
