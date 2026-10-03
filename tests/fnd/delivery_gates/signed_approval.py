"""Use the existing DAA cryptographic verifier with test-only trust material."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import pytest
from tests.security.delivery_approval_authority.fixture import (
    BINDING_DOMAIN,
    PROFILE_DOMAIN,
    _anchors,
    _attestation,
    _binding,
    _key,
    _profile,
    _sign,
)
from tools.governance.delivery_approval_authority.repository import GovernedTrust
from tools.governance.delivery_approval_authority.schemas import SchemaSet
from tools.governance.delivery_approval_authority.verifier import OperationalVerifier
from tools.governance.delivery_gates import satisfaction

from .fixture import ROOT, git, write

TRUST = "contracts/assurance/delivery-approval-authority/trust"


def create_approval(root: Path, snapshot: dict[str, Any], candidate: str) -> dict[str, Any]:
    shutil.copytree(
        ROOT / "contracts/assurance/delivery-approval-authority",
        root / "contracts/assurance/delivery-approval-authority",
        dirs_exist_ok=True,
    )
    keys = {label: _key(label) for label in ("root", "binding", "executor", "qa", "reviewer")}
    anchors, profile = _anchors(keys["root"]), _profile(keys)
    for record in profile["keys"]:
        record["task_envelope_ids"] = [snapshot["task_id"]]
    _sign(profile, keys["root"], PROFILE_DOMAIN)
    anchors_ref = write(root, TRUST + "/anchors/gate-test.json", anchors)
    profile_ref = write(root, TRUST + "/profiles/gate-test.json", profile)
    write(
        root,
        TRUST + "/manifest.json",
        {
            "schema_version": "1.0.0",
            "anchors": anchors_ref,
            "profile": profile_ref,
        },
    )
    bindings, attestations = [], []
    for role in ("Executor", "QA", "Reviewer"):
        binding = _binding(role, keys["binding"])
        binding["task_envelope_ids"] = [snapshot["task_id"]]
        _sign(binding, keys["binding"], BINDING_DOMAIN)
        bindings.append(binding)
        attestations.append(_attestation(role, binding, snapshot, candidate, keys[role.lower()]))
    return {"bindings": bindings, "attestations": attestations}


def install_test_verifier(monkeypatch: pytest.MonkeyPatch, root: Path) -> None:
    def verify(**arguments: Any) -> dict[str, Any]:
        revision = git(root, "rev-parse", "HEAD")
        from tools.governance.delivery_gates.model import parse

        profile = parse((root / (TRUST + "/profiles/gate-test.json")).read_bytes())
        anchors = parse((root / (TRUST + "/anchors/gate-test.json")).read_bytes())
        trust = GovernedTrust(revision, anchors, profile, {})
        verifier = OperationalVerifier(trust, SchemaSet(root, revision))
        return verifier.verify(
            evidence=arguments["evidence"],
            task_envelope=arguments["task_envelope"],
            candidate_sha=arguments["expected_candidate_sha"],
            verification_time="2026-08-22T12:30:00Z",
        )

    monkeypatch.setattr(satisfaction, "verify_delivery_approval", verify)
