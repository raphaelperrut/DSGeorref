from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SLUG = "license-citation-cff-contribuicao-dco-cla-e-gate-de-pu"
TASK_PATH = Path(".codex/tasks/TASK-0034.json")
FOUNDATION_PATH = Path(f"tools/governance/{SLUG}/foundation_validation.py")
AUTOMATION_PATH = Path(
    f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py"
)
EXPECTED_ALLOW_PATHS = (
    ".codex/tasks/TASK-0034.json",
    f"tools/governance/{SLUG}/**",
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/**",
    "evidence/implementation/epic-007/story-0034/**",
)
EXPECTED_DEPENDENCIES = ("STORY-0032", "STORY-0033")
EXPECTED_TEST = "test_epic_007_integracao"
EXPECTED_AC_IDS = tuple(f"AC-ISSUE-0144-{index:02d}" for index in range(1, 5))
EXPECTED_AUTOMATION_AC_IDS = tuple(
    f"AC-ISSUE-0143-{index:02d}" for index in range(1, 5)
)
EXPECTED_REQUIREMENTS = ("REQ-CIT-001", "REQ-EPIC-042", "REQ-OSS-001", "REQ-PUB-002")


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    artifact: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"artifact": self.artifact, "code": self.code, "detail": self.detail}


def _load_task(root: Path) -> tuple[Mapping[str, Any] | None, list[Finding]]:
    try:
        loaded = json.loads((root / TASK_PATH).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [Finding("TASK_INVALID", TASK_PATH.as_posix(), str(error))]
    if not isinstance(loaded, Mapping):
        return None, [Finding("TASK_INVALID", TASK_PATH.as_posix(), "object required")]
    return loaded, []


def _task_findings(task: Mapping[str, Any]) -> list[Finding]:
    expected_scalars = {
        "task_id": "TASK-0034",
        "issue_id": "ISSUE-0144",
        "story_id": "STORY-0034",
        "epic_id": "EPIC-007",
        "role": "Tech Lead",
        "bounded_context": "BC-001",
        "requirement_basis": "DERIVED_CONTROL",
    }
    findings = [
        Finding("TASK_IDENTITY_INVALID", field, f"expected {expected}")
        for field, expected in expected_scalars.items()
        if task.get(field) != expected
    ]
    expected_lists: dict[str, Sequence[str]] = {
        "allow_paths": EXPECTED_ALLOW_PATHS,
        "deny_paths": ("src/**/epic-*", "src/**/issue-*"),
        "tests": (EXPECTED_TEST,),
        "dependencies": EXPECTED_DEPENDENCIES,
        "acceptance_criterion_ids": EXPECTED_AC_IDS,
    }
    for field, expected in expected_lists.items():
        actual = task.get(field)
        if not isinstance(actual, list) or tuple(actual) != tuple(expected):
            findings.append(Finding("TASK_SCOPE_INVALID", field, "governed values drifted"))
    phase_f = task.get("phase_f_review")
    phase_files = phase_f.get("files") if isinstance(phase_f, Mapping) else None
    phase_paths = phase_files.get("allow_paths") if isinstance(phase_files, Mapping) else None
    if not isinstance(phase_paths, list) or tuple(phase_paths) != EXPECTED_ALLOW_PATHS:
        findings.append(
            Finding("TASK_SCOPE_INVALID", "phase_f_review.files", "allow-path parity required")
        )
    return findings


def _run_report(root: Path, relative: Path, arguments: Sequence[str]) -> tuple[object, int]:
    environment = os.environ.copy()
    environment.update(
        {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"}
    )
    try:
        completed = subprocess.run(
            [sys.executable, "-B", str(root / relative), *arguments],
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return json.loads(completed.stdout), completed.returncode
    except (OSError, UnicodeError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        return {"execution_error": str(error)}, -1


def _foundation_findings(report: object, returncode: int) -> list[Finding]:
    checks = report.get("checks") if isinstance(report, Mapping) else None
    valid = bool(
        returncode == 0
        and isinstance(report, Mapping)
        and report.get("issue_id") == "ISSUE-0142"
        and report.get("decision") == "PASS"
        and isinstance(checks, Mapping)
        and checks.get("checkpoint") == {"status": "PASS"}
    )
    return [] if valid else [
        Finding(
            "FOUNDATION_VALIDATION_FAILED",
            FOUNDATION_PATH.as_posix(),
            f"returncode={returncode}",
        )
    ]


def _automation_findings(report: object, returncode: int) -> list[Finding]:
    requirements = report.get("requirement_evidence") if isinstance(report, Mapping) else None
    acceptance = report.get("acceptance_evidence") if isinstance(report, Mapping) else None
    gate = report.get("publication_gate") if isinstance(report, Mapping) else None
    valid = bool(
        returncode == 0
        and isinstance(report, Mapping)
        and report.get("status") == "PASS"
        and report.get("mode") == "DRY_RUN"
        and report.get("destructive_actions") == 0
        and report.get("findings") == []
        and report.get("automation") == "EPIC-007_LICENSE_PUBLICATION_GOVERNANCE_CONTROLS"
        and isinstance(requirements, Mapping)
        and tuple(sorted(requirements)) == EXPECTED_REQUIREMENTS
        and all(
            isinstance(evidence, list) and "test_epic_007_automacao" in evidence
            for evidence in requirements.values()
        )
        and acceptance == dict.fromkeys(EXPECTED_AUTOMATION_AC_IDS, "test_epic_007_automacao")
        and isinstance(gate, Mapping)
        and gate.get("decision") == "BLOCKED"
        and gate.get("failure_mode") == "FAIL_CLOSED"
    )
    return [] if valid else [
        Finding(
            "AUTOMATION_VALIDATION_FAILED",
            AUTOMATION_PATH.as_posix(),
            f"returncode={returncode}",
        )
    ]


def validate_repository_integration(repository_root: Path) -> tuple[Finding, ...]:
    root = repository_root.resolve()
    task, findings = _load_task(root)
    if task is not None:
        findings.extend(_task_findings(task))
    foundation, foundation_code = _run_report(root, FOUNDATION_PATH, ())
    findings.extend(_foundation_findings(foundation, foundation_code))
    automation, automation_code = _run_report(
        root, AUTOMATION_PATH, ("--repository-root", str(root), "--dry-run")
    )
    findings.extend(_automation_findings(automation, automation_code))
    return tuple(sorted(set(findings)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0144 repository integration")
    parser.add_argument(
        "--repository-root", type=Path, default=Path(__file__).resolve().parents[3]
    )
    args = parser.parse_args(argv)
    try:
        findings = validate_repository_integration(args.repository_root)
    except Exception as error:  # CLI boundary must fail closed with one stable report.
        findings = (Finding("INTEGRATION_INTERNAL_ERROR", ".", str(error)),)
    report = {
        "acceptance_evidence": dict.fromkeys(EXPECTED_AC_IDS, EXPECTED_TEST),
        "control_plane": "SUBPROCESS_READ_ONLY",
        "dependencies": list(EXPECTED_DEPENDENCIES),
        "findings": [finding.as_dict() for finding in findings],
        "issue": "ISSUE-0144",
        "publication_gate": "BLOCKED_FAIL_CLOSED",
        "requirement_evidence": dict.fromkeys(EXPECTED_REQUIREMENTS, EXPECTED_TEST),
        "status": "FAIL" if findings else "PASS",
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
