from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from foundation_contract import EXPECTED_FAILURE_POLICY, EXPECTED_SURFACES


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


EXPECTED_STAGES = [
    "CLI_OR_WEB_INPUT",
    "HTTP_API",
    "POSTGRESQL_POSTGIS",
    "RABBITMQ_CELERY",
    "WORKER",
    "DIAGNOSTIC_ARTIFACT",
]
EXPECTED_DEFINITION_OF_DONE = [
    "ALL_STAGES_OBSERVED_IN_ORDER",
    "STATE_COMMITTED_BEFORE_BROKER_ACK",
    "ARTIFACT_HAS_DETERMINISTIC_DIGEST",
    "FAILURE_IS_EXPLICIT",
]
EXPECTED_REQUIREMENT_EVIDENCE = {
    "REQ-DEL-001": "test_walking_skeleton_end_to_end_and_vertical_slice_definition_of_done",
    "REQ-DEV-001": "test_host_container_ci_contract_and_no_implicit_downloads",
}
EXPECTED_ACCEPTANCE_EVIDENCE = {
    "AC-ISSUE-0122-01": "test_epic_003_fundacao",
    "AC-ISSUE-0122-02": "test_epic_003_fundacao",
    "AC-ISSUE-0122-03": "test_foundation_rejects_contract_drift_and_silent_fallback",
    "AC-ISSUE-0122-04": "test_host_container_ci_contract_and_no_implicit_downloads",
}
EXPECTED_ROOT_FIELDS = {
    "schema_version",
    "foundation_id",
    "contract_id",
    "contract_version",
    "owner",
    "status",
    "topology",
    "walking_skeleton",
    "reproducibility",
    "failure_policy",
    "requirement_evidence",
    "acceptance_evidence",
}


def _finding(code: str, field: str, detail: str) -> Finding:
    return Finding(code=code, field=field, detail=detail)


def _expect_equal(
    actual: object, expected: object, *, code: str, field: str
) -> list[Finding]:
    if type(actual) is type(expected) and actual == expected:
        return []
    return [_finding(code, field, f"expected {expected!r}")]


def _validate_contract(contract: dict[str, Any]) -> list[Finding]:
    architecture = contract.get("architecture")
    application_core = (
        architecture.get("application_core", {}) if isinstance(architecture, dict) else {}
    )
    data_authority = (
        architecture.get("data_authority", {}) if isinstance(architecture, dict) else {}
    )
    expected = {
        "contract_id": "MONOREPO-FOUNDATION-CONTRACT",
        "contract_version": "1.0.0",
        "owner": "BC-001",
        "status": "FROZEN",
        "topology": "SINGLE_INSTANCE_MODULAR_MONOLITH",
        "semantic_authority": "APPLICATION_SERVICES",
        "surfaces": EXPECTED_SURFACES,
        "state_authority": "POSTGRESQL_POSTGIS",
        "broker_role": "TRANSPORT_ONLY",
        "failure_policy": EXPECTED_FAILURE_POLICY,
    }
    actual = {
        "contract_id": contract.get("contract_id"),
        "contract_version": contract.get("contract_version"),
        "owner": contract.get("owner"),
        "status": contract.get("status"),
        "topology": architecture.get("topology") if isinstance(architecture, dict) else None,
        "semantic_authority": application_core.get("authority"),
        "surfaces": _surface_projection(contract),
        "state_authority": data_authority.get("state"),
        "broker_role": data_authority.get("broker"),
        "failure_policy": contract.get("failure_policy"),
    }
    return _expect_equal(actual, expected, code="CONTRACT_DRIFT", field="$contract")


def _validate_identity(plan: dict[str, Any]) -> list[Finding]:
    expected = {
        "schema_version": "1.0.0",
        "foundation_id": "DSGEOREF-MONOREPO-FOUNDATION",
        "contract_id": "MONOREPO-FOUNDATION-CONTRACT",
        "contract_version": "1.0.0",
        "owner": "BC-001",
        "status": "CANDIDATE",
    }
    findings: list[Finding] = []
    for field, value in expected.items():
        findings.extend(
            _expect_equal(
                plan.get(field), value, code="FOUNDATION_IDENTITY_INVALID", field=f"$.{field}"
            )
        )
    unknown = sorted(set(plan) - EXPECTED_ROOT_FIELDS)
    for field in unknown:
        findings.append(_finding("FOUNDATION_STRUCTURE_INVALID", f"$.{field}", "unknown field"))
    return findings


def _surface_projection(contract: dict[str, Any]) -> list[dict[str, object]]:
    architecture = contract.get("architecture")
    if not isinstance(architecture, dict):
        return []
    interface_flow = architecture.get("interface_flow")
    if not isinstance(interface_flow, list):
        return []
    keys = ("surface", "invocation", "contract_source")
    return [
        {key: surface.get(key) for key in keys}
        for surface in interface_flow
        if isinstance(surface, dict)
    ]


