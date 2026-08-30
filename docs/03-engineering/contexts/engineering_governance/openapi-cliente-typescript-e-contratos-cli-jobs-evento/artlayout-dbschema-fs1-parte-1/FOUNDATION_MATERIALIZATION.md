# Executable foundation materialization

- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Candidate:** `STORY-0703` / `TASK-0703`
- **Checkpoint version:** `1.0.0`
- **State:** implementation candidate; independent QA and final review pending

## Scope

This slice materializes the governance-side executable checkpoint for the first
functional slice. The checkpoint consumes the frozen contracts integrated by
`STORY-0016`; it does not change OpenAPI, domain schemas, artifact schemas, runtime,
database, migration, endpoint, event, scientific threshold, or corpus.

The executable entry point is `validate_foundation.py`. It returns a machine-readable
`PASS` only when the checkpoint is complete, the consolidation lists `STORY-0703` as
eligible, every canonical contract exists, and the contract invariants used by this
slice still match. Missing, unknown, permissive, or divergent controls return a
non-zero exit code without warning-only fallback.

## Requirement evidence

| Requirement | Executable evidence | Fail-closed case |
|---|---|---|
| `REQ-ARTLAYOUT-010` | `test_req_artlayout_0010` | missing authorization or unsafe locator is rejected |
| `REQ-DBSCHEMA-002` | `test_req_dbschema_002` | non-UUIDv7 or unstable identity policy is rejected |
| `REQ-DBSCHEMA-004` | `test_req_dbschema_004` | implicit last-write-wins is rejected |
| `REQ-FS1-002` | `test_first_functional_slice_decision_02` | arbitrary host path or root escape is rejected |
| `REQ-FS1-003` | `test_first_functional_slice_decision_03` | mutable original or missing hash/metadata is rejected |
| `REQ-FS1-005` | `test_first_functional_slice_decision_05` | nondeterminism or unaudited correspondence is rejected |
| `REQ-FS1-007` | `test_first_functional_slice_decision_07` | optional SGV or hard-gate override is rejected |
| `REQ-FS1-008` | `test_first_functional_slice_decision_08` | partial, mutable, or non-accepted publication is rejected |
| `REQ-FS1-009` | `test_first_functional_slice_decision_09` | missing surface or surface-specific rule is rejected |
| `REQ-FS1-010` | `test_first_functional_slice_decision_10` | missing/failed promotion dimension is rejected |

The validator also binds these controls to the canonical `ProcessingPlan`,
`QualityReport`, `FailureDiagnostic`, Artifact Kind Registry, and `ArtifactSetManifest`.
It checks the canonical tri-state verdict, unique ProcessingPlan capabilities,
diagnostic evidence/remediation fields, artifact publication proof, and the required
COG/provenance/quality artifact kinds.

## Ownership and containment

The stable production path is capability-based and contains no issue identifier. The
TaskEnvelope correction adds only its own control-plane file, the focused test, and the
evidence path already required by the story. No shared registry or frozen contract is
modified, and no data-plane implementation is introduced into `BC-001`.

## Contract impact, risks, and rollback

- **Contract impact:** canonical frozen contracts are read and verified, not modified;
  no compatibility window, public payload, or generated client changes.
- **Persistence/migrations:** not applicable; no table, state, lock, or migration is added.
- **Runtime/Geo/IA:** no runtime algorithm or adapter is introduced. The checkpoint
  preserves classic-first, SGV fail-closed, and optional-IA boundaries.
- **Residual risk:** this slice proves the executable governance gate and negative
  behavior. Runtime implementation and the promoted stratified corpus remain with the
  explicitly assigned downstream stories and gates.
- **Rollback:** revert this candidate before downstream consumption. After a consumer
  pins checkpoint `1.0.0`, preserve history and publish a successor rather than mutate
  the pinned checkpoint.
- **Review:** the implementer claims no approval; QA and Reviewer must assess the same
  candidate commit independently.

## Focused command

```text
py -3.12 -m pytest -p no:cacheprovider tests/fnd/openapi-cliente-typescript-e-contratos-cli-jobs-evento/test_foundation_materialization.py -q
```
