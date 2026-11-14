"""Reuse the approved instance runtime and disposable PostgreSQL fixtures."""

import importlib.util
import sys
from importlib import import_module
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
LEGACY = ROOT / "tests/backend/identity_access/local_identity"
sys.path.insert(0, str(LEGACY))
INSTANCE = (
    ROOT
    / "src/backend/dsgeorref/contexts/identity_access/adapters"
    / "usuarios-e-papeis-da-instancia/acc-auth-impl-parte-1/tests"
)
spec = importlib.util.spec_from_file_location(
    "instance_resource_fixtures", INSTANCE / "conftest.py"
)
upstream = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = upstream
spec.loader.exec_module(upstream)
database, runtime = upstream.database, upstream.runtime
ORIGIN, PASSWORD = upstream.ORIGIN, upstream.PASSWORD
synthetic_profile = upstream.synthetic_profile
CONTRACT = (
    ROOT
    / "contracts/contexts/identity_access/plt"
    / "autorizacao-por-projeto-operacao-artefato-e-caminho/contract.json"
)
ADAPTER = (
    "dsgeorref.contexts.identity_access.adapters."
    "autorizacao-por-projeto-operacao-artefato-e-caminho.acc-auth-impl-parte-1.runtime"
)


@pytest.fixture
def authorization(runtime):
    # Synthetic project existence port; PostgreSQL identity persistence is real.
    return import_module(ADAPTER).build_authorization(
        runtime.tx, lambda store, project: True, CONTRACT
    )
