"""HTTP translation for the production identity boundary."""

import re

from dsgeorref.contexts.identity_access.application.local_identity.sessions import Sessions
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from dsgeorref.contexts.identity_access.domain.local_identity.web import Provenance
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from .web import WebResponses

_REVISION = re.compile(r'"([1-9][0-9]{0,9})"')
_ERRORS = {
    "unauthorized": 401,
    "session_not_found": 404,
    "internal_error": 500,
}


def _single_header(request: Request, name: str, error: str) -> str:
    values = request.headers.getlist(name)
    if len(values) > 1:
        raise Denied(error)
    return values[0] if values else ""


def _credential(request: Request) -> tuple[str, str]:
    authorization = _single_header(request, "Authorization", "unauthorized")
    cookies = [
        value.strip().partition("=")[2]
        for header in request.headers.getlist("Cookie")
        for value in header.split(";")
        if value.strip().partition("=")[0] == "dsgeorref_session"
    ]
    if cookies:
        if len(cookies) != 1 or "Authorization" in request.headers or not cookies[0]:
            raise Denied("unauthorized")
        return cookies[0], "session"
    scheme, _, secret = authorization.partition(" ")
    if scheme.lower() != "bearer" or not secret or any(char.isspace() for char in secret):
        raise Denied("unauthorized")
    return secret, "pat"


def _preconditions(request: Request) -> tuple[str, int]:
    key = _single_header(request, "Idempotency-Key", "internal_error")
    revision = _REVISION.fullmatch(_single_header(request, "If-Match", "internal_error"))
    if not 16 <= len(key) <= 128 or not key.strip() or revision is None:
        raise Denied("internal_error")
    return key, int(revision[1])


def _provenance(request: Request) -> Provenance:
    return Provenance(
        _single_header(request, "Origin", "unauthorized"),
        _single_header(request, "Sec-Fetch-Site", "unauthorized"),
        _single_header(request, "X-CSRF-Token", "unauthorized") or None,
    )


def _problem(code: str, headers: dict[str, str]) -> JSONResponse:
    if code == "forbidden":
        code = "unauthorized"
    if code not in _ERRORS:
        code = "internal_error"
    status = _ERRORS[code]
    return JSONResponse(
        {
            "type": f"https://dsgeorref.local/problems/{code}",
            "title": code.replace("_", " "),
            "status": status,
            "code": code,
        },
        status_code=status,
        headers=headers,
        media_type="application/problem+json",
    )


def create_app(sessions: Sessions, web: WebResponses) -> FastAPI:
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None, redirect_slashes=False)

    @app.delete("/api/v1/auth/session", status_code=204, operation_id="delete_auth_session")
    def logout(request: Request) -> Response:
        headers = web.headers()
        try:
            secret, kind = _credential(request)
            key, revision = _preconditions(request)
            provenance = _provenance(request) if kind == "session" else None
            sessions.logout(secret, kind, revision, key, provenance)
        except Denied as error:
            return _problem(error.code, headers)
        headers["Set-Cookie"] = web.clear_cookie()
        return Response(status_code=204, headers=headers)

    return app
