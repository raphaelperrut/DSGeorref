import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from catalog_contract import (
    CATALOG_SCHEMA_PATH,
    COMMAND,
    CONTRACT_PATH,
    CORPUS_SCHEMA_PATH,
    EXPECTED_CHECKPOINT_IDENTITY,
    EXPECTED_CRITERIA,
    EXPECTED_FAILURE_POLICY,
    EXPECTED_LAYER_POLICY,
    EXPECTED_OWNERS,
    EXPECTED_SOURCES,
    EXPECTED_TESTS,
    ROOT,
)
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    field: str
    detail: str


def _finding(code: str, field: str, detail: str) -> Finding:
    return Finding(code=code, field=field, detail=detail)


def _load_json(path: Path, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [_finding(code, path.as_posix(), str(error))]


def _load_yaml(path: Path, code: str) -> tuple[object | None, list[Finding]]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return None, [_finding(code, path.as_posix(), str(error))]


def _schema_findings(instance: object, schema: object, label: str) -> list[Finding]:
    if not isinstance(schema, dict):
        return [_finding("SCHEMA_DEFINITION_INVALID", label, "schema must be an object")]
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        return [_finding("SCHEMA_DEFINITION_INVALID", label, error.message)]
    validator = Draft202012Validator(schema)
    return [
        _finding(
            f"{label}_SCHEMA_INVALID",
            ".".join(str(part) for part in error.absolute_path) or "$",
            error.message,
        )
        for error in sorted(
            validator.iter_errors(instance),
            key=lambda item: ".".join(str(part) for part in item.absolute_path),
        )
    ]


def _safe_repository_path(value: object) -> Path | None:
    if not isinstance(value, str):
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    try:
        resolved = (ROOT / relative).resolve()
    except OSError:
        return None
    return resolved if resolved.is_relative_to(ROOT.resolve()) else None


def _validate_sources(capability: dict[str, Any], index: int) -> list[Finding]:
    findings: list[Finding] = []
    knowledge_sources = capability.get("knowledge_sources")
    values = [capability.get("contract")]
    if isinstance(knowledge_sources, list):
        values.extend(knowledge_sources)
    for value in values:
        path = _safe_repository_path(value)
        field = f"capabilities.{index}.sources"
        if path is None:
            findings.append(_finding("SOURCE_PATH_INVALID", field, repr(value)))
        elif path.suffix.lower() in {".py", ".pyc", ".pyd", ".so", ".dll"}:
            findings.append(_finding("LEGACY_RUNTIME_IMPORT", field, path.as_posix()))
        elif not path.is_file():
            findings.append(_finding("SOURCE_MISSING", field, path.as_posix()))
    return findings


def _validate_catalog(catalog: object) -> list[Finding]:
    if not isinstance(catalog, dict) or not isinstance(catalog.get("capabilities"), list):
        return []
    findings: list[Finding] = []
    names: list[object] = []
    for index, capability in enumerate(catalog["capabilities"]):
        if not isinstance(capability, dict):
            continue
        name = capability.get("stable_name")
        names.append(name)
        expected_owner = EXPECTED_OWNERS.get(name) if isinstance(name, str) else None
        if expected_owner is None or capability.get("owner") != expected_owner:
            findings.append(
                _finding("CAPABILITY_OWNER_INVALID", f"capabilities.{index}.owner", repr(name))
            )
        findings.extend(_validate_sources(capability, index))
    if len(names) != len(set(map(repr, names))):
        findings.append(
            _finding("CAPABILITY_NAME_DUPLICATE", "capabilities", "stable names must be unique")
        )
    string_names = {name for name in names if isinstance(name, str)}
    if string_names != set(EXPECTED_OWNERS) or len(string_names) != len(names):
        findings.append(
            _finding(
                "CAPABILITY_INVENTORY_DRIFT", "capabilities", "frozen module inventory differs"
            )
        )
    return findings


def _validate_contract(contract: object) -> list[Finding]:
    if not isinstance(contract, dict):
        return [_finding("FOUNDATION_CONTRACT_DRIFT", "$contract", "object required")]
    runtime = contract.get("runtime") if isinstance(contract.get("runtime"), dict) else {}
    compatibility = (
        contract.get("compatibility") if isinstance(contract.get("compatibility"), dict) else {}
    )
    identity = contract.get("contract") if isinstance(contract.get("contract"), dict) else {}
    actual = {
        "contract_version": contract.get("contract_version"),
        "status": contract.get("status"),
        "owner": contract.get("owner"),
        "contract_id": identity.get("id"),
        "requirements": contract.get("requirements"),
        "runtime_implementation": runtime.get("implementation"),
        "unknown_properties": compatibility.get("unknown_properties"),
    }
    expected = {
        "contract_version": "1.0.0",
        "status": "FROZEN",
        "owner": "BC-001",
        "contract_id": "capability-catalog-foundation-contract",
        "requirements": ["REQ-AI-007", "REQ-TST-001"],
        "runtime_implementation": "DOWNSTREAM_STORIES_ONLY",
        "unknown_properties": "REJECT",
    }
    if actual != expected:
        return [_finding("FOUNDATION_CONTRACT_DRIFT", "$contract", repr(actual))]
    return []


def _fixture_payload_findings(fixture: dict[str, Any], path: Path) -> list[Finding]:
    payload, findings = _load_json(path, "CORPUS_FIXTURE_UNREADABLE")
    if findings or not isinstance(payload, dict):
        return findings or [_finding("CORPUS_FIXTURE_INVALID", path.as_posix(), "object required")]
    expected = {"fixture_id": fixture.get("fixture_id"), "layer": fixture.get("layer")}
    actual = {key: payload.get(key) for key in expected}
    if actual != expected or set(payload) != {"fixture_id", "layer", "sentinel"}:
        return [_finding("CORPUS_FIXTURE_INVALID", path.as_posix(), "identity or shape differs")]
    return []


def _validate_fixture(fixture: dict[str, Any], index: int) -> list[Finding]:
    findings: list[Finding] = []
    layer = fixture.get("layer")
    expected_policy = EXPECTED_LAYER_POLICY.get(layer) if isinstance(layer, str) else None
    actual_policy = (fixture.get("split"), fixture.get("access"))
    if expected_policy is None or actual_policy != expected_policy:
        findings.append(_finding("CORPUS_ACCESS_INVALID", f"fixtures.{index}", repr(layer)))
    path = _safe_repository_path(fixture.get("path"))
    if path is None:
        findings.append(_finding("CORPUS_PATH_INVALID", f"fixtures.{index}.path", "unsafe path"))
        return findings
    findings.extend(_fixture_payload_findings(fixture, path))
    if path.is_file():
        try:
            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as error:
            findings.append(_finding("CORPUS_FIXTURE_UNREADABLE", path.as_posix(), str(error)))
        else:
            if actual_hash != fixture.get("sha256"):
                findings.append(
                    _finding("CORPUS_HASH_MISMATCH", f"fixtures.{index}.sha256", actual_hash)
                )
    return findings


def _validate_corpus(corpus: object) -> list[Finding]:
    if not isinstance(corpus, dict) or not isinstance(corpus.get("fixtures"), list):
        return []
    findings: list[Finding] = []
    identities: list[tuple[object, object, object]] = []
    layers: set[str] = set()
    for index, fixture in enumerate(corpus["fixtures"]):
        if not isinstance(fixture, dict):
            continue
        identities.append((fixture.get("fixture_id"), fixture.get("path"), fixture.get("sha256")))
        layer = fixture.get("layer")
        if isinstance(layer, str):
            layers.add(layer)
        findings.extend(_validate_fixture(fixture, index))
    for position, label in enumerate(("fixture_id", "path", "sha256")):
        values = [identity[position] for identity in identities]
        if len(values) != len(set(map(repr, values))):
            findings.append(
                _finding("CORPUS_OVERLAP", label, "values must be unique across splits")
            )
    if layers != set(EXPECTED_LAYER_POLICY):
        findings.append(_finding("CORPUS_LAYER_MISSING", "fixtures", "test pyramid is incomplete"))
    return findings


def _validate_checkpoint(checkpoint: object) -> list[Finding]:
    if not isinstance(checkpoint, dict):
        return [_finding("CHECKPOINT_INVALID", "$", "object required")]
    findings: list[Finding] = []
    identity = {
        key: checkpoint.get(key)
        for key in ("checkpoint_id", "story_id", "issue_id", "task_id", "contract_version")
    }
    if identity != EXPECTED_CHECKPOINT_IDENTITY:
        findings.append(_finding("CHECKPOINT_IDENTITY_INVALID", "$checkpoint", repr(identity)))
    if checkpoint.get("python_runtime") != ">=3.12,<3.13":
        findings.append(_finding("PYTHON_RUNTIME_INVALID", "python_runtime", "3.12 required"))
    if checkpoint.get("sources") != EXPECTED_SOURCES:
        findings.append(_finding("CHECKPOINT_SOURCES_INVALID", "sources", "source paths differ"))
    commands = checkpoint.get("commands")
    if commands != {"local": [COMMAND], "ci": [COMMAND]}:
        findings.append(
            _finding("COMMAND_PARITY_INVALID", "commands", "local and CI command must be identical")
        )
    if checkpoint.get("failure_policy") != EXPECTED_FAILURE_POLICY:
        findings.append(_finding("SILENT_FALLBACK_PROHIBITED", "failure_policy", "must be false"))
    required_tests = checkpoint.get("required_tests")
    if not isinstance(required_tests, list) or set(map(str, required_tests)) != EXPECTED_TESTS:
        findings.append(
            _finding("REQUIRED_TESTS_INVALID", "required_tests", "mandatory tests differ")
        )
    acceptance_evidence = checkpoint.get("acceptance_evidence")
    if not isinstance(acceptance_evidence, dict) or set(acceptance_evidence) != EXPECTED_CRITERIA:
        findings.append(
            _finding("ACCEPTANCE_EVIDENCE_INVALID", "acceptance_evidence", "criteria differ")
        )
    return findings


def validate_paths(
    catalog_path: Path,
    corpus_path: Path,
    checkpoint_path: Path,
) -> list[Finding]:
    paths = {
        "CATALOG": catalog_path,
        "CATALOG_SCHEMA": CATALOG_SCHEMA_PATH,
        "CORPUS": corpus_path,
        "CORPUS_SCHEMA": CORPUS_SCHEMA_PATH,
        "CHECKPOINT": checkpoint_path,
    }
    loaded: dict[str, object] = {}
    findings: list[Finding] = []
    for label, path in paths.items():
        value, errors = _load_json(path, f"{label}_UNREADABLE")
        findings.extend(errors)
        if value is not None:
            loaded[label] = value
    contract, contract_errors = _load_yaml(CONTRACT_PATH, "CONTRACT_UNREADABLE")
    findings.extend(contract_errors)
    if contract is not None:
        loaded["CONTRACT"] = contract
    if findings:
        return sorted(findings)
    findings.extend(_schema_findings(loaded["CATALOG"], loaded["CATALOG_SCHEMA"], "CATALOG"))
    findings.extend(_schema_findings(loaded["CORPUS"], loaded["CORPUS_SCHEMA"], "CORPUS"))
    findings.extend(_validate_contract(loaded["CONTRACT"]))
    findings.extend(_validate_catalog(loaded["CATALOG"]))
    findings.extend(_validate_corpus(loaded["CORPUS"]))
    findings.extend(_validate_checkpoint(loaded["CHECKPOINT"]))
    return sorted(set(findings))
