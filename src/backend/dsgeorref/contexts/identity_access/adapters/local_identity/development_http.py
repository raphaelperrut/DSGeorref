"""Development HTTP composition for the existing BC-002 use cases."""

from collections.abc import Callable
from datetime import datetime
from typing import Annotated
from uuid import UUID

from dsgeorref.contexts.identity_access.application.local_identity.accounts import LocalAccounts
from dsgeorref.contexts.identity_access.application.local_identity.federation import Federation
from dsgeorref.contexts.identity_access.application.local_identity.ports import Store
from dsgeorref.contexts.identity_access.application.local_identity.tokens import Tokens
from dsgeorref.contexts.identity_access.application.local_identity.transactions import (
    IdentityTransactions,
)
from dsgeorref.contexts.identity_access.domain.local_identity.models import (
    Denied,
    IssuedSession,
    Principal,
)
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .http import _credential, _problem, _provenance, _single_header
from .web import WebResponses

_VALIDATION = {"validation_failed": 422, "internal_error": 500}
_LOGIN = {**_VALIDATION, "invalid_credentials": 401, "account_locked": 429, "rate_limited": 429}
_BOOTSTRAP = {**_VALIDATION, "bootstrap_already_completed": 409, "password_policy_failed": 422}
_PROTECTED = {
    **_VALIDATION,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "conflict": 409,
    "precondition_failed": 412,
    "rate_limited": 429,
}
_OIDC = {
    "oidc_state_invalid": 400,
    "oidc_exchange_failed": 502,
    "identity_link_conflict": 409,
    "internal_error": 500,
}


class LoginBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str
    password: str


class BootstrapBody(LoginBody):
    username: Annotated[str, Field(min_length=3)]
    password: Annotated[str, Field(min_length=12)]
    displayName: Annotated[str, Field(min_length=1)]


class TokenBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Annotated[str, Field(min_length=1, max_length=100)]
    scopes: Annotated[list[str], Field(min_length=1)]
    expiresAt: datetime | None = None

    @field_validator("expiresAt", mode="before")
    @classmethod
    def expiry_is_date_time(cls, value: object) -> object:
        if value is not None and (not isinstance(value, str) or "T" not in value.upper()):
            raise ValueError("expected a date-time string")
        return value


class MemberBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    userId: UUID
    role: str


def _key(request: Request) -> str:
    key = _single_header(request, "Idempotency-Key", "validation_failed")
    if not 16 <= len(key) <= 128 or not key.strip():
        raise Denied("validation_failed")
    return key


def _session(issued: IssuedSession, headers: dict[str, str], web: WebResponses) -> dict:
    headers.update(
        {"Set-Cookie": web.cookie(issued.secret), "ETag": f'"{issued.session.revision}"'}
    )
    return {
        "sessionId": str(issued.session.id),
        "userId": str(issued.session.account_id),
        "expiresAt": issued.session.expires_at.isoformat(),
        "csrfToken": issued.csrf,
    }


def _member(member) -> dict:
    return {
        "projectId": str(member.project_id),
        "userId": str(member.account_id),
        "role": member.role,
        "revision": member.revision,
    }


