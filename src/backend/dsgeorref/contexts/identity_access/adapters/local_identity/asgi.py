"""Production ASGI factory for the currently supported BC-002 operations."""

import json
import os
from datetime import timedelta
from importlib import import_module
from pathlib import Path
from uuid import UUID

from dsgeorref.contexts.identity_access.application.local_identity.ports import Store
from dsgeorref.contexts.identity_access.application.local_identity.sessions import Sessions
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from dsgeorref.contexts.identity_access.domain.local_identity.policy import SecurityProfile
from dsgeorref.contexts.identity_access.domain.local_identity.web import WebPolicy
from fastapi import FastAPI
from psycopg import ProgrammingError
from psycopg.conninfo import conninfo_to_dict

from .http import create_app
from .web import WebResponses

_INSTANCE_RUNTIME = (
    "dsgeorref.contexts.identity_access.adapters."
    "usuarios-e-papeis-da-instancia.acc-auth-impl-parte-1.runtime"
)


def _security_profile(path: Path) -> SecurityProfile:
    profile = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(profile["version"], str):
        raise ValueError("invalid profile version")
    for key in ("session_absolute", "session_idle", "pat_lifetime", "oidc_lifetime"):
        seconds = profile[key]
        if type(seconds) not in (int, float):
            raise ValueError("invalid lifetime")
        profile[key] = timedelta(seconds=seconds)
    if type(profile["io_timeout"]) not in (int, float):
        raise ValueError("invalid timeout")
    return SecurityProfile(**profile)


def _eligibility_unavailable(_store: Store, _operation: str, _actor: UUID | None) -> bool:
    # No eligibility-dependent operation is registered by this factory.
    raise Denied("internal_error")


def create_production_app() -> FastAPI:
    try:
        dsn = os.environ["DSGEOREF_IDENTITY_DSN"]
        if not conninfo_to_dict(dsn).get("dbname"):
            raise ValueError("database must be explicit")
        profile = _security_profile(Path(os.environ["DSGEOREF_IDENTITY_SECURITY_PROFILE"]))
        web = WebPolicy(os.environ["DSGEOREF_IDENTITY_ORIGIN"])
        replay_key = bytes.fromhex(os.environ["DSGEOREF_IDENTITY_REPLAY_KEY_HEX"])
        policy_path = Path(os.environ["DSGEOREF_IDENTITY_POLICY"])
        transactions = import_module(_INSTANCE_RUNTIME).build_transactions(
            dsn, profile, web, _eligibility_unavailable, replay_key, policy_path
        )
    except (Denied, OSError, KeyError, TypeError, ValueError, OverflowError, ProgrammingError):
        # Startup diagnostics must not print database credentials or signing material.
        raise RuntimeError("Invalid or missing BC-002 runtime configuration") from None
    return create_app(Sessions(transactions), WebResponses(web))
