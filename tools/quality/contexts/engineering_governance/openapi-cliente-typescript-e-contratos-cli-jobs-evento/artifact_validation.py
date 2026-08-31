from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from registry_validation import REGISTRY_REL, validate_registry
from validation_types import Finding


SLUG = "openapi-cliente-typescript-e-contratos-cli-jobs-evento"
CONTRACT_ROOT = Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}")
TEST_ROOT = Path(f"tests/fnd/{SLUG}")
CONSOLIDATION_ROOT = CONTRACT_ROOT / "consolidacao"
CONSOLIDATION_MANIFEST_REL = CONSOLIDATION_ROOT / "contract-manifest.yaml"
CONSOLIDATION_SCHEMA_REL = CONSOLIDATION_ROOT / "slice-consolidation.schema.json"
CONSOLIDATION_EXAMPLE_REL = CONSOLIDATION_ROOT / "examples/slice-consolidation.json"

SLICE_PACKAGES = (
    (
        CONTRACT_ROOT / "crs-dbschema-epic-parte-1/contract-manifest.yaml",
        CONTRACT_ROOT / "crs-dbschema-epic-parte-1/contract-foundation.schema.json",
        CONTRACT_ROOT / "crs-dbschema-epic-parte-1/examples/contract-foundation.json",
        TEST_ROOT / "test_contract_foundation.py",
    ),
    (
        CONTRACT_ROOT / "runtime-scm-tool-parte-2/contract-manifest.yaml",
        CONTRACT_ROOT / "runtime-scm-tool-parte-2/runtime-schema-conformance.schema.json",
        CONTRACT_ROOT / "runtime-scm-tool-parte-2/examples/runtime-schema-conformance.json",
        TEST_ROOT / "test_runtime_schema_contract.py",
    ),
)
def _finding(code: str, artifact: Path, detail: str) -> Finding:
    return Finding(code, artifact.as_posix(), detail)


