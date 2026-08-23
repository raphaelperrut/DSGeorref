from __future__ import annotations

import copy
import hashlib
import inspect
import itertools
import json
import os
import subprocess
import sys
import tempfile
from unittest import mock
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = ROOT / (
    "tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "frz-gov-adr-gov-dec-parte-1"
)
MODULE_ROOT_2 = ROOT / (
    "tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "sprint-001-tool-parte-2"
)
SECURITY_TEST_ROOT = ROOT / "tests/security"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(MODULE_ROOT))
sys.path.insert(0, str(MODULE_ROOT_2))
sys.path.insert(0, str(SECURITY_TEST_ROOT))

from baseline_lifecycle import (  # noqa: E402
    AppendOnlyRecordLedger,
    build_baseline,
    validate_baseline,
    validate_closure,
    validate_evidence_set,
    validate_reopening,
    validate_transition,
)
import delivery_approval as daa_adapter  # noqa: E402
from delivery_approval_authority.fixture import (  # noqa: E402
    ATTESTATION_DOMAIN as DAA_ATTESTATION_DOMAIN,
    BINDING_DOMAIN as DAA_BINDING_DOMAIN,
    PROFILE_DOMAIN as DAA_PROFILE_DOMAIN,
    _anchors as daa_test_anchors,
    _attestation as daa_test_attestation,
    _binding as daa_test_binding,
    _key as daa_test_key,
    _profile as daa_test_profile,
    _sign as daa_test_sign,
)
from tools.governance.delivery_approval_authority.repository import (  # noqa: E402
    GovernedTrust,
)
from tools.governance.delivery_approval_authority.schemas import SchemaSet  # noqa: E402
from tools.governance.delivery_approval_authority.verifier import (  # noqa: E402
    OperationalVerifier,
)
from canonical_json import canonical_json_bytes  # noqa: E402
from decision_governance import (  # noqa: E402
    DECISION_CLASSIFICATIONS,
    validate_adr_change_governance,
    validate_classification_before_identifier,
    validate_new_adr_eligibility,
)
from portfolio_validation import validate_snapshot_tombstone_delta_history  # noqa: E402
from scope_validation import validate_effective_task_scope  # noqa: E402
from sprint_validation import (  # noqa: E402
    derive_canonical_sprint_selection,
    minimum_sprint_scope,
    validate_graph_derived_selection,
    validate_minimum_sprint_scope,
)
from sprint_decisions import (  # noqa: E402
    validate_ci_capabilities,
    validate_contract_exercises,
    validate_cutover_preconditions,
    validate_diagnostic_claim,
    validate_sprint_closure,
)
from sprint_graph import validate_sprint_extension, validate_wave  # noqa: E402
from sprint_evidence import (  # noqa: E402
    REQUIRED_DECISIONS,
    REQUIRED_EVIDENCE_KINDS,
    REQUIRED_REQUIREMENTS,
    REQUIRED_TESTS,
    SprintEvidenceLedger,
    build_sprint_evidence_set,
    sprint_evidence_human_summary,
    validate_sprint_evidence_set,
)
from toolchain_validation import (  # noqa: E402
    RUNTIME_GATES,
    validate_make_ci_parity,
    validate_python_runtime,
    validate_uv_lock_baseline,
)


TASK_PATH = ".codex/tasks/TASK-0688.json"
CHECKPOINT = "d7788e2b45802ddd71d422b440d63984ee8b70d0"
REJECTED = "0160efea15c84de1703bcd1df0e551376a1ce892"
BASE = "afcbb18719e4531e2046c524633e1f68bf9b6e53"
ADR_AUTHORITY_PATH = (
    "docs/02-architecture/adrs/"
    "ADR-057-release-train-publicacao-e-gates-de-distribuicao.md"
)
SCHEMA_PATH = (
    "docs/03-engineering/contexts/engineering_governance/"
    "governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "frz-gov-adr-gov-dec-parte-1/foundation-baseline-lifecycle.schema.json"
)
_FIXTURE_SEQUENCE = itertools.count()
_DAA_GATES: dict[Path, daa_adapter.DeliveryApprovalGate] = {}
_DAA_TEST_KEYS = {
    label: daa_test_key(label)
    for label in ("root", "binding", "executor", "qa", "reviewer")
}
_DAA_TEST_ANCHORS = daa_test_anchors(_DAA_TEST_KEYS["root"])
_DAA_TEST_VALID_UNTIL = "2027-08-23T00:00:00Z"
for _daa_anchor in _DAA_TEST_ANCHORS["anchors"]:
    _daa_anchor["valid_until"] = _DAA_TEST_VALID_UNTIL
_DAA_TEST_SCHEMAS: SchemaSet | None = None
_DAA_TEST_VERIFIERS: dict[str, OperationalVerifier] = {}


def _revision(name: str = "HEAD", repository: Path = ROOT) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", name],
        check=True,
        capture_output=True,
        encoding="ascii",
    )
    return completed.stdout.strip()


def _git(repository: Path, *arguments: str, text: bool = True) -> str | bytes:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        encoding="utf-8" if text else None,
    )
    return completed.stdout


