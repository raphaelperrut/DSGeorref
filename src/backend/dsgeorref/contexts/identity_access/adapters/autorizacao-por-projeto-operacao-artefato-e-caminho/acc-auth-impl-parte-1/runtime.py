"""Explicit composition using the integrated BC-002 policy and persistence."""

import hashlib
import json
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

APPLICATION = (
    "dsgeorref.contexts.identity_access.application."
    "autorizacao-por-projeto-operacao-artefato-e-caminho.acc-auth-impl-parte-1"
)
CONTRACT_SHA256 = "40126aab34f6af6e44293d3246096c057c01cc1e77dfddd0dba814cf1a6057f5"


def build_authorization(
    tx: IdentityTransactions,
    project_exists: Callable[[Store, UUID], bool],
    contract_path: Path,
) -> Any:
    """Load the frozen composition, verifying its pinned dependency bytes.

    tx comes from the existing instance build_transactions composition root;
    sessions, PATs, membership persistence and audit remain the same services.
    """
    try:
        raw = contract_path.read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(raw).hexdigest() != CONTRACT_SHA256:
            raise ValueError("unrecognized composition")
        document = json.loads(raw)
        if document["contract_id"] != "identity-access-resource-authorization":
            raise ValueError("unknown contract")
        if document["contract_version"] != "1.0.0":
            raise ValueError("unknown version")
        for source, expected in document["source_sha256"].items():
            content = (contract_path.parent / source).read_bytes().replace(b"\r\n", b"\n")
            if hashlib.sha256(content).hexdigest() != expected:
                raise ValueError("contract dependency drift")
        policy_path = contract_path.parent / document["policy_ref"]
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        if (
            policy["version"] != document["policy_version"]
            or tx.access.policy.version != policy["version"]
        ):
            raise ValueError("policy mismatch")
        actions = {
            row["permission"]: document["operation_resources"].get(operation)
            for operation, row in policy["operations"].items()
        }
        return import_module(APPLICATION + ".resources").ResourceAuthorization(
            tx,
            project_exists,
            actions,
            document["artifact_boundary"]["permission"],
            policy["version"],
        )
    except (OSError, ValueError, TypeError, KeyError) as error:
        raise Denied("internal_error") from error
