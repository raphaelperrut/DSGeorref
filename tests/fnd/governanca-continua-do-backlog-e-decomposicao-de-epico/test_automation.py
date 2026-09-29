from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_REL = Path(
    "tools/quality/contexts/engineering_governance/"
    "governanca-continua-do-backlog-e-decomposicao-de-epico/validator.py"
)
CONTRACT_TEST_REL = Path(
    "tests/fnd/governanca-continua-do-backlog-e-decomposicao-de-epico/test_epic_110_contract.py"
)
CONTRACT_REL = Path(
    "contracts/contexts/engineering_governance/fnd/"
    "governanca-continua-do-backlog-e-decomposicao-de-epico"
)
MANIFEST_REL = CONTRACT_REL / "contract-manifest.yaml"
SCHEMA_REL = CONTRACT_REL / "backlog-governance-profile.schema.json"
EXAMPLE_REL = CONTRACT_REL / "examples/backlog-governance-profile.json"
REFERENCED_RELS = (
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "portfolio-snapshot.schema.json"
    ),
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "examples/portfolio-snapshot.json"
    ),
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "issue-forecast.schema.json"
    ),
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "examples/issue-forecast.json"
    ),
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "repositorio-privado-project-central-views-campos-label/"
        "classicprofile-iss-native-parte-1/foundation-conformance.schema.json"
    ),
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "repositorio-privado-project-central-views-campos-label/"
        "classicprofile-iss-native-parte-1/examples/foundation-conformance.json"
    ),
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "foundation-boundaries.schema.json"
    ),
    Path(
        "contracts/contexts/engineering_governance/fnd/"
        "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
        "examples/foundation-boundaries.json"
    ),
)
INPUT_RELS = (MANIFEST_REL, SCHEMA_REL, EXAMPLE_REL, *REFERENCED_RELS)


def _load_validator() -> ModuleType:
    module_directory = str((ROOT / VALIDATOR_REL).parent)
    if module_directory not in sys.path:
        sys.path.insert(0, module_directory)
    spec = importlib.util.spec_from_file_location("epic_110_validator", ROOT / VALIDATOR_REL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = _load_validator()


def _load_contract_test() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "epic_110_contract_test",
        ROOT / CONTRACT_TEST_REL,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


contract_test = _load_contract_test()


def _copy_inputs(destination: Path) -> None:
    for relative in INPUT_RELS:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)


