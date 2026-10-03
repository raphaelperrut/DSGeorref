"""Public-only requests for the existing external DAA custodian; never creates keys."""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from .api import verify_delivery_approval
from .canonical import canonical_json_bytes, load_json_object
from .crypto import digest, instant, signature_message, verify_signature
from .records import profile_code
from .repository import resolve_governed_trust, runtime_governed_repository
from .schemas import SchemaSet
from .verdicts import SOLO_ROLES


def read(path: Path) -> dict[str, Any]:
    return load_json_object(path.read_bytes())


def write_new(path: Path, record: dict[str, Any]) -> None:
    with path.open("xb") as target:
        target.write(canonical_json_bytes(record))


def public_key(root: Path, record: dict[str, Any], kind: str) -> str:
    repository, revision = runtime_governed_repository()
    trust = resolve_governed_trust(repository, revision)
    source = (
        trust.anchors["anchors"]
        if kind == "profile"
        else read(root / "profile.signed.json")["keys"]
    )
    matches = [key for key in source if key["key_id"] == record["signature"]["key_id"]]
    if len(matches) != 1:
        raise ValueError("existing public signing key is unavailable or ambiguous")
    return matches[0]["public_key"]


def attach(root: Path, name: str, kind: str, signature: Path) -> None:
    if re.fullmatch(r"[a-z][a-z-]{1,63}", name) is None:
        raise ValueError("noncanonical record name")
    record = read(root / f"{name}.pending.json")
    record["signature"]["value"] = (
        base64.urlsafe_b64encode(signature.read_bytes()).decode().rstrip("=")
    )
    repository, revision = runtime_governed_repository()
    schemas = SchemaSet(repository, revision)
    if schemas.code(kind, record) is not None:
        raise ValueError("signed record does not conform to the existing DAA schema")
    if not verify_signature(record, public_key(root, record, kind), kind):
        raise ValueError("external signature is invalid; record not written")
    write_new(root / f"{name}.signed.json", record)
    print(f"SIGNATURE_VALID {name} canonical_sha256={digest(record)}")


