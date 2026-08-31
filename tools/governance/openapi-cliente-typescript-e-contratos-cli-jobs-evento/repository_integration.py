from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SLUG = "openapi-cliente-typescript-e-contratos-cli-jobs-evento"
TASK_PATH = Path(".codex/tasks/TASK-0019.json")
REQUIREMENT_PATH = Path(
    "docs/01-product/requirements/"
    "REQ-FS1-006-usar-homografia-canonica-e-usac-magsac-sem-fallback-silencioso.md"
)
RUNTIME_PROFILE_PATH = Path(
    "contracts/contexts/engineering_governance/fnd/"
    f"{SLUG}/runtime-scm-tool-parte-2/examples/runtime-schema-conformance.json"
)
QUALITY_VALIDATOR_PATH = Path(
    f"tools/quality/contexts/engineering_governance/{SLUG}/validator.py"
)
WORKFLOW_PATH = Path(f".github/workflows/{SLUG}.yaml")
EXPECTED_ALLOW_PATHS = (
    f"tools/governance/{SLUG}/**",
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/**",
    "evidence/implementation/epic-004/story-0019/**",
)
EXPECTED_CONTRACTS = (
    "contracts/artifacts/artifact-set-manifest.schema.json",
    (
        "contracts/contexts/engineering_governance/fnd/"
        f"{SLUG}/crs-dbschema-epic-parte-1/contract-foundation.schema.json"
    ),
    "contracts/domain/failure-diagnostic.schema.json",
    "contracts/domain/processing-plan.schema.json",
    "contracts/domain/quality-report.schema.json",
    "contracts/events/job-event.schema.json",
    "contracts/http/openapi.yaml",
)
EXPECTED_TESTS = (
    "test_first_functional_slice_decision_06",
    "test_epic_004_integracao",
)
EXPECTED_AC_IDS = tuple(f"AC-ISSUE-0129-{number:02d}" for number in range(1, 5))


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    artifact: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"artifact": self.artifact, "code": self.code, "detail": self.detail}


def _load_json(root: Path, path: Path) -> tuple[Mapping[str, Any] | None, list[Finding]]:
    try:
        value = json.loads((root / path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [Finding("DOCUMENT_INVALID", path.as_posix(), str(error))]
    if not isinstance(value, Mapping):
        return None, [Finding("DOCUMENT_INVALID", path.as_posix(), "object required")]
    return value, []


def _task_findings(task: Mapping[str, Any]) -> list[Finding]:
    expected = {
        "task_id": "TASK-0019",
        "issue_id": "ISSUE-0129",
        "story_id": "STORY-0019",
        "epic_id": "EPIC-004",
        "role": "Tech Lead",
        "bounded_context": "BC-001",
    }
    findings = [
        Finding("TASK_IDENTITY_INVALID", field, f"expected {value}")
        for field, value in expected.items()
        if task.get(field) != value
    ]
    exact_lists = {
        "allow_paths": EXPECTED_ALLOW_PATHS,
        "deny_paths": ("src/**/epic-*", "src/**/issue-*"),
        "tests": EXPECTED_TESTS,
        "dependencies": ("STORY-0017", "STORY-0018"),
        "acceptance_criterion_ids": EXPECTED_AC_IDS,
    }
    for field, expected_values in exact_lists.items():
        actual = task.get(field)
        if not isinstance(actual, list) or tuple(actual) != expected_values:
            findings.append(Finding("TASK_SCOPE_INVALID", field, "governed values drifted"))
    review = task.get("phase_f_review")
    files = review.get("files") if isinstance(review, Mapping) else None
    phase_allow_paths = files.get("allow_paths") if isinstance(files, Mapping) else None
    if not isinstance(phase_allow_paths, list) or tuple(phase_allow_paths) != EXPECTED_ALLOW_PATHS:
        findings.append(Finding("TASK_SCOPE_INVALID", "phase_f_review.files", "scope drift"))
    return findings


def _requirement_binding_findings(
    task: Mapping[str, Any], requirement_text: str, runtime: Mapping[str, Any]
) -> list[Finding]:
    references = task.get("references")
    expected_reference = REQUIREMENT_PATH.as_posix()
    required_tokens = (
        "REQ-FS1-006",
        "usar homografia canônica e USAC_MAGSAC sem fallback silencioso",
        "test_first_functional_slice_decision_06",
        "Owner normativo:** `ADR-045`",
    )
    findings: list[Finding] = []
    if not isinstance(references, list) or expected_reference not in references:
        findings.append(Finding("REQ_FS1_006_UNBOUND", TASK_PATH.as_posix(), expected_reference))
    if any(token not in requirement_text for token in required_tokens):
        findings.append(
            Finding("REQ_FS1_006_UNBOUND", REQUIREMENT_PATH.as_posix(), "canonical text drift")
        )
    findings.extend(_runtime_control_findings(runtime))
    return findings


