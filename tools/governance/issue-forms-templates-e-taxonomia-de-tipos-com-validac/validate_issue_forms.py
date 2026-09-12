from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

SLUG = "issue-forms-templates-e-taxonomia-de-tipos-com-validac"
TASK_PATH = Path(".codex/tasks/TASK-0556.json")
CONTRACT_PATH = Path(
    "contracts/contexts/engineering_governance/fnd"
    f"/{SLUG}/examples/issue-form-governance.json"
)
REGISTRY_PATH = Path(
    "docs/03-engineering/contexts/engineering_governance"
    f"/{SLUG}/issue-form-registry.json"
)
TEMPLATE_ROOT = Path(".github/ISSUE_TEMPLATE")
WORKFLOW_PATH = Path(".github/workflows/issue-form-governance.yaml")
EXPECTED_COMMAND = (
    f"python tools/governance/{SLUG}/validate_issue_forms.py --repository-root ."
)
EXPECTED_ALLOW_PATHS = (
    ".codex/tasks/TASK-0556.json",
    ".github/ISSUE_TEMPLATE/**",
    ".github/workflows/issue-form-governance.yaml",
    f"tools/governance/{SLUG}/**",
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/**",
    f"tests/fnd/{SLUG}/test_foundation.py",
    "evidence/implementation/epic-090/story-0556/**",
)
EXPECTED_TESTS = (
    "test_issue_form_required_acceptance_risk_test_rollback_fields",
    "test_epic_090_fundacao",
)
EXPECTED_AC_IDS = tuple(f"AC-ISSUE-0666-{index:02d}" for index in range(1, 5))


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    artifact: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"artifact": self.artifact, "code": self.code, "detail": self.detail}


def _load_json(path: Path, artifact: str) -> tuple[dict[str, Any] | None, list[Finding]]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [Finding("DOCUMENT_INVALID", artifact, str(error))]
    if not isinstance(loaded, dict):
        return None, [Finding("DOCUMENT_INVALID", artifact, "object required")]
    return loaded, []


def _load_yaml(path: Path, artifact: str) -> tuple[dict[str, Any] | None, list[Finding]]:
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return None, [Finding("DOCUMENT_INVALID", artifact, str(error))]
    if not isinstance(loaded, dict):
        return None, [Finding("DOCUMENT_INVALID", artifact, "object required")]
    return loaded, []


def _task_findings(task: Mapping[str, Any]) -> list[Finding]:
    expected_scalars = {
        "task_id": "TASK-0556",
        "issue_id": "ISSUE-0666",
        "story_id": "STORY-0556",
        "epic_id": "EPIC-090",
        "role": "Tech Lead",
        "bounded_context": "BC-001",
    }
    findings = [
        Finding("TASK_IDENTITY_INVALID", field, f"expected {expected}")
        for field, expected in expected_scalars.items()
        if task.get(field) != expected
    ]
    expected_lists: dict[str, Sequence[str]] = {
        "allow_paths": EXPECTED_ALLOW_PATHS,
        "tests": EXPECTED_TESTS,
        "dependencies": ("STORY-0555",),
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
    if not isinstance(phase_allow_paths, list) or tuple(phase_allow_paths) != EXPECTED_ALLOW_PATHS:
        findings.append(
            Finding("TASK_SCOPE_INVALID", "phase_f_review.files", "allow-path parity required")
        )
    return findings


def _contract_forms(contract: Mapping[str, Any]) -> tuple[dict[str, dict[str, Any]], list[Finding]]:
    taxonomy = contract.get("issue_taxonomy")
    raw_forms = taxonomy.get("types") if isinstance(taxonomy, Mapping) else None
    if not isinstance(raw_forms, list):
        return {}, [Finding("CONTRACT_INVALID", CONTRACT_PATH.as_posix(), "types required")]

    forms: dict[str, dict[str, Any]] = {}
    for raw_form in raw_forms:
        if not isinstance(raw_form, dict):
            return {}, [
                Finding("CONTRACT_INVALID", CONTRACT_PATH.as_posix(), "form object required")
            ]
        issue_type = raw_form.get("type")
        if not isinstance(issue_type, str) or issue_type in forms:
            return {}, [
                Finding("CONTRACT_INVALID", CONTRACT_PATH.as_posix(), "unique type required")
            ]
        forms[issue_type] = raw_form
    return forms, []


def _registry_forms(registry: Mapping[str, Any]) -> tuple[dict[str, dict[str, Any]], list[Finding]]:
    raw_forms = registry.get("forms")
    if not isinstance(raw_forms, list):
        return {}, [Finding("REGISTRY_INVALID", REGISTRY_PATH.as_posix(), "forms required")]

    forms: dict[str, dict[str, Any]] = {}
    for raw_form in raw_forms:
        if not isinstance(raw_form, dict):
            return {}, [
                Finding("REGISTRY_INVALID", REGISTRY_PATH.as_posix(), "form object required")
            ]
        issue_type = raw_form.get("type")
        if not isinstance(issue_type, str) or issue_type in forms:
            return {}, [
                Finding("REGISTRY_INVALID", REGISTRY_PATH.as_posix(), "unique type required")
            ]
        forms[issue_type] = raw_form
    return forms, []


def _registry_findings(
    contract: Mapping[str, Any], registry: Mapping[str, Any]
) -> tuple[dict[str, dict[str, Any]], list[Finding]]:
    findings: list[Finding] = []
    for field in ("schema_version", "contract_id", "contract_version"):
        if registry.get(field) != contract.get(field):
            findings.append(
                Finding("REGISTRY_CONTRACT_DRIFT", REGISTRY_PATH.as_posix(), field)
            )

    contract_forms, contract_findings = _contract_forms(contract)
    registry_forms, registry_findings = _registry_forms(registry)
    findings.extend(contract_findings)
    findings.extend(registry_findings)
    if findings:
        return {}, findings
    if set(registry_forms) != set(contract_forms):
        findings.append(
            Finding("ISSUE_TYPE_INVALID", REGISTRY_PATH.as_posix(), "taxonomy mismatch")
        )
        return {}, findings

    for issue_type, expected in contract_forms.items():
        registered = registry_forms[issue_type]
        required_fields = registered.get("required_fields")
        expected_fields = expected.get("required_fields")
        if registered.get("template") != expected.get("template"):
            findings.append(
                Finding("REGISTRY_CONTRACT_DRIFT", issue_type, "template mismatch")
            )
        if not isinstance(required_fields, dict) or not isinstance(expected_fields, list):
            findings.append(
                Finding("REGISTRY_INVALID", issue_type, "required field mapping missing")
            )
        elif set(required_fields) != set(expected_fields) or any(
            not isinstance(body_id, str) or not body_id for body_id in required_fields.values()
        ):
            findings.append(
                Finding("REGISTRY_CONTRACT_DRIFT", issue_type, "required fields mismatch")
            )
    return registry_forms, findings


def form_document_findings(
    template: str, document: Mapping[str, Any], field_mapping: Mapping[str, Any]
) -> list[Finding]:
    findings: list[Finding] = []
    allowed_top_level = {"name", "description", "title", "labels", "assignees", "body"}
    if set(document) - allowed_top_level:
        findings.append(Finding("FORM_STRUCTURE_INVALID", template, "unknown top-level key"))
    if not isinstance(document.get("name"), str) or not isinstance(
        document.get("description"), str
    ):
        findings.append(
            Finding("FORM_STRUCTURE_INVALID", template, "name and description required")
        )

    body = document.get("body")
    if not isinstance(body, list):
        findings.append(Finding("FORM_STRUCTURE_INVALID", template, "body required"))
        return findings
    controls: dict[str, Mapping[str, Any]] = {}
    duplicate_ids: set[str] = set()
    allowed_body_keys = {"type", "id", "attributes", "validations"}
    for item in body:
        if not isinstance(item, Mapping):
            findings.append(Finding("FORM_STRUCTURE_INVALID", template, "body item invalid"))
            continue
        if set(item) - allowed_body_keys:
            findings.append(
                Finding("FORM_STRUCTURE_INVALID", template, "unknown body item key")
            )
        body_id = item.get("id")
        if isinstance(body_id, str):
            if body_id in controls:
                duplicate_ids.add(body_id)
            controls[body_id] = item
    for body_id in sorted(duplicate_ids):
        findings.append(Finding("FORM_STRUCTURE_INVALID", template, f"duplicate id {body_id}"))

    for logical_field, body_id in field_mapping.items():
        if not isinstance(body_id, str) or body_id not in controls:
            findings.append(
                Finding("REQUIRED_FIELD_MISSING", template, str(logical_field))
            )
            continue
        validations = controls[body_id].get("validations")
        if not isinstance(validations, Mapping) or validations.get("required") is not True:
            findings.append(
                Finding("REQUIRED_MARKER_INVALID", template, str(logical_field))
            )
    return findings


def _template_findings(
    root: Path, registry: Mapping[str, Any], registry_forms: Mapping[str, Mapping[str, Any]]
) -> list[Finding]:
    findings: list[Finding] = []
    template_root = root / TEMPLATE_ROOT
    expected_files = {"config.yml"}
    for issue_type, registered in registry_forms.items():
        template = registered.get("template")
        field_mapping = registered.get("required_fields")
        if not isinstance(template, str) or not isinstance(field_mapping, Mapping):
            findings.append(Finding("REGISTRY_INVALID", issue_type, "template mapping invalid"))
            continue
        expected_files.add(template)
        document, load_findings = _load_yaml(template_root / template, template)
        findings.extend(load_findings)
        if document is not None:
            findings.extend(form_document_findings(template, document, field_mapping))

    try:
        actual_files = {
            path.name
            for path in template_root.iterdir()
            if path.is_file() and path.suffix in {".yml", ".yaml"}
        }
    except OSError as error:
        findings.append(Finding("DOCUMENT_INVALID", TEMPLATE_ROOT.as_posix(), str(error)))
        return findings
    if actual_files != expected_files:
        findings.append(
            Finding("ISSUE_TYPE_INVALID", TEMPLATE_ROOT.as_posix(), "unknown or missing form")
        )

    configuration = registry.get("configuration")
    if not isinstance(configuration, Mapping):
        findings.append(
            Finding("REGISTRY_INVALID", REGISTRY_PATH.as_posix(), "configuration required")
        )
        return findings
    config_path = configuration.get("path")
    if config_path != TEMPLATE_ROOT.joinpath("config.yml").as_posix():
        findings.append(Finding("REGISTRY_INVALID", REGISTRY_PATH.as_posix(), "config path"))
        return findings
    config, config_findings = _load_yaml(root / str(config_path), str(config_path))
    findings.extend(config_findings)
    if config is None:
        return findings
    if config.get("blank_issues_enabled") is not False:
        findings.append(Finding("BLANK_ISSUE_BYPASS", str(config_path), "must be false"))
    contact_links = config.get("contact_links")
    security_url = configuration.get("security_advisory_url")
    has_private_route = bool(
        isinstance(contact_links, list)
        and isinstance(security_url, str)
        and any(
            isinstance(link, Mapping) and link.get("url") == security_url
            for link in contact_links
        )
    )
    if not has_private_route:
        findings.append(
            Finding("SECURITY_ROUTE_MISSING", str(config_path), "private advisory required")
        )
    return findings


def _workflow_findings(root: Path) -> list[Finding]:
    try:
        normalized = " ".join((root / WORKFLOW_PATH).read_text(encoding="utf-8").split())
    except (OSError, UnicodeError) as error:
        return [Finding("CI_COMMAND_INVALID", WORKFLOW_PATH.as_posix(), str(error))]
    if EXPECTED_COMMAND not in normalized:
        return [
            Finding("CI_COMMAND_INVALID", WORKFLOW_PATH.as_posix(), "local command not reused")
        ]
    return []


def validate_repository(repository_root: Path) -> tuple[Finding, ...]:
    root = repository_root.resolve()
    contract, findings = _load_json(root / CONTRACT_PATH, CONTRACT_PATH.as_posix())
    registry, registry_load_findings = _load_json(root / REGISTRY_PATH, REGISTRY_PATH.as_posix())
    task, task_load_findings = _load_json(root / TASK_PATH, TASK_PATH.as_posix())
    findings.extend(registry_load_findings)
    findings.extend(task_load_findings)
    if task is not None:
        findings.extend(_task_findings(task))
    if contract is not None and registry is not None:
        registry_forms, registry_findings = _registry_findings(contract, registry)
        findings.extend(registry_findings)
        if not registry_findings:
            findings.extend(_template_findings(root, registry, registry_forms))
    findings.extend(_workflow_findings(root))
    return tuple(sorted(set(findings)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ISSUE-0666 GitHub Issue Forms")
    parser.add_argument(
        "--repository-root", type=Path, default=Path(__file__).resolve().parents[3]
    )
    args = parser.parse_args(argv)
    try:
        findings = validate_repository(args.repository_root)
    except Exception as error:  # CLI boundary must fail closed with one stable report.
        findings = (Finding("VALIDATOR_INTERNAL_ERROR", ".", str(error)),)
    report = {
        "acceptance_evidence": dict.fromkeys(EXPECTED_AC_IDS, "test_epic_090_fundacao"),
        "failure_policy": "FAIL_CLOSED",
        "findings": [finding.as_dict() for finding in findings],
        "issue": "ISSUE-0666",
        "requirement_evidence": {
            "REQ-GOV-002": "test_issue_form_required_acceptance_risk_test_rollback_fields"
        },
        "status": "FAIL" if findings else "PASS",
        "templates": ["BUG", "SPIKE", "STORY", "TASK"],
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
