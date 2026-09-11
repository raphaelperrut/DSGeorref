from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

CONTRACT_ROOT = Path(
    "contracts/contexts/engineering_governance/fnd/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw"
)
MANIFEST_PATH = CONTRACT_ROOT / "contract-manifest.yaml"
SCHEMA_PATH = CONTRACT_ROOT / "walking-skeleton.schema.json"
PROFILE_PATH = CONTRACT_ROOT / "examples/walking-skeleton.json"
TASK_PATH = Path(".codex/tasks/TASK-0536.json")
TEST_PATH = Path(
    "tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/"
    "test_automation.py"
)
WORKFLOW_PATH = Path(
    ".github/workflows/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw.yaml"
)
EXPECTED_REQUIREMENTS = {
    "REQ-EPIC-001": "test_executable_foundation_gate_clean_room_end_to_end",
    "REQ-SPRINT-001-004": "test_sprint_zero_baseline_decision_04",
}
EXPECTED_ACCEPTANCE_IDS = tuple(f"AC-ISSUE-0646-{index:02d}" for index in range(1, 5))
EXPECTED_ALLOW_PATHS = {
    "tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/**",
    "tools/quality/contexts/engineering_governance/"
    "walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/**",
    ".github/workflows/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw.yaml",
}
EXPECTED_STAGES = (
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
    path: str
    message: str
    remediation: str


def _load(path: Path, root: Path, *, yaml_document: bool = False) -> Any | None:
    try:
        text = (root / path).read_text(encoding="utf-8")
        return yaml.safe_load(text) if yaml_document else json.loads(text)
    except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError):
        return None


def _finding(code: str, path: Path, message: str, remediation: str) -> Finding:
    return Finding(code, path.as_posix(), message, remediation)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def _validate_contract(
    manifest: Any, schema: Any, profile: Any
) -> list[Finding]:
    findings: list[Finding] = []
    if not all(isinstance(value, dict) for value in (manifest, schema, profile)):
        return findings
    expected_contract = {
        "schema": SCHEMA_PATH.as_posix(),
        "example": PROFILE_PATH.as_posix(),
    }
    manifest_identity_valid = (
        manifest.get("schema_version") == "1.0.0"
        and manifest.get("contract_version") == "1.0.0"
        and manifest.get("status") == "FROZEN"
    )
    if not manifest_identity_valid or manifest.get("contract") != {
        "id": "walking-skeleton-foundation-contract", **expected_contract
    }:
        findings.append(_finding(
            "CONTRACT_MANIFEST_INVALID", MANIFEST_PATH,
            "The frozen manifest does not bind the canonical schema and example.",
            "Restore the STORY-0534 frozen manifest before running this gate.",
        ))
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(Draft202012Validator(schema).iter_errors(profile), key=str)
    except SchemaError:
        errors = [None]
    if errors:
        detail = "schema itself is invalid" if errors[0] is None else errors[0].message
        findings.append(_finding(
            "PROFILE_SCHEMA_INVALID", PROFILE_PATH, detail,
            "Correct the profile or publish an approved, versioned contract revision.",
        ))
    return findings


def _validate_traceability(manifest: Any, profile: Any, root: Path) -> list[Finding]:
    if not isinstance(manifest, dict) or not isinstance(profile, dict):
        return []
    items = manifest.get("traceability", {}).get("requirements", [])
    actual = {
        item.get("id"): item.get("evidence")
        for item in items
        if isinstance(item, dict)
    }
    test_text = "\n".join(_read_text(path) for path in (root / "tests").rglob("test_*.py"))
    valid = actual == EXPECTED_REQUIREMENTS and set(profile.get("requirement_ids", [])) == set(
        EXPECTED_REQUIREMENTS
    )
    valid = valid and all(f"def {test_id}(" in test_text for test_id in actual.values())
    if valid:
        return []
    return [_finding(
        "REQUIREMENT_EVIDENCE_INVALID", MANIFEST_PATH,
        "Requirement-to-test evidence is missing, changed, or does not resolve.",
        "Restore both required requirement IDs and their executable test checkpoints.",
    )]


def _openapi_operations(document: Any) -> set[str]:
    if not isinstance(document, dict):
        return set()
    operations: set[str] = set()
    for path_item in document.get("paths", {}).values():
        if not isinstance(path_item, dict):
            continue
        for operation in path_item.values():
            if isinstance(operation, dict) and isinstance(operation.get("operationId"), str):
                operations.add(operation["operationId"])
    return operations


