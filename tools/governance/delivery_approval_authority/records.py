from __future__ import annotations

from datetime import datetime
from typing import Any

from .crypto import digest, instant, usable, verify_signature
from .schemas import SchemaSet
from .verdicts import ROLE_DECISIONS, SCOPE


def _one(
    records: list[dict[str, Any]],
    field: str,
    value: str,
    missing_code: str,
) -> tuple[dict[str, Any] | None, str | None]:
    matches = [record for record in records if record.get(field) == value]
    return (matches[0], None) if len(matches) == 1 else (None, missing_code)


def profile_code(
    schemas: SchemaSet,
    anchors: dict[str, Any],
    profile: dict[str, Any],
    checked_at: datetime,
) -> str | None:
    if (code := schemas.code("anchors", anchors)) is not None:
        return "TRUST_ANCHOR_INVALID" if code == "SCHEMA_INVALID" else code
    if (code := schemas.code("profile", profile)) is not None:
        return "TRUST_PROFILE_INVALID" if code == "SCHEMA_INVALID" else code
    anchor_ids = [record["key_id"] for record in anchors["anchors"]]
    issuers = [record["issuer"] for record in profile["identity_issuers"]]
    key_ids = [record["key_id"] for record in profile["keys"]]
    if len(anchor_ids) != len(set(anchor_ids)):
        return "TRUST_ANCHOR_INVALID"
    if len(issuers) != len(set(issuers)) or len(key_ids) != len(set(key_ids)):
        return "TRUST_PROFILE_INVALID"
    anchor, code = _one(
        anchors["anchors"],
        "key_id",
        profile["signature"]["key_id"],
        "TRUST_ANCHOR_INVALID",
    )
    if code is not None or anchor is None:
        return code
    if (code := usable(anchor, checked_at, checked_at)) is not None:
        return code
    if not (instant(profile["valid_from"]) <= checked_at < instant(profile["valid_until"])):
        return "TEMPORAL_INVALID"
    if not verify_signature(profile, anchor["public_key"], "profile"):
        return "SIGNATURE_INVALID"
    return None


def _issuer_code(
    profile: dict[str, Any],
    issuer: str,
    issued_at: datetime,
    checked_at: datetime,
) -> str | None:
    trusted, code = _one(profile["identity_issuers"], "issuer", issuer, "ISSUER_UNTRUSTED")
    return code if trusted is None else usable(trusted, issued_at, checked_at)


def _key(
    profile: dict[str, Any],
    key_id: str,
    purpose: str,
    role: str,
    task_id: str,
    issued_at: datetime,
    checked_at: datetime,
) -> tuple[dict[str, Any] | None, str | None]:
    trusted, code = _one(profile["keys"], "key_id", key_id, "SIGNER_UNKNOWN")
    if code is not None or trusted is None:
        return None, code
    if trusted["purpose"] != purpose or trusted["trust_scope"] != SCOPE:
        return None, "SIGNER_PURPOSE_INVALID"
    if role not in trusted["roles"] or task_id not in trusted["task_envelope_ids"]:
        return None, "SCOPE_INVALID"
    return trusted, usable(trusted, issued_at, checked_at)


def _binding_code(
    schemas: SchemaSet,
    binding: dict[str, Any],
    attestation: dict[str, Any],
    profile: dict[str, Any],
    checked_at: datetime,
) -> str | None:
    if (code := schemas.code("binding", binding)) is not None:
        return "BINDING_INVALID" if code == "SCHEMA_INVALID" else code
    issued_at = instant(attestation["issued_at"])
    comparisons = (
        (binding["policy"], attestation["policy"], "POLICY_MISMATCH"),
        (binding["principal"], attestation["principal"], "PRINCIPAL_MISMATCH"),
        (binding["role"], attestation["role"], "ROLE_MISMATCH"),
        (
            binding["accountable_subject"],
            attestation["accountable_subject"],
            "ACCOUNTABLE_SUBJECT_MISMATCH",
        ),
    )
    for actual, expected, code in comparisons:
        if actual != expected:
            return code
    task_id = attestation["task_envelope"]["task_id"]
    if task_id not in binding["task_envelope_ids"]:
        return "SCOPE_INVALID"
    if (code := usable(binding, issued_at, checked_at)) is not None:
        return code
    key, code = _key(
        profile,
        binding["signature"]["key_id"],
        "DELIVERY_ROLE_BINDING",
        binding["role"],
        task_id,
        issued_at,
        checked_at,
    )
    if code is not None or key is None:
        return code
    if key["principal"] is not None:
        return "SIGNER_PURPOSE_INVALID"
    if not verify_signature(binding, key["public_key"], "binding"):
        return "SIGNATURE_INVALID"
    if digest(binding) != attestation["binding"]["digest_sha256"]:
        return "BINDING_MISMATCH"
    return None


def attestation_code(
    schemas: SchemaSet,
    attestation: dict[str, Any],
    bindings: list[dict[str, Any]],
    profile: dict[str, Any],
    task_id: str,
    task_digest: str,
    candidate_sha: str,
    checked_at: datetime,
) -> str | None:
    if (code := schemas.code("attestation", attestation)) is not None:
        return code
    issued_at = instant(attestation["issued_at"])
    if issued_at > checked_at:
        return "TEMPORAL_INVALID"
    expected_policy = {
        "profile_id": profile["profile_id"],
        "profile_version": profile["profile_version"],
    }
    if attestation["policy"] != expected_policy:
        return "POLICY_MISMATCH"
    if (code := _issuer_code(
        profile,
        attestation["principal"]["issuer"],
        issued_at,
        checked_at,
    )) is not None:
        return code
    expected_task = {"task_id": task_id, "digest_sha256": task_digest}
    if attestation["task_envelope"] != expected_task:
        return "TASK_ENVELOPE_DIGEST_MISMATCH"
    if attestation["candidate_sha"] != candidate_sha:
        return "CANDIDATE_SHA_MISMATCH"
    binding, code = _one(
        bindings,
        "binding_id",
        attestation["binding"]["binding_id"],
        "BINDING_MISSING",
    )
    if code is not None or binding is None:
        return code
    if binding.get("binding_version") != attestation["binding"]["binding_version"]:
        return "BINDING_MISMATCH"
    if (code := _binding_code(schemas, binding, attestation, profile, checked_at)) is not None:
        return code
    key, code = _key(
        profile,
        attestation["signature"]["key_id"],
        "DELIVERY_APPROVAL_ATTESTATION",
        attestation["role"],
        task_id,
        issued_at,
        checked_at,
    )
    if code is not None or key is None:
        return code
    if key["principal"] != attestation["principal"]:
        return "PRINCIPAL_MISMATCH"
    if not verify_signature(attestation, key["public_key"], "attestation"):
        return "SIGNATURE_INVALID"
    if ROLE_DECISIONS[attestation["role"]] != attestation["decision"]:
        return "DECISION_INVALID"
    return None
