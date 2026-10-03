"""External signature requests must never produce approval from unsigned material."""

from pathlib import Path

import pytest
from tools.governance.delivery_approval_authority.signing_requests import (
    attach,
    prepare_attestation,
    write_new,
)


def test_unsigned_profile_cannot_be_imported(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[3]
    request = root / (
        "evidence/delivery-gates/DG-TASK-0738-A/"
        "e14f7e4f23a8bb4e7d16827d9cb2312a1d03d912/signing-request/profile.pending.json"
    )
    (tmp_path / "profile.pending.json").write_bytes(request.read_bytes())
    signature = tmp_path / "invalid.sig"
    signature.write_bytes(bytes(64))
    with pytest.raises(ValueError, match="external signature is invalid"):
        attach(tmp_path, "profile", "profile", signature)
    assert not (tmp_path / "profile.signed.json").exists()


@pytest.mark.parametrize(
    "role,decision",
    [("Executor", "PASS"), ("QA", "DELIVERED"), ("Reviewer", "PASS"), ("Project Owner", "APPROVE")],
)
def test_cross_role_decision_rejected(tmp_path: Path, role: str, decision: str) -> None:
    with pytest.raises(ValueError, match="decision does not belong to role"):
        prepare_attestation(tmp_path, role, decision)
    assert list(tmp_path.iterdir()) == []


def test_signed_record_is_append_only(tmp_path: Path) -> None:
    target = tmp_path / "record.signed.json"
    write_new(target, {"signed_content": "original"})
    original = target.read_bytes()
    with pytest.raises(FileExistsError):
        write_new(target, {"signed_content": "replacement"})
    assert target.read_bytes() == original
