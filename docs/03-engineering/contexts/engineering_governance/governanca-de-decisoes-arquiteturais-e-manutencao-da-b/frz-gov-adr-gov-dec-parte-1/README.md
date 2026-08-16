# Foundation baseline lifecycle and normative validators

## Scope

This package materializes the executable validation owned by `STORY-0688`. The
contract authority is `foundation-baseline-lifecycle.schema.json`; canonical JSON
and digest generation follow the `SPEC-001-JCS` profile. The implementation is a
repository governance tool and does not create a second runtime or persistence
authority.

## Modules

- `canonical_json.py` rejects duplicate keys, BOM, non-UTF-8 input, non-finite
  numbers and NFC key collisions, then emits the project JCS representation.
- `contract_validation.py` loads and checks the Draft 2020-12 lifecycle schema
  before validating a record.
- `baseline_lifecycle.py` derives coverage from the governed TaskEnvelope reference
  at a full Git commit and validates baseline digests and supersession lineage.
- `governed_artifacts.py`, `lifecycle_evidence.py` and `lifecycle_records.py`
  resolve evidence from exact Git revisions, verify proof semantics/authority and
  preserve append-only closure history.
- `decision_governance.py` derives classification, eligibility, identity, owner,
  overlap references and Owner gate from repository history, the ADR index and ADR
  metadata instead of accepting caller booleans as facts.
- `portfolio_validation.py` validates historical snapshot immutability and exact
  governed delta, approval and tombstone consistency.
- `sprint_validation.py` reads `AP-008` and the canonical story dependency graph to
  validate exact minimum scope and the complete deterministic SPRINT-001 selection.
- `scope_validation.py` composes frozen control-plane authority with TaskEnvelope
  allow/deny paths without adding a self-authorizing allowlist entry.
- `foundation_validation_types.py` provides ordered findings and the controlled exception used
  by fail-closed call sites.

All public validators return findings in deterministic order. Builders raise a
controlled validation exception and do not return partially accepted state.

## Lifecycle rules

Coverage is exactly the TaskEnvelope named by `coverage_authority` plus its
`references` array at `source_revision`. Paths, blobs and ordering are verified
from Git; a second inventory is not accepted. The digest projection replaces
`baseline_digest` with 64 lowercase zeroes before canonical serialization and
SHA-256.

A digest change requires a matching supersession record. The append-only ledger
preserves each baseline identity/version and rejects reuse of any immutable record
identity/version with different canonical bytes.
Closure requires the full proof set loaded from each exact `source_revision`,
semantic proof type/result/baseline linkage, candidate ancestry and role authority
for QA, Reviewer, human merge and first-slice authorization. Reopening requires a
governed material trigger linked to the new candidate/evidence identities and
byte-identical preservation of the prior closure and evidence set.

## Parallel Story boundary

The validators consume accepted facts by reference. They deliberately do not
define or publish payloads, stores or automation owned by:

- `STORY-0692`: ADR classification/application implementation;
- `STORY-0693`: ADR promotion, overlap and Owner-gate implementation;
- `STORY-0754`: portfolio snapshot/tombstone/delta implementation;
- `STORY-0757`: Foundation Gate result implementation;
- `STORY-0758`: Sprint selection implementation.

These Stories are not runtime dependencies. This slice only validates the current
repository artifacts. It does not create their persistence, GitHub/Project
automation, gate result or selection publication mechanisms.

## Failure and rollback

Malformed schemas, records, Git paths, digests, lineage, evidence, classification,
history or graph state fail closed with stable finding codes. Rollback consists of
reverting the implementation commit: no database, queue, endpoint, GitHub or
Project state is mutated by these validators. Published immutable closure history
must never be deleted or rewritten as a rollback mechanism.
