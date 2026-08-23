# SPRINT-001 governance validators — Slice 2/2

## Purpose and authorities

This package materializes validator behavior for `STORY-0689` / `ISSUE-0799`.
Its normative authorities are `AP-008`, `AP-001`, `RELEASE_GATES`, the applicable
`REQ-SPRINT-001` and `REQ-TOOL` records listed by `TASK-0689`, and their referenced
ADRs. It does not replace those authorities or publish a shared contract.

Identity, role binding, candidate approval, and independence are delegated to the
Delivery Approval Authority from `ADR-058`. The slice calls the operational entry
point `tools.governance.delivery_approval_authority.verify_delivery_approval`
published by `STORY-0761`; it does not copy or reinterpret that trust boundary.

The slice validates AP-008 decisions 03 and 05–10: graph-derived waves, exercised
essential contracts, honest synthetic diagnostics, capability-proportional CI,
immutable sprint evidence, evidence-based closure, directly blocked extensions,
and cutover preconditions. It also validates the Python runtime baseline, future
runtime gates, a frozen `uv` workspace/lock declaration, and Make/CI parity.

A wave is one graph-derived readiness frontier: every direct predecessor must be
completed before the wave starts. Dependencies cannot be satisfied by another
story inside the same wave. This gives executable meaning to small topological
waves without inventing an arbitrary numeric limit.

`REQ-TOOL-002` is implemented as a validator behavior contract. Positive and
negative fixtures prove how a conforming baseline is accepted and how a missing,
divergent, non-frozen, or implicitly updated lock is rejected. This slice does not
create `uv.lock`, migrate the repository, or alter shared toolchain surfaces.

## Inputs and outputs

Repository-dependent inputs are full Git revisions. The validators enumerate the
tracked Python, Make, runtime, workflow, and local composite-action surfaces at that revision;
caller-provided inventories are not authoritative. Record inputs use governed
references containing the revision, repository-relative path, and SHA-256 digest.
Unknown fields and absent normative fields fail closed. Findings are deterministic.

The DAA gate accepts no repository, verifier, profile, anchor, issuer, key, or
policy configuration. The operational verifier resolves its own governed checkout,
pinned anchor, manifest, and signed profile. Untrusted records contain only bindings
and attestations. It binds them to the validated TaskEnvelope digest and exact
candidate SHA, and requires pairwise-disjoint accountable subjects for Executor,
QA, and Reviewer. Git authors, labels, task IDs, caller-supplied trust, and test or
conformance verifiers never establish identity or independence. Synthetic keys used
by unit tests remain fixture-only and never enter the production adapter.
The gate receives an explicit timestamp captured by its trusted operational context;
candidate commit timestamps and caller-supplied timestamps are never clocks of trust.

`SprintEvidenceSet` is canonical JSON bound to a source revision and governed
artifacts. Its digest covers the complete record through a zero-digest projection.
The human summary is derived from the machine-readable record. Closure reconstructs
the artifact's repository-wide Git history, requires one immutable path per evidence
identity, and delegates byte-level append-only enforcement to the Slice 1 ledger; a
ledger supplied or reconstructed by the caller is not accepted.

The applicable requirement, evidence-kind, and canonical-test inventories are
exact. Validation evidence binds a governed subject and the kind-specific validator;
test evidence binds the tested revision and an exact governed report result. The
execution report requires a pre-existing DevOps TaskEnvelope, a verified DAA
approval set, and must strictly precede the QA assurance artifact. A self-emitted `result: PASS`, an
empty finding list, or an unrelated blob is not substantive evidence.

## Slice 1 reuse

The implementation imports the Slice 1 canonical JSON profile, ordered findings,
controlled validation error, governed-artifact resolver, Git ancestry check,
append-only ledger, and deterministic SPRINT-001 selection. It does not copy the
foundation schema or create parallel implementations of those primitives.

## Boundaries and failure modes

The package validates records; it does not execute a walking skeleton, CI, runtime
promotion, dependency installation, G1 transition, or cutover. A `PASS` value used
in a controlled validator fixture is not a claim about current repository state.
The executable diagnostic job belongs to the SPRINT-001 walking-skeleton capability
listed under `EPIC-086`; this slice consumes its governed diagnostic evidence and
rejects any functional-georeferencing claim.
In particular, `docs/04-quality/RELEASE_GATES.md` remains authoritative for G1,
which is still blocked. Cutover validation requires an already valid evidence set,
its governed append-only record, and the governed Slice 1 Foundation closure record.
The closure and linked evidence must pass the frozen founder schema. The G1 proof
and first-slice authorization must each resolve to their pre-existing TaskEnvelope
and exact candidate, with identity and independence proven by DAA.

Malformed records, unknown fields, invalid graph edges, absent evidence, digest or
revision divergence, mutable history, calendar closure, indirect blockers,
functional georeferencing claims, missing runtime gates, workspace/lock semantic
divergence, mutable lock behavior, and Make/CI bypasses produce stable findings and
no fallback.

Make parity enumerates every governed workflow and local composite action. An
invoked target must contain or delegate to a substantive governed command; a target
that only echoes or no-ops is rejected. Shell comments are removed before command
inspection, so `# uv sync --frozen` is inert and cannot satisfy frozen-lock policy.

Wave completion additionally requires candidate-bound QA and Reviewer artifacts
consistent with the governed TaskEnvelope. Extension blockers require a governed
observation bound to the exact graph revision; caller completion lists and blocker
prose cannot establish those facts.

## Operation and rollback

The canonical tests are in
`tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/test_materialization.py`.
Rollback is a revert of the candidate commit. No database, broker, API, Project,
G1, cutover, runtime, lockfile, or shared CI state is mutated by this package.
