from __future__ import annotations

import base64
import copy
import csv
import hashlib
import json
import sys
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = ROOT / "contracts/assurance/delivery-approval-authority"
VECTOR_PATH = CONTRACT_ROOT / "test-vectors/conformance-suite.json"
TASK_SCHEMA_PATH = ROOT / ".codex/tasks/TASK_ENVELOPE.schema.json"
OWNERSHIP_PATH = ROOT / "contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv"
CANONICAL_ROOT = ROOT / (
    "tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "frz-gov-adr-gov-dec-parte-1"
)
sys.path.insert(0, str(CANONICAL_ROOT))
from canonical_json import canonical_json_bytes  # noqa: E402


SCOPE = "DSGEOREF-DELIVERY-APPROVAL-AUTHORITY-V1"
DOMAINS = {
    "profile": "DSGEOREF-DELIVERY-APPROVAL-TRUST-PROFILE-V1",
    "binding": "DSGEOREF-DELIVERY-APPROVAL-ROLE-BINDING-V1",
    "attestation": "DSGEOREF-DELIVERY-APPROVAL-ATTESTATION-V1",
}
SCHEMA_PATHS = {
    "anchors": CONTRACT_ROOT / "trust-anchor-set.schema.json",
    "profile": CONTRACT_ROOT / "trust-profile.schema.json",
    "binding": CONTRACT_ROOT / "role-binding.schema.json",
    "attestation": CONTRACT_ROOT / "approval-attestation.schema.json",
    "verdict": CONTRACT_ROOT / "verification-verdict.schema.json",
}
PUBLISHED_PATHS = {
    path.relative_to(ROOT).as_posix()
    for path in [CONTRACT_ROOT / "README.md", VECTOR_PATH, *SCHEMA_PATHS.values()]
}
ROLE_DECISIONS = {"Executor": "DELIVERED", "QA": "APPROVE", "Reviewer": "APPROVE"}


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _validator(name: str) -> Draft202012Validator:
    schema = _load_json(SCHEMA_PATHS[name])
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _private_key(label: str) -> Ed25519PrivateKey:
    seed = hashlib.sha256(f"daa-test:{label}".encode()).digest()
    return Ed25519PrivateKey.from_private_bytes(seed)


def _public_key(label: str) -> str:
    public_bytes = _private_key(label).public_key().public_bytes_raw()
    return base64.urlsafe_b64encode(public_bytes).rstrip(b"=").decode()


def _signature_message(document: dict[str, Any], domain: str) -> bytes:
    projection = copy.deepcopy(document)
    projection["signature"]["value"] = ""
    return domain.encode("ascii") + b"\x00" + canonical_json_bytes(projection)


def _resign(document: dict[str, Any], label: str, domain: str) -> None:
    signature = _private_key(label).sign(_signature_message(document, domain))
    document["signature"]["value"] = base64.urlsafe_b64encode(signature).rstrip(b"=").decode()


def _verify_signature(document: dict[str, Any], public_key: str, domain: str) -> bool:
    try:
        Ed25519PublicKey.from_public_bytes(_decode(public_key)).verify(
            _decode(document["signature"]["value"]),
            _signature_message(document, domain),
        )
    except (InvalidSignature, ValueError, KeyError, TypeError):
        return False
    return True


