from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from validation_types import Finding

SLUG = "migrations-ci-secret-dependency-scan-e-telemetria-mini"
CONTRACT_ROOT = Path(f"contracts/contexts/engineering_governance/fnd/{SLUG}")
TEST_ROOT = Path(f"tests/fnd/{SLUG}")
CONSOLIDATION_REL = Path(
    f"docs/03-engineering/contexts/engineering_governance/{SLUG}/consolidacao/CONSOLIDATION.json"
)
VERSION_MATRIX_REL = Path("contracts/operations/version-and-rollback-matrix.yaml")
SLO_CATALOG_REL = Path("contracts/operations/slo-sli-catalog.yaml")

CONTRACT_PACKAGES = (
    (
        CONTRACT_ROOT / "aie-bex-epic-parte-1/contract-manifest.yaml",
        CONTRACT_ROOT / "aie-bex-epic-parte-1/contract-foundation.schema.json",
        CONTRACT_ROOT / "aie-bex-epic-parte-1/examples/contract-foundation.json",
        TEST_ROOT / "test_contract_foundation.py",
    ),
    (
        CONTRACT_ROOT / "sgvcal-parte-2/contract-manifest.yaml",
        CONTRACT_ROOT / "sgvcal-parte-2/sgvcal-conformance.schema.json",
        CONTRACT_ROOT / "sgvcal-parte-2/examples/sgvcal-conformance.json",
        TEST_ROOT / "test_sgvcal_conformance.py",
    ),
)

IMPLEMENTATION_EVIDENCE = {
    Path(
        "evidence/implementation/migrations-ci-secret-dependency-scan-e-telemetria/"
        "aie-bex-parte-1/IMPLEMENTATION_EVIDENCE.yaml"
    ): ("STORY-0708", "ISSUE-0818", "TASK-0708"),
    Path(
        "evidence/implementation/migrations-ci-secret-dependency-scan-e-telemetria/"
        "bex-epic-frz-parte-2/IMPLEMENTATION_EVIDENCE.yaml"
    ): ("STORY-0709", "ISSUE-0819", "TASK-0709"),
    Path(
        "evidence/implementation/migrations-ci-secret-dependency-scan-e-telemetria/"
        "fs1-gov-sgvcal-parte-3/IMPLEMENTATION_EVIDENCE.yaml"
    ): ("STORY-0710", "ISSUE-0820", "TASK-0710"),
    Path(
        "evidence/implementation/migrations-ci-secret-dependency-scan-e-telemetria/"
        "sgvcal-srg-srp-parte-4/IMPLEMENTATION_EVIDENCE.yaml"
    ): ("STORY-0711", "ISSUE-0821", "TASK-0711"),
}


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


def _contract_findings(root: Path) -> tuple[dict[str, str], list[Finding]]:
    evidence: dict[str, str] = {}
    findings: list[Finding] = []
    for manifest_rel, schema_rel, example_rel, test_rel in CONTRACT_PACKAGES:
        manifest, manifest_errors = _load_yaml(root, manifest_rel, "CONTRACT_UNREADABLE")
        schema, schema_errors = _load_json(root, schema_rel, "CONTRACT_UNREADABLE")
        example, example_errors = _load_json(root, example_rel, "CONTRACT_UNREADABLE")
        findings.extend(manifest_errors + schema_errors + example_errors)
        if schema is not None and example is not None:
            findings.extend(_schema_findings(example, schema, example_rel))
        functions, function_errors = _defined_functions(root, test_rel)
        findings.extend(function_errors)
        if not isinstance(manifest, dict):
            continue
        contract = manifest.get("contract")
        valid_manifest = (
            manifest.get("status") == "FROZEN"
            and manifest.get("owner") == "BC-001"
            and manifest.get("schema_version") == manifest.get("contract_version") == "1.0.0"
            and isinstance(contract, dict)
            and contract.get("schema") == schema_rel.as_posix()
            and contract.get("example") == example_rel.as_posix()
        )
        if not valid_manifest:
            findings.append(
                _finding("CONTRACT_MANIFEST_INVALID", manifest_rel, "frozen 1.0.0 package required")
            )
        requirements = manifest.get("requirements")
        if not isinstance(requirements, list):
            findings.append(
                _finding("REQUIREMENT_EVIDENCE_INVALID", manifest_rel, "requirements list required")
            )
            continue
        declared: list[str] = []
        for entry in requirements:
            if not isinstance(entry, dict):
                findings.append(
                    _finding(
                        "REQUIREMENT_EVIDENCE_INVALID", manifest_rel, "requirement object required"
                    )
                )
                continue
            requirement, test = entry.get("id"), entry.get("test")
            valid = (
                isinstance(requirement, str)
                and isinstance(test, str)
                and isinstance(entry.get("control"), str)
                and bool(entry.get("failure_modes"))
            )
            if not valid:
                findings.append(
                    _finding("REQUIREMENT_EVIDENCE_INVALID", manifest_rel, str(requirement))
                )
                continue
            previous = evidence.get(requirement)
            if previous is not None and previous != test:
                findings.append(
                    _finding(
                        "REQUIREMENT_EVIDENCE_INVALID",
                        manifest_rel,
                        f"conflicting proof for {requirement}",
                    )
                )
            evidence[requirement] = test
            declared.append(test)
            if test not in functions:
                findings.append(
                    _finding("REQUIREMENT_TEST_MISSING", test_rel, f"{requirement} requires {test}")
                )
        proof = manifest.get("proof")
        if not isinstance(proof, dict) or proof.get("required_tests") != declared:
            findings.append(
                _finding("REQUIREMENT_EVIDENCE_INVALID", manifest_rel, "proof.required_tests drift")
            )
    return evidence, findings