def _validate_sources(profile: Any, root: Path) -> list[Finding]:
    if not isinstance(profile, dict) or not isinstance(profile.get("contract_sources"), dict):
        return []
    findings: list[Finding] = []
    sources = profile["contract_sources"]
    for name, value in sources.items():
        if name != "operations" and isinstance(value, str) and not (root / value).is_file():
            findings.append(_finding(
                "CONTRACT_SOURCE_MISSING", Path(value), f"Contract source '{name}' is absent.",
                "Restore the versioned source; this gate never substitutes a fallback.",
            ))
    openapi = _load(Path(str(sources.get("http", ""))), root, yaml_document=True)
    required_operations = set(sources.get("operations", []))
    missing = sorted(required_operations - _openapi_operations(openapi))
    if missing:
        findings.append(_finding(
            "HTTP_OPERATION_MISSING", Path(str(sources.get("http", ""))),
            f"Required operationIds are absent: {', '.join(missing)}.",
            "Restore the frozen operationIds or revise the contract through its owner.",
        ))
    return findings


def _validate_automation_wiring(task: Any, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    test_text = _read_text(root / TEST_PATH)
    workflow = _read_text(root / WORKFLOW_PATH)
    task_valid = (
        isinstance(task, dict)
        and tuple(task.get("acceptance_criterion_ids", [])) == EXPECTED_ACCEPTANCE_IDS
    )
    task_valid = task_valid and task.get("tests") == ["test_epic_086_automacao"]
    task_valid = task_valid and set(task.get("allow_paths", [])) >= EXPECTED_ALLOW_PATHS
    phase_f_paths = task.get("phase_f_review", {}).get("files", {}).get("allow_paths", [])
    task_valid = task_valid and set(phase_f_paths) >= EXPECTED_ALLOW_PATHS
    if not task_valid or "def test_epic_086_automacao(" not in test_text:
        findings.append(_finding(
            "AUTOMATION_EVIDENCE_MISSING", TEST_PATH,
            "Task acceptance IDs are not bound to the required executable test.",
            "Restore TASK-0536 traceability and test_epic_086_automacao.",
        ))
    fragments = (
        "permissions:\n  contents: read",
        "validator.py",
        "--dry-run",
        "--output",
        "test_epic_086_automacao",
        "actions/upload-artifact@v4",
    )
    if any(fragment not in workflow for fragment in fragments):
        findings.append(_finding(
            "WORKFLOW_CONTROL_MISSING", WORKFLOW_PATH,
            "The read-only CI gate, dry-run, focused test, or diagnostic artifact is not wired.",
            "Restore the scoped workflow controls required by TASK-0536.",
        ))
    return findings


def validate_repository(root: Path) -> list[Finding]:
    inputs = (
        (MANIFEST_PATH, True),
        (SCHEMA_PATH, False),
        (PROFILE_PATH, False),
        (TASK_PATH, False),
    )
    loaded: list[Any] = []
    findings: list[Finding] = []
    for path, yaml_document in inputs:
        value = _load(path, root, yaml_document=yaml_document)
        loaded.append(value)
        if value is None:
            findings.append(_finding(
                "INPUT_UNREADABLE", path, "Required input is absent or malformed.",
                "Restore a readable, versioned input; validation stops closed.",
            ))
    manifest, schema, profile, task = loaded
    findings.extend(_validate_contract(manifest, schema, profile))
    findings.extend(_validate_traceability(manifest, profile, root))
    findings.extend(_validate_sources(profile, root))
    findings.extend(_validate_automation_wiring(task, root))
    return sorted(set(findings))


def build_report(root: Path, *, dry_run: bool) -> dict[str, Any]:
    findings = validate_repository(root)
    digest_paths = (MANIFEST_PATH, SCHEMA_PATH, PROFILE_PATH, TASK_PATH, TEST_PATH, WORKFLOW_PATH)
    digests: dict[str, str] = {}
    for path in digest_paths:
        try:
            digests[path.as_posix()] = hashlib.sha256((root / path).read_bytes()).hexdigest()
        except OSError:
            continue
    return {
        "schema_version": "1.0.0",
        "status": "PASS" if not findings else "FAIL",
        "mode": "DRY_RUN" if dry_run else "VALIDATE",
        "repository_mutation_performed": False,
        "flow": list(EXPECTED_STAGES),
        "requirement_evidence": EXPECTED_REQUIREMENTS,
        "acceptance_evidence": dict.fromkeys(EXPECTED_ACCEPTANCE_IDS, "test_epic_086_automacao"),
        "input_sha256": digests,
        "findings": [asdict(finding) for finding in findings],
    }


def _serialize(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the walking-skeleton delivery gate.")
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("-"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    report = build_report(args.repository_root.resolve(), dry_run=args.dry_run)
    report["requested_output"] = args.output.as_posix()
    report["output_write_performed"] = not args.dry_run and args.output != Path("-")
    payload = _serialize(report)
    if args.output == Path("-") or args.dry_run:
        print(payload, end="")
    else:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            temporary = args.output.with_name(f".{args.output.name}.tmp")
            temporary.write_text(payload, encoding="utf-8", newline="\n")
            temporary.replace(args.output)
        except OSError as error:
            report["status"] = "FAIL"
            report["output_write_performed"] = False
            report["findings"].append(asdict(_finding(
                "OUTPUT_WRITE_FAILED", args.output, str(error),
                "Choose a writable output path or run with --dry-run.",
            )))
            print(_serialize(report), end="")
            return 2
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
