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

SLUG = "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca"
TASK_PATH = Path(".codex/tasks/TASK-0029.json")
CATALOG_PATH = Path(
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/capability-catalog.json"
)
FOUNDATION_VALIDATOR_PATH = Path(f"tools/governance/{SLUG}/validate_catalog.py")
AUTOMATION_VALIDATOR_PATH = Path(
    f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py"
)
EXPECTED_ALLOW_PATHS = (
    ".codex/tasks/TASK-0029.json",
    f"tools/governance/{SLUG}/**",
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/**",
    f"tests/fnd/{SLUG}/test_foundation.py",
    "evidence/implementation/epic-006/story-0029/**",
)
EXPECTED_DEPENDENCIES = ("STORY-0027", "STORY-0028")
EXPECTED_TESTS = ("test_epic_006_integracao",)
EXPECTED_AC_IDS = tuple(f"AC-ISSUE-0139-{index:02d}" for index in range(1, 5))
EXPECTED_AUTOMATION_AC_IDS = tuple(
    f"AC-ISSUE-0138-{index:02d}" for index in range(1, 5)
)
EXPECTED_REQUIREMENTS = ("REQ-AI-007", "REQ-TST-001")


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    artifact: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"artifact": self.artifact, "code": self.code, "detail": self.detail}


def _load_json(root: Path, relative: Path) -> tuple[Mapping[str, Any] | None, list[Finding]]:
    try:
        loaded = json.loads((root / relative).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [Finding("DOCUMENT_INVALID", relative.as_posix(), str(error))]
    if not isinstance(loaded, Mapping):
        return None, [Finding("DOCUMENT_INVALID", relative.as_posix(), "object required")]
    return loaded, []


def _task_findings(task: Mapping[str, Any]) -> list[Finding]:
    expected_scalars = {
        "task_id": "TASK-0029",
        "issue_id": "ISSUE-0139",
        "story_id": "STORY-0029",
        "epic_id": "EPIC-006",
        "role": "Tech Lead",
        "bounded_context": "BC-001",
        "requirement_basis": "DERIVED_CONTROL",
    }
    findings = [
        Finding("TASK_IDENTITY_INVALID", field, f"expected {value}")
        for field, value in expected_scalars.items()
        if task.get(field) != value
    ]
    expected_lists: dict[str, Sequence[str]] = {
        "allow_paths": EXPECTED_ALLOW_PATHS,
        "deny_paths": ("src/**/epic-*", "src/**/issue-*"),
        "tests": EXPECTED_TESTS,
        "dependencies": EXPECTED_DEPENDENCIES,
        "acceptance_criterion_ids": EXPECTED_AC_IDS,
    }
    for field, expected in expected_lists.items():
        actual = task.get(field)
        if not isinstance(actual, list) or tuple(actual) != tuple(expected):
            findings.append(Finding("TASK_SCOPE_INVALID", field, "governed values drifted"))
    phase_f = task.get("phase_f_review")
    phase_files = phase_f.get("files") if isinstance(phase_f, Mapping) else None
    phase_allow_paths = (
        phase_files.get("allow_paths") if isinstance(phase_files, Mapping) else None
    )
    if (
        not isinstance(phase_files, Mapping)
        or not isinstance(phase_allow_paths, list)
        or tuple(phase_allow_paths) != EXPECTED_ALLOW_PATHS
    ):
        findings.append(
            Finding("TASK_SCOPE_INVALID", "phase_f_review.files", "allow-path parity required")
        )
    return findings


def _requirement_findings(catalog: Mapping[str, Any]) -> list[Finding]:
    evidence = catalog.get("requirement_evidence")
    if not isinstance(evidence, Mapping) or tuple(sorted(evidence)) != EXPECTED_REQUIREMENTS:
        return [
            Finding(
                "REQUIREMENT_EVIDENCE_INVALID",
                CATALOG_PATH.as_posix(),
                "REQ-AI-007 and REQ-TST-001 evidence required",
            )
        ]
    if any(
        not isinstance(evidence[item], str) or not evidence[item]
        for item in EXPECTED_REQUIREMENTS
    ):
        return [
            Finding(
                "REQUIREMENT_EVIDENCE_INVALID",
                CATALOG_PATH.as_posix(),
                "each linked requirement must name executable evidence",
            )
        ]
    return []