def _validate_topology(plan: dict[str, Any]) -> list[Finding]:
    topology = plan.get("topology")
    if not isinstance(topology, dict):
        return [_finding("TOPOLOGY_INVALID", "$.topology", "object is required")]
    expected = {
        "kind": "SINGLE_INSTANCE_MODULAR_MONOLITH",
        "semantic_authority": "APPLICATION_SERVICES",
        "surfaces": EXPECTED_SURFACES,
    }
    return _expect_equal(topology, expected, code="TOPOLOGY_INVALID", field="$.topology")


def _validate_walking_skeleton(plan: dict[str, Any]) -> list[Finding]:
    skeleton = plan.get("walking_skeleton")
    if not isinstance(skeleton, dict):
        return [_finding("WALKING_SKELETON_INVALID", "$.walking_skeleton", "object is required")]
    expected = {
        "stages": EXPECTED_STAGES,
        "state_authority": "POSTGRESQL_POSTGIS",
        "broker_role": "TRANSPORT_ONLY",
        "artifact_policy": "DIAGNOSTIC_ONLY_UNTIL_PRODUCT_GATES",
        "definition_of_done": EXPECTED_DEFINITION_OF_DONE,
    }
    return _expect_equal(
        skeleton, expected, code="WALKING_SKELETON_INVALID", field="$.walking_skeleton"
    )


def _validate_reproducibility(plan: dict[str, Any]) -> list[Finding]:
    policy = plan.get("reproducibility")
    if not isinstance(policy, dict):
        return [_finding("REPRODUCIBILITY_INVALID", "$.reproducibility", "object is required")]
    findings: list[Finding] = []
    for field, expected in {
        "dependency_resolution": "REPOSITORY_PINNED_ONLY",
        "implicit_downloads": "PROHIBITED",
        "network_required": False,
    }.items():
        findings.extend(
            _expect_equal(
                policy.get(field),
                expected,
                code="REPRODUCIBILITY_INVALID",
                field=f"$.reproducibility.{field}",
            )
        )
    local = policy.get("local_commands")
    container = policy.get("container_commands")
    ci = policy.get("ci_commands")
    if not isinstance(local, list) or not local or not (local == container == ci):
        findings.append(
            _finding(
                "COMMAND_PARITY_INVALID",
                "$.reproducibility",
                "non-empty local, container, and CI commands must be identical",
            )
        )
    expected_fields = {
        "dependency_resolution",
        "implicit_downloads",
        "network_required",
        "local_commands",
        "container_commands",
        "ci_commands",
    }
    for field in sorted(set(policy) - expected_fields):
        findings.append(
            _finding(
                "REPRODUCIBILITY_INVALID",
                f"$.reproducibility.{field}",
                "unknown field",
            )
        )
    return findings


def _validate_failure_policy(plan: dict[str, Any]) -> list[Finding]:
    actual = plan.get("failure_policy")
    return _expect_equal(
        actual,
        EXPECTED_FAILURE_POLICY,
        code="FAILURE_POLICY_INVALID",
        field="$.failure_policy",
    )


def _validate_evidence(plan: dict[str, Any]) -> list[Finding]:
    findings = _expect_equal(
        plan.get("requirement_evidence"),
        EXPECTED_REQUIREMENT_EVIDENCE,
        code="REQUIREMENT_EVIDENCE_INVALID",
        field="$.requirement_evidence",
    )
    findings.extend(
        _expect_equal(
            plan.get("acceptance_evidence"),
            EXPECTED_ACCEPTANCE_EVIDENCE,
            code="ACCEPTANCE_EVIDENCE_INVALID",
            field="$.acceptance_evidence",
        )
    )
    return findings


def validate_foundation(plan: object, contract: object) -> list[Finding]:
    if not isinstance(plan, dict):
        return [_finding("FOUNDATION_STRUCTURE_INVALID", "$", "object is required")]
    if not isinstance(contract, dict):
        return [_finding("CONTRACT_UNREADABLE", "$contract", "object is required")]
    findings = _validate_contract(contract)
    findings.extend(_validate_identity(plan))
    findings.extend(_validate_topology(plan))
    findings.extend(_validate_walking_skeleton(plan))
    findings.extend(_validate_reproducibility(plan))
    findings.extend(_validate_failure_policy(plan))
    findings.extend(_validate_evidence(plan))
    return sorted(findings)


def _load_json(path: Path, *, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [_finding(code, str(path), str(error))]


def validate_paths(foundation_path: Path, contract_path: Path) -> list[Finding]:
    plan, findings = _load_json(foundation_path, code="FOUNDATION_UNREADABLE")
    contract, contract_findings = _load_json(contract_path, code="CONTRACT_UNREADABLE")
    findings.extend(contract_findings)
    if findings:
        return sorted(findings)
    return validate_foundation(plan, contract)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the EPIC-003 foundation candidate")
    parser.add_argument("--foundation", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    findings = validate_paths(args.foundation, args.contract)
    report = {
        "foundation": str(args.foundation.as_posix()),
        "status": "FAIL" if findings else "PASS",
        "findings": [asdict(finding) for finding in findings],
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 2 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
