"""Offline recovery ceremony: one-time kit, explicit trusted administrative decision."""

import hmac
from collections.abc import Callable
from uuid import UUID

from dsgeorref.contexts.identity_access.domain.local_identity.credentials import digest, opaque
from dsgeorref.contexts.identity_access.domain.local_identity.models import Denied

from .observations import audit_denial
from .transactions import IdentityTransactions

CeremonyDecision = Callable[[UUID, UUID], bool]


class AdministrativeRecovery:
    def __init__(self, transactions: IdentityTransactions, decision: CeremonyDecision) -> None:
        self.tx, self.decision = transactions, decision

    @audit_denial("recover")
    def recover(self, account_id: UUID, kit: str, new_password: str, ceremony_id: UUID) -> str:
        if not callable(self.decision) or self.decision(account_id, ceremony_id) is not True:
            raise Denied("forbidden")
        encoded = self.tx.passwords.hash(new_password)
        next_kit = opaque()
        with self.tx.access.uow() as store:
            account = store.get("accounts", {"id": account_id}, lock=True)
            if not account or not account["administrator"]:
                raise Denied("forbidden")
            if not hmac.compare_digest(account["recovery_hash"], digest(kit)):
                raise Denied("forbidden")
            if store.get("ceremonies", {"id": ceremony_id}):
                raise Denied("conflict")
            store.insert(
                "ceremonies", {"id": ceremony_id, "account_id": account_id, "kit_hash": digest(kit)}
            )
            store.update(
                "accounts",
                {"id": account_id},
                {
                    "password_hash": encoded,
                    "recovery_hash": digest(next_kit),
                    "state": "active",
                    "revision": account["revision"] + 1,
                },
            )
            for table in ("sessions", "tokens"):
                for row in store.rows(table, {"account_id": account_id}):
                    if row["state"] == "active":
                        store.update(
                            table,
                            {"id": row["id"]},
                            {"state": "revoked", "revision": row["revision"] + 1},
                        )
            self.tx.observe(store, account_id, "recover", account_id)
        return next_kit
