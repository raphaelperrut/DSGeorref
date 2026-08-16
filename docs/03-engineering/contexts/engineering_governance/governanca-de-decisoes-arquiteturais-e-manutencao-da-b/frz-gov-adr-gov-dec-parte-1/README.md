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
- `baseline_lifecycle.py` derives coverage from `TASK-0688` at a full Git commit,
  computes and validates baseline digests, checks supersession lineage, verifies
  closure evidence and validates material reopening against preserved history.
- `decision_governance.py` validates the closed decision classification set,
  `NEW_ADR` eligibility, anti-promotion, overlap resolution, normative owner and
  Owner gate.
- `portfolio_validation.py` validates historical snapshot immutability, tombstones
  for removals and approval of applied deltas.
- `sprint_validation.py` reads `AP-008` and the canonical story dependency graph to
  validate exact minimum scope and deterministic hard-predecessor selection.
- `foundation_validation_types.py` provides ordered findings and the controlled exception used
  by fail-closed call sites.

All public validators return findings in deterministic order. Builders raise a
controlled validation exception and do not return partially accepted state.

## Lifecycle rules

Coverage is exactly `.codex/tasks/TASK-0688.json` plus its `references` array at
`source_revision`. Paths, blobs and ordering are verified from Git; a second
inventory is not accepted. The digest projection replaces `baseline_digest` with
64 lowercase zeroes before canonical serialization and SHA-256.

A digest change requires a matching supersession record. The append-only ledger
preserves each baseline identity/version and rejects reuse of any immutable record
identity/version with different canonical bytes.
Closure requires the full proof set, artifact digest verification and candidate or
merge linkage. Reopening requires a material trigger, a new candidate and evidence
identity, and byte-identical preservation of the prior closure and evidence set.

## Parallel Story boundary

The validators consume accepted facts by reference. They deliberately do not
define or publish payloads, stores or automation owned by:

- `STORY-0692`: ADR classification/application implementation;
- `STORY-0693`: ADR promotion, overlap and Owner-gate implementation;
- `STORY-0754`: portfolio snapshot/tombstone/delta implementation;
- `STORY-0757`: Foundation Gate result implementation;
- `STORY-0758`: Sprint selection implementation.

These Stories are not runtime dependencies. For `STORY-0688`, graph-derived
selection resolves only `STORY-0001` as a hard predecessor.

## Failure and rollback

Malformed schemas, records, Git paths, digests, lineage, evidence, classification,
history or graph state fail closed with stable finding codes. Rollback consists of
reverting the implementation commit: no database, queue, endpoint, GitHub or
Project state is mutated by these validators. Published immutable closure history
must never be deleted or rewritten as a rollback mechanism.
