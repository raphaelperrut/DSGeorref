"""CPU-only resource authorization composition; no acceleration is declared here."""

from collections.abc import Callable
from importlib import import_module
from pathlib import Path
from typing import Any
from uuid import UUID

from dsgeorref.contexts.identity_access.application.local_identity.ports import Store
from dsgeorref.contexts.identity_access.application.local_identity.transactions import (
    IdentityTransactions,
)
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied

CPU_RUNTIME = (
    "dsgeorref.contexts.identity_access.adapters."
    "autorizacao-por-projeto-operacao-artefato-e-caminho.acc-auth-impl-parte-1.runtime"
)


def build_authorization(
    tx: IdentityTransactions,
    project_exists: Callable[[Store, UUID], bool],
    contract_path: Path,
    *,
    execution_mode: str = "cpu",
) -> Any:
    """Select the existing CPU implementation without changing policy or algorithms.

    This is an internal composition option, not an HTTP field or a permission.
    GPU/automatic/other acceleration modes have no declared implementation or
    authorization in BC-002. Reject them before constructing a service; never
    probe a driver, download a dependency or silently substitute CPU.
    """
    if type(execution_mode) is not str or execution_mode != "cpu":
        raise Denied("validation_failed")
    return import_module(CPU_RUNTIME).build_authorization(tx, project_exists, contract_path)
