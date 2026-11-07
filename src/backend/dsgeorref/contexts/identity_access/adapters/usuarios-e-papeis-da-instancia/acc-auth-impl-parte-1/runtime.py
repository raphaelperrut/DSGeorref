"""Compose the instance services with the integrated policy and existing PostgreSQL UoW."""

import hashlib
import json
from importlib import import_module
from pathlib import Path
from types import MappingProxyType

from dsgeorref.contexts.identity_access.adapters.local_identity.crypto import ArgonPasswords
from dsgeorref.contexts.identity_access.adapters.local_identity.postgres import PostgresUnitOfWork
from dsgeorref.contexts.identity_access.application.local_identity.transactions import (
    Eligibility,
    IdentityTransactions,
)
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from dsgeorref.contexts.identity_access.domain.local_identity.policy import (
    AuthorizationPolicy,
    SecurityProfile,
)
from dsgeorref.contexts.identity_access.domain.local_identity.web import WebPolicy

APPLICATION = (
    "dsgeorref.contexts.identity_access.application."
    "usuarios-e-papeis-da-instancia.acc-auth-impl-parte-1"
)
# Canonical JSON of the approved 1.1.0 policy; a different deployment needs review.
POLICY_SHA256 = "f82c7222ab740b85bc28c2caaa479b53a80128eba64da6f4c4ab1f5a8de78a9f"


def build_transactions(
    dsn: str,
    profile: SecurityProfile,
    web: WebPolicy,
    eligibility: Eligibility,
    replay_key: bytes,
    policy_path: Path,
    *,
    installation_authorized: bool = False,
) -> IdentityTransactions:
    """Installation capability must be verified by the server composition root.

    Merely loading the published policy never authorizes bootstrap. Missing
    policy/profile/eligibility fails closed; no synthetic production defaults.
    """
    try:
        document = json.loads(policy_path.read_text(encoding="utf-8"))
        canonical = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
        if hashlib.sha256(canonical).hexdigest() != POLICY_SHA256:
            raise ValueError("unrecognized policy")
        roles = {
            role: frozenset(grants) for role, grants in document["project_role_grants"].items()
        }
        operations = document["operations"].values()
        authentication = frozenset(
            row["permission"]
            for row in operations
            if row["grant_source"] == "authentication_policy"
        )
        installation = frozenset(
            row["permission"]
            for row in operations
            if row["grant_source"] == "installation_capability" and installation_authorized is True
        )
        policy = AuthorizationPolicy(
            document["version"],
            MappingProxyType({}),
            MappingProxyType(roles),
            installation,
            authentication,
        )
        access = import_module(APPLICATION + ".access").InstanceAccess(
            PostgresUnitOfWork(dsn), policy, profile, frozenset(document["self_service_grants"])
        )
        return IdentityTransactions(access, ArgonPasswords(profile), web, eligibility, replay_key)
    except (OSError, ValueError, TypeError, KeyError) as error:
        raise Denied("internal_error") from error