def _run_report(root: Path, relative: Path, arguments: Sequence[str]) -> tuple[object, int]:
    environment = os.environ.copy()
    environment.update(
        {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"}
    )
    command = [sys.executable, "-B", str(root / relative), *arguments]
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout), completed.returncode
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return {"execution_error": str(error)}, -1


def _foundation_report_findings(report: object, returncode: int) -> list[Finding]:
    valid = bool(
        isinstance(report, Mapping)
        and returncode == 0
        and report.get("status") == "PASS"
        and report.get("findings") == []
    )
    return [] if valid else [
        Finding(
            "FOUNDATION_VALIDATION_FAILED",
            FOUNDATION_VALIDATOR_PATH.as_posix(),
            f"returncode={returncode}",
        )
    ]


def _automation_report_findings(report: object, returncode: int) -> list[Finding]:
    requirements = report.get("requirement_evidence") if isinstance(report, Mapping) else None
    acceptance = report.get("acceptance_evidence") if isinstance(report, Mapping) else None
    valid = bool(
        isinstance(report, Mapping)
        and returncode == 0
        and report.get("status") == "PASS"
        and report.get("mode") == "DRY_RUN"
        and report.get("destructive_actions") == 0
        and report.get("findings") == []
        and report.get("automation") == "EPIC-006_CAPABILITY_CATALOG_CONTROLS"
        and isinstance(requirements, Mapping)
        and tuple(sorted(requirements)) == EXPECTED_REQUIREMENTS
        and acceptance
        == dict.fromkeys(EXPECTED_AUTOMATION_AC_IDS, "test_epic_006_automacao")
    )
    return [] if valid else [
        Finding(
            "AUTOMATION_VALIDATION_FAILED",
            AUTOMATION_VALIDATOR_PATH.as_posix(),
            f"returncode={returncode}",
        )
    ]


def validate_repository_integration(repository_root: Path) -> tuple[Finding, ...]:
    root = repository_root.resolve()
    task, findings = _load_json(root, TASK_PATH)
    catalog, catalog_findings = _load_json(root, CATALOG_PATH)
    findings.extend(catalog_findings)
    if task is not None:
        findings.extend(_task_findings(task))
    if catalog is not None:
        findings.extend(_requirement_findings(catalog))
    foundation_report, foundation_code = _run_report(root, FOUNDATION_VALIDATOR_PATH, ())
    findings.extend(_foundation_report_findings(foundation_report, foundation_code))
    automation_report, automation_code = _run_report(
        root,
        AUTOMATION_VALIDATOR_PATH,
        ("--repository-root", str(root), "--dry-run"),
    )
    findings.extend(_automation_report_findings(automation_report, automation_code))
    return tuple(sorted(set(findings)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0139 repository integration")
    parser.add_argument(
        "--repository-root", type=Path, default=Path(__file__).resolve().parents[3]
    )
    args = parser.parse_args(argv)
    try:
        findings = validate_repository_integration(args.repository_root)
    except Exception as error:  # CLI boundary must fail closed with one stable report.
        findings = (Finding("INTEGRATION_INTERNAL_ERROR", ".", str(error)),)
    report = {
        "acceptance_evidence": dict.fromkeys(EXPECTED_AC_IDS, EXPECTED_TESTS[0]),
        "control_plane": "SUBPROCESS_READ_ONLY",
        "dependencies": list(EXPECTED_DEPENDENCIES),
        "findings": [finding.as_dict() for finding in findings],
        "issue": "ISSUE-0139",
        "requirement_evidence": dict.fromkeys(EXPECTED_REQUIREMENTS, EXPECTED_TESTS[0]),
        "status": "FAIL" if findings else "PASS",
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