def _instant(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _usable(record: dict[str, Any], at: datetime, verification_time: datetime) -> str | None:
    if not (_instant(record["valid_from"]) <= at < _instant(record["valid_until"])):
        return "TEMPORAL_INVALID"
    revoked_at = record["revoked_at"]
    if revoked_at is not None and _instant(revoked_at) <= verification_time:
        return "REVOKED"
    return None


def _unique_by(records: list[dict[str, Any]], field: str) -> bool:
    values = [record[field] for record in records]
    return len(values) == len(set(values))


def _schema_code(name: str, record: dict[str, Any]) -> str | None:
    errors = sorted(_validator(name).iter_errors(record), key=lambda error: list(error.path))
    if not errors:
        return None
    error = errors[0]
    if list(error.path)[-1:] == ["trust_scope"]:
        return "TRUST_SCOPE_INVALID"
    return "SCHEMA_INVALID"


def _verdict(
    status: str,
    code: str,
    task: dict[str, Any],
    candidate_sha: str,
    profile: dict[str, Any],
    verification_time: str,
    subjects: dict[str, set[str]] | None = None,
) -> dict[str, Any]:
    accountable = subjects or {role: set() for role in ROLE_DECISIONS}
    verdict = {
        "schema_version": "1.0.0",
        "status": status,
        "code": code,
        "trust_scope": SCOPE,
        "profile": {
            "profile_id": profile.get("profile_id", "invalid"),
            "profile_version": profile.get("profile_version", "invalid"),
        },
        "task_envelope": {
            "task_id": task.get("task_id", "INVALID"),
            "digest_sha256": _digest(task),
        },
        "candidate_sha": candidate_sha,
        "verification_time": verification_time,
        "validated_roles": list(ROLE_DECISIONS) if status == "PASS" else [],
        "accountable_subjects": {
            role: sorted(accountable[role]) if status == "PASS" else []
            for role in ROLE_DECISIONS
        },
    }
    _validator("verdict").validate(verdict)
    return verdict


def _profile_trusted(
    anchors: dict[str, Any], profile: dict[str, Any], verification_time: datetime
) -> str | None:
    if (code := _schema_code("anchors", anchors)) is not None:
        return "TRUST_ANCHOR_INVALID" if code == "SCHEMA_INVALID" else code
    if (code := _schema_code("profile", profile)) is not None:
        return "TRUST_PROFILE_INVALID" if code == "SCHEMA_INVALID" else code
    if not _unique_by(anchors["anchors"], "key_id"):
        return "TRUST_ANCHOR_INVALID"
    if not _unique_by(profile["identity_issuers"], "issuer") or not _unique_by(
        profile["keys"], "key_id"
    ):
        return "TRUST_PROFILE_INVALID"
    matches = [
        anchor
        for anchor in anchors["anchors"]
        if anchor["key_id"] == profile["signature"]["key_id"]
    ]
    if len(matches) != 1:
        return "TRUST_ANCHOR_INVALID"
    anchor = matches[0]
    if (code := _usable(anchor, verification_time, verification_time)) is not None:
        return code
    if not (
        _instant(profile["valid_from"])
        <= verification_time
        < _instant(profile["valid_until"])
    ):
        return "TEMPORAL_INVALID"
    if not _verify_signature(profile, anchor["public_key"], DOMAINS["profile"]):
        return "SIGNATURE_INVALID"
    return None


def _trusted_record(
    records: list[dict[str, Any]], field: str, value: str, missing_code: str
) -> tuple[dict[str, Any] | None, str | None]:
    matches = [record for record in records if record[field] == value]
    if len(matches) != 1:
        return None, missing_code
    return matches[0], None


def _issuer_code(
    profile: dict[str, Any], issuer: str, issued_at: datetime, verification_time: datetime
) -> str | None:
    trusted, code = _trusted_record(
        profile["identity_issuers"], "issuer", issuer, "ISSUER_UNTRUSTED"
    )
    if code is not None or trusted is None:
        return code
    return _usable(trusted, issued_at, verification_time)


def _key_code(
    profile: dict[str, Any],
    key_id: str,
    purpose: str,
    role: str,
    task_id: str,
    issued_at: datetime,
    verification_time: datetime,
) -> tuple[dict[str, Any] | None, str | None]:
    key, code = _trusted_record(profile["keys"], "key_id", key_id, "SIGNER_UNKNOWN")
    if code is not None or key is None:
        return None, code
    if key["purpose"] != purpose or key["trust_scope"] != SCOPE:
        return None, "SIGNER_PURPOSE_INVALID"
    if role not in key["roles"] or task_id not in key["task_envelope_ids"]:
        return None, "SCOPE_INVALID"
    return key, _usable(key, issued_at, verification_time)


def _binding_code(
    binding: dict[str, Any],
    attestation: dict[str, Any],
    profile: dict[str, Any],
    verification_time: datetime,
) -> str | None:
    if (code := _schema_code("binding", binding)) is not None:
        return "BINDING_INVALID" if code == "SCHEMA_INVALID" else code
    issued_at = _instant(attestation["issued_at"])
    if binding["policy"] != attestation["policy"]:
        return "POLICY_MISMATCH"
    if binding["principal"] != attestation["principal"]:
        return "PRINCIPAL_MISMATCH"
    if binding["role"] != attestation["role"]:
        return "ROLE_MISMATCH"
    if binding["accountable_subject"] != attestation["accountable_subject"]:
        return "ACCOUNTABLE_SUBJECT_MISMATCH"
    if attestation["task_envelope"]["task_id"] not in binding["task_envelope_ids"]:
        return "SCOPE_INVALID"
    if (code := _usable(binding, issued_at, verification_time)) is not None:
        return code
    key, code = _key_code(
        profile,
        binding["signature"]["key_id"],
        "DELIVERY_ROLE_BINDING",
        binding["role"],
        attestation["task_envelope"]["task_id"],
        issued_at,
        verification_time,
    )
    if code is not None or key is None:
        return code
    if key["principal"] is not None:
        return "SIGNER_PURPOSE_INVALID"
    if not _verify_signature(binding, key["public_key"], DOMAINS["binding"]):
        return "SIGNATURE_INVALID"
    if _digest(binding) != attestation["binding"]["digest_sha256"]:
        return "BINDING_MISMATCH"
    return None


def _attestation_code(
    attestation: dict[str, Any],
    bindings: list[dict[str, Any]],
    profile: dict[str, Any],
    task_id: str,
    task_digest: str,
    candidate_sha: str,
    verification_time: datetime,
) -> str | None:
    if (code := _schema_code("attestation", attestation)) is not None:
        return code
    issued_at = _instant(attestation["issued_at"])
    if issued_at > verification_time:
        return "TEMPORAL_INVALID"
    if attestation["policy"] != {
        "profile_id": profile["profile_id"],
        "profile_version": profile["profile_version"],
    }:
        return "POLICY_MISMATCH"
    if (code := _issuer_code(
        profile, attestation["principal"]["issuer"], issued_at, verification_time
    )) is not None:
        return code
    if attestation["task_envelope"] != {
        "task_id": task_id,
        "digest_sha256": task_digest,
    }:
        return "TASK_ENVELOPE_DIGEST_MISMATCH"
    if attestation["candidate_sha"] != candidate_sha:
        return "CANDIDATE_SHA_MISMATCH"
    binding, code = _trusted_record(
        bindings, "binding_id", attestation["binding"]["binding_id"], "BINDING_MISSING"
    )
    if code is not None or binding is None:
        return code
    if binding["binding_version"] != attestation["binding"]["binding_version"]:
        return "BINDING_MISMATCH"
    if (code := _binding_code(binding, attestation, profile, verification_time)) is not None:
        return code
    key, code = _key_code(
        profile,
        attestation["signature"]["key_id"],
        "DELIVERY_APPROVAL_ATTESTATION",
        attestation["role"],
        task_id,
        issued_at,
        verification_time,
    )
    if code is not None or key is None:
        return code
    if key["principal"] != attestation["principal"]:
        return "PRINCIPAL_MISMATCH"
    if not _verify_signature(attestation, key["public_key"], DOMAINS["attestation"]):
        return "SIGNATURE_INVALID"
    if ROLE_DECISIONS[attestation["role"]] != attestation["decision"]:
        return "DECISION_INVALID"
    return None


def _verify(
    evidence: dict[str, Any],
    trust_anchors: dict[str, Any],
    trust_profile: dict[str, Any],
    task_envelope: dict[str, Any],
    expected_candidate_sha: str,
    verification_time: str,
) -> dict[str, Any]:
    if set(evidence) != {"bindings", "attestations"}:
        return _verdict(
            "FAIL",
            "SCHEMA_INVALID",
            task_envelope,
            expected_candidate_sha,
            trust_profile,
            verification_time,
        )
    checked_at = _instant(verification_time)
    if (code := _profile_trusted(trust_anchors, trust_profile, checked_at)) is not None:
        return _verdict(
            "FAIL",
            code,
            task_envelope,
            expected_candidate_sha,
            trust_profile,
            verification_time,
        )
    if list(
        Draft202012Validator(_load_json(TASK_SCHEMA_PATH)).iter_errors(task_envelope)
    ):
        return _verdict(
            "FAIL",
            "TASK_ENVELOPE_INVALID",
            task_envelope,
            expected_candidate_sha,
            trust_profile,
            verification_time,
        )
    task_id = task_envelope["task_id"]
    task_digest = _digest(task_envelope)
    subjects = {role: set() for role in ROLE_DECISIONS}
    for attestation in evidence["attestations"]:
        code = _attestation_code(
            attestation,
            evidence["bindings"],
            trust_profile,
            task_id,
            task_digest,
            expected_candidate_sha,
            checked_at,
        )
        if code is not None:
            return _verdict(
                "FAIL",
                code,
                task_envelope,
                expected_candidate_sha,
                trust_profile,
                verification_time,
            )
        subjects[attestation["role"]].add(attestation["accountable_subject"])
    if any(not subjects[role] for role in ROLE_DECISIONS):
        return _verdict(
            "FAIL",
            "APPROVAL_MISSING",
            task_envelope,
            expected_candidate_sha,
            trust_profile,
            verification_time,
        )
    pairs = [("Executor", "QA"), ("Executor", "Reviewer"), ("QA", "Reviewer")]
    if any(subjects[left] & subjects[right] for left, right in pairs):
        return _verdict(
            "FAIL",
            "INDEPENDENCE_VIOLATION",
            task_envelope,
            expected_candidate_sha,
            trust_profile,
            verification_time,
        )
    return _verdict(
        "PASS",
        "APPROVAL_AUTHORITY_VERIFIED",
        task_envelope,
        expected_candidate_sha,
        trust_profile,
        verification_time,
        subjects,
    )


def _evidence(suite: dict[str, Any]) -> dict[str, Any]:
    return {
        "bindings": copy.deepcopy(suite["bindings"]),
        "attestations": copy.deepcopy(suite["attestations"]),
    }


def _context(suite: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_envelope": _load_json(ROOT / suite["task_envelope"]["path"]),
        "candidate_sha": suite["candidate_sha"],
    }


def _change_key(profile: dict[str, Any], key_id: str, field: str, value: Any) -> None:
    key = next(item for item in profile["keys"] if item["key_id"] == key_id)
    key[field] = value
    _resign(profile, "root", DOMAINS["profile"])


def _refresh_binding(
    evidence: dict[str, Any], role: str, mutation: Callable[[dict[str, Any]], None]
) -> None:
    binding = next(item for item in evidence["bindings"] if item["role"] == role)
    attestation = next(item for item in evidence["attestations"] if item["role"] == role)
    mutation(binding)
    _resign(binding, "binding", DOMAINS["binding"])
    attestation["binding"]["digest_sha256"] = _digest(binding)
    _resign(attestation, role.lower(), DOMAINS["attestation"])


def _apply_probe(
    probe_id: str,
    evidence: dict[str, Any],
    profile: dict[str, Any],
    context: dict[str, Any],
) -> None:
    qa = evidence["attestations"][1]
    if probe_id == "caller-declared-trust-profile":
        evidence["trust_profile"] = copy.deepcopy(profile)
    elif probe_id == "caller-declared-public-key":
        evidence["public_key"] = profile["keys"][2]["public_key"]
    elif probe_id == "caller-declared-issuer":
        qa["principal"]["issuer"] = "https://caller.invalid"
        _resign(qa, "qa", DOMAINS["attestation"])
    elif probe_id == "unknown-signer":
        qa["signature"]["key_id"] = "caller-key"
    elif probe_id == "revoked-signer":
        _change_key(profile, "daa-test-qa", "revoked_at", "2026-08-18T12:30:00Z")
    elif probe_id == "expired-signer":
        _change_key(profile, "daa-test-qa", "valid_until", "2026-08-18T11:00:00Z")
    elif probe_id == "signer-out-of-scope":
        _change_key(profile, "daa-test-qa", "task_envelope_ids", ["TASK-0759"])
    elif probe_id == "binding-missing":
        evidence["bindings"] = [
            item for item in evidence["bindings"] if item["role"] != "QA"
        ]
    elif probe_id == "binding-signature-invalid":
        evidence["bindings"][1]["signature"]["value"] = "A" * 86
    elif probe_id == "binding-temporal-incompatible":
        _refresh_binding(
            evidence,
            "QA",
            lambda binding: binding.update(valid_from="2026-08-19T00:00:00Z"),
        )
    elif probe_id == "principal-divergent":
        qa["principal"]["subject"] = "principal-other"
        _resign(qa, "qa", DOMAINS["attestation"])
    elif probe_id == "role-divergent":
        qa["role"] = "Reviewer"
        _resign(qa, "qa", DOMAINS["attestation"])
    elif probe_id == "accountable-subject-divergent":
        qa["accountable_subject"] = "acct:person/other"
        _resign(qa, "qa", DOMAINS["attestation"])
    elif probe_id == "task-envelope-invalid":
        context["task_envelope"].pop("role")
    elif probe_id == "task-envelope-digest-divergent":
        qa["task_envelope"]["digest_sha256"] = "0" * 64
        _resign(qa, "qa", DOMAINS["attestation"])
    elif probe_id == "task-envelope-replay":
        context["task_envelope"] = _load_json(ROOT / ".codex/tasks/TASK-0759.json")
    elif probe_id == "candidate-sha-divergent":
        qa["candidate_sha"] = "f" * 40
        _resign(qa, "qa", DOMAINS["attestation"])
    elif probe_id == "candidate-sha-replay":
        context["candidate_sha"] = "e" * 40
    elif probe_id == "approval-missing":
        evidence["attestations"] = [
            item for item in evidence["attestations"] if item["role"] != "QA"
        ]
    elif probe_id == "approval-tampered":
        qa["decision"] = "REJECT"
    elif probe_id == "approval-reject":
        qa["decision"] = "REJECT"
        _resign(qa, "qa", DOMAINS["attestation"])
    elif probe_id == "accountable-subject-overlap":
        _refresh_binding(
            evidence,
            "QA",
            lambda binding: binding.update(accountable_subject="acct:person/executor"),
        )
        qa["accountable_subject"] = "acct:person/executor"
        _resign(qa, "qa", DOMAINS["attestation"])
    elif probe_id == "spec001-trust-scope-cross-use":
        qa["trust_scope"] = "SPEC-001-PROMPT-BUNDLE-V1"
        _resign(qa, "qa", DOMAINS["attestation"])
    elif probe_id == "spec001-signature-domain-cross-use":
        _resign(qa, "qa", "DSGEOREF-PROMPT-BUNDLE-V1")
    else:
        raise AssertionError(f"probe is not implemented: {probe_id}")


def test_delivery_approval_authority_contract() -> None:
    suite = _load_json(VECTOR_PATH)
    trusted = suite["trusted_configuration"]
    _validator("anchors").validate(trusted["trust_anchors"])
    _validator("profile").validate(trusted["trust_profile"])
    for binding in suite["bindings"]:
        _validator("binding").validate(binding)
    for attestation in suite["attestations"]:
        _validator("attestation").validate(attestation)
    evidence = _evidence(suite)
    context = _context(suite)
    assert _digest(context["task_envelope"]) == suite["task_envelope"]["digest_sha256"]
    verdict = _verify(
        evidence,
        trusted["trust_anchors"],
        trusted["trust_profile"],
        context["task_envelope"],
        context["candidate_sha"],
        suite["verification_time"],
    )
    assert verdict["status"] == "PASS"
    assert verdict["code"] == "APPROVAL_AUTHORITY_VERIFIED"
    assert set(verdict["validated_roles"]) == set(ROLE_DECISIONS)
    assert all(verdict["accountable_subjects"][role] for role in ROLE_DECISIONS)
    with OWNERSHIP_PATH.open(encoding="utf-8", newline="") as ownership_file:
        registered = {row["contract"] for row in csv.DictReader(ownership_file)}
    assert PUBLISHED_PATHS <= registered
    prompt_schema = _load_json(ROOT / "contracts/prompts/prompt-bundle-signature.schema.json")
    assert prompt_schema["properties"]["message_profile"]["const"] not in DOMAINS.values()
    assert SCOPE not in json.dumps(prompt_schema, sort_keys=True)


def test_multiple_valid_executors_are_accepted() -> None:
    suite = _load_json(VECTOR_PATH)
    trusted = suite["trusted_configuration"]
    evidence = _evidence(suite)
    context = _context(suite)
    profile = copy.deepcopy(trusted["trust_profile"])

    first_key = next(key for key in profile["keys"] if key["key_id"] == "daa-test-executor")
    second_key = copy.deepcopy(first_key)
    second_key.update(
        key_id="daa-test-executor-2",
        public_key=_public_key("executor-2"),
        principal={
            "issuer": first_key["principal"]["issuer"],
            "subject": "principal-executor-2",
        },
    )
    profile["keys"].append(second_key)
    _resign(profile, "root", DOMAINS["profile"])

    first_binding = next(item for item in evidence["bindings"] if item["role"] == "Executor")
    second_binding = copy.deepcopy(first_binding)
    second_binding.update(
        binding_id="daa-binding-executor-2",
        principal=second_key["principal"],
        accountable_subject="acct:person/executor-2",
    )
    _resign(second_binding, "binding", DOMAINS["binding"])
    evidence["bindings"].append(second_binding)

    first_attestation = next(
        item for item in evidence["attestations"] if item["role"] == "Executor"
    )
    second_attestation = copy.deepcopy(first_attestation)
    second_attestation.update(
        attestation_id="daa-attestation-executor-2",
        principal=second_key["principal"],
        accountable_subject="acct:person/executor-2",
        binding={
            "binding_id": second_binding["binding_id"],
            "binding_version": second_binding["binding_version"],
            "digest_sha256": _digest(second_binding),
        },
    )
    second_attestation["signature"]["key_id"] = second_key["key_id"]
    _resign(second_attestation, "executor-2", DOMAINS["attestation"])
    evidence["attestations"].append(second_attestation)

    verdict = _verify(
        evidence,
        trusted["trust_anchors"],
        profile,
        context["task_envelope"],
        context["candidate_sha"],
        suite["verification_time"],
    )
    assert verdict["status"] == "PASS"
    assert verdict["code"] == "APPROVAL_AUTHORITY_VERIFIED"
    assert verdict["accountable_subjects"]["Executor"] == [
        "acct:person/executor",
        "acct:person/executor-2",
    ]
    assert not (
        set(verdict["accountable_subjects"]["Executor"])
        & set(verdict["accountable_subjects"]["QA"])
        | set(verdict["accountable_subjects"]["Executor"])
        & set(verdict["accountable_subjects"]["Reviewer"])
    )


def test_delivery_approval_authority_fail_closed() -> None:
    suite = _load_json(VECTOR_PATH)
    trusted = suite["trusted_configuration"]
    observed: dict[str, str] = {}
    for probe in suite["probes"]:
        evidence = _evidence(suite)
        context = _context(suite)
        profile = copy.deepcopy(trusted["trust_profile"])
        _apply_probe(probe["probe_id"], evidence, profile, context)
        verdict = _verify(
            evidence,
            trusted["trust_anchors"],
            profile,
            context["task_envelope"],
            context["candidate_sha"],
            suite["verification_time"],
        )
        assert verdict["status"] == probe["expected_status"] == "FAIL"
        assert verdict["code"] == probe["expected_code"]
        assert verdict["validated_roles"] == []
        assert all(not values for values in verdict["accountable_subjects"].values())
        observed[probe["probe_id"]] = verdict["code"]
    assert len(observed) == len(suite["probes"]) == 24
