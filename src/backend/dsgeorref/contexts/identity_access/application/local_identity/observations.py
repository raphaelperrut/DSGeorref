"""Persist denied attempts separately from rolled-back business effects."""

from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, Protocol, TypeVar

from dsgeorref.contexts.identity_access.domain.local_identity.credentials import uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied

from .transactions import IdentityTransactions


class ObservedApplication(Protocol):
    tx: IdentityTransactions


Application = TypeVar("Application", bound=ObservedApplication)
Parameters = ParamSpec("Parameters")
Result = TypeVar("Result")

# Operation-specific translations frozen by the owner contract v1.0.0.
# Private application operations retain their own reasons; no new HTTP code is introduced.
ERROR_TRANSLATIONS = {
    "post_auth_bootstrap": {
        "forbidden": "validation_failed",
        "rate_limited": "internal_error",
        "conflict": "bootstrap_already_completed",
    },
    "post_auth_session": {"forbidden": "validation_failed", "conflict": "internal_error"},
    "delete_auth_session": {"forbidden": "unauthorized", "precondition_failed": "internal_error"},
    "get_auth_oidc_callback": {
        "rate_limited": "oidc_exchange_failed",
        "forbidden": "oidc_state_invalid",
    },
}


def audit_denial(
    operation: str,
) -> Callable[
    [Callable[Concatenate[Application, Parameters], Result]],
    Callable[Concatenate[Application, Parameters], Result],
]:
    def decorate(
        function: Callable[Concatenate[Application, Parameters], Result],
    ) -> Callable[Concatenate[Application, Parameters], Result]:
        @wraps(function)
        def observed(
            self: Application, /, *args: Parameters.args, **kwargs: Parameters.kwargs
        ) -> Result:
            try:
                return function(self, *args, **kwargs)
            except Denied as error:
                # Only allowlisted metadata; arguments and exception details are never serialized.
                with self.tx.access.uow() as store:
                    store.audit(
                        None,
                        operation,
                        None,
                        "DENIED",
                        self.tx.access.policy.version,
                        uuid7(),
                        reason=error.code,
                    )
                mapped = ERROR_TRANSLATIONS.get(operation, {}).get(error.code, error.code)
                if mapped != error.code:
                    raise Denied(mapped) from error
                raise

        return observed

    return decorate