def trusted_bindings(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    repository, revision = runtime_governed_repository()
    trust = resolve_governed_trust(repository, revision)
    schemas = SchemaSet(repository, revision)
    profile = read(root / "profile.signed.json")
    code = profile_code(schemas, trust.anchors, profile, datetime.now(UTC))
    if code is not None:
        raise ValueError(f"external profile invalid: {code}")
    bindings = [
        read(root / f"{role.lower().replace(' ', '-')}-binding.signed.json") for role in SOLO_ROLES
    ]
    for record in bindings:
        if schemas.code("binding", record) is not None or not verify_signature(
            record, public_key(root, record, "binding"), "binding"
        ):
            raise ValueError("external binding invalid")
    return profile, bindings


def session_inputs(root: Path, role: str) -> tuple[dict, list, dict, list, str]:
    profile, bindings = trusted_bindings(root)
    context = read(root / "request-context.json")
    snapshot = read(root.parent / "task-envelope.acceptance.json")
    if digest(snapshot) != context["snapshot_canonical_sha256"]:
        raise ValueError("acceptance snapshot drift")
    manifest = (root.parent / "acceptance-manifest.json").read_bytes()
    if hashlib.sha256(manifest).hexdigest() != context["manifest_sha256"]:
        raise ValueError("acceptance manifest drift")
    sequence = SOLO_ROLES.index(role) + 1
    prior = [
        read(root / f"{item.lower().replace(' ', '-')}-attestation.signed.json")
        for item in SOLO_ROLES[: sequence - 1]
    ]
    for record in prior:
        if not verify_signature(record, public_key(root, record, "attestation"), "attestation"):
            raise ValueError("predecessor signature invalid")
    now = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    if prior and instant(now) <= instant(prior[-1]["issued_at"]):
        raise ValueError("session must begin after signed predecessor")
    expected = {"task_id": "TASK-0738", "digest_sha256": digest(snapshot)}
    if any(
        item["task_envelope"] != expected or item["role"] != expected_role
        for item, expected_role in zip(bindings, SOLO_ROLES, strict=True)
    ):
        raise ValueError("bindings must authorize the final snapshot in role order")
    return context, bindings, profile, prior, now


def functional_session(context: dict, bindings: list, prior: list, role: str, now: str) -> dict:
    session = {
        "session_id": f"task-0738-{uuid4().hex}",
        "role": role,
        "sequence": SOLO_ROLES.index(role) + 1,
        "started_at": now,
        "input_snapshot_digest_sha256": context["snapshot_canonical_sha256"],
        "predecessor_attestation_digest_sha256": digest(prior[-1]) if prior else None,
        "verifier_input_set_digest_sha256": None,
    }
    if role == "Project Owner":
        session["verifier_input_set_digest_sha256"] = digest(
            {
                "task_envelope": bindings[0]["task_envelope"],
                "candidate_sha": context["candidate_sha"],
                "bindings": [
                    {"role": item["role"], "digest_sha256": digest(item)} for item in bindings
                ],
                "attestations": [
                    {"role": item["role"], "digest_sha256": digest(item)} for item in prior
                ],
            }
        )
    return session


def prepare_attestation(root: Path, role: str, decision: str) -> None:
    allowed = {
        "Executor": ("DELIVERED",),
        "QA": ("APPROVE", "REJECT"),
        "Reviewer": ("APPROVE", "REJECT"),
        "Project Owner": ("PASS", "NO_GO"),
    }
    if decision not in allowed[role]:
        raise ValueError("decision does not belong to role")
    context, bindings, profile, prior, now = session_inputs(root, role)
    binding = bindings[SOLO_ROLES.index(role)]
    record = copy.deepcopy(context["attestation_template"])
    record.update(
        attestation_id=f"task-0738-{uuid4().hex}",
        role=role,
        decision=decision,
        task_envelope=binding["task_envelope"],
        issued_at=now,
        binding={
            "binding_id": binding["binding_id"],
            "binding_version": "2.0.0",
            "digest_sha256": digest(binding),
        },
    )
    record["functional_session"] = functional_session(context, bindings, prior, role, now)
    keys = [
        key
        for key in profile["keys"]
        if key["purpose"] == "DELIVERY_APPROVAL_ATTESTATION" and key["roles"] == [role]
    ]
    if len(keys) != 1:
        raise ValueError("distinct existing role key required")
    record["signature"]["key_id"] = keys[0]["key_id"]
    name = role.lower().replace(" ", "-") + "-attestation"
    write_new(root / f"{name}.pending.json", record)
    (root / f"{name}.message.bin").write_bytes(signature_message(record, "attestation"))
    print(f"ATTESTATION_REQUEST {name} issued_at={now}")


def verify(root: Path) -> dict[str, Any]:
    context = read(root / "request-context.json")
    bundle = {"bindings": [], "attestations": []}
    for role in SOLO_ROLES:
        name = role.lower().replace(" ", "-")
        for kind, field in (("binding", "bindings"), ("attestation", "attestations")):
            path = root / f"{name}-{kind}.signed.json"
            if path.exists():
                bundle[field].append(read(path))
    verdict = verify_delivery_approval(
        task_envelope=read(root.parent / "task-envelope.acceptance.json"),
        expected_candidate_sha=context["candidate_sha"],
        verification_time=datetime.now(UTC).isoformat(),
        evidence=bundle,
    )
    if verdict["status"] == "PASS":
        write_new(root.parent / "daa-bundle.json", bundle)
    return verdict


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    imported = commands.add_parser("attach")
    imported.add_argument("--name", required=True)
    imported.add_argument("--kind", choices=("profile", "binding", "attestation"), required=True)
    imported.add_argument("--signature", type=Path, required=True)
    prepared = commands.add_parser("prepare-attestation")
    prepared.add_argument("--role", choices=SOLO_ROLES, required=True)
    prepared.add_argument(
        "--decision", choices=("DELIVERED", "APPROVE", "REJECT", "PASS", "NO_GO"), required=True
    )
    commands.add_parser("verify")
    args = parser.parse_args()
    if args.command == "attach":
        attach(args.root, args.name, args.kind, args.signature)
    elif args.command == "prepare-attestation":
        prepare_attestation(args.root, args.role, args.decision)
    else:
        import json

        result = verify(args.root)
        print(json.dumps(result, indent=2))
        raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