def _init_repository(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q")
    _git(path, "config", "user.name", "Governed Fixture")
    _git(path, "config", "user.email", "fixture@dsgeorref.invalid")


def _write(repository: Path, relative_path: str, content: bytes) -> None:
    target = repository / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


def _fixture_directory(name: str) -> Path:
    suffix = f"{os.getpid()}-{next(_FIXTURE_SEQUENCE)}"
    target = Path(tempfile.gettempdir()) / f"dsg0798-{name}-{suffix}"
    target.mkdir(parents=True)
    return target


def _commit(repository: Path, message: str) -> str:
    _install_pending_daa_records(repository)
    _git(repository, "add", ".")
    _git(repository, "commit", "-q", "-m", message)
    return _revision(repository=repository)


def _install_pending_daa_records(repository: Path) -> None:
    claims: set[tuple[str, str]] = set()
    for path in repository.rglob("*.json"):
        if ".git" in path.parts or "delivery-approval-authority" in path.parts:
            continue
        try:
            _collect_authority_claims(json.loads(path.read_text(encoding="utf-8")), claims)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
    for task_id, candidate in sorted(claims):
        task_path = f".codex/tasks/{task_id}.json"
        try:
            task = json.loads(_git(repository, "show", f"{candidate}:{task_path}"))
        except subprocess.CalledProcessError:
            continue
        evidence = _signed_daa_evidence(task, candidate)
        target = f"evidence/delivery-approval-authority/{task_id}/{candidate}.json"
        _write(repository, target, canonical_json_bytes(evidence))


def _collect_authority_claims(value: object, claims: set[tuple[str, str]]) -> None:
    if isinstance(value, dict):
        task_id = value.get("task_id")
        candidate = value.get("reviewed_candidate_commit")
        if isinstance(task_id, str) and isinstance(candidate, str) and len(candidate) == 40:
            claims.add((task_id, candidate))
        for item in value.values():
            _collect_authority_claims(item, claims)
    elif isinstance(value, list):
        for item in value:
            _collect_authority_claims(item, claims)


def _signed_daa_evidence(task: dict[str, Any], candidate: str) -> dict[str, Any]:
    task_id = task["task_id"]
    bindings = [
        daa_test_binding(role, _DAA_TEST_KEYS["binding"])
        for role in ("Executor", "QA", "Reviewer")
    ]
    for binding in bindings:
        binding["task_envelope_ids"] = [task_id]
        binding["valid_until"] = _DAA_TEST_VALID_UNTIL
        daa_test_sign(
            binding,
            _DAA_TEST_KEYS["binding"],
            DAA_BINDING_DOMAIN,
        )
    attestations = [
        daa_test_attestation(
            role,
            binding,
            task,
            candidate,
            _DAA_TEST_KEYS[role.lower()],
        )
        for role, binding in zip(
            ("Executor", "QA", "Reviewer"), bindings, strict=True
        )
    ]
    return {"bindings": bindings, "attestations": attestations}


def _operational_test_verdict(
    *,
    task_envelope: Any,
    expected_candidate_sha: Any,
    verification_time: Any,
    evidence: Any,
) -> dict[str, Any]:
    global _DAA_TEST_SCHEMAS
    task_id = task_envelope.get("task_id") if isinstance(task_envelope, dict) else None
    if not isinstance(task_id, str):
        task_id = "INVALID"
    verifier = _DAA_TEST_VERIFIERS.get(task_id)
    if verifier is None:
        profile = daa_test_profile(_DAA_TEST_KEYS)
        profile["valid_until"] = _DAA_TEST_VALID_UNTIL
        for issuer in profile["identity_issuers"]:
            issuer["valid_until"] = _DAA_TEST_VALID_UNTIL
        for signer in profile["keys"]:
            signer["valid_until"] = _DAA_TEST_VALID_UNTIL
            signer["task_envelope_ids"] = [task_id]
        daa_test_sign(profile, _DAA_TEST_KEYS["root"], DAA_PROFILE_DOMAIN)
        revision = _revision(repository=ROOT)
        if _DAA_TEST_SCHEMAS is None:
            _DAA_TEST_SCHEMAS = SchemaSet(ROOT, revision)
        trust = GovernedTrust(
            revision=revision,
            anchors=copy.deepcopy(_DAA_TEST_ANCHORS),
            profile=profile,
            digests={},
        )
        verifier = OperationalVerifier(trust, _DAA_TEST_SCHEMAS)
        _DAA_TEST_VERIFIERS[task_id] = verifier
    return verifier.verify(
        evidence=evidence,
        task_envelope=task_envelope,
        candidate_sha=expected_candidate_sha,
        verification_time=verification_time,
    )


def _daa_gate(repository: Path) -> daa_adapter.DeliveryApprovalGate:
    key = repository.resolve()
    if key not in _DAA_GATES:
        _DAA_GATES[key] = daa_adapter.DeliveryApprovalGate()
    return _DAA_GATES[key]


_BUILD_SPRINT_EVIDENCE_SET = build_sprint_evidence_set
_VALIDATE_CONTRACT_EXERCISES = validate_contract_exercises
_VALIDATE_CUTOVER_PRECONDITIONS = validate_cutover_preconditions
_VALIDATE_DIAGNOSTIC_CLAIM = validate_diagnostic_claim
_VALIDATE_PYTHON_RUNTIME = validate_python_runtime
_VALIDATE_SPRINT_CLOSURE = validate_sprint_closure
_VALIDATE_SPRINT_EVIDENCE_SET = validate_sprint_evidence_set
_VALIDATE_SPRINT_EXTENSION = validate_sprint_extension
_VALIDATE_WAVE = validate_wave


def _with_daa(function: Any, repository: Path, *args: Any, **kwargs: Any) -> Any:
    kwargs.setdefault("delivery_gate", _daa_gate(repository))
    with mock.patch.object(
        daa_adapter,
        "verify_delivery_approval",
        _operational_test_verdict,
    ):
        return function(repository, *args, **kwargs)


def build_sprint_evidence_set(repository: Path, **kwargs: Any) -> dict[str, Any]:
    return _with_daa(_BUILD_SPRINT_EVIDENCE_SET, repository, **kwargs)


def validate_contract_exercises(repository: Path, *args: Any, **kwargs: Any) -> Any:
    return _with_daa(_VALIDATE_CONTRACT_EXERCISES, repository, *args, **kwargs)


def validate_cutover_preconditions(repository: Path, *args: Any, **kwargs: Any) -> Any:
    return _with_daa(_VALIDATE_CUTOVER_PRECONDITIONS, repository, *args, **kwargs)


def validate_diagnostic_claim(repository: Path, *args: Any, **kwargs: Any) -> Any:
    return _with_daa(_VALIDATE_DIAGNOSTIC_CLAIM, repository, *args, **kwargs)


def validate_python_runtime(repository: Path, *args: Any, **kwargs: Any) -> Any:
    return _with_daa(_VALIDATE_PYTHON_RUNTIME, repository, *args, **kwargs)


def validate_sprint_closure(repository: Path, *args: Any, **kwargs: Any) -> Any:
    return _with_daa(_VALIDATE_SPRINT_CLOSURE, repository, *args, **kwargs)


def validate_sprint_evidence_set(repository: Path, *args: Any, **kwargs: Any) -> Any:
    return _with_daa(_VALIDATE_SPRINT_EVIDENCE_SET, repository, *args, **kwargs)


def validate_sprint_extension(repository: Path, *args: Any, **kwargs: Any) -> Any:
    return _with_daa(_VALIDATE_SPRINT_EXTENSION, repository, *args, **kwargs)


def validate_wave(repository: Path, *args: Any, **kwargs: Any) -> Any:
    return _with_daa(_VALIDATE_WAVE, repository, *args, **kwargs)


def _reference(repository: Path, revision: str, path: str) -> dict[str, str]:
    content = _git(repository, "show", f"{revision}:{path}", text=False)
    assert isinstance(content, bytes)
    return {
        "source_revision": revision,
        "path": path,
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def _codes(findings: list[Any]) -> set[str]:
    return {finding.code for finding in findings}


def _baseline(revision: str | None = None, version: str = "1.0.0") -> dict[str, Any]:
    return build_baseline(
        ROOT,
        revision or _revision(),
        "FOUNDATION-BASELINE-CANONICAL",
        version,
        TASK_PATH,
    )


def test_foundation_baseline_digest_controlled_change_and_adr_supersession() -> None:
    current = _baseline()
    predecessor = _baseline(_revision("origin/main"), "0.9.0")
    assert current == _baseline()
    assert validate_baseline(ROOT, current) == []
    assert current["coverage"] == sorted(current["coverage"], key=lambda row: row["path"])
    assert any(row["path"] == TASK_PATH for row in current["coverage"])
    assert _codes(validate_transition(ROOT, predecessor, current, None)) == {
        "SUPERSESSION_REQUIRED"
    }
    supersession = {
        "schema_version": "2.0.0",
        "record_type": "FOUNDATION_BASELINE_SUPERSESSION",
        "supersession_id": "FOUNDATION-SUPERSESSION-CANONICAL-1",
        "predecessor": {
            key: predecessor[key]
            for key in ("baseline_id", "baseline_version", "baseline_digest")
        },
        "successor": {
            key: current[key]
            for key in ("baseline_id", "baseline_version", "baseline_digest")
        },
        "reason": "Coverage authority changed under governed reconciliation.",
        "authority": _reference(ROOT, current["source_revision"], ADR_AUTHORITY_PATH),
        "recorded_at": "2026-08-16T18:00:00Z",
    }
    assert validate_transition(ROOT, predecessor, current, supersession) == []

    forged = copy.deepcopy(supersession)
    forged["authority"] = {
        "source_revision": current["source_revision"],
        "path": "does/not/exist.json",
        "sha256": "a" * 64,
    }
    assert "AUTHORITY_INVALID" in _codes(
        validate_transition(ROOT, predecessor, current, forged)
    )
    inconsistent = copy.deepcopy(current)
    inconsistent["coverage"] = list(reversed(inconsistent["coverage"]))
    assert {"COVERAGE_MISMATCH", "DIGEST_MISMATCH"} <= _codes(
        validate_baseline(ROOT, inconsistent)
    )
    ledger = AppendOnlyRecordLedger()
    ledger.append(current)
    replacement = copy.deepcopy(current)
    replacement["baseline_digest"] = "b" * 64
    try:
        ledger.append(replacement)
    except ValueError as error:
        assert "silent replacement" in str(error)
    else:
        raise AssertionError("immutable record replacement was accepted")


def _closure_fixture() -> tuple[
    Path,
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    repository = _fixture_directory("governed-evidence")
    _init_repository(repository)
    _write(repository, SCHEMA_PATH, (ROOT / SCHEMA_PATH).read_bytes())
    _write(
        repository,
        "docs/00-governance/DEFINITION_OF_DONE.md",
        (ROOT / "docs/00-governance/DEFINITION_OF_DONE.md").read_bytes(),
    )
    _write(repository, ADR_AUTHORITY_PATH, (ROOT / ADR_AUTHORITY_PATH).read_bytes())
    _write(
        repository,
        ".codex/policies/file-scopes.yaml",
        (ROOT / ".codex/policies/file-scopes.yaml")
        .read_bytes()
        .replace(b"role: Architect", b"role: Arquiteto"),
    )
    _install_authority(
        repository,
        role="QA",
        task_id="TASK-9001",
        issue_id="ISSUE-9001",
        story_id="STORY-9001",
        references=["STORY-0688"],
        allow_paths=["evidence/qa/qa-approval.json"],
    )
    _install_authority(
        repository,
        role="Reviewer",
        task_id="TASK-9002",
        issue_id="ISSUE-9002",
        story_id="STORY-9002",
        references=["G1 Foundation", "STORY-0688"],
        allow_paths=["evidence/reviews/**"],
    )
    _install_authority(
        repository,
        role="Product Owner",
        task_id="TASK-9003",
        issue_id="ISSUE-9003",
        story_id="STORY-9003",
        references=["REQ-SPRINT-001-010", "STORY-0688"],
        allow_paths=["docs/01-product/**"],
    )
    _commit(repository, "pre-existing closure authority control plane")
    _write(repository, "candidate/implementation.txt", b"foundation candidate\n")
    candidate = _commit(repository, "candidate implementation")
    main_branch = str(_git(repository, "branch", "--show-current")).strip()
    _git(repository, "checkout", "-q", "-b", "governed-review")
    _write(repository, "evidence/reviews/review-marker.txt", b"reviewed candidate\n")
    _commit(repository, "independent review")
    _git(repository, "checkout", "-q", main_branch)
    _write(repository, "evidence/merge-marker.txt", b"human merge\n")
    _commit(repository, "prepare human merge")
    _git(repository, "merge", "-q", "--no-ff", "governed-review", "-m", "merge reviewed candidate")
    merged = _revision(repository=repository)
    baseline = {
        "baseline_id": "FOUNDATION-BASELINE-CANONICAL",
        "baseline_version": "1.0.0",
        "baseline_digest": "a" * 64,
    }
    proof_names = (
        "IMPLEMENTATION_AND_MANDATORY_TESTS",
        "ARTIFACTS_AND_CONTRACTS_SYNCHRONIZED",
        "MIGRATIONS_AND_ROLLBACK_APPLICABILITY",
        "APPLICABLE_INVARIANTS",
        "ACCEPTANCE_CRITERIA",
        "QA_APPROVAL",
        "REVIEWER_APPROVAL",
        "DOCUMENTATION_AND_TRACEABILITY",
        "HUMAN_MERGE",
        "APPLICABLE_CTO_CONTROLS",
        "SPRINT_EVIDENCE_SET",
        "FOUNDATION_CHECKS",
        "NETWORK_AUTHENTICATION_APPLICABILITY",
        "SECURE_ROOTS",
        "DIAGNOSTIC_FLOW",
        "FIRST_SLICE_AUTHORIZATION",
        "G1_FOUNDATION_GATE_RESULT",
    )
    roles = {
        "QA_APPROVAL": "QA",
        "REVIEWER_APPROVAL": "Reviewer",
        "HUMAN_MERGE": "Autoridade Humana",
        "FIRST_SLICE_AUTHORIZATION": "Product Owner",
    }
    proof_paths: dict[str, str] = {}
    for proof_name in proof_names:
        payload: dict[str, Any] = {
            "record_type": "FOUNDATION_CLOSURE_PROOF",
            "proof_type": proof_name,
            "result": "PASS",
            "baseline": baseline,
            "reviewed_candidate_commit": candidate,
        }
        if proof_name == "HUMAN_MERGE":
            payload["merged_commit"] = merged
        if proof_name in roles:
            payload["authority_role"] = roles[proof_name]
        if proof_name == "QA_APPROVAL":
            payload.update(
                {
                    "task_id": "TASK-9001",
                    "issue_id": "ISSUE-9001",
                    "story_id": "STORY-9001",
                }
            )
        if proof_name == "G1_FOUNDATION_GATE_RESULT":
            payload.update(
                {
                    "authority_role": "Reviewer",
                    "task_id": "TASK-9002",
                    "issue_id": "ISSUE-9002",
                    "story_id": "STORY-9002",
                }
            )
        if proof_name == "FIRST_SLICE_AUTHORIZATION":
            payload.update(
                {
                    "task_id": "TASK-9003",
                    "issue_id": "ISSUE-9003",
                    "story_id": "STORY-9003",
                }
            )
        governed_role_paths = {
            "QA_APPROVAL": "evidence/qa/qa-approval.json",
            "REVIEWER_APPROVAL": "evidence/reviews/reviewer-approval.json",
            "FIRST_SLICE_AUTHORIZATION": (
                "docs/01-product/first-slice-authorization.json"
            ),
            "G1_FOUNDATION_GATE_RESULT": "evidence/reviews/g1-foundation.json",
        }
        path = governed_role_paths.get(
            proof_name, f"evidence/proofs/{proof_name.lower()}.json"
        )
        _write(repository, path, canonical_json_bytes(payload))
        if proof_name == "QA_APPROVAL":
            _write(
                repository,
                "evidence/qa/forged-qa-approval.json",
                canonical_json_bytes(payload),
            )
        proof_paths[proof_name] = path
    _write(repository, "evidence/proofs/arbitrary.json", b'{"result":"PASS"}')
    proof_revision = _commit(repository, "governed closure proofs")
    proofs = {
        name: {
            "result": "PASS",
            "artifact": _reference(repository, proof_revision, proof_paths[name]),
        }
        for name in proof_names
    }
    evidence_set = {
        "schema_version": "2.0.0",
        "record_type": "FOUNDATION_CLOSURE_EVIDENCE_SET",
        "evidence_set_id": "FOUNDATION-CLOSURE-EVIDENCE-CANONICAL-1",
        "baseline": baseline,
        "reviewed_candidate_commit": candidate,
        "merged_commit": merged,
        "proofs": proofs,
    }
    _write(repository, "evidence/closure-set.json", canonical_json_bytes(evidence_set))
    evidence_revision = _commit(repository, "governed closure evidence set")
    closure = {
        "schema_version": "2.0.0",
        "record_type": "FOUNDATION_CLOSURE",
        "closure_id": "FOUNDATION-CLOSURE-CANONICAL-1",
        "baseline": baseline,
        "evidence_set_id": evidence_set["evidence_set_id"],
        "evidence_set": _reference(
            repository, evidence_revision, "evidence/closure-set.json"
        ),
        "closure_authority": _reference(
            repository,
            evidence_revision,
            "docs/00-governance/DEFINITION_OF_DONE.md",
        ),
        "closed_at": "2026-08-16T18:30:00Z",
    }
    _write(
        repository,
        "evidence/foundation-closure.json",
        canonical_json_bytes(closure),
    )
    _commit(repository, "governed foundation closure")
    trigger = {
        "record_type": "FOUNDATION_REOPENING_TRIGGER",
        "kind": "COVERED_SOURCE_DIGEST_CHANGED",
        "prior_closure_id": closure["closure_id"],
        "prior_baseline": baseline,
        "new_candidate_id": "FOUNDATION-CANDIDATE-CANONICAL-2",
        "new_evidence_set_id": "FOUNDATION-CLOSURE-EVIDENCE-CANONICAL-2",
    }
    candidate_record = {
        "record_type": "FOUNDATION_REOPENING_CANDIDATE",
        "candidate_id": trigger["new_candidate_id"],
        "prior_closure_id": closure["closure_id"],
        "prior_baseline": baseline,
    }
    evidence_record = {
        "record_type": "FOUNDATION_REOPENING_EVIDENCE_SET",
        "evidence_set_id": trigger["new_evidence_set_id"],
        "candidate_id": trigger["new_candidate_id"],
        "status": "OPEN",
    }
    _write(
        repository,
        "evidence/reopening/new-candidate.json",
        canonical_json_bytes(candidate_record),
    )
    _write(
        repository,
        "evidence/reopening/new-evidence-set.json",
        canonical_json_bytes(evidence_record),
    )
    reopening_links_revision = _commit(repository, "governed reopening links")
    trigger["new_candidate"] = _reference(
        repository,
        reopening_links_revision,
        "evidence/reopening/new-candidate.json",
    )
    trigger["new_evidence_set"] = _reference(
        repository,
        reopening_links_revision,
        "evidence/reopening/new-evidence-set.json",
    )
    _write(repository, "evidence/prior-closure.json", canonical_json_bytes(closure))
    _write(repository, "evidence/material-trigger.json", canonical_json_bytes(trigger))
    reopening_revision = _commit(repository, "governed reopening evidence")
    reopening = {
        "schema_version": "2.0.0",
        "record_type": "FOUNDATION_REOPENING",
        "reopening_id": "FOUNDATION-REOPENING-CANONICAL-1",
        "prior_closure_id": closure["closure_id"],
        "prior_closure": _reference(
            repository, reopening_revision, "evidence/prior-closure.json"
        ),
        "prior_baseline": baseline,
        "material_trigger": {
            "kind": trigger["kind"],
            "evidence": _reference(
                repository, reopening_revision, "evidence/material-trigger.json"
            ),
        },
        "new_candidate_id": trigger["new_candidate_id"],
        "new_evidence_set_id": trigger["new_evidence_set_id"],
        "authority": _reference(repository, reopening_revision, ADR_AUTHORITY_PATH),
        "reopened_at": "2026-08-16T19:00:00Z",
    }
    return repository, baseline, evidence_set, closure, reopening


def test_foundation_closure_evidence_set_and_material_reopening_criteria() -> None:
    repository, baseline, evidence_set, closure, reopening = _closure_fixture()
    assert validate_evidence_set(repository, evidence_set, baseline) == []
    assert validate_closure(repository, closure, evidence_set, baseline) == []
    ledger = AppendOnlyRecordLedger()
    ledger.append(evidence_set)
    ledger.append(closure)
    assert validate_reopening(
        repository, reopening, closure, baseline, evidence_set, ledger
    ) == []

    incomplete = copy.deepcopy(evidence_set)
    incomplete["proofs"].pop("QA_APPROVAL")
    assert "SCHEMA_INVALID" in _codes(
        validate_evidence_set(repository, incomplete, baseline)
    )
    arbitrary = copy.deepcopy(evidence_set)
    arbitrary["proofs"]["QA_APPROVAL"]["artifact"] = _reference(
        repository,
        next(iter(evidence_set["proofs"].values()))["artifact"]["source_revision"],
        "evidence/proofs/arbitrary.json",
    )
    assert "EVIDENCE_INVALID" in _codes(
        validate_evidence_set(repository, arbitrary, baseline)
    )
    forged_role = copy.deepcopy(evidence_set)
    forged_role["proofs"]["QA_APPROVAL"]["artifact"] = _reference(
        repository,
        _revision(repository=repository),
        "evidence/qa/forged-qa-approval.json",
    )
    assert "EVIDENCE_AUTHORITY_INVALID" in _codes(
        validate_evidence_set(repository, forged_role, baseline)
    )
    forged_closure = copy.deepcopy(closure)
    forged_closure["closure_authority"] = arbitrary["proofs"]["QA_APPROVAL"][
        "artifact"
    ]
    assert "AUTHORITY_INVALID" in _codes(
        validate_closure(repository, forged_closure, evidence_set, baseline)
    )
    forged_reopening = copy.deepcopy(reopening)
    forged_reopening["authority"] = arbitrary["proofs"]["QA_APPROVAL"]["artifact"]
    assert "REOPENING_AUTHORITY_INVALID" in _codes(
        validate_reopening(
            repository, forged_reopening, closure, baseline, evidence_set, ledger
        )
    )
    wrong_trigger = copy.deepcopy(reopening)
    wrong_trigger["new_candidate_id"] = "FOUNDATION-CANDIDATE-FORGED"
    assert "MATERIAL_TRIGGER_INVALID" in _codes(
        validate_reopening(
            repository, wrong_trigger, closure, baseline, evidence_set, ledger
        )
    )
    mutated_evidence = copy.deepcopy(evidence_set)
    mutated_evidence["merged_commit"] = "e" * 40
    assert "HISTORY_NOT_PRESERVED" in _codes(
        validate_reopening(
            repository, reopening, closure, baseline, mutated_evidence, ledger
        )
    )


def test_adr_governance_overlap() -> None:
    path = (
        "docs/02-architecture/adrs/"
        "ADR-006-prompts-permanentes-taskenvelope-e-precedencia-de-instrucoes.md"
    )
    assert validate_adr_change_governance(
        ROOT,
        base_revision=BASE,
        candidate_revision=REJECTED,
        proposal_path=path,
        overlapping_adr_ids=(),
        superseded_adr_ids=(),
        declared_normative_owner="ADR-006",
    ) == []
    forged = validate_adr_change_governance(
        ROOT,
        base_revision=BASE,
        candidate_revision=REJECTED,
        proposal_path=path,
        overlapping_adr_ids=("ADR-999",),
        superseded_adr_ids=("ADR-999",),
        declared_normative_owner="CALLER-OWNER",
    )
    assert {
        "ADR_REFERENCE_UNKNOWN",
        "ADR_OVERLAP_UNRESOLVED",
        "SUPERSESSION_CLAIM_MISMATCH",
        "NORMATIVE_OWNER_INVALID",
    } <= _codes(forged)
    duplicate = validate_adr_change_governance(
        ROOT,
        base_revision=BASE,
        candidate_revision=REJECTED,
        proposal_path=path,
        overlapping_adr_ids=("ADR-006", "ADR-006"),
        superseded_adr_ids=(),
        declared_normative_owner="ADR-006",
    )
    assert "ADR_REFERENCE_DUPLICATE" in _codes(duplicate)

    repository, base, candidate, proposal = _adr_overlap_repository(
        "Durable dispatch state is stored authoritatively in PostgreSQL, "
        "while RabbitMQ only transports messages."
    )
    bypass = validate_adr_change_governance(
        repository,
        base_revision=base,
        candidate_revision=candidate,
        proposal_path=proposal,
        overlapping_adr_ids=(),
        superseded_adr_ids=(),
        declared_normative_owner="ADR-001",
    )
    assert "ADR_OVERLAP_UNRESOLVED" in _codes(bypass)

    repository, base, candidate, proposal = _adr_overlap_repository(
        "Browser color themes are selected per user preference."
    )
    unrelated = validate_adr_change_governance(
        repository,
        base_revision=base,
        candidate_revision=candidate,
        proposal_path=proposal,
        overlapping_adr_ids=(),
        superseded_adr_ids=(),
        declared_normative_owner="ADR-001",
    )
    assert "ADR_OVERLAP_UNRESOLVED" not in _codes(unrelated)


def _adr_overlap_repository(candidate_decision: str) -> tuple[Path, str, str, str]:
    repository = _fixture_directory("overlap-authority")
    _init_repository(repository)
    header = (
        b"adr_id,status,title,file,independent_boundary,bounded_contexts,"
        b"depends_on,owned_requirement_count\n"
    )
    rows = (
        b"ADR-001,Accepted,One,ADR-001-one.md,true,BC-001,,1\n"
        b"ADR-002,Accepted,Two,ADR-002-two.md,true,BC-001,,1\n"
    )
    _write(repository, "docs/00-governance/ADR_INDEX.csv", header + rows)
    first_path = "docs/02-architecture/adrs/ADR-001-one.md"
    second_path = "docs/02-architecture/adrs/ADR-002-two.md"
    _write(repository, first_path, _adr_fixture("ADR-001", "Unique boundary one."))
    _write(
        repository,
        second_path,
        _adr_fixture(
            "ADR-002",
            "PostgreSQL is authoritative for durable dispatch state; "
            "RabbitMQ is transport only.",
        ),
    )
    base = _commit(repository, "accepted ADR baseline")
    _write(
        repository,
        first_path,
        _adr_fixture("ADR-001", candidate_decision),
    )
    candidate = _commit(repository, "material overlapping ADR change")
    return repository, base, candidate, first_path


def _adr_fixture(identifier: str, decision: str) -> bytes:
    return f"""# {identifier}

- **Status:** `Accepted`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `{identifier}`
- **Boundary independente:** `SIM`
- **Substitui:** `Nenhuma`

## Decisão

- {decision}

## Rastreabilidade SAR

- **Requisitos owned:** `REQ-{identifier[-3:]}`
""".encode()


def _decision_repository() -> tuple[Path, str, str, str]:
    repository = _fixture_directory("decision-authority")
    _init_repository(repository)
    _write(
        repository,
        "docs/00-governance/ADR_INDEX.csv",
        b"adr_id,status,title,file,independent_boundary,bounded_contexts,depends_on,owned_requirement_count\n",
    )
    base = _commit(repository, "classification base")
    proposal_path = "docs/02-architecture/adrs/ADR-058-new-governed-boundary.md"
    adr = """# ADR-058 — New governed boundary

- **Status:** `Accepted`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-058`
- **Boundary independente:** `SIM`

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão.
""".encode()
    _write(repository, proposal_path, adr)
    row = (
        "ADR-058,Accepted,New governed boundary,ADR-058-new-governed-boundary.md,"
        "true,BC-001,,1\n"
    ).encode()
    _write(
        repository,
        "docs/00-governance/ADR_INDEX.csv",
        (
            b"adr_id,status,title,file,independent_boundary,bounded_contexts,depends_on,owned_requirement_count\n"
            + row
        ),
    )
    candidate = _commit(repository, "allocated ADR without prior classification record")
    return repository, base, candidate, proposal_path


def test_req_gov_dec_001() -> None:
    assert DECISION_CLASSIFICATIONS == {
        "NEW_ADR",
        "REFINE_EXISTING",
        "APPLICATION_PROFILE",
        "BENCHMARK_PROFILE",
        "ISSUE_DETAIL",
    }
    existing = (
        "docs/02-architecture/adrs/"
        "ADR-006-prompts-permanentes-taskenvelope-e-precedencia-de-instrucoes.md"
    )
    assert validate_classification_before_identifier(
        ROOT,
        base_revision=BASE,
        candidate_revision=REJECTED,
        proposal_path=existing,
        declared_classification="REFINE_EXISTING",
        allocated_identifier="ADR-006",
    ) == []
    repository, base, candidate, proposal = _decision_repository()
    early = validate_classification_before_identifier(
        repository,
        base_revision=base,
        candidate_revision=candidate,
        proposal_path=proposal,
        declared_classification="NEW_ADR",
        allocated_identifier="ADR-058",
    )
    assert _codes(early) == {"IDENTIFIER_ALLOCATED_EARLY"}
    forged = validate_classification_before_identifier(
        ROOT,
        base_revision=BASE,
        candidate_revision=REJECTED,
        proposal_path=existing,
        declared_classification="NEW_ADR",
        allocated_identifier="ADR-999",
    )
    assert {"CLASSIFICATION_MISMATCH", "IDENTIFIER_MISMATCH"} <= _codes(forged)


def test_req_gov_dec_002() -> None:
    existing = (
        "docs/02-architecture/adrs/"
        "ADR-006-prompts-permanentes-taskenvelope-e-precedencia-de-instrucoes.md"
    )
    artificial = validate_new_adr_eligibility(
        ROOT,
        base_revision=BASE,
        candidate_revision=REJECTED,
        proposal_path=existing,
        declared_classification="NEW_ADR",
    )
    assert {"CLASSIFICATION_MISMATCH", "ARTIFICIAL_ADR_PROMOTION"} <= _codes(
        artificial
    )
    repository, base, candidate, proposal = _decision_repository()
    governed = validate_new_adr_eligibility(
        repository,
        base_revision=base,
        candidate_revision=candidate,
        proposal_path=proposal,
        declared_classification="NEW_ADR",
    )
    assert "NEW_ADR_INELIGIBLE" not in _codes(governed)
    assert "IDENTIFIER_ALLOCATED_EARLY" in _codes(governed)
    assert "OWNER_GATE_REQUIRED" in _codes(
        validate_adr_change_governance(
            repository,
            base_revision=base,
            candidate_revision=candidate,
            proposal_path=proposal,
            overlapping_adr_ids=(),
            superseded_adr_ids=(),
            declared_normative_owner="ADR-058",
        )
    )


def _portfolio_repository() -> tuple[Path, dict[str, dict[str, str]]]:
    repository = _fixture_directory("portfolio-authority")
    _init_repository(repository)
    _write(
        repository,
        ".codex/policies/file-scopes.yaml",
        (ROOT / ".codex/policies/file-scopes.yaml")
        .read_bytes()
        .replace(b"role: Architect", b"role: Arquiteto"),
    )
    owner_task = {
        "task_id": "TASK-9002",
        "issue_id": "ISSUE-9002",
        "story_id": "STORY-9002",
        "role": "Product Owner",
        "references": [
            "docs/01-product/requirements/REQ-ISM-010-governed-deltas.md"
        ],
        "allow_paths": ["docs/01-product/portfolio-delta-approval.json"],
        "deny_paths": [],
        "dependencies": [],
    }
    _write(
        repository,
        ".codex/tasks/TASK-9002.json",
        canonical_json_bytes(owner_task),
    )
    _write(repository, "README.md", b"governed portfolio fixture\n")
    _commit(repository, "portfolio base")
    previous = {"ITEM-1": {"value": "old"}, "ITEM-2": {"value": "removed"}}
    current = {"ITEM-1": {"value": "new"}}
    delta = {
        "record_type": "PORTFOLIO_DELTA",
        "delta_id": "DELTA-1",
        "changes": [
            {"item_id": "ITEM-1", "before": previous["ITEM-1"], "after": current["ITEM-1"]},
            {"item_id": "ITEM-2", "before": previous["ITEM-2"], "after": None},
        ],
    }
    approval = {
        "record_type": "PORTFOLIO_DELTA_APPROVAL",
        "delta_id": "DELTA-1",
        "delta_sha256": hashlib.sha256(canonical_json_bytes(delta)).hexdigest(),
        "status": "APPROVED",
        "authority_role": "Product Owner",
        "task_id": "TASK-9002",
        "issue_id": "ISSUE-9002",
        "story_id": "STORY-9002",
    }
    tombstone = {
        "record_type": "PORTFOLIO_TOMBSTONE",
        "item_id": "ITEM-2",
        "delta_id": "DELTA-1",
        "prior_item_sha256": hashlib.sha256(
            canonical_json_bytes(previous["ITEM-2"])
        ).hexdigest(),
    }
    active_tombstone = {
        "record_type": "PORTFOLIO_TOMBSTONE",
        "item_id": "ITEM-1",
        "delta_id": "DELTA-1",
        "prior_item_sha256": hashlib.sha256(
            canonical_json_bytes(previous["ITEM-1"])
        ).hexdigest(),
    }
    fake_approval = dict(approval)
    forged_approval = dict(approval)
    records = {
        "delta": delta,
        "approval": approval,
        "tombstone": tombstone,
        "active-tombstone": active_tombstone,
        "fake-approval": fake_approval,
        "forged-approval": forged_approval,
    }
    paths = {
        "delta": "records/delta.json",
        "approval": "docs/01-product/portfolio-delta-approval.json",
        "tombstone": "records/tombstone.json",
        "active-tombstone": "records/active-tombstone.json",
        "fake-approval": "records/fake-approval.json",
        "forged-approval": "docs/01-product/forged-portfolio-approval.json",
    }
    for name, record in records.items():
        _write(repository, paths[name], canonical_json_bytes(record))
    revision = _commit(repository, "governed portfolio transition")
    refs = {
        name: _reference(repository, revision, paths[name])
        for name in records
    }
    return repository, refs


def test_portfolio_snapshot_tombstone_approved_delta() -> None:
    repository, refs = _portfolio_repository()
    previous = {"ITEM-1": {"value": "old"}, "ITEM-2": {"value": "removed"}}
    current = {"ITEM-1": {"value": "new"}}
    snapshots = (("SNAPSHOT-1", previous), ("SNAPSHOT-2", current))
    assert validate_snapshot_tombstone_delta_history(
        repository,
        snapshots,
        previous_items=previous,
        current_items=current,
        tombstone_references=(refs["tombstone"],),
        delta_references=(refs["delta"],),
        approval_references=(refs["approval"],),
    ) == []
    unexplained = validate_snapshot_tombstone_delta_history(
        repository,
        snapshots,
        previous_items=previous,
        current_items=current,
        tombstone_references=(),
        delta_references=(),
        approval_references=(),
    )
    assert {"DELTA_TRANSITION_MISMATCH", "TOMBSTONE_REQUIRED"} <= _codes(
        unexplained
    )
    active = validate_snapshot_tombstone_delta_history(
        repository,
        snapshots,
        previous_items=previous,
        current_items=current,
        tombstone_references=(refs["active-tombstone"],),
        delta_references=(refs["delta"], refs["delta"]),
        approval_references=(refs["fake-approval"],),
    )
    assert {
        "TOMBSTONE_INVALID",
        "TOMBSTONE_REQUIRED",
        "DELTA_DUPLICATE",
        "DELTA_APPROVAL_INVALID",
    } <= _codes(active)
    forged_owner = validate_snapshot_tombstone_delta_history(
        repository,
        snapshots,
        previous_items=previous,
        current_items=current,
        tombstone_references=(refs["tombstone"],),
        delta_references=(refs["delta"],),
        approval_references=(refs["forged-approval"],),
    )
    assert "DELTA_APPROVAL_INVALID" in _codes(forged_owner)
    mutated_snapshots = (("SNAPSHOT-1", previous), ("SNAPSHOT-1", current))
    assert "SNAPSHOT_MUTATED" in _codes(
        validate_snapshot_tombstone_delta_history(
            repository,
            mutated_snapshots,
            previous_items=previous,
            current_items=current,
            tombstone_references=(refs["tombstone"],),
            delta_references=(refs["delta"],),
            approval_references=(refs["approval"],),
        )
    )
    mismatched_snapshots = (("SNAPSHOT-1", current), ("SNAPSHOT-2", previous))
    assert "SNAPSHOT_HISTORY_INVALID" in _codes(
        validate_snapshot_tombstone_delta_history(
            repository,
            mismatched_snapshots,
            previous_items=previous,
            current_items=current,
            tombstone_references=(refs["tombstone"],),
            delta_references=(refs["delta"],),
            approval_references=(refs["approval"],),
        )
    )


def test_sprint_zero_baseline_decision_01() -> None:
    expected = minimum_sprint_scope(ROOT)
    assert len(expected) == 7
    assert expected[-1] == "SprintEvidenceSet machine-readable"
    assert validate_minimum_sprint_scope(ROOT, expected) == []
    assert _codes(validate_minimum_sprint_scope(ROOT, expected[:-1])) == {
        "SPRINT_MINIMUM_SCOPE_MISMATCH"
    }


def test_sprint_zero_baseline_decision_02() -> None:
    expected = derive_canonical_sprint_selection(ROOT)
    assert len(expected) == 93
    assert "STORY-0688" in expected
    assert "STORY-0760" in expected
    assert expected == derive_canonical_sprint_selection(ROOT)
    assert validate_graph_derived_selection(ROOT, expected) == []
    arbitrary = validate_graph_derived_selection(ROOT, ("STORY-0001", "STORY-0688"))
    assert _codes(arbitrary) == {"SPRINT_SELECTION_NON_CANONICAL"}


def test_taskenvelope_control_plane_scope() -> None:
    assert validate_effective_task_scope(
        ROOT,
        base_revision=BASE,
        authority_checkpoint=CHECKPOINT,
        candidate_revision=REJECTED,
        task_envelope_path=TASK_PATH,
    ) == []
    unauthorized = validate_effective_task_scope(
        ROOT,
        base_revision=BASE,
        authority_checkpoint=BASE,
        candidate_revision=REJECTED,
        task_envelope_path=TASK_PATH,
    )
    assert "TASK_CONTROL_PLANE_UNAUTHORIZED" in _codes(unauthorized)


def _recompute_evidence_digest(record: dict[str, Any]) -> None:
    record["evidence_set_digest"] = "0" * 64
    record["evidence_set_digest"] = hashlib.sha256(
        canonical_json_bytes(record)
    ).hexdigest()


def _sprint_evidence_fixture() -> tuple[
    Path,
    dict[str, Any],
    SprintEvidenceLedger,
    dict[str, Any],
    str,
]:
    repository = _fixture_directory("sprint-evidence")
    _init_repository(repository)
    source_revision, artifacts, tests = _sprint_evidence_inputs(repository)
    evidence_set = build_sprint_evidence_set(
        repository,
        schema_version="1.0.0",
        evidence_set_id="SPRINT-001-EVIDENCE-CANONICAL",
        sprint_id="SPRINT-001",
        source_revision=source_revision,
        artifacts=artifacts,
        requirements=REQUIRED_REQUIREMENTS,
        tests=tests,
        decisions=REQUIRED_DECISIONS,
        digest_algorithm="SHA-256",
    )
    ledger = SprintEvidenceLedger()
    ledger.append(evidence_set)
    evidence_path = "evidence/sprint-evidence-set.json"
    _write(repository, evidence_path, canonical_json_bytes(evidence_set))
    evidence_revision = _commit(repository, "immutable sprint evidence")
    closure = {
        "record_type": "SPRINT_CLOSURE",
        "closure_id": "SPRINT-001-CLOSURE-CANONICAL",
        "sprint_id": "SPRINT-001",
        "closure_basis": "EVIDENCE",
        "evidence_set": _reference(repository, evidence_revision, evidence_path),
        **_authority_payload(
            role="QA",
            task_id="TASK-9901",
            issue_id="ISSUE-9901",
            story_id="STORY-9901",
            candidate=evidence_revision,
        ),
    }
    closure_path = "evidence/qa/sprint-closure.json"
    _write(repository, closure_path, canonical_json_bytes(closure))
    closure_revision = _commit(repository, "governed sprint closure")
    return (
        repository,
        evidence_set,
        ledger,
        _reference(repository, closure_revision, closure_path),
        evidence_revision,
    )


def _install_authority(
    repository: Path,
    *,
    role: str,
    task_id: str,
    issue_id: str,
    story_id: str,
    references: list[str],
    allow_paths: list[str],
) -> None:
    _write(
        repository,
        ".codex/policies/file-scopes.yaml",
        (ROOT / ".codex/policies/file-scopes.yaml")
        .read_bytes()
        .replace(b"role: Architect", b"role: Arquiteto"),
    )
    task = json.loads((ROOT / ".codex/tasks/TASK-0689.json").read_text(encoding="utf-8"))
    task.update(
        {
            "task_id": task_id,
            "issue_id": issue_id,
            "story_id": story_id,
            "role": role,
            "references": references,
            "allow_paths": allow_paths,
            "deny_paths": [],
            "dependencies": references,
        }
    )
    task["phase_f_review"]["files"] = {
        "status": "PASS",
        "allow_paths": allow_paths,
        "deny_paths": [],
    }
    _write(
        repository,
        f".codex/tasks/{task_id}.json",
        canonical_json_bytes(task),
    )


def _authority_payload(
    *,
    role: str,
    task_id: str,
    issue_id: str,
    story_id: str,
    candidate: str,
) -> dict[str, str]:
    return {
        "authority_role": role,
        "task_id": task_id,
        "issue_id": issue_id,
        "story_id": story_id,
        "reviewed_candidate_commit": candidate,
    }


def _govern_record(
    repository: Path,
    record: dict[str, Any],
    *,
    path: str,
    record_type: str,
    digest_field: str,
    authority: dict[str, str],
) -> dict[str, str]:
    projection = {key: value for key, value in record.items() if key != "authority"}
    payload = {
        "record_type": record_type,
        digest_field: hashlib.sha256(canonical_json_bytes(projection)).hexdigest(),
        **authority,
    }
    _write(repository, path, canonical_json_bytes(payload))
    revision = _commit(repository, f"governed {record_type}")
    return _reference(repository, revision, path)


def _sprint_evidence_inputs(
    repository: Path,
) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    qa_identity = {
        "role": "QA",
        "task_id": "TASK-9901",
        "issue_id": "ISSUE-9901",
        "story_id": "STORY-9901",
    }
    devops_identity = {
        "role": "DevOps",
        "task_id": "TASK-9900",
        "issue_id": "ISSUE-9900",
        "story_id": "STORY-9900",
    }
    _install_authority(
        repository,
        **qa_identity,
        references=[
            "STORY-0689",
            "REQ-SPRINT-001-009",
            "REQ-TOOL-001",
        ],
        allow_paths=["evidence/qa/**"],
    )
    _install_authority(
        repository,
        **devops_identity,
        references=["STORY-0689", "REQ-TOOL-001"],
        allow_paths=["evidence/operations/**"],
    )
    _commit(repository, "pre-existing execution and QA control plane")
    validator_root = (
        "tools/governance/governanca-de-decisoes-arquiteturais-e-"
        "manutencao-da-b/sprint-001-tool-parte-2"
    )
    validator_by_kind = {
        "AP008_DECISION_03_WAVE": "sprint_graph.py",
        "AP008_DECISION_05_CONTRACTS": "sprint_decisions.py",
        "AP008_DECISION_06_DIAGNOSTIC": "sprint_decisions.py",
        "AP008_DECISION_07_CI": "sprint_decisions.py",
        "AP008_DECISION_08_EVIDENCE_SET": "sprint_evidence.py",
        "AP008_DECISION_09_CLOSURE_EXTENSION": "sprint_decisions.py",
        "AP008_DECISION_10_CUTOVER": "sprint_decisions.py",
        "REQ_TOOL_MAKE_CI_PARITY": "toolchain_validation.py",
        "REQ_TOOL_PYTHON_RUNTIME": "toolchain_validation.py",
        "REQ_TOOL_UV_LOCK_FROZEN": "toolchain_validation.py",
    }
    for validator in sorted(set(validator_by_kind.values())):
        _write(repository, f"{validator_root}/{validator}", b"# governed validator\n")
    _write(repository, "evidence/subjects/repository-state.json", b'{"governed":true}\n')
    candidate = _commit(repository, "reviewed validator candidate")
    subject = _reference(
        repository, candidate, "evidence/subjects/repository-state.json"
    )
    validation_report_paths: dict[str, str] = {}
    for index, kind in enumerate(REQUIRED_EVIDENCE_KINDS):
        path = f"evidence/operations/reports/validation-{index:02d}.txt"
        _write(repository, path, f"{kind}: PASS\n".encode())
        validation_report_paths[kind] = path
    for index, test_id in enumerate(REQUIRED_TESTS):
        _write(
            repository,
            f"evidence/operations/reports/test-{index:02d}.txt",
            f"{test_id}: PASS\n".encode(),
        )
    report_revision = _commit(repository, "independent QA execution reports")
    authority = _authority_payload(candidate=candidate, **qa_identity)
    execution_authority = _authority_payload(
        candidate=candidate, **devops_identity
    )
    artifact_paths: list[tuple[str, str]] = []
    for index, kind in enumerate(REQUIRED_EVIDENCE_KINDS):
        path = f"evidence/qa/validation/{index:02d}.json"
        payload = {
            "record_type": "SPRINT_VALIDATION_EVIDENCE",
            "evidence_type": kind,
            "subject": subject,
            "validator": _reference(
                repository,
                candidate,
                f"{validator_root}/{validator_by_kind[kind]}",
            ),
            "finding_codes": [],
            "execution_report": _reference(
                repository, report_revision, validation_report_paths[kind]
            ),
            "execution_authority": execution_authority,
            **authority,
        }
        _write(repository, path, canonical_json_bytes(payload))
        artifact_paths.append((kind, path))
    test_paths: list[tuple[str, str]] = []
    for index, test_id in enumerate(REQUIRED_TESTS):
        path = f"evidence/qa/tests/{index:02d}.json"
        payload = {
            "record_type": "SPRINT_TEST_EVIDENCE",
            "test_id": test_id,
            "report": _reference(
                repository,
                report_revision,
                f"evidence/operations/reports/test-{index:02d}.txt",
            ),
            "execution_authority": execution_authority,
            **authority,
        }
        _write(repository, path, canonical_json_bytes(payload))
        test_paths.append((test_id, path))
    source_revision = _commit(repository, "governed sprint validation inputs")
    artifacts = [
        {"kind": kind, **_reference(repository, source_revision, path)}
        for kind, path in artifact_paths
    ]
    tests = [
        {
            "test_id": test_id,
            "result": "PASS",
            "artifact": _reference(repository, source_revision, path),
        }
        for test_id, path in test_paths
    ]
    return source_revision, artifacts, tests


def _build_sprint_evidence_at(
    repository: Path,
    source_revision: str,
    artifacts: list[dict[str, Any]],
    tests: list[dict[str, Any]],
) -> dict[str, Any]:
    return build_sprint_evidence_set(
        repository,
        schema_version="1.0.0",
        evidence_set_id="SPRINT-001-EVIDENCE-CANONICAL",
        sprint_id="SPRINT-001",
        source_revision=source_revision,
        artifacts=artifacts,
        requirements=REQUIRED_REQUIREMENTS,
        tests=tests,
        decisions=REQUIRED_DECISIONS,
        digest_algorithm="SHA-256",
    )


def _canonical_graph() -> tuple[str, dict[str, Any], tuple[str, str]]:
    revision = _revision()
    graph = json.loads(
        _git(
            ROOT,
            "show",
            f"{revision}:docs/06-delivery/STORY_DEPENDENCY_GRAPH.json",
        )
    )
    selected = set(derive_canonical_sprint_selection(ROOT))
    edge = next(
        (item["from"], item["to"])
        for item in graph["edges"]
        if item["from"] in selected and item["to"] in selected
    )
    return revision, graph, edge


def _governed_graph_fixture() -> tuple[
    Path, str, dict[str, str], dict[str, str], dict[str, str]
]:
    repository = _fixture_directory("governed-wave")
    _init_repository(repository)
    authorities = (
        ("QA", "TASK-9902", "ISSUE-9902", "STORY-9902", ["STORY-9001", "STORY-9002"], ["evidence/qa/**"]),
        ("Reviewer", "TASK-9903", "ISSUE-9903", "STORY-9903", ["STORY-9001"], ["evidence/reviews/**"]),
        ("Product Owner", "TASK-9904", "ISSUE-9904", "STORY-9904", ["REQ-SPRINT-001-009"], ["docs/01-product/**"]),
        ("Tech Lead", "TASK-9905", "ISSUE-9905", "STORY-9905", ["REQ-SPRINT-001-003"], ["docs/06-delivery/**"]),
    )
    for role, task_id, issue_id, story_id, references, allow_paths in authorities:
        _install_authority(
            repository,
            role=role,
            task_id=task_id,
            issue_id=issue_id,
            story_id=story_id,
            references=references,
            allow_paths=allow_paths,
        )
    _commit(repository, "pre-existing wave authority control plane")
    graph_path = "docs/06-delivery/STORY_DEPENDENCY_GRAPH.json"
    graph = {
        "semantics": "Only hard blockers; edge from prerequisite to dependent.",
        "nodes": [
            {"id": "STORY-9001", "task_id": "TASK-9001"},
            {"id": "STORY-9002", "task_id": "TASK-9002"},
        ],
        "edges": [
            {"from": "STORY-9001", "to": "STORY-9002", "relation": "blocks"}
        ],
    }
    _write(repository, graph_path, canonical_json_bytes(graph))
    _write(
        repository,
        "docs/03-engineering/application-profiles/AP-008-sprint-001-execution-profile.md",
        b"# AP-008 \xe2\x80\x94 SPRINT-001 execution profile\n",
    )
    _write(
        repository,
        "docs/06-delivery/sprint-backlogs/SPRINT-001-BACKLOG.md",
        b"- **Sprint:** `SPRINT-001`\n\n| `STORY-9002` | selected |\n",
    )
    for suffix in ("1", "2"):
        task = {
            "task_id": f"TASK-900{suffix}",
            "story_id": f"STORY-900{suffix}",
            "sprint_id": "SPRINT-001",
            "requirements_review_status": "PASS",
            "phase_f_review": {
                "dependencies": {"status": "PASS"},
                "review": {"required_roles": ["QA", "Reviewer"]},
            },
            "phase_g_review": {"status": "PASS"},
        }
        _write(
            repository,
            f".codex/tasks/TASK-900{suffix}.json",
            canonical_json_bytes(task),
        )
    candidate = _commit(repository, "candidate with canonical graph")
    assurance_paths: list[str] = []
    for index, role in enumerate(("QA", "Reviewer")):
        identity = authorities[index]
        prefix = "qa" if role == "QA" else "reviews"
        path = f"evidence/{prefix}/{index:02d}-{role.lower()}.json"
        _write(
            repository,
            path,
            canonical_json_bytes(
                {
                    "record_type": "CANDIDATE_ASSURANCE_EVIDENCE",
                    "authority_role": role,
                    "task_id": identity[1],
                    "issue_id": identity[2],
                    "story_id": identity[3],
                    "reviewed_story_id": "STORY-9001",
                    "reviewed_candidate_commit": candidate,
                    "result": "PASS",
                }
            ),
        )
        assurance_paths.append(path)
    assurance_revision = _commit(repository, "governed candidate assurances")
    completion_path = "evidence/completions/STORY-9001.json"
    completion = {
        "record_type": "STORY_COMPLETION_EVIDENCE",
        "story_id": "STORY-9001",
        "task_id": "TASK-9001",
        "state": "COMPLETED",
        "candidate_revision": candidate,
        "assurance_evidence": [
            _reference(repository, assurance_revision, path)
            for path in assurance_paths
        ],
    }
    _write(repository, completion_path, canonical_json_bytes(completion))
    completion_revision = _commit(repository, "governed story completion")
    observation_path = "evidence/qa/STORY-9002-observation.json"
    observation = {
        "record_type": "BLOCKER_OBSERVATION_EVIDENCE",
        "blocked_story_id": "STORY-9002",
        "blocker_story_id": "STORY-9001",
        "observed_revision": completion_revision,
        "status": "ACTIVE",
        **_authority_payload(
            role="QA",
            task_id="TASK-9902",
            issue_id="ISSUE-9902",
            story_id="STORY-9902",
            candidate=completion_revision,
        ),
    }
    _write(repository, observation_path, canonical_json_bytes(observation))
    observation_revision = _commit(repository, "governed blocker observation")
    blocker_path = "evidence/blockers/STORY-9002.json"
    blocker = {
        "record_type": "SPRINT_BLOCKER_EVIDENCE",
        "blocked_story_id": "STORY-9002",
        "blocker_story_id": "STORY-9001",
        "state": "ACTIVE",
        "reason": "The direct predecessor remains blocked at the observed revision.",
        "observed_revision": completion_revision,
        "observation": _reference(
            repository, observation_revision, observation_path
        ),
    }
    _write(repository, blocker_path, canonical_json_bytes(blocker))
    blocker_revision = _commit(repository, "governed direct blocker")
    return (
        repository,
        completion_revision,
        _reference(repository, completion_revision, completion_path),
        _reference(repository, completion_revision, graph_path),
        _reference(repository, blocker_revision, blocker_path),
    )


def test_daa_operational_trust_boundary() -> None:
    assert inspect.signature(daa_adapter.DeliveryApprovalGate).parameters == {}
    forbidden = {
        "repository",
        "revision",
        "verifier",
        "trust_profile",
        "trust_anchors",
        "anchors",
    }
    assert forbidden.isdisjoint(
        inspect.signature(daa_adapter.verify_delivery_approval).parameters
    )
    task = json.loads((ROOT / ".codex/tasks/TASK-0689.json").read_text(encoding="utf-8"))
    verdict = daa_adapter.verify_delivery_approval(
        task_envelope=task,
        expected_candidate_sha=_revision(repository=ROOT),
        verification_time="2026-08-22T12:30:00Z",
        evidence={
            "bindings": [],
            "attestations": [],
            "trust_profile": daa_test_profile(_DAA_TEST_KEYS),
            "trust_anchors": copy.deepcopy(_DAA_TEST_ANCHORS),
        },
    )
    assert verdict["status"] == "FAIL"
    assert verdict["validated_roles"] == []
    source = inspect.getsource(daa_adapter)
    assert "test_delivery_approval_authority_contract" not in source
    assert "test-vectors" not in source


def test_sprint_zero_baseline_decision_03() -> None:
    repository, revision, completion, _graph, _blocker = _governed_graph_fixture()
    wave = {
        "wave_id": "SPRINT-001-WAVE-CANONICAL",
        "graph_revision": revision,
        "story_ids": ["STORY-9002"],
        "completion_evidence": [completion],
        "evidence_oriented": True,
    }
    wave["authority"] = _govern_record(
        repository,
        wave,
        path="docs/06-delivery/waves/wave-9002.json",
        record_type="SPRINT_WAVE_AUTHORIZATION",
        digest_field="wave_sha256",
        authority=_authority_payload(
            role="Tech Lead",
            task_id="TASK-9905",
            issue_id="ISSUE-9905",
            story_id="STORY-9905",
            candidate=revision,
        ),
    )
    assert validate_wave(repository, wave) == []
    incompatible = copy.deepcopy(wave)
    incompatible["completion_evidence"] = []
    assert "WAVE_GRAPH_MISMATCH" in _codes(
        validate_wave(repository, incompatible)
    )
    oversized = dict(wave)
    oversized["story_ids"] = ["STORY-9001", "STORY-9002"]
    oversized["completion_evidence"] = []
    assert {"WAVE_GRAPH_MISMATCH", "WAVE_NOT_SMALL"} <= _codes(
        validate_wave(repository, oversized)
    )
    autodeclared = dict(wave)
    autodeclared.pop("completion_evidence")
    autodeclared["completed_story_ids"] = ["STORY-9001"]
    assert {"FIELD_MISSING", "FIELD_UNKNOWN"} <= _codes(
        validate_wave(repository, autodeclared)
    )
    completion_payload = json.loads(
        _git(
            repository,
            "show",
            f"{completion['source_revision']}:{completion['path']}",
        )
    )
    completion_payload["assurance_evidence"] = [
        completion_payload["assurance_evidence"][0],
        completion_payload["assurance_evidence"][0],
    ]
    forged_path = "evidence/completions/STORY-9001-forged.json"
    _write(repository, forged_path, canonical_json_bytes(completion_payload))
    forged_revision = _commit(repository, "single-actor assurance probe")
    forged_wave = dict(wave)
    forged_wave["completion_evidence"] = [
        _reference(repository, forged_revision, forged_path)
    ]
    forged_wave["authority"] = _govern_record(
        repository,
        forged_wave,
        path="docs/06-delivery/waves/forged-wave.json",
        record_type="SPRINT_WAVE_AUTHORIZATION",
        digest_field="wave_sha256",
        authority=_authority_payload(
            role="Tech Lead",
            task_id="TASK-9905",
            issue_id="ISSUE-9905",
            story_id="STORY-9905",
            candidate=revision,
        ),
    )
    assert "EVIDENCE_AUTHORITY_INVALID" in _codes(
        validate_wave(repository, forged_wave)
    )
    authority_payload = json.loads(
        _git(
            repository,
            "show",
            f"{wave['authority']['source_revision']}:{wave['authority']['path']}",
        )
    )
    daa_path = (
        "evidence/delivery-approval-authority/TASK-9905/"
        f"{revision}.json"
    )
    forged_daa = json.loads(_git(repository, "show", f"HEAD:{daa_path}"))
    executor_subject = next(
        item["accountable_subject"]
        for item in forged_daa["bindings"]
        if item["role"] == "Executor"
    )
    qa_binding = next(
        item for item in forged_daa["bindings"] if item["role"] == "QA"
    )
    qa_binding["accountable_subject"] = executor_subject
    daa_test_sign(qa_binding, _DAA_TEST_KEYS["binding"], DAA_BINDING_DOMAIN)
    qa_attestation = next(
        item for item in forged_daa["attestations"] if item["role"] == "QA"
    )
    qa_attestation["accountable_subject"] = executor_subject
    qa_attestation["binding"]["digest_sha256"] = hashlib.sha256(
        canonical_json_bytes(qa_binding)
    ).hexdigest()
    daa_test_sign(
        qa_attestation,
        _DAA_TEST_KEYS["qa"],
        DAA_ATTESTATION_DOMAIN,
    )
    single_actor_authority_path = "docs/06-delivery/waves/single-actor.json"
    _write(repository, daa_path, canonical_json_bytes(forged_daa))
    _write(
        repository,
        single_actor_authority_path,
        canonical_json_bytes(authority_payload),
    )
    _git(repository, "add", ".")
    _git(repository, "commit", "-q", "-m", "single accountable subject DAA probe")
    single_actor_revision = _revision(repository=repository)
    single_actor_wave = dict(wave)
    single_actor_wave["authority"] = _reference(
        repository, single_actor_revision, single_actor_authority_path
    )
    assert "DELIVERY_APPROVAL_INVALID" in _codes(
        validate_wave(repository, single_actor_wave)
    )

    class CallerVerifier:
        def verify(self, **_kwargs: Any) -> tuple[object, list[object]]:
            return object(), []

    assert "DELIVERY_APPROVAL_INVALID" in _codes(
        validate_wave(repository, wave, delivery_gate=CallerVerifier())
    )


def test_sprint_zero_baseline_decision_05() -> None:
    repository = _fixture_directory("essential-contract")
    _init_repository(repository)
    _install_authority(
        repository,
        role="Arquiteto",
        task_id="TASK-9910",
        issue_id="ISSUE-9910",
        story_id="STORY-9910",
        references=["REQ-SPRINT-001-005"],
        allow_paths=["contracts/**"],
    )
    _install_authority(
        repository,
        role="QA",
        task_id="TASK-9911",
        issue_id="ISSUE-9911",
        story_id="STORY-9911",
        references=["REQ-SPRINT-001-005"],
        allow_paths=["evidence/qa/**"],
    )
    _install_authority(
        repository,
        role="DevOps",
        task_id="TASK-9912",
        issue_id="ISSUE-9912",
        story_id="STORY-9912",
        references=["REQ-SPRINT-001-005"],
        allow_paths=["evidence/operations/**"],
    )
    _commit(repository, "pre-existing contract authorities")
    _write(repository, "contracts/essential.json", b'{"schema_version":"1.0.0"}')
    contract_revision = _commit(repository, "essential contract")
    contract = _reference(
        repository, contract_revision, "contracts/essential.json"
    )
    manifest_path = "contracts/governance/essential-contracts.json"
    manifest = {
        "record_type": "ESSENTIAL_CONTRACT_MANIFEST",
        "contracts": [contract],
        **_authority_payload(
            role="Arquiteto",
            task_id="TASK-9910",
            issue_id="ISSUE-9910",
            story_id="STORY-9910",
            candidate=contract_revision,
        ),
    }
    _write(repository, manifest_path, canonical_json_bytes(manifest))
    manifest_revision = _commit(repository, "governed essential contract manifest")
    manifest_reference = _reference(repository, manifest_revision, manifest_path)
    report_path = "evidence/operations/reports/contract-exercise.txt"
    _write(repository, report_path, f"{contract['sha256']}: PASS\n".encode())
    report_revision = _commit(repository, "independent contract execution report")
    exercise_record = {
        "record_type": "CONTRACT_EXERCISE_EVIDENCE",
        "contract_sha256": contract["sha256"],
        "result": "PASS",
        "execution_report": _reference(repository, report_revision, report_path),
        "execution_authority": _authority_payload(
            role="DevOps",
            task_id="TASK-9912",
            issue_id="ISSUE-9912",
            story_id="STORY-9912",
            candidate=contract_revision,
        ),
        **_authority_payload(
            role="QA",
            task_id="TASK-9911",
            issue_id="ISSUE-9911",
            story_id="STORY-9911",
            candidate=contract_revision,
        ),
    }
    _write(
        repository,
        "evidence/qa/contract-exercise.json",
        canonical_json_bytes(exercise_record),
    )
    evidence_revision = _commit(repository, "contract exercise evidence")
    evidence = _reference(
        repository, evidence_revision, "evidence/qa/contract-exercise.json"
    )
    exercises = [{"contract": contract, "evidence": evidence}]
    assert validate_contract_exercises(repository, manifest_reference, exercises) == []
    assert "CONTRACT_EXERCISE_MISMATCH" in _codes(
        validate_contract_exercises(repository, manifest_reference, [])
    )
    forged = copy.deepcopy(exercises)
    forged[0]["contract"]["sha256"] = "a" * 64
    assert {
        "CONTRACT_EVIDENCE_INVALID",
        "GOVERNED_ARTIFACT_INVALID",
    } <= _codes(validate_contract_exercises(repository, manifest_reference, forged))


def test_sprint_zero_baseline_decision_06() -> None:
    repository = _fixture_directory("diagnostic-evidence")
    _init_repository(repository)
    _install_authority(
        repository,
        role="QA",
        task_id="TASK-9920",
        issue_id="ISSUE-9920",
        story_id="STORY-9920",
        references=["REQ-SPRINT-001-006"],
        allow_paths=["evidence/qa/**"],
    )
    _install_authority(
        repository,
        role="DevOps",
        task_id="TASK-9921",
        issue_id="ISSUE-9921",
        story_id="STORY-9921",
        references=["REQ-SPRINT-001-006"],
        allow_paths=["evidence/operations/**"],
    )
    _commit(repository, "pre-existing diagnostic QA authority")
    _write(repository, "diagnostic/candidate.txt", b"synthetic diagnostic candidate\n")
    candidate = _commit(repository, "diagnostic candidate")
    report_path = "evidence/operations/reports/diagnostic.txt"
    _write(repository, report_path, b"REQ-SPRINT-001-006: PASS\n")
    report_revision = _commit(repository, "independent diagnostic execution report")
    diagnostic = {
        "record_type": "SYNTHETIC_DIAGNOSTIC_EVIDENCE",
        "synthetic": True,
        "end_to_end": True,
        "functional_georeferencing_claimed": False,
        "result": "PASS",
        "execution_report": _reference(repository, report_revision, report_path),
        "execution_authority": _authority_payload(
            role="DevOps",
            task_id="TASK-9921",
            issue_id="ISSUE-9921",
            story_id="STORY-9921",
            candidate=candidate,
        ),
        **_authority_payload(
            role="QA",
            task_id="TASK-9920",
            issue_id="ISSUE-9920",
            story_id="STORY-9920",
            candidate=candidate,
        ),
    }
    _write(
        repository,
        "evidence/qa/diagnostic.json",
        canonical_json_bytes(diagnostic),
    )
    revision = _commit(repository, "governed diagnostic evidence")
    reference = _reference(repository, revision, "evidence/qa/diagnostic.json")
    assert validate_diagnostic_claim(repository, reference) == []
    dishonest = dict(diagnostic)
    dishonest["functional_georeferencing_claimed"] = True
    _write(
        repository,
        "evidence/qa/dishonest-diagnostic.json",
        canonical_json_bytes(dishonest),
    )
    dishonest_revision = _commit(repository, "dishonest diagnostic claim")
    dishonest_reference = _reference(
        repository,
        dishonest_revision,
        "evidence/qa/dishonest-diagnostic.json",
    )
    assert "FUNCTIONAL_GEOREFERENCE_CLAIMED" in _codes(
        validate_diagnostic_claim(repository, dishonest_reference)
    )


def test_sprint_zero_baseline_decision_07() -> None:
    repository = _fixture_directory("repository-bound-capabilities")
    _init_repository(repository)
    _write(repository, "src/contracts/schema.py", b"SCHEMA_VERSION = '1.0.0'\n")
    _write(repository, "tests/contracts/test_schema.py", b"def test_schema(): assert True\n")
    _write(repository, "Makefile", b"verify:\n\tpytest\n")
    _write(
        repository,
        ".github/workflows/ci.yml",
        b"jobs:\n  quality:\n    steps:\n      - run: make verify\n",
    )
    revision = _commit(repository, "repository-bound capability")
    assert validate_ci_capabilities(repository, revision) == []
    _write(
        repository,
        "evidence/caller-capabilities.json",
        b'{"capabilities":["fictitious"]}\n',
    )
    assertion_revision = _commit(repository, "caller capability assertion probe")
    assert validate_ci_capabilities(repository, assertion_revision) == []
    _write(repository, "src/runtime/engine.py", b"PRESENT = True\n")
    divergent_revision = _commit(repository, "capability without governed tests")
    assert "CI_CAPABILITY_MISMATCH" in _codes(
        validate_ci_capabilities(repository, divergent_revision)
    )
    _write(repository, "tests/runtime/test_engine.py", b"def test_fake(): assert True\n")
    _write(repository, "Makefile", b"verify:\n\t@echo verified\n")
    fake_surface_revision = _commit(
        repository, "fictitious capability and empty Make target probe"
    )
    assert "MAKE_TARGET_NOT_SUBSTANTIVE" in _codes(
        validate_ci_capabilities(repository, fake_surface_revision)
    )


def test_sprint_zero_baseline_decision_08() -> None:
    repository, evidence_set, ledger, _closure, evidence_revision = (
        _sprint_evidence_fixture()
    )
    assert validate_sprint_evidence_set(repository, evidence_set) == []
    assert "10 passing tests" in sprint_evidence_human_summary(evidence_set)
    assert ledger.contains_exactly(evidence_set)

    incomplete = copy.deepcopy(evidence_set)
    incomplete["tests"] = []
    _recompute_evidence_digest(incomplete)
    assert "EVIDENCE_INCOMPLETE" in _codes(
        validate_sprint_evidence_set(repository, incomplete)
    )
    mutated = copy.deepcopy(evidence_set)
    mutated["decisions"] = list(reversed(mutated["decisions"]))
    _recompute_evidence_digest(mutated)
    try:
        ledger.append(mutated)
    except ValueError as error:
        assert "silent replacement" in str(error)
    else:
        raise AssertionError("mutable SprintEvidenceSet was accepted")

    forged = copy.deepcopy(evidence_set)
    forged["artifacts"][0]["sha256"] = "a" * 64
    _recompute_evidence_digest(forged)
    assert "GOVERNED_ARTIFACT_INVALID" in _codes(
        validate_sprint_evidence_set(repository, forged)
    )
    arbitrary = copy.deepcopy(evidence_set)
    arbitrary["artifacts"][0].update(arbitrary["tests"][0]["artifact"])
    _recompute_evidence_digest(arbitrary)
    assert "EVIDENCE_PAYLOAD_INVALID" in _codes(
        validate_sprint_evidence_set(repository, arbitrary)
    )
    original_artifact = evidence_set["artifacts"][0]
    fabricated_payload = json.loads(
        _git(
            repository,
            "show",
            f"{original_artifact['source_revision']}:{original_artifact['path']}",
        )
    )
    fabricated_payload.update(
        {"task_id": "TASK-CALLER", "issue_id": "ISSUE-CALLER", "story_id": "STORY-CALLER"}
    )
    fabricated_path = "evidence/qa/validation/fabricated.json"
    _write(
        repository,
        fabricated_path,
        canonical_json_bytes(fabricated_payload),
    )
    fabricated_revision = _commit(repository, "self-declared pass probe")
    fabricated = copy.deepcopy(evidence_set)
    fabricated["source_revision"] = fabricated_revision
    fabricated["artifacts"][0].update(
        _reference(repository, fabricated_revision, fabricated_path)
    )
    _recompute_evidence_digest(fabricated)
    assert "DELIVERY_APPROVAL_INVALID" in _codes(
        validate_sprint_evidence_set(repository, fabricated)
    )
    single_actor_payload = json.loads(
        _git(
            repository,
            "show",
            f"{original_artifact['source_revision']}:{original_artifact['path']}",
        )
    )
    single_actor_payload["execution_authority"] = {
        field: single_actor_payload[field]
        for field in (
            "authority_role",
            "task_id",
            "issue_id",
            "story_id",
            "reviewed_candidate_commit",
        )
    }
    single_actor_path = "evidence/qa/validation/single-actor.json"
    _write(
        repository,
        single_actor_path,
        canonical_json_bytes(single_actor_payload),
    )
    single_actor_revision = _commit(repository, "single-actor execution probe")
    single_actor = copy.deepcopy(evidence_set)
    single_actor["source_revision"] = single_actor_revision
    single_actor["artifacts"][0].update(
        _reference(repository, single_actor_revision, single_actor_path)
    )
    _recompute_evidence_digest(single_actor)
    assert "EVIDENCE_AUTHORITY_INVALID" in _codes(
        validate_sprint_evidence_set(repository, single_actor)
    )
    divergent = copy.deepcopy(evidence_set)
    divergent["artifacts"] = [
        {
            "kind": "sprint-evidence",
            **_reference(
                repository,
                evidence_revision,
                "evidence/sprint-evidence-set.json",
            ),
        }
    ]
    _recompute_evidence_digest(divergent)
    assert "EVIDENCE_REVISION_DIVERGENT" in _codes(
        validate_sprint_evidence_set(repository, divergent)
    )


def test_sprint_zero_baseline_decision_09() -> None:
    repository, evidence_set, _ledger, closure_reference, _revision_value = (
        _sprint_evidence_fixture()
    )
    assert validate_sprint_closure(repository, closure_reference) == []
    closure = json.loads(
        _git(
            repository,
            "show",
            f"{closure_reference['source_revision']}:{closure_reference['path']}",
        )
    )
    rebuilt_evidence_path = "evidence/qa/rebuilt-sprint-evidence.json"
    _write(
        repository,
        rebuilt_evidence_path,
        canonical_json_bytes(evidence_set),
    )
    rebuilt_evidence_revision = _commit(
        repository, "artificial evidence history reconstruction probe"
    )
    rebuilt_closure = copy.deepcopy(closure)
    rebuilt_closure["closure_id"] = "SPRINT-001-CLOSURE-REBUILT"
    rebuilt_closure["evidence_set"] = _reference(
        repository, rebuilt_evidence_revision, rebuilt_evidence_path
    )
    rebuilt_closure.update(
        _authority_payload(
            role="QA",
            task_id="TASK-9901",
            issue_id="ISSUE-9901",
            story_id="STORY-9901",
            candidate=rebuilt_evidence_revision,
        )
    )
    rebuilt_closure_path = "evidence/qa/rebuilt-sprint-closure.json"
    _write(
        repository,
        rebuilt_closure_path,
        canonical_json_bytes(rebuilt_closure),
    )
    rebuilt_closure_revision = _commit(
        repository, "artificial closure history reconstruction probe"
    )
    assert "EVIDENCE_HISTORY_INVALID" in _codes(
        validate_sprint_closure(
            repository,
            _reference(
                repository, rebuilt_closure_revision, rebuilt_closure_path
            ),
        )
    )
    calendar = dict(closure)
    calendar["closure_basis"] = "CALENDAR"
    calendar_path = "evidence/calendar-closure.json"
    _write(repository, calendar_path, canonical_json_bytes(calendar))
    calendar_revision = _commit(repository, "calendar closure probe")
    assert "CLOSURE_NOT_EVIDENCE_BASED" in _codes(
        validate_sprint_closure(
            repository, _reference(repository, calendar_revision, calendar_path)
        )
    )

    mutated = copy.deepcopy(evidence_set)
    mutated["decisions"] = list(reversed(mutated["decisions"]))
    _recompute_evidence_digest(mutated)
    _write(
        repository,
        "evidence/sprint-evidence-set.json",
        canonical_json_bytes(mutated),
    )
    mutated_revision = _commit(repository, "mutated historical evidence probe")
    mutated_closure = dict(closure)
    mutated_closure["evidence_set"] = _reference(
        repository, mutated_revision, "evidence/sprint-evidence-set.json"
    )
    mutated_closure_path = "evidence/mutated-closure.json"
    _write(repository, mutated_closure_path, canonical_json_bytes(mutated_closure))
    mutated_closure_revision = _commit(repository, "closure over recreated ledger")
    assert "EVIDENCE_HISTORY_INVALID" in _codes(
        validate_sprint_closure(
            repository,
            _reference(
                repository, mutated_closure_revision, mutated_closure_path
            ),
        )
    )

    graph_repository, graph_revision, _completion, graph, blocker = (
        _governed_graph_fixture()
    )
    extension = {
        "record_type": "SPRINT_EXTENSION",
        "extension_id": "SPRINT-001-EXTENSION-CANONICAL",
        "sprint_id": "SPRINT-001",
        "blocker_evidence": blocker,
        "graph": graph,
    }
    extension["authority"] = _govern_record(
        graph_repository,
        extension,
        path="docs/01-product/sprint-extensions/extension-9002.json",
        record_type="SPRINT_EXTENSION_AUTHORIZATION",
        digest_field="extension_sha256",
        authority=_authority_payload(
            role="Product Owner",
            task_id="TASK-9904",
            issue_id="ISSUE-9904",
            story_id="STORY-9904",
            candidate=blocker["source_revision"],
        ),
    )
    assert validate_sprint_extension(graph_repository, extension) == []
    autodeclared = {
        "record_type": "SPRINT_EXTENSION",
        "extension_id": "SPRINT-001-EXTENSION-AUTODECLARED",
        "sprint_id": "SPRINT-001",
        "blocker": {"reason": "caller text"},
        "evidence": graph,
    }
    assert {"FIELD_MISSING", "FIELD_UNKNOWN"} <= _codes(
        validate_sprint_extension(graph_repository, autodeclared)
    )


def test_sprint_zero_baseline_decision_10() -> None:
    repository, baseline, foundation_evidence, foundation_closure, _reopening = (
        _closure_fixture()
    )
    foundation_closure_revision = str(
        _git(
            repository,
            "log",
            "-1",
            "--format=%H",
            "--",
            "evidence/foundation-closure.json",
        )
    ).strip()
    foundation_reference = _reference(
        repository,
        foundation_closure_revision,
        "evidence/foundation-closure.json",
    )
    source_revision, artifacts, tests = _sprint_evidence_inputs(repository)
    evidence_set = _build_sprint_evidence_at(
        repository, source_revision, artifacts, tests
    )
    evidence_path = "evidence/cutover/sprint-evidence-set.json"
    _write(repository, evidence_path, canonical_json_bytes(evidence_set))
    evidence_revision = _commit(repository, "governed cutover sprint evidence")
    evidence_reference = _reference(
        repository, evidence_revision, evidence_path
    )
    closure = {
        "record_type": "SPRINT_CLOSURE",
        "closure_id": "SPRINT-001-CUTOVER-CLOSURE",
        "sprint_id": "SPRINT-001",
        "closure_basis": "EVIDENCE",
        "evidence_set": evidence_reference,
        **_authority_payload(
            role="QA",
            task_id="TASK-9901",
            issue_id="ISSUE-9901",
            story_id="STORY-9901",
            candidate=evidence_revision,
        ),
    }
    closure_path = "evidence/qa/cutover/sprint-closure.json"
    _write(repository, closure_path, canonical_json_bytes(closure))
    closure_revision = _commit(repository, "governed cutover closure")
    closure_reference = _reference(repository, closure_revision, closure_path)
    assert validate_cutover_preconditions(
        repository,
        closure_reference,
        foundation_reference,
        baseline,
    ) == []
    no_g1 = copy.deepcopy(foundation_evidence)
    no_g1["proofs"].pop("G1_FOUNDATION_GATE_RESULT")
    no_g1_path = "evidence/closure-set-no-g1.json"
    _write(repository, no_g1_path, canonical_json_bytes(no_g1))
    no_g1_revision = _commit(repository, "foundation evidence without G1 probe")
    no_g1_closure = copy.deepcopy(foundation_closure)
    no_g1_closure["evidence_set"] = _reference(
        repository, no_g1_revision, no_g1_path
    )
    no_g1_closure_path = "evidence/foundation-closure-no-g1.json"
    _write(repository, no_g1_closure_path, canonical_json_bytes(no_g1_closure))
    no_g1_closure_revision = _commit(repository, "foundation closure without G1 probe")
    no_g1_codes = _codes(
        validate_cutover_preconditions(
            repository,
            closure_reference,
            _reference(
                repository, no_g1_closure_revision, no_g1_closure_path
            ),
            baseline,
        )
    )
    assert {
        "CUTOVER_FOUNDATION_EVIDENCE_INVALID",
        "CUTOVER_G1_NOT_APPROVED",
    } <= no_g1_codes
    no_authorization = copy.deepcopy(foundation_evidence)
    no_authorization["proofs"].pop("FIRST_SLICE_AUTHORIZATION")
    no_authorization_path = "evidence/closure-set-no-authorization.json"
    _write(repository, no_authorization_path, canonical_json_bytes(no_authorization))
    no_authorization_revision = _commit(
        repository, "foundation evidence without authorization probe"
    )
    no_authorization_closure = copy.deepcopy(foundation_closure)
    no_authorization_closure["evidence_set"] = _reference(
        repository, no_authorization_revision, no_authorization_path
    )
    no_authorization_closure_path = (
        "evidence/foundation-closure-no-authorization.json"
    )
    _write(
        repository,
        no_authorization_closure_path,
        canonical_json_bytes(no_authorization_closure),
    )
    no_authorization_closure_revision = _commit(
        repository, "foundation closure without authorization probe"
    )
    no_authorization_codes = _codes(
        validate_cutover_preconditions(
            repository,
            closure_reference,
            _reference(
                repository,
                no_authorization_closure_revision,
                no_authorization_closure_path,
            ),
            baseline,
        )
    )
    assert {
        "CUTOVER_FOUNDATION_EVIDENCE_INVALID",
        "CUTOVER_NOT_AUTHORIZED",
    } <= no_authorization_codes


def _runtime_gate_results(
    repository: Path, revision: str, version: str
) -> list[dict[str, Any]]:
    return [
        {
            "gate": gate,
            "result": "PASS",
            "artifact": _reference(
                repository,
                revision,
                f"evidence/qa/runtime/gates/{version}-{index:02d}.json",
            ),
        }
        for index, gate in enumerate(sorted(RUNTIME_GATES))
    ]


def test_python_312_primary_and_upgrade_gates() -> None:
    repository = _fixture_directory("repository-bound-runtime")
    _init_repository(repository)
    runtime_authorities = (
        ("QA", "TASK-9930", "ISSUE-9930", "STORY-9930", ["evidence/qa/**"]),
        ("DevOps", "TASK-9931", "ISSUE-9931", "STORY-9931", ["evidence/operations/**"]),
        ("Arquiteto", "TASK-9932", "ISSUE-9932", "STORY-9932", ["contracts/**"]),
        ("Reviewer", "TASK-9933", "ISSUE-9933", "STORY-9933", ["evidence/reviews/**"]),
    )
    for role, task_id, issue_id, story_id, allow_paths in runtime_authorities:
        _install_authority(
            repository,
            role=role,
            task_id=task_id,
            issue_id=issue_id,
            story_id=story_id,
            references=["REQ-TOOL-001"],
            allow_paths=allow_paths,
        )
    _commit(repository, "pre-existing runtime authorities")
    _write(repository, ".python-version", b"3.12.13\n")
    _write(
        repository,
        "pyproject.toml",
        b'[project]\nname="fixture"\nversion="0.0.0"\n'
        b'requires-python=">=3.12,<3.13"\n'
        b'[tool.ruff]\ntarget-version="py312"\n'
        b'[tool.mypy]\npython_version="3.12"\n',
    )
    baseline_revision = _commit(repository, "Python 3.12 repository baseline")
    assert validate_python_runtime(repository, baseline_revision) == []
    _write(repository, "evidence/caller-runtime.json", b'{"runtime":"3.14"}\n')
    assertion_revision = _commit(repository, "caller runtime assertion probe")
    assert validate_python_runtime(repository, assertion_revision) == []
    report_paths: dict[tuple[str, str], str] = {}
    for version in ("3.13", "3.14"):
        for index, gate in enumerate(sorted(RUNTIME_GATES)):
            report_path = (
                f"evidence/operations/runtime/reports/{version}-{index:02d}.txt"
            )
            _write(
                repository,
                report_path,
                f"{version}:{gate}: PASS\n".encode(),
            )
            report_paths[(version, gate)] = report_path
    approval_paths: dict[tuple[str, str], str] = {}
    for version in ("3.13", "3.14"):
        for role in ("Arquiteto", "Reviewer"):
            identity = next(item for item in runtime_authorities if item[0] == role)
            prefix = "contracts/runtime" if role == "Arquiteto" else "evidence/reviews"
            path = f"{prefix}/python-{version}-{role.lower()}-approval.json"
            approval_paths[(version, role)] = path
            _write(
                repository,
                path,
                canonical_json_bytes(
                    {
                        "record_type": "PYTHON_RUNTIME_GATE_APPROVAL",
                        "version": version,
                        "gate": "ARCHITECT_AND_REVIEWER_APPROVAL",
                        "result": "PASS",
                        **_authority_payload(
                            role=role,
                            task_id=identity[1],
                            issue_id=identity[2],
                            story_id=identity[3],
                            candidate=baseline_revision,
                        ),
                    }
                ),
            )
    proof_revision = _commit(repository, "independent runtime reports and approvals")
    for version in ("3.13", "3.14"):
        for index, gate in enumerate(sorted(RUNTIME_GATES)):
            approvals: list[dict[str, str]] = []
            if gate == "ARCHITECT_AND_REVIEWER_APPROVAL":
                approvals = [
                    _reference(repository, proof_revision, approval_paths[(version, role)])
                    for role in ("Arquiteto", "Reviewer")
                ]
            _write(
                repository,
                f"evidence/qa/runtime/gates/{version}-{index:02d}.json",
                canonical_json_bytes(
                    {
                        "record_type": "PYTHON_RUNTIME_GATE_EVIDENCE",
                        "version": version,
                        "gate": gate,
                        "result": "PASS",
                        "approvals": approvals,
                        "execution_report": _reference(
                            repository,
                            proof_revision,
                            report_paths[(version, gate)],
                        ),
                        "execution_authority": _authority_payload(
                            role="DevOps",
                            task_id="TASK-9931",
                            issue_id="ISSUE-9931",
                            story_id="STORY-9931",
                            candidate=baseline_revision,
                        ),
                        **_authority_payload(
                            role="QA",
                            task_id="TASK-9930",
                            issue_id="ISSUE-9930",
                            story_id="STORY-9930",
                            candidate=baseline_revision,
                        ),
                    }
                ),
            )
    gate_revision = _commit(repository, "governed runtime gate evidence")
    lane_313 = {
        "record_type": "PYTHON_RUNTIME_LANE_EVIDENCE",
        "version": "3.13",
        "state": "STABLE",
        "stable": True,
        "gates": _runtime_gate_results(repository, gate_revision, "3.13"),
        **_authority_payload(
            role="DevOps",
            task_id="TASK-9931",
            issue_id="ISSUE-9931",
            story_id="STORY-9931",
            candidate=baseline_revision,
        ),
    }
    lane_314 = {
        "record_type": "PYTHON_RUNTIME_LANE_EVIDENCE",
        "version": "3.14",
        "state": "PROMOTED",
        "stable": False,
        "gates": _runtime_gate_results(repository, gate_revision, "3.14"),
        **_authority_payload(
            role="DevOps",
            task_id="TASK-9931",
            issue_id="ISSUE-9931",
            story_id="STORY-9931",
            candidate=baseline_revision,
        ),
    }
    _write(
        repository,
        "evidence/operations/runtime/python-3.13.json",
        canonical_json_bytes(lane_313),
    )
    _write(
        repository,
        "evidence/operations/runtime/python-3.14.json",
        canonical_json_bytes(lane_314),
    )
    promoted_revision = _commit(repository, "governed promoted runtime lanes")
    assert validate_python_runtime(repository, promoted_revision) == []
    forged_gate = next(
        item for item in lane_313["gates"]
        if item["gate"] != "ARCHITECT_AND_REVIEWER_APPROVAL"
    )
    forged_payload = json.loads(
        _git(
            repository,
            "show",
            f"{forged_gate['artifact']['source_revision']}:{forged_gate['artifact']['path']}",
        )
    )
    forged_payload.update(
        {"task_id": "TASK-CALLER", "issue_id": "ISSUE-CALLER", "story_id": "STORY-CALLER"}
    )
    forged_gate_path = "evidence/qa/runtime/gates/caller-pass.json"
    _write(repository, forged_gate_path, canonical_json_bytes(forged_payload))
    forged_gate_revision = _commit(repository, "caller runtime PASS probe")
    forged_lane = copy.deepcopy(lane_313)
    gate_index = next(
        index for index, item in enumerate(forged_lane["gates"])
        if item["gate"] == forged_gate["gate"]
    )
    forged_lane["gates"][gate_index]["artifact"] = _reference(
        repository, forged_gate_revision, forged_gate_path
    )
    _write(
        repository,
        "evidence/operations/runtime/python-3.13.json",
        canonical_json_bytes(forged_lane),
    )
    forged_lane_revision = _commit(repository, "unauthorized runtime lane probe")
    assert "DELIVERY_APPROVAL_INVALID" in _codes(
        validate_python_runtime(repository, forged_lane_revision)
    )
    incomplete = copy.deepcopy(lane_313)
    incomplete["gates"] = incomplete["gates"][:-1]
    _write(
        repository,
        "evidence/operations/runtime/python-3.13.json",
        canonical_json_bytes(incomplete),
    )
    incomplete_revision = _commit(repository, "incomplete runtime gate probe")
    assert "PYTHON_RUNTIME_GATE_INCOMPLETE" in _codes(
        validate_python_runtime(repository, incomplete_revision)
    )
    premature = copy.deepcopy(lane_313)
    premature["state"] = "PROMOTED"
    premature["stable"] = False
    _write(
        repository,
        "evidence/operations/runtime/python-3.13.json",
        canonical_json_bytes(premature),
    )
    premature_revision = _commit(repository, "premature 3.14 probe")
    assert "PYTHON_314_PRECONDITION_MISSING" in _codes(
        validate_python_runtime(repository, premature_revision)
    )


def test_uv_lock_frozen() -> None:
    repository = _fixture_directory("uv-workspace")
    _init_repository(repository)
    _write(
        repository,
        "pyproject.toml",
        b'[project]\nname="fixture"\nversion="0.0.0"\n'
        b'[tool.uv.workspace]\nmembers=["packages/*"]\n',
    )
    _write(
        repository,
        "packages/member/pyproject.toml",
        b'[project]\nname="member"\nversion="0.1.0"\n',
    )
    lock_content = (
        b"version = 1\nrevision = 1\n"
        b'[[package]]\nname = "fixture"\nversion = "0.0.0"\n'
        b'source = { virtual = "." }\n'
        b'[[package]]\nname = "member"\nversion = "0.1.0"\n'
        b'source = { virtual = "packages/member" }\n'
    )
    _write(repository, "uv.lock", lock_content)
    _write(repository, "Makefile", b"sync:\n\tuv sync --frozen\n")
    _write(
        repository,
        ".github/workflows/ci.yml",
        b"jobs:\n  sync:\n    steps:\n      - run: make sync\n",
    )
    frozen_revision = _commit(repository, "repository-bound frozen uv baseline")
    assert validate_uv_lock_baseline(repository, frozen_revision) == []
    _write(
        repository,
        "evidence/caller-lock-declaration.json",
        b'{"lock_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}\n',
    )
    assertion_revision = _commit(repository, "caller lock declaration probe")
    assert validate_uv_lock_baseline(repository, assertion_revision) == []
    _write(
        repository,
        "packages/member/pyproject.toml",
        b'[project]\nname="member"\nversion="0.2.0"\n',
    )
    divergent_revision = _commit(repository, "divergent workspace lock probe")
    assert "UV_LOCK_DIVERGENT" in _codes(
        validate_uv_lock_baseline(repository, divergent_revision)
    )
    _write(
        repository,
        "packages/member/pyproject.toml",
        b'[project]\nname="member"\nversion="0.1.0"\n',
    )
    _commit(repository, "restore governed workspace manifest")
    _write(repository, "Makefile", b"sync:\n\tuv sync\n")
    not_frozen_revision = _commit(repository, "non-frozen uv probe")
    assert "UV_NOT_FROZEN" in _codes(
        validate_uv_lock_baseline(repository, not_frozen_revision)
    )
    _write(repository, "Makefile", b"sync:\n\tuv sync --frozen --upgrade\n")
    implicit_revision = _commit(repository, "implicit lock update probe")
    assert "UV_IMPLICIT_LOCK_UPDATE" in _codes(
        validate_uv_lock_baseline(repository, implicit_revision)
    )
    _write(
        repository,
        "Makefile",
        b"sync:\n\tuv sync --frozen \\\n\t  --upgrade\n",
    )
    multiline_update_revision = _commit(
        repository, "multiline implicit lock update probe"
    )
    assert "UV_IMPLICIT_LOCK_UPDATE" in _codes(
        validate_uv_lock_baseline(repository, multiline_update_revision)
    )
    _write(repository, "Makefile", b"sync:\n\t# uv sync --frozen\n")
    comment_only_revision = _commit(repository, "comment-only uv probe")
    assert "UV_SYNC_COMMAND_INVALID" in _codes(
        validate_uv_lock_baseline(repository, comment_only_revision)
    )
    _git(repository, "rm", "-q", "uv.lock")
    missing_revision = _commit(repository, "missing lock probe")
    assert "UV_LOCK_MISSING" in _codes(
        validate_uv_lock_baseline(repository, missing_revision)
    )


def test_make_ci_parity() -> None:
    repository = _fixture_directory("make-ci-parity")
    _init_repository(repository)
    _write(repository, "Makefile", b"test:\n\tpytest\nverify:\n\tpython tools/validate_repository.py\n")
    _write(
        repository,
        ".github/workflows/ci.yml",
        b"jobs:\n  quality:\n    steps:\n      - run: make test\n      - run: make verify\n",
    )
    revision = _commit(repository, "repository-bound Make and CI")
    assert validate_make_ci_parity(repository, revision) == []
    _write(
        repository,
        ".github/workflows/ci.yml",
        b"jobs:\n  quality:\n    steps:\n      - run: pytest\n      - run: make verify\n",
    )
    direct_revision = _commit(repository, "direct pytest bypass probe")
    codes = _codes(validate_make_ci_parity(repository, direct_revision))
    assert "MAKE_CI_BYPASS" in codes
    _write(
        repository,
        ".github/workflows/ci.yml",
        b"jobs:\n  quality:\n    steps:\n      - run: make test\n"
        b"      - run: echo prep && pytest\n      - run: make verify\n",
    )
    chained_revision = _commit(repository, "chained pytest bypass probe")
    assert "MAKE_CI_BYPASS" in _codes(
        validate_make_ci_parity(repository, chained_revision)
    )
    _write(
        repository,
        ".github/workflows/ci.yml",
        b"jobs:\n  quality:\n    steps:\n      - run: make test\n"
        b"      - run: |\n          echo prep && pytest\n"
        b"      - run: make verify\n",
    )
    multiline_revision = _commit(repository, "multiline pytest bypass probe")
    assert "MAKE_CI_BYPASS" in _codes(
        validate_make_ci_parity(repository, multiline_revision)
    )
    _write(
        repository,
        ".github/workflows/ci.yml",
        b"jobs:\n  quality:\n    steps:\n      - run: make test\n"
        b"      - run: bash -c \"pytest\"\n      - run: make verify\n",
    )
    nested_shell_revision = _commit(repository, "nested shell bypass probe")
    assert "MAKE_CI_BYPASS" in _codes(
        validate_make_ci_parity(repository, nested_shell_revision)
    )
    _write(
        repository,
        ".github/workflows/ci.yml",
        b"jobs:\n  quality:\n    steps:\n      - run: make verify\n"
        b"      - uses: ./.github/actions/hidden-quality\n",
    )
    _write(
        repository,
        ".github/actions/hidden-quality/action.yml",
        b"name: hidden quality\nruns:\n  using: composite\n  steps:\n"
        b"    - run: pytest\n      shell: bash\n",
    )
    local_action_revision = _commit(repository, "local action bypass probe")
    assert "MAKE_CI_BYPASS" in _codes(
        validate_make_ci_parity(repository, local_action_revision)
    )
    _write(
        repository,
        ".github/workflows/ci.yml",
        b"jobs:\n  quality:\n    steps:\n      - run: make test\n      - run: make verify\n",
    )
    _write(
        repository,
        ".github/workflows/omitted.yml",
        b"jobs:\n  hidden:\n    steps:\n      - run: pytest\n",
    )
    omitted_revision = _commit(repository, "omitted workflow inventory probe")
    assert "MAKE_CI_BYPASS" in _codes(
        validate_make_ci_parity(repository, omitted_revision)
    )
    _write(repository, "Makefile", b"verify:\n\t@echo verified\n")
    _write(
        repository,
        ".github/workflows/ci.yml",
        b"jobs:\n  quality:\n    steps:\n      - run: make verify\n",
    )
    empty_target_revision = _commit(repository, "empty Make target probe")
    assert "MAKE_TARGET_NOT_SUBSTANTIVE" in _codes(
        validate_make_ci_parity(repository, empty_target_revision)
    )