def _implementation_findings(root: Path, evidence: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    for relative, expected_identity in IMPLEMENTATION_EVIDENCE.items():
        document, load_errors = _load_yaml(root, relative, "EVIDENCE_UNREADABLE")
        findings.extend(load_errors)
        if not isinstance(document, dict):
            continue
        identity = document.get("identity")
        expected = {
            "epic_id": "EPIC-005",
            "story_id": expected_identity[0],
            "issue_id": expected_identity[1],
            "task_id": expected_identity[2],
        }
        coverage = document.get("coverage")
        artifacts = document.get("implementation_artifacts")
        valid = (
            document.get("schema_version") == "1.0.0"
            and isinstance(identity, dict)
            and all(identity.get(key) == value for key, value in expected.items())
            and isinstance(coverage, list)
            and len(coverage) == 10
            and isinstance(artifacts, list)
        )
        if not valid:
            findings.append(
                _finding("EVIDENCE_INVALID", relative, "identity, coverage, or artifact list drift")
            )
            continue
        test_paths = [
            Path(value)
            for value in artifacts
            if isinstance(value, str) and Path(value).name.startswith("test_")
        ]
        functions: set[str] = set()
        for test_path in test_paths:
            defined, errors = _defined_functions(root, test_path)
            functions.update(defined)
            findings.extend(errors)
        for artifact in artifacts:
            if not isinstance(artifact, str) or not (root / artifact).is_file():
                findings.append(
                    _finding(
                        "IMPLEMENTATION_ARTIFACT_MISSING", Path(str(artifact)), relative.as_posix()
                    )
                )
        for entry in coverage:
            requirement = entry.get("requirement") if isinstance(entry, dict) else None
            raw_test = entry.get("test") if isinstance(entry, dict) else None
            test = raw_test.split()[0] if isinstance(raw_test, str) else None
            if not isinstance(requirement, str) or not isinstance(test, str):
                findings.append(_finding("EVIDENCE_INVALID", relative, "coverage entry invalid"))
                continue
            previous = evidence.get(requirement)
            if previous is not None and previous != test:
                findings.append(
                    _finding(
                        "REQUIREMENT_EVIDENCE_INVALID",
                        relative,
                        f"conflicting proof for {requirement}",
                    )
                )
            evidence[requirement] = test
            if test not in functions:
                findings.append(
                    _finding("REQUIREMENT_TEST_MISSING", relative, f"{requirement} requires {test}")
                )
    if len(evidence) != 51:
        findings.append(
            _finding(
                "REQUIREMENT_EVIDENCE_INVALID",
                CONSOLIDATION_REL,
                f"expected 51 requirements, found {len(evidence)}",
            )
        )
    return findings


def _consolidation_findings(root: Path) -> list[Finding]:
    document, findings = _load_json(root, CONSOLIDATION_REL, "CONSOLIDATION_UNREADABLE")
    if not isinstance(document, dict):
        return findings
    gate = document.get("review_gate")
    predecessors = document.get("predecessors")
    valid = (
        document.get("schema_version") == "1.0.0"
        and document.get("identity", {}).get("story_id") == "STORY-0022"
        and isinstance(predecessors, list)
        and len(predecessors) == 4
        and isinstance(gate, dict)
        and gate.get("candidate_state") == "READY_FOR_SENTINEL_QA"
        and gate.get("self_approval") == "PROHIBITED"
        and gate.get("released_dependents") == []
    )
    if not valid:
        findings.append(
            _finding("CONSOLIDATION_INVALID", CONSOLIDATION_REL, "identity or review gate drift")
        )
        return findings
    expected_paths = {path.as_posix() for path in IMPLEMENTATION_EVIDENCE}
    actual_paths = {item.get("evidence_path") for item in predecessors if isinstance(item, dict)}
    if actual_paths != expected_paths:
        findings.append(
            _finding("CONSOLIDATION_INVALID", CONSOLIDATION_REL, "predecessor evidence set drift")
        )
    for item in predecessors:
        if not isinstance(item, dict) or not isinstance(item.get("evidence_path"), str):
            continue
        path = Path(item["evidence_path"])
        try:
            content = (root / path).read_bytes().replace(b"\r\n", b"\n")
        except OSError as error:
            findings.append(_finding("EVIDENCE_UNREADABLE", path, str(error)))
            continue
        if hashlib.sha256(content).hexdigest() != item.get("evidence_sha256"):
            findings.append(
                _finding("EVIDENCE_DIGEST_DRIFT", path, "sha256 differs from consolidation")
            )
    return findings


def _operational_control_findings(root: Path) -> list[Finding]:
    profile_rel = CONTRACT_PACKAGES[0][2]
    profile, findings = _load_json(root, profile_rel, "CONTRACT_UNREADABLE")
    matrix, matrix_errors = _load_yaml(root, VERSION_MATRIX_REL, "MIGRATION_CONTROL_UNREADABLE")
    catalog, catalog_errors = _load_yaml(root, SLO_CATALOG_REL, "TELEMETRY_CONTROL_UNREADABLE")
    findings.extend(matrix_errors + catalog_errors)
    controls = profile.get("controls") if isinstance(profile, dict) else None
    migrations = controls.get("schema_migrations") if isinstance(controls, dict) else None
    telemetry = controls.get("telemetry") if isinstance(controls, dict) else None
    migration_valid = (
        isinstance(migrations, dict)
        and migrations.get("authority") == "POSTGRESQL"
        and migrations.get("flow") == "EXPAND_MIGRATE_CONTRACT"
        and migrations.get("implicit_restart_migration") == "PROHIBITED"
        and migrations.get("failed_cutover") == "REJECT"
        and isinstance(matrix, dict)
        and matrix.get("status") == "FROZEN"
        and matrix.get("migration_rules")
        == [
            "no implicit migration on restart",
            "backup preflight",
            "readiness and smoke evidence",
            "rollback decision before contract phase",
        ]
    )
    if not migration_valid:
        findings.append(
            _finding(
                "MIGRATION_CONTROL_INVALID",
                VERSION_MATRIX_REL,
                "fail-closed migration policy required",
            )
        )
    telemetry_valid = (
        isinstance(telemetry, dict)
        and telemetry.get("protocol") == "OPENTELEMETRY"
        and telemetry.get("backend") == "REPLACEABLE"
        and telemetry.get("authority") == "NON_AUTHORITATIVE"
        and telemetry.get("exporter_outage") == "KEEP_LOCAL_MINIMUM_SIGNALS"
        and telemetry.get("missing_correlation") == "REJECT"
        and isinstance(catalog, dict)
        and catalog.get("status") == "TARGETS_REQUIRE_MEASUREMENT"
        and catalog.get("scientific", {}).get("no_unbenchmarked_claims") is True
    )
    if not telemetry_valid:
        findings.append(
            _finding(
                "TELEMETRY_CONTROL_INVALID",
                SLO_CATALOG_REL,
                "bounded non-authoritative telemetry required",
            )
        )
    return findings


def validate_artifacts(root: Path) -> tuple[list[Finding], list[str]]:
    resolved = root.resolve()
    evidence, findings = _contract_findings(resolved)
    findings.extend(_implementation_findings(resolved, evidence))
    findings.extend(_consolidation_findings(resolved))
    findings.extend(_operational_control_findings(resolved))
    return sorted(set(findings)), sorted(evidence)