class DevelopmentRoutes:
    def __init__(
        self,
        tx: IdentityTransactions,
        web: WebResponses,
        accounts: LocalAccounts,
        memberships,
        project_exists: Callable[[Store, UUID], bool],
        oidc: tuple[Federation, Callable[[Request], str]] | None,
        stage_recovery: Callable[[UUID, str], None] | None,
    ) -> None:
        self.tx, self.web, self.accounts = tx, web, accounts
        self.memberships, self.project_exists = memberships, project_exists
        self.tokens = Tokens(tx)
        self.oidc = oidc
        self.stage_recovery = stage_recovery

    def _respond(self, errors, status, operation) -> JSONResponse:
        headers = self.web.headers()
        try:
            data = operation(headers)
        except Denied as error:
            return _problem(error.code, headers, errors)
        return JSONResponse(data, status_code=status, headers=headers)

    def login(self, request: Request, body: LoginBody) -> JSONResponse:
        def execute(headers):
            if "\x00" in body.username:
                raise Denied("validation_failed")
            issued = self.accounts.login(
                body.username,
                body.password,
                _key(request),
                _provenance(request, "validation_failed"),
            )
            return {"data": _session(issued, headers, self.web)}

        return self._respond(_LOGIN, 202, execute)

    def bootstrap(self, request: Request, body: BootstrapBody) -> JSONResponse:
        def execute(_headers):
            if "\x00" in body.username:
                raise Denied("validation_failed")
            account, issued, _ = self.accounts.bootstrap(
                body.username,
                body.password,
                _key(request),
                _provenance(request, "validation_failed"),
                display_name=body.displayName,
                stage_recovery=self.stage_recovery,
            )
            created = issued.session.expires_at - self.tx.access.profile.session_absolute
            return {
                "data": {
                    "administratorId": str(account.id),
                    "sessionId": str(issued.session.id),
                    "createdAt": created.isoformat(),
                }
            }

        return self._respond(_BOOTSTRAP, 202, execute)

    def token(self, request: Request, body: TokenBody) -> JSONResponse:
        def execute(_headers):
            secret, kind = _credential(request)
            issued = self.tokens.issue(
                secret,
                kind,
                body.scopes,
                _key(request),
                _provenance(request, "forbidden") if kind == "session" else None,
                expires=body.expiresAt,
                name=body.name,
            )
            return {
                "data": {
                    "tokenId": str(issued.token.id),
                    "token": issued.secret,
                    "prefix": issued.secret[:12],
                    "scopes": issued.token.scopes,
                    "expiresAt": issued.token.expires_at.isoformat(),
                }
            }

        return self._respond(_PROTECTED, 201, execute)

    def list_members(self, request: Request, projectId: UUID) -> JSONResponse:
        def execute(_headers):
            items = [
                _member(member)
                for member in self.memberships.list(
                    *_credential(request),
                    projectId,
                )
            ]
            return {"items": items, "page": {"limit": max(1, len(items)), "nextCursor": None}}

        return self._respond(_PROTECTED, 200, execute)

    def add_member(self, request: Request, projectId: UUID, body: MemberBody) -> JSONResponse:
        def execute(_headers):
            secret, kind = _credential(request)
            member = self.memberships.add(
                secret,
                kind,
                projectId,
                body.userId,
                body.role,
                _key(request),
                _provenance(request, "forbidden") if kind == "session" else None,
            )
            return {"data": _member(member)}

        return self._respond(_PROTECTED, 201, execute)

    def authorization(
        self,
        request: Request,
        action: str,
        resourceType: str,
        resourceId: UUID | None = None,
    ) -> JSONResponse:
        def execute(_headers):
            if (resourceType, resourceId is not None) not in {
                ("instance", False),
                ("project", True),
            }:
                raise Denied("validation_failed")
            allowed = self.tx.access.check(
                *_credential(request),
                action,
                resourceId,
                guard=lambda store, principal: self._check_resource(store, principal, resourceId),
            )
            return {
                "data": {
                    "allowed": allowed,
                    "policyVersion": self.tx.access.policy.version,
                    "reasonCode": "allowed" if allowed else "forbidden",
                }
            }

        return self._respond(_PROTECTED, 200, execute)

    def _check_resource(self, store: Store, principal: Principal, project: UUID | None) -> None:
        if project is not None:
            exists = self.project_exists(store, project)
            if exists is not True:
                raise Denied("not_found" if exists is False else "internal_error")
        self.tx.eligible(store, "get_authorization_check", principal.account.id)

    def oidc_callback(self, request: Request) -> JSONResponse:
        def execute(headers):
            if self.oidc is None:
                raise Denied("oidc_exchange_failed")
            federation, browser_binding = self.oidc
            codes, states = (
                request.query_params.getlist("code"),
                request.query_params.getlist("state"),
            )
            if len(codes) != 1 or len(states) != 1 or not codes[0] or not states[0]:
                raise Denied("oidc_state_invalid")
            binding = browser_binding(request)
            if not binding:
                raise Denied("oidc_state_invalid")
            issued, linked = federation.callback(states[0], binding, codes[0])
            return {"data": {"session": _session(issued, headers, self.web), "linked": linked}}

        return self._respond(_OIDC, 200, execute)

    def register(self, app: FastAPI) -> None:
        for path, method, handler, status, operation in (
            ("/auth/session", "POST", self.login, 202, "post_auth_session"),
            ("/auth/bootstrap", "POST", self.bootstrap, 202, "post_auth_bootstrap"),
            ("/auth/tokens", "POST", self.token, 201, "post_auth_tokens"),
            ("/auth/oidc/callback", "GET", self.oidc_callback, 200, "get_auth_oidc_callback"),
            (
                "/projects/{projectId}/members",
                "GET",
                self.list_members,
                200,
                "get_projects_projectid_members",
            ),
            (
                "/projects/{projectId}/members",
                "POST",
                self.add_member,
                201,
                "post_projects_projectid_members",
            ),
            ("/authorization/check", "GET", self.authorization, 200, "get_authorization_check"),
        ):
            app.add_api_route(
                "/api/v1" + path,
                handler,
                methods=[method],
                status_code=status,
                operation_id=operation,
            )

        @app.exception_handler(RequestValidationError)
        async def invalid_request(
            _request: Request, _error: RequestValidationError
        ) -> JSONResponse:
            return _problem("validation_failed", self.web.headers(), _VALIDATION)
