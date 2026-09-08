from __future__ import annotations

import argparse
import ast
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from foundation_expectations import (
    CONTRACT_PATH,
    EVIDENCE_PATH,
    EXPECTED_CAPABILITY_SCOPE,
    EXPECTED_FAILURE_POLICY,
    EXPECTED_REQUIREMENTS,
    EXPECTED_TEST_TARGETS,
    POLICY_PATH,
    ROOT_FIELDS,
    TASK_PATH_PATTERN,
)


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


class FoundationValidationError(ValueError):
    def __init__(self, findings: list[Finding]) -> None:
        self.findings = tuple(sorted(findings))
        super().__init__("; ".join(f"{item.code} at {item.field}" for item in findings))


def _finding(code: str, field: str, detail: str) -> Finding:
    return Finding(code=code, field=field, detail=detail)


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError("JSON root must be an object")
    return loaded


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_file(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def _checkpoint_findings(policy: dict[str, Any], root: Path) -> list[Finding]:
    evidence = policy.get("requirement_evidence")
    if not isinstance(evidence, dict):
        return [
            _finding("REQUIREMENT_EVIDENCE_INVALID", "$.requirement_evidence", "object required")
        ]
    findings: list[Finding] = []
    if list(evidence) != EXPECTED_REQUIREMENTS:
        findings.append(
            _finding(
                "REQUIREMENT_EVIDENCE_INVALID", "$.requirement_evidence", "coverage/order mismatch"
            )
        )
    for requirement_id, item in evidence.items():
        field = f"$.requirement_evidence.{requirement_id}"
        if not isinstance(item, dict):
            findings.append(_finding("REQUIREMENT_EVIDENCE_INVALID", field, "object required"))
            continue
        test_path = _safe_file(root, item.get("test_path"))
        test_id = item.get("test_id")
        checkpoint = item.get("checkpoint")
        target = EXPECTED_TEST_TARGETS.get(requirement_id)
        expected_item = (
            {
                "test_path": target[0],
                "test_id": target[1],
                "checkpoint": f"{target[0]}::{target[1]}",
            }
            if target
            else None
        )
        if item != expected_item:
            findings.append(_finding("CHECKPOINT_INVALID", field, "canonical target required"))
            continue
        if test_path is None or not isinstance(test_id, str):
            findings.append(_finding("CHECKPOINT_INVALID", field, "test target missing or unsafe"))
            continue
        if checkpoint != f"{item['test_path']}::{test_id}":
            findings.append(
                _finding("CHECKPOINT_INVALID", f"{field}.checkpoint", "selector mismatch")
            )
            continue
        try:
            tree = ast.parse(test_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, SyntaxError) as error:
            findings.append(_finding("CHECKPOINT_INVALID", field, str(error)))
            continue
        functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
        if test_id not in functions:
            findings.append(_finding("CHECKPOINT_INVALID", f"{field}.test_id", "test absent"))
    return findings


def _slice_findings(policy: dict[str, Any], root: Path) -> list[Finding]:
    scope = policy.get("write_scope")
    if not isinstance(scope, list) or not scope or not isinstance(scope[0], str):
        return [_finding("SLICE_POLICY_INVALID", "$.slice", "TaskEnvelope unavailable")]
    try:
        task = _load_json(root / scope[0])
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [_finding("SLICE_POLICY_INVALID", "$.slice", str(error))]
    expected = {
        "number": 1,
        "total": 2,
        "dependency_story_ids": task.get("dependencies"),
        "requirement_ids": EXPECTED_REQUIREMENTS,
        "boundary": "CURRENT_SLICE_ONLY",
        "next_slice": "SEPARATE_AUTHORIZATION_REQUIRED",
    }
    if policy.get("slice") != expected:
        return [_finding("SLICE_POLICY_INVALID", "$.slice", "thin slice contract mismatch")]
    return []


def _contract_findings(policy: dict[str, Any], root: Path) -> list[Finding]:
    binding = policy.get("contract")
    if not isinstance(binding, dict) or binding.get("path") != CONTRACT_PATH:
        return [_finding("CONTRACT_BINDING_INVALID", "$.contract", "frozen contract path required")]
    contract_path = _safe_file(root, binding["path"])
    if contract_path is None:
        return [_finding("CONTRACT_BINDING_INVALID", "$.contract.path", "contract missing")]
    try:
        contract = _load_json(contract_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [_finding("CONTRACT_BINDING_INVALID", "$.contract.path", str(error))]
    expected = {
        "path": CONTRACT_PATH,
        "version": contract.get("contract_version"),
        "sha256": _sha256(contract_path),
        "exercise": "ESSENTIAL_ONLY",
    }
    findings = (
        []
        if binding == expected
        else [_finding("CONTRACT_BINDING_INVALID", "$.contract", "version or digest drift")]
    )
    failure = contract.get("failure_policy")
    for key, value in EXPECTED_FAILURE_POLICY.items():
        if not isinstance(failure, dict) or failure.get(key) != value:
            findings.append(
                _finding(
                    "CONTRACT_FAILURE_POLICY_INVALID",
                    f"$contract.failure_policy.{key}",
                    "fail-closed contract required",
                )
            )
    return findings


def _scope_findings(policy: dict[str, Any], root: Path) -> list[Finding]:
    scope = policy.get("write_scope")
    if (
        not isinstance(scope, list)
        or len(scope) != len(EXPECTED_CAPABILITY_SCOPE) + 1
        or not isinstance(scope[0], str)
        or TASK_PATH_PATTERN.fullmatch(scope[0]) is None
        or scope[1:] != EXPECTED_CAPABILITY_SCOPE
    ):
        return [
            _finding("WRITE_SCOPE_INVALID", "$.write_scope", "stable capability scope required")
        ]
    roots = [item.removesuffix("/**") for item in scope]
    if len(roots) != len(set(roots)) or any(
        left.startswith(f"{right}/") or right.startswith(f"{left}/")
        for index, left in enumerate(roots)
        for right in roots[index + 1 :]
    ):
        return [_finding("WRITE_SCOPE_INVALID", "$.write_scope", "scope overlaps")]
    try:
        task = _load_json(root / scope[0])
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [_finding("TASK_ENVELOPE_INVALID", "$.write_scope", str(error))]
    review_scope = task.get("phase_f_review", {}).get("files", {}).get("allow_paths")
    if task.get("allow_paths") != scope or review_scope != scope:
        return [_finding("TASK_ENVELOPE_INVALID", "$.write_scope", "allow path mismatch")]
    if task.get("deny_paths") != ["src/**/epic-*", "src/**/issue-*"]:
        return [_finding("TASK_ENVELOPE_INVALID", "$.write_scope", "deny paths changed")]
    return []


def _evidence_payload_findings(
    payload: object, policy: dict[str, Any], root: Path
) -> list[Finding]:
    if not isinstance(payload, dict):
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set.payload", "object required")]
    scope = policy.get("write_scope")
    if not isinstance(scope, list) or not scope or not isinstance(scope[0], str):
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set.payload", "scope required")]
    try:
        task = _load_json(root / scope[0])
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as error:
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set.payload", str(error))]
    expected_fields = {
        "schema_version",
        "evidence_set_id",
        "owner",
        "status",
        "requirements",
        "acceptance_criteria",
        "contract",
        "failure_policy",
        "limitations",
        "review_gate",
    }
    expected_values = {
        "schema_version": "1.0.0",
        "evidence_set_id": "EXECUTABLE-FOUNDATION-SLICE-1",
        "owner": "BC-001",
        "status": "CANDIDATE",
        "requirements": EXPECTED_REQUIREMENTS,
        "acceptance_criteria": task.get("acceptance_criterion_ids"),
        "contract": {key: policy.get("contract", {}).get(key) for key in ("version", "sha256")},
        "failure_policy": "FAIL_CLOSED",
        "limitations": [
            "PRIVATE_CPU_ONLY",
            "SYNTHETIC_JOB_WITHOUT_FUNCTIONAL_GEOREFERENCING",
            "NO_PUBLIC_OPERATIONAL_CLAIMS",
        ],
        "review_gate": "INDEPENDENT_QA_AND_REVIEWER_SAME_CANDIDATE",
    }
    if set(payload) != expected_fields or payload != expected_values:
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set.payload", "content drift")]
    return []


def _evidence_findings(policy: dict[str, Any], root: Path) -> list[Finding]:
    descriptor = policy.get("evidence_set")
    expected = {
        "path": EVIDENCE_PATH,
        "digest_algorithm": "sha256",
        "immutable": True,
        "machine_readable": True,
        "human_summary": POLICY_PATH.removesuffix("foundation-policy.json") + "README.md",
    }
    if descriptor != expected:
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set", "descriptor mismatch")]
    path = _safe_file(root, descriptor["path"])
    if path is None:
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set.path", "evidence missing")]
    try:
        evidence = _load_json(path)
        payload = evidence["payload"]
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode()
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set", str(error))]
    if evidence.get("payload_sha256") != hashlib.sha256(encoded).hexdigest():
        return [
            _finding("EVIDENCE_DIGEST_INVALID", "$.evidence_set.payload_sha256", "digest mismatch")
        ]
    return _evidence_payload_findings(payload, policy, root)


def validate_policy(policy: object, repository_root: Path) -> list[Finding]:
    if not isinstance(policy, dict):
        return [_finding("POLICY_STRUCTURE_INVALID", "$", "object required")]
    findings: list[Finding] = []
    if set(policy) != ROOT_FIELDS:
        findings.append(_finding("POLICY_STRUCTURE_INVALID", "$", "root fields mismatch"))
    expected_identity = ("1.0.0", "EXECUTABLE-FOUNDATION-WALKING-SKELETON", "BC-001", "CANDIDATE")
    actual_identity = tuple(
        policy.get(key) for key in ("schema_version", "foundation_id", "owner", "status")
    )
    if actual_identity != expected_identity:
        findings.append(_finding("POLICY_IDENTITY_INVALID", "$", "identity mismatch"))
    if policy.get("private_baseline") != {
        "visibility": "PRIVATE",
        "installation": "CLEAN_REPOSITORY_PINNED",
        "compute": "CPU_ONLY",
        "flow": "APPROVED_WALKING_SKELETON",
        "evidence": "REPRODUCIBLE",
        "public_claims": False,
    }:
        findings.append(
            _finding(
                "BASELINE_POLICY_INVALID", "$.private_baseline", "private CPU baseline required"
            )
        )
    if policy.get("diagnostic_job") != {"kind": "SYNTHETIC", "functional_georeferencing": False}:
        findings.append(
            _finding(
                "DIAGNOSTIC_JOB_INVALID",
                "$.diagnostic_job",
                "synthetic non-georeferencing job required",
            )
        )
    if policy.get("ci_gate") != {
        "mode": "PROGRESSIVE",
        "scope": "CAPABILITIES_PRESENT",
        "command": "make verify",
    }:
        findings.append(
            _finding("CI_GATE_INVALID", "$.ci_gate", "progressive repository gate required")
        )
    failure = policy.get("failure_policy")
    if failure != EXPECTED_FAILURE_POLICY:
        findings.append(
            _finding("FAILURE_POLICY_INVALID", "$.failure_policy", "silent fallback prohibited")
        )
    findings.extend(_contract_findings(policy, repository_root))
    findings.extend(_checkpoint_findings(policy, repository_root))
    findings.extend(_slice_findings(policy, repository_root))
    findings.extend(_scope_findings(policy, repository_root))
    findings.extend(_evidence_findings(policy, repository_root))
    return sorted(set(findings))


def validate_path(policy_path: Path, repository_root: Path) -> list[Finding]:
    try:
        policy = _load_json(policy_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [_finding("POLICY_UNREADABLE", str(policy_path), str(error))]
    return validate_policy(policy, repository_root.resolve())


def load_policy(policy_path: Path, repository_root: Path) -> dict[str, Any]:
    policy = _load_json(policy_path)
    findings = validate_policy(policy, repository_root.resolve())
    if findings:
        raise FoundationValidationError(findings)
    return policy


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the executable foundation materialization"
    )
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("--repository-root", required=True, type=Path)
    args = parser.parse_args(argv)
    findings = validate_path(args.policy, args.repository_root)
    print(
        json.dumps(
            {
                "status": "FAIL" if findings else "PASS",
                "findings": [asdict(item) for item in findings],
            },
            sort_keys=True,
        )
    )
    return 2 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
