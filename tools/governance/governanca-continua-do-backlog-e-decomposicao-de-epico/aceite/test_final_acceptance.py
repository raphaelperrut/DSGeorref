from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CAPABILITY = "governanca-continua-do-backlog-e-decomposicao-de-epico"
TEST_ROOT = f"tests/fnd/{CAPABILITY}"
AUTOMATION = f"{TEST_ROOT}/test_automation.py"
CONTRACT = f"{TEST_ROOT}/test_epic_110_contract.py"
INTEGRATION = f"tools/governance/{CAPABILITY}/integracao/test_repository_integration.py"


def _assert_existing_tests_pass(nodes: tuple[str, ...], temporary_root: Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "--basetemp",
            str(temporary_root / "delegated"),
            *nodes,
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    print(completed.stdout)


def test_epic_110_aceite_happy_path(tmp_path: Path) -> None:
    _assert_existing_tests_pass(
        (
            f"{INTEGRATION}::test_epic_110_integracao",
            f"{AUTOMATION}::test_epic_110_automacao",
            f"{CONTRACT}::test_epic_110_contrato",
        ),
        tmp_path,
    )


def test_epic_110_aceite_negative_paths(tmp_path: Path) -> None:
    _assert_existing_tests_pass(
        (
            f"{AUTOMATION}::test_fail_closed_errors_have_actionable_diagnostics",
            f"{AUTOMATION}::test_six_mapping_and_proof_regression_is_fail_closed_and_idempotent",
            f"{AUTOMATION}::test_contract_sentinel_rejects_six_mapping_and_proof_regression",
            f"{CONTRACT}::test_epic_110_contract_rejects_fail_open_paths",
            f"{CONTRACT}::test_epic_110_contract_rejects_missing_unknown_or_wrong_authority",
            f"{CONTRACT}::test_epic_110_v1_reader_rejects_optional_additions_and_new_version",
        ),
        tmp_path,
    )
