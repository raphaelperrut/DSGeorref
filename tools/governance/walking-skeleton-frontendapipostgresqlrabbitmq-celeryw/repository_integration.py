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

SLUG = "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw"
TASK_PATH = Path(".codex/tasks/TASK-0537.json")
CONSOLIDATION_CHECKPOINT = Path(
    f"tests/fnd/{SLUG}/test_slice_consolidation.py"
)
CONSOLIDATION_TEST = (
    f"{CONSOLIDATION_CHECKPOINT.as_posix()}::"
    "test_story_0535_slice_consolidation"
)
AUTOMATION_PATH = Path(
    "tools/quality/contexts/engineering_governance"
) / SLUG / "validator.py"
EXPECTED_ALLOW_PATHS = (
    ".codex/tasks/TASK-0537.json",
    f"tools/governance/{SLUG}/**",
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/**",
    "evidence/implementation/epic-086/story-0537/**",
)
EXPECTED_DEPENDENCIES = ("STORY-0535", "STORY-0536")
EXPECTED_TEST = "test_epic_086_integracao"
EXPECTED_AC_IDS = tuple(f"AC-ISSUE-0647-{index:02d}" for index in range(1, 5))
EXPECTED_AUTOMATION_AC_IDS = tuple(
    f"AC-ISSUE-0646-{index:02d}" for index in range(1, 5)
)
EXPECTED_REQUIREMENTS = (
    "REQ-DEL-001",
    "REQ-DEL-002",
    "REQ-EPIC-001",
    "REQ-ISM-003",
    "REQ-SPRINT-001-001",
    "REQ-SPRINT-001-002",
    "REQ-SPRINT-001-003",
    "REQ-SPRINT-001-004",
    "REQ-SPRINT-001-005",
    "REQ-SPRINT-001-006",
    "REQ-SPRINT-001-007",
    "REQ-SPRINT-001-008",
    "REQ-SPRINT-001-009",
    "REQ-SPRINT-001-010",
)
EXPECTED_AUTOMATION_REQUIREMENTS = {
    "REQ-EPIC-001": "test_executable_foundation_gate_clean_room_end_to_end",
    "REQ-SPRINT-001-004": "test_sprint_zero_baseline_decision_04",
}
EXPECTED_FLOW = (
    "FRONTEND",
    "API",
    "POSTGRESQL",
    "RABBITMQ_CELERY",
    "WORKER",
    "DIAGNOSTIC_ARTIFACT",
)


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
        "task_id": "TASK-0537",
        "issue_id": "ISSUE-0647",
        "story_id": "STORY-0537",
        "epic_id": "EPIC-086",
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
            findings.append(
                Finding("TASK_SCOPE_INVALID", field, "governed values drifted")
            )
    phase_f = task.get("phase_f_review")
    phase_files = phase_f.get("files") if isinstance(phase_f, Mapping) else None
    phase_paths = (
        phase_files.get("allow_paths")
        if isinstance(phase_files, Mapping)
        else None
    )
    if not isinstance(phase_paths, list) or tuple(phase_paths) != EXPECTED_ALLOW_PATHS:
        findings.append(
            Finding(
                "TASK_SCOPE_INVALID",
                "phase_f_review.files",
                "allow-path parity required",
            )
        )
    return findings


def _environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment.update(
        {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"}
    )
    return environment


def _run_consolidation(root: Path) -> tuple[str, int]:
    command = [
        sys.executable,
        "-B",
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        CONSOLIDATION_TEST,
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            env=_environment(),
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return completed.stdout + completed.stderr, completed.returncode
    except (OSError, UnicodeError, subprocess.TimeoutExpired) as error:
        return str(error), -1


def _run_automation(root: Path) -> tuple[object, int]:
    command = [
        sys.executable,
        "-B",
        str(root / AUTOMATION_PATH),
        "--repository-root",
        str(root),
        "--dry-run",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            env=_environment(),
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return json.loads(completed.stdout), completed.returncode
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        subprocess.TimeoutExpired,
    ) as error:
        return {"execution_error": str(error)}, -1


def _consolidation_findings(output: str, returncode: int) -> list[Finding]:
    if returncode == 0:
        return []
    detail = output.strip().splitlines()[-1] if output.strip() else "no output"
    return [
        Finding(
            "CONSOLIDATION_CHECKPOINT_FAILED",
            CONSOLIDATION_TEST,
            f"returncode={returncode}; {detail}",
        )
    ]


def _automation_findings(report: object, returncode: int) -> list[Finding]:
    acceptance = report.get("acceptance_evidence") if isinstance(report, Mapping) else None
    valid = bool(
        returncode == 0
        and isinstance(report, Mapping)
        and report.get("status") == "PASS"
        and report.get("mode") == "DRY_RUN"
        and report.get("repository_mutation_performed") is False
        and report.get("output_write_performed") is False
        and report.get("flow") == list(EXPECTED_FLOW)
        and report.get("requirement_evidence") == EXPECTED_AUTOMATION_REQUIREMENTS
        and acceptance
        == dict.fromkeys(EXPECTED_AUTOMATION_AC_IDS, "test_epic_086_automacao")
        and report.get("findings") == []
    )
    if valid:
        return []
    return [
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
    consolidation_output, consolidation_code = _run_consolidation(root)
    findings.extend(_consolidation_findings(consolidation_output, consolidation_code))
    automation_report, automation_code = _run_automation(root)
    findings.extend(_automation_findings(automation_report, automation_code))
    return tuple(sorted(set(findings)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0647 integration")
    parser.add_argument(
        "--repository-root", type=Path, default=Path(__file__).resolve().parents[3]
    )
    args = parser.parse_args(argv)
    try:
        findings = validate_repository_integration(args.repository_root)
    except Exception as error:  # CLI boundary must fail closed deterministically.
        findings = (Finding("INTEGRATION_INTERNAL_ERROR", ".", str(error)),)
    report = {
        "acceptance_evidence": dict.fromkeys(EXPECTED_AC_IDS, EXPECTED_TEST),
        "control_plane": "SUBPROCESS_READ_ONLY",
        "dependencies": list(EXPECTED_DEPENDENCIES),
        "diagnostic_artifact": "AUTOMATION_REPORT_JSON",
        "findings": [finding.as_dict() for finding in findings],
        "flow": list(EXPECTED_FLOW),
        "issue": "ISSUE-0647",
        "requirement_evidence": dict.fromkeys(EXPECTED_REQUIREMENTS, EXPECTED_TEST),
        "schema_version": "1.0.0",
        "status": "FAIL" if findings else "PASS",
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
