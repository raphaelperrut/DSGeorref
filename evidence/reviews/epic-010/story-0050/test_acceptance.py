"""Compose integrated EPIC-010 tests; no authorization or fixture logic lives here."""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[4]
BACKEND = "tests/backend/identity_access/resource_authorization"
SECURITY = (
    "tests/security/contexts/identity_access/"
    "autorizacao-por-projeto-operacao-artefato-e-caminho/"
    "test_resource_authorization_security.py"
)
CONTRACT = (
    "contracts/contexts/identity_access/plt/"
    "autorizacao-por-projeto-operacao-artefato-e-caminho/test_resource_authorization.py"
)
SURFACE = (
    "src/contexts/identity_access/features/"
    "autorizacao-por-projeto-operacao-artefato-e-caminho/surface.test.tsx"
)


def run_report(
    command: list[str],
    cwd: Path,
    report: Path,
    expected: int,
    selected_name: str | None = None,
) -> None:
    result = subprocess.run(
        command, cwd=cwd, capture_output=True, encoding="utf-8", errors="replace", check=False
    )
    output = result.stdout + result.stderr
    print(output, end="")
    assert result.returncode == 0, output
    suites = list(ElementTree.parse(report).getroot().iter("testsuite"))
    assert suites, output
    assert all(
        int(suite.attrib.get(key, "0")) == 0 for suite in suites for key in ("errors", "failures")
    ), output
    cases = [case for suite in suites for case in suite.findall("testcase")]
    assert len(cases) == sum(int(suite.attrib["tests"]) for suite in suites), output
    selected = (
        cases
        if selected_name is None
        else [case for case in cases if case.attrib["name"] == selected_name]
    )
    assert len(selected) == expected, output
    assert all(len(case) == 0 for case in selected), output
    # Vitest reports name-filtered cases as skipped; the selected case must run.
    assert all(case.find("skipped") is not None for case in cases if case not in selected), output
    assert sum(int(suite.attrib.get("skipped", "0")) for suite in suites) == (
        len(cases) - len(selected)
    ), output


def run_cases(tmp_path: Path, *nodes: str, expected: int) -> None:
    report = tmp_path / "canonical-python.xml"
    run_report(
        [
            sys.executable,
            "-X",
            "utf8",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "--import-mode=importlib",
            f"--junitxml={report}",
            f"--basetemp={tmp_path / 'python-tmp'}",
            *nodes,
        ],
        ROOT,
        report,
        expected,
    )


def test_epic_010_aceite_happy_path(tmp_path: Path) -> None:
    run_cases(
        tmp_path,
        f"{CONTRACT}::test_epic_010_politica",
        f"{SECURITY}::test_epic_010_seguranca_happy_path",
        f"{BACKEND}/test_consolidation.py::test_story_0047_slice_consolidation",
        f"{BACKEND}/test_consolidation.py::test_consolidation_preserves_requirement_ownership",
        f"{BACKEND}/test_hardware.py::test_cpu_baseline_gpu_optional_no_silent_fallback",
        expected=9,
    )
    report = tmp_path / "canonical-surface.xml"
    pnpm = shutil.which(os.environ.get("PNPM", "pnpm"))
    assert pnpm is not None, "Pinned pnpm must be available on PATH"
    run_report(
        [
            pnpm,
            "exec",
            "vitest",
            "run",
            SURFACE,
            "--environment",
            "jsdom",
            "-t",
            "^test_epic_010_superficie$",
            "--reporter=junit",
            f"--outputFile={report}",
        ],
        ROOT / "src/frontend",
        report,
        1,
        selected_name="test_epic_010_superficie",
    )


def test_epic_010_aceite_negative_paths(tmp_path: Path) -> None:
    run_cases(
        tmp_path,
        f"{SECURITY}::test_epic_010_seguranca_negative_paths",
        f"{SECURITY}::test_abuse_eligibility_is_conjunctive",
        f"{SECURITY}::test_previous_allow_never_survives_authority_change",
        f"{SECURITY}::test_query_permission_does_not_expand_pat_scope",
        f"{SECURITY}::test_persisted_secret_minimization_and_audit_allowlist",
        f"{BACKEND}/test_resources.py::test_project_authority_is_required",
        f"{BACKEND}/test_resources.py::test_audit_is_durable_bounded_and_mandatory",
        f"{BACKEND}/test_resources.py::test_missing_or_drifted_contract_fails_closed",
        f"{BACKEND}/test_resources.py::test_eligibility_and_database_failure_never_fall_back",
        f"{BACKEND}/test_hardware.py::test_unsupported_execution_mode_fails_before_cpu_composition",
        expected=35,
    )