def _snapshot(root: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        sorted(
            (
                path.relative_to(root).as_posix(),
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
            for path in root.rglob("*")
            if path.is_file()
        )
    )


def _run_cli(root: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONHASHSEED": "0",
            "PYTHONUTF8": "1",
        }
    )
    return subprocess.run(
        [
            sys.executable,
            "-B",
            str(ROOT / VALIDATOR_REL),
            "--repository-root",
            str(root),
        ],
        cwd=root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


def _read_json(root: Path, relative: Path) -> dict[str, Any]:
    loaded = json.loads((root / relative).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _write_json(root: Path, relative: Path, value: dict[str, Any]) -> None:
    (root / relative).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _read_manifest(root: Path) -> dict[str, Any]:
    manifest = yaml.safe_load((root / MANIFEST_REL).read_text(encoding="utf-8"))
    assert isinstance(manifest, dict)
    return manifest


def _write_manifest(root: Path, manifest: dict[str, Any]) -> None:
    (root / MANIFEST_REL).write_text(
        yaml.safe_dump(manifest, sort_keys=False),
        encoding="utf-8",
    )


def _remove_manifest(root: Path) -> None:
    (root / MANIFEST_REL).unlink()


def _truncate_profile(root: Path) -> None:
    (root / EXAMPLE_REL).write_text('{"controls":', encoding="utf-8")


def _add_fail_open_fallback(root: Path) -> None:
    profile = _read_json(root, EXAMPLE_REL)
    profile["fallback"] = "ACCEPT"
    _write_json(root, EXAMPLE_REL, profile)


def _remove_requirement_mapping(root: Path) -> None:
    manifest = _read_manifest(root)
    manifest["requirements"] = manifest["requirements"][1:]
    _write_manifest(root, manifest)


def _duplicate_requirement_mapping(root: Path) -> None:
    manifest = _read_manifest(root)
    manifest["requirements"].append(copy.deepcopy(manifest["requirements"][0]))
    _write_manifest(root, manifest)


def _duplicate_proof(root: Path) -> None:
    manifest = _read_manifest(root)
    manifest["proof"]["required_tests"].append(manifest["proof"]["required_tests"][0])
    _write_manifest(root, manifest)


def _duplicate_mapping_and_proof(root: Path) -> None:
    manifest = _read_manifest(root)
    manifest["requirements"].append(copy.deepcopy(manifest["requirements"][0]))
    manifest["proof"]["required_tests"].append(manifest["proof"]["required_tests"][0])
    _write_manifest(root, manifest)


def _remove_referenced_contract(root: Path) -> None:
    (root / REFERENCED_RELS[0]).unlink()


Mutation = Callable[[Path], None]


FAIL_CLOSED_CASES: tuple[tuple[str, str, Mutation], ...] = (
    ("missing manifest", "ARTIFACT_MISSING", _remove_manifest),
    ("invalid profile JSON", "JSON_INVALID", _truncate_profile),
    ("fail-open fallback", "PROFILE_SCHEMA_VIOLATION", _add_fail_open_fallback),
    (
        "missing requirement mapping",
        "REQUIREMENT_MAPPING_MISMATCH",
        _remove_requirement_mapping,
    ),
    ("missing referenced contract", "ARTIFACT_MISSING", _remove_referenced_contract),
)


def test_epic_110_automacao() -> None:
    report = validator.build_report(ROOT)

    assert report["status"] == "PASS"
    assert report["failure_policy"] == "FAIL_CLOSED"
    assert report["execution_mode"] == "READ_ONLY"
    assert report["destructive_actions"] is False
    assert report["dry_run"] == "NOT_APPLICABLE_READ_ONLY"
    assert report["findings"] == []
    assert report["contract"] == {
        "manifest": MANIFEST_REL.as_posix(),
        "schema": SCHEMA_REL.as_posix(),
        "example": EXAMPLE_REL.as_posix(),
        "version": "1.0.0",
        "owner": "BC-001",
    }
    requirement_ids = [evidence["requirement_id"] for evidence in report["requirement_evidence"]]
    assert len(requirement_ids) == 5
    assert len(set(requirement_ids)) == len(requirement_ids)
    assert set(requirement_ids) == {
        "REQ-ISM-004",
        "REQ-ISS-002",
        "REQ-PLN-009",
        "REQ-PRJ-004",
        "REQ-SPRINT-001-004",
    }


def test_automation_is_idempotent_and_read_only(tmp_path: Path) -> None:
    _copy_inputs(tmp_path)
    before = _snapshot(tmp_path)

    first = validator.build_report(tmp_path)
    between = _snapshot(tmp_path)
    second = validator.build_report(tmp_path)
    after = _snapshot(tmp_path)

    assert first == second
    assert first["status"] == "PASS"
    assert first["dry_run"] == "NOT_APPLICABLE_READ_ONLY"
    assert before == between == after

    first_cli = _run_cli(tmp_path)
    second_cli = _run_cli(tmp_path)
    assert first_cli.returncode == second_cli.returncode == 0
    assert first_cli.stdout == second_cli.stdout
    assert first_cli.stderr == second_cli.stderr == ""
    assert _snapshot(tmp_path) == after


def test_duplicate_requirement_mapping_is_rejected_with_diagnostic(
    tmp_path: Path,
) -> None:
    _copy_inputs(tmp_path)
    _duplicate_requirement_mapping(tmp_path)

    report = validator.build_report(tmp_path)

    assert report["status"] == "FAIL"
    duplicate = next(
        finding
        for finding in report["findings"]
        if finding["code"] == "DUPLICATE_REQUIREMENT_MAPPING"
    )
    assert "REQ-ISM-004" in duplicate["detail"]
    assert "2 times" in duplicate["detail"]
    assert "exactly one mapping" in duplicate["remediation"]


def test_duplicate_proof_is_rejected_with_diagnostic(tmp_path: Path) -> None:
    _copy_inputs(tmp_path)
    _duplicate_proof(tmp_path)

    report = validator.build_report(tmp_path)

    assert report["status"] == "FAIL"
    duplicate = next(
        finding for finding in report["findings"] if finding["code"] == "DUPLICATE_PROOF"
    )
    assert "test_versioned_issue_portfolio_catalog_github_reconciliation" in duplicate["detail"]
    assert "2 times" in duplicate["detail"]
    assert "exactly one proof entry" in duplicate["remediation"]


def test_six_mapping_and_proof_regression_is_fail_closed_and_idempotent(
    tmp_path: Path,
) -> None:
    _copy_inputs(tmp_path)
    _duplicate_mapping_and_proof(tmp_path)
    manifest = _read_manifest(tmp_path)
    assert len(manifest["requirements"]) == 6
    assert len(manifest["proof"]["required_tests"]) == 6
    before = _snapshot(tmp_path)

    first = _run_cli(tmp_path)
    second = _run_cli(tmp_path)

    assert first.returncode == second.returncode == 1
    assert first.stdout == second.stdout
    assert first.stderr == second.stderr == ""
    assert "Traceback" not in first.stdout
    report = json.loads(first.stdout)
    assert report["status"] == "FAIL"
    assert report["failure_policy"] == "FAIL_CLOSED"
    codes = {finding["code"] for finding in report["findings"]}
    assert {
        "DUPLICATE_REQUIREMENT_MAPPING",
        "REQUIREMENT_MAPPING_COUNT_MISMATCH",
        "DUPLICATE_PROOF",
        "PROOF_COUNT_MISMATCH",
    } <= codes
    assert _snapshot(tmp_path) == before


def test_contract_sentinel_rejects_six_mapping_and_proof_regression(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _copy_inputs(tmp_path)
    _duplicate_mapping_and_proof(tmp_path)
    monkeypatch.setattr(contract_test, "MANIFEST_PATH", tmp_path / MANIFEST_REL)
    contract_test._load_manifest.cache_clear()

    with pytest.raises(AssertionError):
        contract_test.test_epic_110_contrato()

    contract_test._load_manifest.cache_clear()


@pytest.mark.parametrize(("case", "expected_code", "mutate"), FAIL_CLOSED_CASES)
def test_fail_closed_errors_have_actionable_diagnostics(
    tmp_path: Path,
    case: str,
    expected_code: str,
    mutate: Mutation,
) -> None:
    _copy_inputs(tmp_path)
    mutate(tmp_path)
    before = _snapshot(tmp_path)

    completed = _run_cli(tmp_path)

    assert completed.returncode == 1, case
    assert completed.stderr == "", case
    assert "Traceback" not in completed.stdout, case
    report = json.loads(completed.stdout)
    assert report["status"] == "FAIL", case
    assert report["failure_policy"] == "FAIL_CLOSED", case
    assert report["findings"], case
    assert expected_code in {finding["code"] for finding in report["findings"]}, case
    assert all(finding["artifact"] for finding in report["findings"]), case
    assert all(finding["detail"] for finding in report["findings"]), case
    assert all(finding["remediation"] for finding in report["findings"]), case
    assert _snapshot(tmp_path) == before, case
