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

SLUG = "fechamento-da-sprint-001-e-autorizacao-da-primeira-fat"
ROOT = Path(__file__).resolve().parents[3]
TASK_REL = Path(".codex/tasks/TASK-0568.json")
REGISTRY_REL = Path(
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/"
    "integration-evidence-registry.json"
)
CHECKPOINT_REL = Path(f"tools/governance/{SLUG}/integration-checkpoint.json")
TEST_REL = Path(f"tests/fnd/{SLUG}/test_integration.py")
DEPENDENCY_VALIDATOR_REL = Path(
    f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py"
)
EVIDENCE_REL = Path("evidence/implementation/epic-092/story-0568/IMPLEMENTATION.md")
REQUIRED_TEST = "test_epic_092_integracao"
ACCEPTANCE_IDS = [f"AC-ISSUE-0678-{index:02d}" for index in range(1, 5)]
EXPECTED_ALLOW_PATHS = [
    TASK_REL.as_posix(),
    f"tools/governance/{SLUG}/**",
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/**",
    TEST_REL.as_posix(),
    "evidence/implementation/epic-092/story-0568/**",
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


def _load_json(root: Path, relative: Path) -> tuple[object, list[Finding]]:
    try:
        return json.loads((root / relative).read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [
            _finding(
                "DOCUMENT_UNREADABLE",
                relative,
                str(error),
                f"Restore a valid JSON document at {relative.as_posix()}.",
            )
        ]


def _task_findings(root: Path) -> list[Finding]:
    task, findings = _load_json(root, TASK_REL)
    if not isinstance(task, dict):
        return [
            *findings,
            _finding(
                "TASK_CONTROL_INVALID",
                TASK_REL,
                "TaskEnvelope must be a JSON object",
                "Restore TASK-0568 with the approved ISSUE-0678 controls.",
            )
        ]
    expected: dict[str, object] = {
        "task_id": "TASK-0568",
        "issue_id": "ISSUE-0678",
        "story_id": "STORY-0568",
        "epic_id": "EPIC-092",
        "role": "Tech Lead",
        "dependencies": ["STORY-0566", "STORY-0567"],
        "tests": [REQUIRED_TEST],
        "acceptance_criterion_ids": ACCEPTANCE_IDS,
        "allow_paths": EXPECTED_ALLOW_PATHS,
    }
    drifted = [field for field, value in expected.items() if task.get(field) != value]
    if drifted:
        findings.append(
            _finding(
                "TASK_CONTROL_INVALID",
                TASK_REL,
                f"governed fields drifted: {', '.join(drifted)}",
                "Restore the approved identity, scope, dependencies, test, and AC IDs.",
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


def _registry_findings(root: Path) -> tuple[dict[str, Any] | None, list[Finding]]:
    registry, findings = _load_json(root, REGISTRY_REL)
    expected_fields = {
        "schema_version",
        "registry_id",
        "issue_id",
        "story_id",
        "task_id",
        "dependency_issues",
        "dependency_validator",
        "requirement_evidence",
        "acceptance_evidence",
        "required_test",
        "required_result",
        "failure_policy",
        "authorization_claim",
    }
    if not isinstance(registry, dict) or set(registry) != expected_fields:
        findings.append(
            _finding(
                "REGISTRY_INVALID",
                REGISTRY_REL,
                "integration registry is absent or its fields diverge",
                "Restore the complete ISSUE-0678 integration registry.",
            )
        )
        return None, findings
    expected: dict[str, object] = {
        "schema_version": "1.0.0",
        "registry_id": "SPRINT-001-CLOSURE-INTEGRATION-EVIDENCE",
        "issue_id": "ISSUE-0678",
        "story_id": "STORY-0568",
        "task_id": "TASK-0568",
        "dependency_issues": ["ISSUE-0676", "ISSUE-0677"],
        "dependency_validator": DEPENDENCY_VALIDATOR_REL.as_posix(),
        "acceptance_evidence": dict.fromkeys(ACCEPTANCE_IDS, REQUIRED_TEST),
        "required_test": REQUIRED_TEST,
        "required_result": "READY_FOR_INDEPENDENT_REVIEW",
        "failure_policy": "BLOCK_ON_ANY_FINDING",
        "authorization_claim": "NOT_ASSERTED_BY_INTEGRATION",
    }
    drifted = [field for field, value in expected.items() if registry.get(field) != value]
    requirement_evidence = registry.get("requirement_evidence")
    if not isinstance(requirement_evidence, dict) or not requirement_evidence or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in requirement_evidence.items()
    ):
        drifted.append("requirement_evidence")
    if drifted:
        findings.append(
            _finding(
                "REGISTRY_INVALID",
                REGISTRY_REL,
                f"governed fields drifted: {', '.join(drifted)}",
                "Restore the ISSUE-0678 dependency, requirement, AC, and safety evidence.",
            )
        )
    return registry, findings


def _checkpoint_findings(root: Path) -> list[Finding]:
    checkpoint, findings = _load_json(root, CHECKPOINT_REL)
    expected = {
        "schema_version": "1.0.0",
        "issue_id": "ISSUE-0678",
        "story_id": "STORY-0568",
        "task_id": "TASK-0568",
        "evidence_registry": REGISTRY_REL.as_posix(),
        "dependency_validator": DEPENDENCY_VALIDATOR_REL.as_posix(),
        "reproducible_command": (
            "python -X utf8 -m pytest -q -p no:cacheprovider "
            f"{TEST_REL.as_posix()}::{REQUIRED_TEST}"
        ),
        "candidate_state": "READY_FOR_INDEPENDENT_REVIEW",
        "authorization_claim": "NOT_ASSERTED_BY_INTEGRATION",
        "migration": "NOT_APPLICABLE",
        "rollback": "REVERT_COMMIT",
    }
    if not isinstance(checkpoint, dict) or checkpoint != expected:
        findings.append(
            _finding(
                "CHECKPOINT_INVALID",
                CHECKPOINT_REL,
                "integration checkpoint is absent, incomplete, or contradictory",
                "Restore the exact ISSUE-0678 checkpoint.",
            )
        )
    return findings


def _test_and_evidence_findings(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        tree = ast.parse((root / TEST_REL).read_text(encoding="utf-8"))
        tests = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    except (OSError, UnicodeError, SyntaxError) as error:
        tests = set()
        findings.append(
            _finding(
                "TEST_SOURCE_INVALID",
                TEST_REL,
                str(error),
                "Restore valid ISSUE-0678 test source.",
            )
        )
    if REQUIRED_TEST not in tests:
        findings.append(
            _finding(
                "REQUIRED_TEST_MISSING",
                TEST_REL,
                REQUIRED_TEST,
                f"Restore {REQUIRED_TEST} in {TEST_REL.as_posix()}.",
            )
        )
    try:
        evidence = (root / EVIDENCE_REL).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        findings.append(
            _finding(
                "IMPLEMENTATION_EVIDENCE_MISSING",
                EVIDENCE_REL,
                str(error),
                "Restore the versioned ISSUE-0678 implementation evidence.",
            )
        )
    else:
        required_markers = ["ISSUE-0678", REQUIRED_TEST, *ACCEPTANCE_IDS]
        if any(marker not in evidence for marker in required_markers):
            findings.append(
                _finding(
                    "IMPLEMENTATION_EVIDENCE_INVALID",
                    EVIDENCE_REL,
                    "required issue, test, or AC marker is absent",
                    "Restore explicit ISSUE-0678 acceptance evidence.",
                )
            )
    return findings


def _dependency_findings(
    root: Path, candidate_sha: str | None, registry: dict[str, Any]
) -> list[Finding]:
    if not candidate_sha:
        return [
            _finding(
                "CANDIDATE_SHA_REQUIRED",
                DEPENDENCY_VALIDATOR_REL,
                "candidate SHA was not provided",
                "Pass --candidate-sha with the exact commit under validation.",
            )
        ]
    command = [
        sys.executable,
        "-B",
        str(root / DEPENDENCY_VALIDATOR_REL),
        "--repository-root",
        str(root),
        "--candidate-sha",
        candidate_sha,
        "--dry-run",
    ]
    environment = os.environ.copy()
    environment.update(
        {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"}
    )
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        report = json.loads(completed.stdout)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [
            _finding(
                "DEPENDENCY_REPORT_INVALID",
                DEPENDENCY_VALIDATOR_REL,
                str(error),
                "Restore and run the ISSUE-0677 validator for the candidate SHA.",
            )
        ]
    expected = {
        "status": "PASS",
        "issue": "ISSUE-0677",
        "foundation_issue": "ISSUE-0676",
        "candidate_sha": candidate_sha,
        "candidate_state": "READY_FOR_INDEPENDENT_REVIEW",
        "authorization_claim": "NOT_ASSERTED_BY_AUTOMATION",
        "findings": [],
        "requirement_evidence": registry["requirement_evidence"],
    }
    invalid = (
        completed.returncode != 0
        or completed.stderr != ""
        or not isinstance(report, dict)
        or any(report.get(field) != value for field, value in expected.items())
    )
    if not invalid:
        return []
    detail = report.get("findings") if isinstance(report, dict) else completed.stderr
    return [
        _finding(
            "DEPENDENCY_VALIDATION_FAILED",
            DEPENDENCY_VALIDATOR_REL,
            json.dumps(detail, sort_keys=True),
            "Resolve ISSUE-0676/0677 findings on this candidate before integration review.",
        )
    ]


def validate(root: Path, candidate_sha: str | None) -> list[Finding]:
    repository_root = root.resolve()
    findings = _task_findings(repository_root)
    registry, registry_findings = _registry_findings(repository_root)
    findings.extend(registry_findings)
    findings.extend(_checkpoint_findings(repository_root))
    findings.extend(_test_and_evidence_findings(repository_root))
    if not findings and registry is not None:
        findings.extend(_dependency_findings(repository_root, candidate_sha, registry))
    return sorted(set(findings))


def _report(
    findings: list[Finding], *, candidate_sha: str | None, registry: object
) -> dict[str, Any]:
    evidence = registry if isinstance(registry, dict) else {}
    return {
        "acceptance_evidence": evidence.get("acceptance_evidence", {}),
        "authorization_claim": "NOT_ASSERTED_BY_INTEGRATION",
        "candidate_sha": candidate_sha,
        "candidate_state": "BLOCKED" if findings else "READY_FOR_INDEPENDENT_REVIEW",
        "dependency_issues": ["ISSUE-0676", "ISSUE-0677"],
        "findings": [finding.as_dict() for finding in findings],
        "integration": "EPIC-092_SPRINT_001_CLOSURE",
        "issue": "ISSUE-0678",
        "migration": "NOT_APPLICABLE",
        "requirement_evidence": evidence.get("requirement_evidence", {}),
        "rollback": "REVERT_COMMIT",
        "status": "FAIL" if findings else "PASS",
        "story": "STORY-0568",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0678 integration.")
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--candidate-sha")
    args = parser.parse_args(argv)
    try:
        root = args.repository_root.resolve()
        findings = validate(root, args.candidate_sha)
        registry, _ = _load_json(root, REGISTRY_REL)
    except Exception as error:  # CLI boundary is deliberately fail-closed.
        registry = {}
        findings = [
            _finding(
                "VALIDATOR_INTERNAL_ERROR",
                Path("."),
                str(error),
                "Inspect the complete checkout and retry the ISSUE-0678 validator.",
            )
        ]
    report = _report(findings, candidate_sha=args.candidate_sha, registry=registry)
    print(json.dumps(report, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