def _runtime_control_findings(runtime: Mapping[str, Any]) -> list[Finding]:
    controls = runtime.get("controls")
    http = controls.get("http_adapter") if isinstance(controls, Mapping) else None
    composition = (
        controls.get("processing_plan_composition")
        if isinstance(controls, Mapping)
        else None
    )
    forbidden = http.get("forbidden_direct_dependencies") if isinstance(http, Mapping) else None
    bypass = composition.get("gate_bypass") if isinstance(composition, Mapping) else None
    fail_closed = (
        isinstance(forbidden, list)
        and "GEOSPATIAL_ALGORITHM" in forbidden
        and isinstance(bypass, Mapping)
        and bool(bypass)
        and all(value is False for value in bypass.values())
        and composition.get("unregistered_capability") == "REJECT"
    )
    if not fail_closed:
        return [
            Finding(
                "REQ_FS1_006_FAIL_CLOSED_INVALID",
                RUNTIME_PROFILE_PATH.as_posix(),
                "governance must delegate geometry and prohibit gate bypass",
            )
        ]
    return []


def validate_requirement_evidence(repository_root: Path) -> tuple[Finding, ...]:
    root = repository_root.resolve()
    task, findings = _load_json(root, TASK_PATH)
    runtime, runtime_findings = _load_json(root, RUNTIME_PROFILE_PATH)
    findings.extend(runtime_findings)
    try:
        requirement_text = (root / REQUIREMENT_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        findings.append(Finding("DOCUMENT_INVALID", REQUIREMENT_PATH.as_posix(), str(error)))
        requirement_text = ""
    if task is not None and runtime is not None:
        findings.extend(_requirement_binding_findings(task, requirement_text, runtime))
    return tuple(sorted(set(findings)))


def _quality_report_findings(report: object, returncode: int) -> list[Finding]:
    if not isinstance(report, Mapping):
        return [Finding("QUALITY_VALIDATOR_INVALID", QUALITY_VALIDATOR_PATH.as_posix(), "object required")]
    raw_findings = report.get("findings")
    contracts = report.get("contracts")
    valid = (
        returncode == 0
        and report.get("status") == "PASS"
        and report.get("mode") == "DRY_RUN"
        and report.get("destructive_actions") == 0
        and raw_findings == []
        and isinstance(contracts, list)
        and tuple(contracts) == EXPECTED_CONTRACTS
    )
    if valid:
        return []
    return [
        Finding(
            "QUALITY_VALIDATION_FAILED",
            QUALITY_VALIDATOR_PATH.as_posix(),
            f"returncode={returncode} status={report.get('status')}",
        )
    ]


def _quality_findings(root: Path) -> list[Finding]:
    environment = os.environ.copy()
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"})
    command = [
        sys.executable,
        "-B",
        str(root / QUALITY_VALIDATOR_PATH),
        "--repository-root",
        str(root),
        "--dry-run",
    ]
    try:
        completed = subprocess.run(
            command, cwd=root, env=environment, check=False, capture_output=True, text=True
        )
        report = json.loads(completed.stdout)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [Finding("QUALITY_VALIDATOR_INVALID", QUALITY_VALIDATOR_PATH.as_posix(), str(error))]
    return _quality_report_findings(report, completed.returncode)


def _workflow_findings(root: Path) -> list[Finding]:
    try:
        workflow = (root / WORKFLOW_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [Finding("CONTROL_PLANE_INVALID", WORKFLOW_PATH.as_posix(), str(error))]
    required = (
        QUALITY_VALIDATOR_PATH.as_posix(),
        "--dry-run",
        "test_automation.py::test_epic_004_automacao",
        "contents: read",
    )
    missing = [token for token in required if token not in workflow]
    return [] if not missing else [
        Finding("CONTROL_PLANE_INVALID", WORKFLOW_PATH.as_posix(), ",".join(missing))
    ]


def validate_repository_integration(repository_root: Path) -> tuple[Finding, ...]:
    root = repository_root.resolve()
    task, findings = _load_json(root, TASK_PATH)
    if task is not None:
        findings.extend(_task_findings(task))
    findings.extend(validate_requirement_evidence(root))
    findings.extend(_workflow_findings(root))
    findings.extend(_quality_findings(root))
    return tuple(sorted(set(findings)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0129 repository integration")
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args(argv)
    findings = validate_repository_integration(args.repository_root)
    report = {
        "acceptance_criteria": list(EXPECTED_AC_IDS),
        "contracts": list(EXPECTED_CONTRACTS),
        "findings": [finding.as_dict() for finding in findings],
        "issue": "ISSUE-0129",
        "requirement": "REQ-FS1-006",
        "status": "FAIL" if findings else "PASS",
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
