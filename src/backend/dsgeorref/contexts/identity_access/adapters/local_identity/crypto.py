"""Argon2id PHC, opaque credentials and application-generated UUIDv7."""

import secrets
import threading

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied
from dsgeorref.contexts.identity_access.domain.local_identity.policy import SecurityProfile


class ArgonPasswords:
    def __init__(self, profile: SecurityProfile) -> None:
        profile.validate()
        self.profile = profile
        self._budget = threading.BoundedSemaphore(profile.hash_concurrency)

    def hash(self, password: str) -> str:
        self.profile.password_eligible(password)
        if not self._budget.acquire(blocking=False):
            raise Denied("internal_error")
        try:
            kdf = Argon2id(
                salt=secrets.token_bytes(16),
                length=32,
                iterations=self.profile.iterations,
                lanes=self.profile.lanes,
                memory_cost=self.profile.memory_kib,
            )
            return kdf.derive_phc_encoded(password.encode())
        finally:
            self._budget.release()

    def verify(self, password: str, encoded: str) -> bool:
        self.profile.password_eligible(password)
        expected = f"m={self.profile.memory_kib},t={self.profile.iterations},p={self.profile.lanes}"
        if not encoded.startswith(f"$argon2id$v=19${expected}$"):
            raise Denied("internal_error")
        if not self._budget.acquire(blocking=False):
            raise Denied("internal_error")
        try:
            Argon2id.verify_phc_encoded(password.encode(), encoded)
            return True
        except InvalidKey:
            return False
        finally:
            self._budget.release()
