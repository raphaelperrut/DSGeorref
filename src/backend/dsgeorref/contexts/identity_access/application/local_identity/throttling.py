"""PostgreSQL-backed login eligibility and decision evidence."""

import hashlib
import hmac
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import cast
from uuid import UUID

from dsgeorref.contexts.identity_access.domain.local_identity.credentials import uuid7
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied, Record

from .ports import Store, UnitOfWork

SNAPSHOT_FIELDS = {
    "state": "state",
    "revision": "revision",
    "failureCount": "failure_count",
    "windowStartedAt": "window_started_at",
    "windowEndsAt": "window_ends_at",
    "blockedUntil": "blocked_until",
}


def _snapshot(row: Record) -> Record:
    return {
        name: value.isoformat() if isinstance(value, datetime) else value
        for name, field in SNAPSHOT_FIELDS.items()
        for value in (row[field],)
    }


@dataclass(frozen=True)
class LoginThrottleProfile:
    version: str
    limit_after: int
    lock_after: int
    window_seconds: int
    cooldown_seconds: int
    lock_seconds: int

    def __post_init__(self) -> None:
        values = (
            self.limit_after,
            self.lock_after,
            self.window_seconds,
            self.cooldown_seconds,
            self.lock_seconds,
        )
        if (
            not isinstance(self.version, str)
            or not self.version.startswith("development-")
            or not self.version.removeprefix("development-").strip()
            or any(type(value) is not int or not 0 < value <= 2_147_483_647 for value in values)
            or self.limit_after >= self.lock_after
            or not self.cooldown_seconds < min(self.lock_seconds, self.window_seconds)
        ):
            raise Denied("internal_error")


class LoginThrottle:
    def __init__(self, profile: LoginThrottleProfile, key: bytes) -> None:
        if not isinstance(key, bytes) or len(key) < 32:
            raise Denied("internal_error")
        self.profile, self.key = profile, key

    def begin(
        self,
        store: Store,
        subject: str,
        operation: str = "post_auth_session",
    ) -> tuple[Record, Record, datetime]:
        digest = hmac.new(self.key, f"{operation}\0{subject}".encode(), hashlib.sha256).hexdigest()
        now = store.now()
        before = store.throttle_bucket(
            {
                "operation": operation,
                "bucket_digest": digest,
                "policy_version": self.profile.version,
                "window_started_at": now,
                "window_ends_at": now + timedelta(seconds=self.profile.window_seconds),
            }
        )
        now = store.now()
        if before["policy_version"] != self.profile.version or now < before["window_started_at"]:
            raise Denied("internal_error")
        current = before.copy()
        if before["blocked_until"] and now >= before["blocked_until"]:
            current.update(state="open", blocked_until=None)
        if current["state"] == "open" and now >= current["window_ends_at"]:
            current.update(
                failure_count=0,
                attempt_count=0,
                window_started_at=now,
                window_ends_at=now + timedelta(seconds=self.profile.window_seconds),
            )
        return before, current, now

    def admit(self, uow: UnitOfWork, operation: str, actor: UUID | None) -> bool:
        """Commit the admission budget even if the calling operation later rolls back."""
        with uow() as store:
            before, current, now = self.begin(store, str(actor), operation)
            failure = None
            if current["state"] != "open":
                failure = Denied("rate_limited")
            elif current["attempt_count"] >= self.profile.limit_after:
                current.update(
                    state="limited",
                    blocked_until=now + timedelta(seconds=self.profile.cooldown_seconds),
                )
                failure = Denied("rate_limited")
            else:
                current["attempt_count"] += 1
            self.finish(store, before, current, now, failure=failure)
        return failure is None

    def finish(
        self,
        store: Store,
        before: Record,
        current: Record,
        now: datetime,
        *,
        failure: Denied | None,
    ) -> None:
        self._count_failure(current, now, failure)
        if current != before:
            current["revision"] = cast(int, before["revision"]) + 1
            store.update(
                "throttle_buckets",
                {name: before[name] for name in ("operation", "bucket_digest", "revision")},
                {name: value for name, value in current.items() if value != before[name]},
            )
        reason = "eligible"
        if current["state"] != "open":
            reason = "account_locked" if current["state"] == "locked" else "rate_limited"
        correlation = uuid7()
        store.throttle_decision(
            {
                "id": correlation,
                "operation": before["operation"],
                "bucket_digest": before["bucket_digest"],
                "observed_at": now,
                "policy_version": self.profile.version,
                "reason": reason,
                "allowed": current["state"] == "open",
                "before_state": _snapshot(before),
                "after_state": _snapshot(current),
            }
        )
        store.audit(
            None,
            before["operation"],
            None,
            "DENIED" if failure else "COMMITTED",
            self.profile.version,
            correlation,
            failure.code if failure else None,
        )

    def _count_failure(self, current: Record, now: datetime, failure: Denied | None) -> None:
        if current["state"] != "open" or not failure:
            return
        if failure.code not in {"invalid_credentials", "account_locked"}:
            return
        count = cast(int, current["failure_count"]) + 1
        current["failure_count"] = count
        if count >= self.profile.lock_after:
            current.update(
                state="locked", blocked_until=now + timedelta(seconds=self.profile.lock_seconds)
            )
        elif count >= self.profile.limit_after:
            current.update(
                state="limited",
                blocked_until=now + timedelta(seconds=self.profile.cooldown_seconds),
            )
