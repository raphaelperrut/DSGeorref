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
    EXPECTED_CLOSURE_POLICY,
    EXPECTED_CUTOVER_POLICY,
    EXPECTED_FAILURE_POLICY,
    EXPECTED_REQUIREMENTS,
    EXPECTED_TEST_TARGETS,
    POLICY_PATH,
    ROOT_FIELDS,
    TASK_PATH_PATTERN,
    TICKET_PATTERN,
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


def canonical_json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


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


def _identity_findings(policy: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    if set(policy) != ROOT_FIELDS:
        findings.append(_finding("POLICY_STRUCTURE_INVALID", "$", "root fields mismatch"))
    expected = ("1.0.0", "EXECUTABLE-FOUNDATION-WALKING-SKELETON", "BC-001", "CANDIDATE")
    actual = tuple(
        policy.get(field) for field in ("schema_version", "foundation_id", "owner", "status")
    )
    if actual != expected:
        findings.append(_finding("POLICY_IDENTITY_INVALID", "$", "identity mismatch"))
    return findings


def _slice_findings(policy: dict[str, Any], root: Path) -> list[Finding]:
    try:
        task = _load_json(root / EXPECTED_CAPABILITY_SCOPE[0])
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [_finding("TASK_ENVELOPE_INVALID", "$.slice", str(error))]
    expected = {
        "number": 2,
        "total": 2,
        "dependency_story_ids": task.get("dependencies"),
        "requirement_ids": EXPECTED_REQUIREMENTS,
        "boundary": "CURRENT_SLICE_ONLY",
        "next_slice": None,
    }
    if policy.get("slice") != expected:
        return [_finding("SLICE_POLICY_INVALID", "$.slice", "slice contract mismatch")]
    contract_path = _safe_file(root, CONTRACT_PATH)
    if contract_path is None:
        return [_finding("CONTRACT_BINDING_INVALID", "$.contract.path", "contract missing")]
    try:
        contract = _load_json(contract_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [_finding("CONTRACT_BINDING_INVALID", "$.contract.path", str(error))]
    expected_contract = {
        "path": CONTRACT_PATH,
        "version": contract.get("contract_version"),
        "sha256": canonical_json_sha256(contract),
        "change": "NONE",
    }
    if policy.get("contract") != expected_contract:
        return [_finding("CONTRACT_BINDING_INVALID", "$.contract", "version or digest drift")]
    return []


def _checkpoint_findings(policy: dict[str, Any], root: Path) -> list[Finding]:
    evidence = policy.get("requirement_evidence")
    if not isinstance(evidence, dict) or list(evidence) != EXPECTED_REQUIREMENTS:
        return [
            _finding(
                "REQUIREMENT_EVIDENCE_INVALID", "$.requirement_evidence", "coverage/order mismatch"
            )
        ]
    findings: list[Finding] = []
    for requirement, target in EXPECTED_TEST_TARGETS.items():
        path, test_id = target
        expected = {"test_path": path, "test_id": test_id, "checkpoint": f"{path}::{test_id}"}
        item = evidence.get(requirement)
        field = f"$.requirement_evidence.{requirement}"
        if item != expected:
            findings.append(_finding("CHECKPOINT_INVALID", field, "canonical target required"))
            continue
        test_path = _safe_file(root, path)
        if test_path is None:
            findings.append(_finding("CHECKPOINT_INVALID", field, "test file missing"))
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


def _scope_findings(policy: dict[str, Any], root: Path) -> list[Finding]:
    scope = policy.get("write_scope")
    if (
        scope != EXPECTED_CAPABILITY_SCOPE
        or not isinstance(scope, list)
        or TASK_PATH_PATTERN.fullmatch(str(scope[0])) is None
    ):
        return [
            _finding("WRITE_SCOPE_INVALID", "$.write_scope", "stable capability scope required")
        ]
    roots = [str(item).removesuffix("/**") for item in scope]
    if len(roots) != len(set(roots)) or any(
        left.startswith(f"{right}/") or right.startswith(f"{left}/")
        for index, left in enumerate(roots)
        for right in roots[index + 1 :]
    ):
        return [_finding("WRITE_SCOPE_INVALID", "$.write_scope", "scope overlaps")]
    try:
        task = _load_json(root / str(scope[0]))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [_finding("TASK_ENVELOPE_INVALID", "$.write_scope", str(error))]
    review_scope = task.get("phase_f_review", {}).get("files", {}).get("allow_paths")
    if task.get("allow_paths") != scope or review_scope != scope:
        return [_finding("TASK_ENVELOPE_INVALID", "$.write_scope", "allow path mismatch")]
    if task.get("deny_paths") != ["src/**/epic-*", "src/**/issue-*"]:
        return [_finding("TASK_ENVELOPE_INVALID", "$.write_scope", "deny paths changed")]
    module_root = root / EXPECTED_CAPABILITY_SCOPE[2].removesuffix("/**")
    if any(
        TICKET_PATTERN.search(path.read_text(encoding="utf-8")) for path in module_root.glob("*.py")
    ):
        return [_finding("TICKET_IDENTIFIER_INVALID", "$.write_scope", "ticket identifier in code")]
    return []


def _evidence_findings(policy: dict[str, Any], root: Path) -> list[Finding]:
    descriptor = policy.get("evidence_set")
    expected_descriptor = {
        "path": EVIDENCE_PATH,
        "digest_algorithm": "sha256",
        "immutable": True,
        "machine_readable": True,
        "human_summary": POLICY_PATH.removesuffix("foundation-policy.json") + "README.md",
    }
    if descriptor != expected_descriptor:
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set", "descriptor mismatch")]
    evidence_path = _safe_file(root, EVIDENCE_PATH)
    if evidence_path is None:
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set.path", "evidence missing")]
    try:
        evidence = _load_json(evidence_path)
        payload = evidence["payload"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, ValueError) as error:
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set", str(error))]
    if evidence.get("payload_sha256") != canonical_json_sha256(payload):
        return [
            _finding("EVIDENCE_DIGEST_INVALID", "$.evidence_set.payload_sha256", "digest mismatch")
        ]
    try:
        task = _load_json(root / EXPECTED_CAPABILITY_SCOPE[0])
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set", str(error))]
    expected_payload = {
        "schema_version": "1.0.0",
        "evidence_set_id": "EXECUTABLE-FOUNDATION-CLOSURE-CUTOVER",
        "owner": "BC-001",
        "status": "CANDIDATE",
        "requirements": EXPECTED_REQUIREMENTS,
        "acceptance_criteria": task.get("acceptance_criterion_ids"),
        "contract": {key: policy.get("contract", {}).get(key) for key in ("version", "sha256")},
        "policies": {
            "sprint_closure": EXPECTED_CLOSURE_POLICY,
            "first_slice_cutover": EXPECTED_CUTOVER_POLICY,
        },
        "failure_policy": "FAIL_CLOSED",
        "limitations": [
            "NO_CUTOVER_AUTHORIZATION_GRANTED",
            "NO_PRODUCT_RUNTIME_OR_MIGRATION_CHANGE",
            "INDEPENDENT_REVIEW_PENDING",
        ],
        "review_gate": "INDEPENDENT_QA_AND_REVIEWER_SAME_CANDIDATE",
        "rollback": "REVERT_COMMIT_NO_DATA_ACTION",
    }
    if payload != expected_payload:
        return [_finding("EVIDENCE_SET_INVALID", "$.evidence_set.payload", "content drift")]
    return []


def validate_policy(policy: object, repository_root: Path) -> list[Finding]:
    if not isinstance(policy, dict):
        return [_finding("POLICY_STRUCTURE_INVALID", "$", "object required")]
    findings = _identity_findings(policy)
    findings.extend(_slice_findings(policy, repository_root))
    if policy.get("sprint_closure") != EXPECTED_CLOSURE_POLICY:
        findings.append(
            _finding(
                "SPRINT_CLOSURE_POLICY_INVALID", "$.sprint_closure", "evidence closure required"
            )
        )
    if policy.get("first_slice_cutover") != EXPECTED_CUTOVER_POLICY:
        findings.append(
            _finding(
                "CUTOVER_POLICY_INVALID", "$.first_slice_cutover", "explicit gated cutover required"
            )
        )
    if policy.get("failure_policy") != EXPECTED_FAILURE_POLICY:
        findings.append(
            _finding("FAILURE_POLICY_INVALID", "$.failure_policy", "silent fallback prohibited")
        )
    findings.extend(_checkpoint_findings(policy, repository_root))
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
    parser = argparse.ArgumentParser(description="Validate foundation closure and cutover policy")
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
