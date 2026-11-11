"""Executa cenários integrados do BC-002 em PostgreSQL descartável."""

import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[3]
IDENTITY = "tests/backend/identity_access/local_identity"
SECURITY = (
    "tests/security/contexts/identity_access/usuarios-e-papeis-da-instancia/"
    "test_instance_security.py"
)
ACCESS = (
    "src/backend/dsgeorref/contexts/identity_access/adapters/"
    "usuarios-e-papeis-da-instancia/acc-auth-impl-parte-1/tests"
)


def run_cases(tmp_path: Path, *nodes: str, expected: int) -> None:
    report = tmp_path / "acceptance.xml"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "--import-mode=importlib",
            f"--junitxml={report}",
            *nodes,
        ],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    suite = ElementTree.parse(report).getroot().find("testsuite")
    assert suite is not None, output
    assert int(suite.attrib["tests"]) == expected, output
    assert all(suite.attrib[key] == "0" for key in ("errors", "failures", "skipped")), output
    print(output, end="")


def test_epic_009_aceite_happy_path(tmp_path: Path) -> None:
    run_cases(
        tmp_path,
        f"{SECURITY}::test_epic_009_seguranca_happy_path",
        f"{IDENTITY}/test_development_surface.py::test_oidc_callback_uses_browser_bound_transaction",
        f"{ACCESS}/test_canonical.py::test_role_project_operation_access",
        expected=6,
    )


def test_epic_009_aceite_negative_paths(tmp_path: Path) -> None:
    denied = f"{SECURITY}::test_epic_009_seguranca_negative_paths"
    run_cases(
        tmp_path,
        f"{denied}[ambiguous-credentials-401-unauthorized]",
        f"{denied}[viewer-escalation-403-forbidden]",
        f"{denied}[administrator-cross-project-403-forbidden]",
        f"{denied}[invalid-csrf-403-forbidden]",
        f"{denied}[no-project-authority-500-internal_error]",
        f"{denied}_credentials[pat-revoked-401-unauthorized]",
        f"{denied}_credentials[session-revoked-401-unauthorized]",
        f"{denied}_oidc[outage]",
        f"{denied}_abuse",
        f"{denied}_postgres_failure",
        expected=10,
    )
