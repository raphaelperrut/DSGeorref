"""Production ASGI factory for the currently supported BC-002 operations."""

import json
import os
from collections.abc import Callable
from datetime import timedelta
from importlib import import_module
from pathlib import Path
from urllib.parse import urlsplit
from uuid import UUID

from dsgeorref.contexts.identity_access.application.local_identity.accounts import LocalAccounts
from dsgeorref.contexts.identity_access.application.local_identity.federation import Federation
from dsgeorref.contexts.identity_access.application.local_identity.ports import Store
from dsgeorref.contexts.identity_access.application.local_identity.sessions import Sessions
from dsgeorref.contexts.identity_access.application.local_identity.throttling import (
    LoginThrottle,
    LoginThrottleProfile,
)
from dsgeorref.contexts.identity_access.domain.local_identity.federation import OidcProvider
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from dsgeorref.contexts.identity_access.domain.local_identity.policy import SecurityProfile
from dsgeorref.contexts.identity_access.domain.local_identity.web import WebPolicy
from fastapi import FastAPI, Request
from psycopg import ProgrammingError
from psycopg.conninfo import conninfo_to_dict, make_conninfo

from .development_http import DevelopmentRoutes
from .http import create_app
from .web import WebResponses

_INSTANCE_RUNTIME = (
    "dsgeorref.contexts.identity_access.adapters."
    "usuarios-e-papeis-da-instancia.acc-auth-impl-parte-1.runtime"
)


def _security_profile(path: Path, *, development: bool = False) -> SecurityProfile:
    profile = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(profile["version"], str) or profile.pop("development", False) is not False:
        raise ValueError("invalid profile version")
    for key in ("session_absolute", "session_idle", "pat_lifetime", "oidc_lifetime"):
        seconds = profile[key]
        if type(seconds) not in (int, float):
            raise ValueError("invalid lifetime")
        profile[key] = timedelta(seconds=seconds)
    if type(profile["io_timeout"]) not in (int, float):
        raise ValueError("invalid timeout")
    return SecurityProfile(**profile, development=development)


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


def _project_authority_unavailable(_store: Store, _project: UUID) -> bool:
    raise Denied("internal_error")


def create_development_app(
    *,
    project_exists: Callable[[Store, UUID], bool] = _project_authority_unavailable,
    installation_authorized: bool = False,
    oidc: tuple[OidcProvider, Callable[[Request], str]] | None = None,
    stage_recovery: Callable[[UUID, str], None] | None = None,
) -> FastAPI:
    """Enable the Sprint 002 surface with explicit local development configuration."""
    try:
        origin = os.environ["DSGEOREF_IDENTITY_ORIGIN"]
        if os.environ["DSGEOREF_IDENTITY_MODE"] != "development" or urlsplit(
            origin
        ).hostname not in {"127.0.0.1", "::1", "localhost"}:
            raise ValueError("development requires a loopback origin")
        profile = _security_profile(
            Path(os.environ["DSGEOREF_IDENTITY_SECURITY_PROFILE"]),
            development=True,
        )
        config = Path(os.environ["DSGEOREF_IDENTITY_THROTTLE_PROFILE"])
        throttle = LoginThrottle(
            LoginThrottleProfile(**json.loads(config.read_text(encoding="utf-8"))),
            bytes.fromhex(os.environ["DSGEOREF_IDENTITY_THROTTLE_KEY_HEX"]),
        )
        dsn = os.environ["DSGEOREF_IDENTITY_DSN"]
        settings = conninfo_to_dict(dsn)
        host = settings.get("host")
        if not settings.get("dbname") or host not in {"127.0.0.1", "::1", "localhost"}:
            raise ValueError("development requires local PostgreSQL")
        address = settings.get("hostaddr", "127.0.0.1" if host == "localhost" else host)
        if address not in {"127.0.0.1", "::1"}:
            raise ValueError("development requires a loopback PostgreSQL address")
        return _development_routes(
            make_conninfo(dsn, hostaddr=address),
            profile,
            WebPolicy(origin),
            throttle,
            project_exists,
            installation_authorized,
            oidc,
            stage_recovery,
        )
    except (Denied, OSError, KeyError, TypeError, ValueError, OverflowError, ProgrammingError):
        raise RuntimeError("Invalid or missing BC-002 development configuration") from None


def _development_routes(
    dsn, profile, policy, throttle, project_exists, installation_authorized, oidc, stage_recovery
):
    from .postgres import PostgresUnitOfWork

    uow = PostgresUnitOfWork(dsn)

    def eligibility(_store, operation, actor):
        return throttle.admit(uow, operation, actor)

    runtime = import_module(_INSTANCE_RUNTIME)
    replay_key = bytes.fromhex(os.environ["DSGEOREF_IDENTITY_REPLAY_KEY_HEX"])
    if replay_key == throttle.key:
        raise ValueError("distinct throttle and replay keys required")
    tx = runtime.build_transactions(
        dsn,
        profile,
        policy,
        eligibility,
        replay_key,
        Path(os.environ["DSGEOREF_IDENTITY_POLICY"]),
        installation_authorized=installation_authorized is True and callable(stage_recovery),
    )
    web = WebResponses(policy)
    app = create_app(Sessions(tx), web)
    memberships = import_module(runtime.APPLICATION + ".memberships").Memberships(
        tx, project_exists
    )
    callback = (Federation(tx, oidc[0]), oidc[1]) if oidc is not None else None
    DevelopmentRoutes(
        tx, web, LocalAccounts(tx, throttle), memberships, project_exists, callback, stage_recovery
    ).register(app)
    return app
