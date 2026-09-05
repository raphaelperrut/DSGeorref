from __future__ import annotations

import hashlib
import importlib
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
SLUG = "catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca"
DOC_ROOT = ROOT / "docs/03-engineering/contexts/engineering_governance" / SLUG
TOOL_ROOT = ROOT / "tools/governance" / SLUG
VALIDATOR = TOOL_ROOT / "validate_catalog.py"
CATALOG = DOC_ROOT / "capability-catalog.json"
CORPUS = DOC_ROOT / "test-corpus-manifest.json"
CHECKPOINT = TOOL_ROOT / "foundation-checkpoint.json"
TASK = ROOT / ".codex/tasks/TASK-0027.json"


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _run_validator(*arguments: object) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(VALIDATOR), *(str(argument) for argument in arguments)]
    return subprocess.run(command, cwd=ROOT, capture_output=True, check=False, text=True)


def _report(result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    value = json.loads(result.stdout)
    assert isinstance(value, dict)
    return value


def _validator_module() -> ModuleType:
    sys.path.insert(0, str(TOOL_ROOT))
    try:
        return importlib.import_module("catalog_validation")
    finally:
        sys.path.remove(str(TOOL_ROOT))


def test_reference_capability_inventory_no_code_import() -> None:
    result = _run_validator()
    catalog = _json(CATALOG)

    assert result.returncode == 0, result.stdout + result.stderr
    assert _report(result)["status"] == "PASS"
    assert catalog["source_policy"] == {
        "prior_system_use": "REQUIREMENTS_AND_ATTRIBUTED_CORPUS_ONLY",
        "code_import": "PROHIBITED",
        "plugin_import": "PROHIBITED",
        "runtime_import": "PROHIBITED",
        "provenance": "REQUIRED",
    }
    capabilities = catalog["capabilities"]
    assert {item["owner"]["module"] for item in capabilities} == {"MOD-005", "MOD-006", "MOD-007"}
    assert len({item["stable_name"] for item in capabilities}) == len(capabilities)
    source_suffixes = {
        Path(source).suffix
        for item in capabilities
        for source in [item["contract"], *item["knowledge_sources"]]
    }
    assert source_suffixes <= {".json", ".md", ".yaml"}


def test_corpus_license_hash_split_and_access_integrity() -> None:
    corpus = _json(CORPUS)
    expected_access = {
        "DEVELOPMENT": "DEVELOPMENT",
        "VALIDATION_PROTECTED": "QA_PROTECTED",
        "HOLDOUT_BLIND": "INDEPENDENT_QA_BLIND",
    }
    hashes: list[str] = []

    assert corpus["splits"] == ["DEVELOPMENT", "VALIDATION_PROTECTED", "HOLDOUT_BLIND"]
    assert corpus["scientific_claim"] == "PROHIBITED"
    for fixture in corpus["fixtures"]:
        payload_path = ROOT / fixture["path"]
        actual_hash = hashlib.sha256(payload_path.read_bytes()).hexdigest()
        assert fixture["origin"] == "GENERATED_DSGEOREF_CONTROL_SENTINEL"
        assert fixture["license"] == "CC-BY-4.0"
        assert fixture["access"] == expected_access[fixture["split"]]
        assert fixture["sha256"] == actual_hash
        hashes.append(actual_hash)
    assert len(hashes) == len(set(hashes))


def test_epic_006_fundacao() -> None:
    result = _run_validator()
    checkpoint = _json(CHECKPOINT)
    task = _json(TASK)

    assert result.returncode == 0, result.stdout + result.stderr
    assert checkpoint["commands"]["local"] == checkpoint["commands"]["ci"]
    assert set(checkpoint["required_tests"]) == set(task["tests"])
    assert set(checkpoint["acceptance_evidence"]) == set(task["acceptance_criterion_ids"])
    assert task["allow_paths"] == task["phase_f_review"]["files"]["allow_paths"]
    required_paths = {
        ".codex/tasks/TASK-0027.json",
        f"tests/fnd/{SLUG}/test_foundation.py",
        "evidence/implementation/epic-006/story-0027/**",
    }
    assert required_paths <= set(task["allow_paths"])


def test_foundation_rejects_contract_drift_silent_fallback_and_corpus_tampering() -> None:
    validator = _validator_module()
    catalog = _json(CATALOG)
    catalog["capabilities"][0]["runtime_import"] = "legacy.module"

    checkpoint = _json(CHECKPOINT)
    checkpoint["failure_policy"]["silent_fallback"] = True

    contract, contract_errors = validator._load_yaml(validator.CONTRACT_PATH, "CONTRACT_UNREADABLE")
    assert not contract_errors and isinstance(contract, dict)
    contract["contract_version"] = "2.0.0"

    corpus = _json(CORPUS)
    corpus["fixtures"][1]["sha256"] = corpus["fixtures"][0]["sha256"]
    findings = validator._schema_findings(
        catalog,
        _json(DOC_ROOT / "capability-catalog.schema.json"),
        "CATALOG",
    )
    findings.extend(validator._validate_catalog(catalog))
    findings.extend(validator._validate_contract(contract))
    findings.extend(validator._validate_checkpoint(checkpoint))
    findings.extend(validator._validate_corpus(corpus))
    codes = {finding.code for finding in findings}

    assert {
        "CATALOG_SCHEMA_INVALID",
        "CORPUS_HASH_MISMATCH",
        "CORPUS_OVERLAP",
        "FOUNDATION_CONTRACT_DRIFT",
        "SILENT_FALLBACK_PROHIBITED",
    } <= codes


def test_foundation_rejects_missing_catalog_without_fallback() -> None:
    result = _run_validator("--catalog", ROOT / "missing-issue-0137-catalog.json")

    assert result.returncode == 2
    assert {finding["code"] for finding in _report(result)["findings"]} == {"CATALOG_UNREADABLE"}