def _load_json(root: Path, relative: Path, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return json.loads((root / relative).read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [_finding(code, relative, str(error))]


def _load_yaml(root: Path, relative: Path, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return yaml.safe_load((root / relative).read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return None, [_finding(code, relative, str(error))]


def _schema_findings(document: object, schema: object, artifact: Path) -> list[Finding]:
    if not isinstance(schema, dict):
        return [_finding("CONTRACT_SCHEMA_INVALID", artifact, "schema object required")]
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        return [_finding("CONTRACT_SCHEMA_INVALID", artifact, error.message)]
    return [
        _finding("CONTRACT_SCHEMA_INVALID", artifact, f"{error.json_path}: {error.message}")
        for error in Draft202012Validator(schema).iter_errors(document)
    ]


def _defined_functions(root: Path, relative: Path) -> tuple[set[str], list[Finding]]:
    try:
        tree = ast.parse((root / relative).read_text(encoding="utf-8"), relative.as_posix())
    except (OSError, UnicodeError, SyntaxError) as error:
        return set(), [_finding("TEST_SOURCE_INVALID", relative, str(error))]
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }, []


def _slice_findings(root: Path) -> tuple[dict[str, str], list[Finding]]:
    requirement_tests: dict[str, str] = {}
    findings: list[Finding] = []
    for manifest_rel, schema_rel, example_rel, test_rel in SLICE_PACKAGES:
        manifest, manifest_findings = _load_yaml(root, manifest_rel, "CONTRACT_MANIFEST_UNREADABLE")
        schema, schema_findings = _load_json(root, schema_rel, "CONTRACT_SCHEMA_UNREADABLE")
        example, example_findings = _load_json(root, example_rel, "CONTRACT_UNREADABLE")
        findings.extend(manifest_findings + schema_findings + example_findings)
        if schema is not None and example is not None:
            findings.extend(_schema_findings(example, schema, example_rel))
        if not isinstance(manifest, dict):
            continue
        expected_contract = {"schema": schema_rel.as_posix(), "example": example_rel.as_posix()}
        contract = manifest.get("contract")
        compatible = (
            manifest.get("schema_version") == manifest.get("contract_version") == "1.0.0"
            and manifest.get("status") == "FROZEN"
            and manifest.get("owner") == "BC-001"
            and isinstance(contract, dict)
            and all(contract.get(key) == value for key, value in expected_contract.items())
        )
        if not compatible:
            findings.append(
                _finding(
                    "CONTRACT_MANIFEST_INVALID",
                    manifest_rel,
                    "frozen 1.0.0 package required",
                )
            )
        functions, function_findings = _defined_functions(root, test_rel)
        findings.extend(function_findings)
        requirements = manifest.get("requirements")
        if not isinstance(requirements, list):
            findings.append(
                _finding(
                    "REQUIREMENT_EVIDENCE_INVALID",
                    manifest_rel,
                    "requirements list required",
                )
            )
            continue
        declared_tests: list[str] = []
        for entry in requirements:
            if not isinstance(entry, dict):
                findings.append(
                    _finding(
                        "REQUIREMENT_EVIDENCE_INVALID",
                        manifest_rel,
                        "requirement object required",
                    )
                )
                continue
            requirement, test = entry.get("id"), entry.get("test")
            valid = (
                isinstance(requirement, str)
                and isinstance(test, str)
                and isinstance(entry.get("control"), str)
                and isinstance(entry.get("failure_modes"), list)
                and bool(entry["failure_modes"])
            )
            if not valid or requirement in requirement_tests:
                findings.append(
                    _finding(
                        "REQUIREMENT_EVIDENCE_INVALID",
                        manifest_rel,
                        str(requirement),
                    )
                )
                continue
            requirement_tests[requirement] = test
            declared_tests.append(test)
            if test not in functions:
                findings.append(
                    _finding(
                        "REQUIREMENT_TEST_MISSING",
                        test_rel,
                        f"{requirement} requires {test}",
                    )
                )
        proof = manifest.get("proof")
        if not isinstance(proof, dict) or proof.get("required_tests") != declared_tests:
            findings.append(
                _finding(
                    "REQUIREMENT_EVIDENCE_INVALID",
                    manifest_rel,
                    "proof.required_tests drift",
                )
            )
    return requirement_tests, findings


def _consolidation_findings(root: Path, requirements: set[str]) -> list[Finding]:
    manifest, findings = _load_yaml(root, CONSOLIDATION_MANIFEST_REL, "CONSOLIDATION_UNREADABLE")
    schema, schema_findings = _load_json(root, CONSOLIDATION_SCHEMA_REL, "CONSOLIDATION_UNREADABLE")
    profile, profile_findings = _load_json(
        root, CONSOLIDATION_EXAMPLE_REL, "CONSOLIDATION_UNREADABLE"
    )
    findings.extend(schema_findings + profile_findings)
    if schema is not None and profile is not None:
        findings.extend(_schema_findings(profile, schema, CONSOLIDATION_EXAMPLE_REL))
    if not isinstance(manifest, dict) or not isinstance(profile, dict):
        return findings
    coverage = profile.get("coverage")
    gate = profile.get("review_gate")
    valid = (
        manifest.get("status") == profile.get("status") == "FROZEN"
        and manifest.get("contract_version") == profile.get("contract_version") == "1.0.0"
        and isinstance(coverage, dict)
        and set(coverage.get("requirement_ids", [])) == requirements
        and coverage.get("duplicates") == []
        and coverage.get("unassigned") == []
        and isinstance(gate, dict)
        and gate.get("candidate_state") == "READY_FOR_INDEPENDENT_REVIEW"
        and "STORY-0018" in gate.get("eligible_dependents", [])
        and gate.get("self_approval") == "PROHIBITED"
    )
    expected_artifacts = {
        relative.as_posix()
        for package in SLICE_PACKAGES
        for relative in package[:3]
    } | {REGISTRY_REL.as_posix()}
    recorded_artifacts: set[str] = set()
    for slice_record in profile.get("slices", []):
        if not isinstance(slice_record, dict):
            valid = False
            continue
        if set(slice_record.get("requirements", [])).difference(requirements):
            valid = False
        for artifact in slice_record.get("artifacts", []):
            if not isinstance(artifact, dict) or artifact.get("path") not in expected_artifacts:
                valid = False
                continue
            relative = Path(artifact["path"])
            try:
                content = (root / relative).read_bytes().replace(b"\r\n", b"\n")
                digest = hashlib.sha256(content).hexdigest()
            except OSError as error:
                findings.append(_finding("CONSOLIDATION_ARTIFACT_UNREADABLE", relative, str(error)))
                continue
            recorded_artifacts.add(relative.as_posix())
            if artifact.get("sha256") != digest:
                findings.append(
                    _finding(
                        "CONSOLIDATION_DIGEST_DRIFT",
                        relative,
                        "sha256 differs from frozen baseline",
                    )
                )
    if recorded_artifacts != expected_artifacts:
        valid = False
    if not valid:
        findings.append(
            _finding(
                "CONSOLIDATION_INVALID",
                CONSOLIDATION_EXAMPLE_REL,
                "coverage, gate, or artifacts drifted",
            )
        )
    return findings


def validate_contracts(root: Path) -> tuple[list[Finding], list[str]]:
    resolved = root.resolve()
    requirement_tests, findings = _slice_findings(resolved)
    findings.extend(_consolidation_findings(resolved, set(requirement_tests)))
    findings.extend(validate_registry(resolved))
    return sorted(set(findings)), sorted(requirement_tests)
