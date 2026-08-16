from __future__ import annotations

import copy
import hashlib
import itertools
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = ROOT / (
    "tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/"
    "frz-gov-adr-gov-dec-parte-1"
)
sys.path.insert(0, str(MODULE_ROOT))

from baseline_lifecycle import (  # noqa: E402
    AppendOnlyRecordLedger,
    build_baseline,
    validate_baseline,
    validate_closure,
    validate_evidence_set,
    validate_reopening,
    validate_transition,
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
    _git(repository, "add", ".")
    _git(repository, "commit", "-q", "-m", message)
    return _revision(repository=repository)


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
        (ROOT / ".codex/policies/file-scopes.yaml").read_bytes(),
    )
    qa_task = {
        "task_id": "TASK-9001",
        "issue_id": "ISSUE-9001",
        "story_id": "STORY-9001",
        "role": "QA",
        "references": [
            "docs/06-delivery/stories/STORY-0688-governed-foundation.md"
        ],
        "allow_paths": ["evidence/qa/qa-approval.json"],
        "deny_paths": [],
        "dependencies": ["STORY-0688"],
    }
    _write(
        repository,
        ".codex/tasks/TASK-9001.json",
        canonical_json_bytes(qa_task),
    )
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
        governed_role_paths = {
            "QA_APPROVAL": "evidence/qa/qa-approval.json",
            "REVIEWER_APPROVAL": "evidence/reviews/reviewer-approval.json",
            "FIRST_SLICE_AUTHORIZATION": (
                "docs/01-product/first-slice-authorization.json"
            ),
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

    repository, base, candidate, proposal = _overlapping_adr_repository()
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


def _overlapping_adr_repository() -> tuple[Path, str, str, str]:
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
        _adr_fixture("ADR-002", "Shared durable boundary decision."),
    )
    base = _commit(repository, "accepted ADR baseline")
    _write(
        repository,
        first_path,
        _adr_fixture("ADR-001", "Shared durable boundary decision."),
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
        (ROOT / ".codex/policies/file-scopes.yaml").read_bytes(),
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
    assert len(expected) == 92
    assert "STORY-0688" in expected
    assert expected == derive_canonical_sprint_selection(ROOT)
    assert validate_graph_derived_selection(ROOT, expected) == []
    arbitrary = validate_graph_derived_selection(ROOT, ("STORY-0001", "STORY-0688"))
    assert _codes(arbitrary) == {"SPRINT_SELECTION_NON_CANONICAL"}


def test_taskenvelope_control_plane_scope() -> None:
    assert validate_effective_task_scope(
        ROOT,
        base_revision="origin/main",
        authority_checkpoint=CHECKPOINT,
        candidate_revision=REJECTED,
        task_envelope_path=TASK_PATH,
    ) == []
    unauthorized = validate_effective_task_scope(
        ROOT,
        base_revision="origin/main",
        authority_checkpoint="origin/main",
        candidate_revision=REJECTED,
        task_envelope_path=TASK_PATH,
    )
    assert "TASK_CONTROL_PLANE_UNAUTHORIZED" in _codes(unauthorized)
