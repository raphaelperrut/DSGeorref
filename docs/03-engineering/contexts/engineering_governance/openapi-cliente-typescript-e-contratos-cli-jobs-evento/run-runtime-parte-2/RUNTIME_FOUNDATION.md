# RUN/RUNTIME executable foundation

- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Candidate:** `STORY-0704` / `TASK-0704`
- **Checkpoint version:** `1.0.0`
- **State:** implementation candidate; independent QA and final review pending

## Scope

This slice materializes the governance-side executable checkpoint for the RUN and
RUNTIME boundaries assigned to `STORY-0704`. It consumes the frozen profiles
integrated by `STORY-0016` and verifies their recorded SHA-256 digests. It changes no
OpenAPI operation, generated TypeScript client, public payload, domain schema,
artifact schema, runtime process, endpoint, event, table, migration, or scientific
rule.

The executable entry point is `validate_runtime_foundation.py`. It emits a
machine-readable `PASS` only when the checkpoint is complete, the consolidation
lists `STORY-0704` as eligible, both frozen profiles retain their pinned digests, and
all required controls match. Missing, unknown, permissive, unbound, or unreadable
input returns a non-zero status without warning-only fallback.

## Requirement evidence

| Requirement | Executable evidence | Fail-closed case |
|---|---|---|
| `REQ-RUN-002` | `test_req_run_002` | async or framework-dependent domain core is rejected |
| `REQ-RUN-003` | `test_req_run_003` | implicit root or non-constructor injection is rejected |
| `REQ-RUN-004` | `test_req_run_004` | untyped, unstratified, or best-effort required setting is rejected |
| `REQ-RUN-005` | `test_req_run_005` | implicit UoW or unbounded transaction is rejected |
| `REQ-RUN-007` | `test_req_run_007` | volatile/in-memory idempotency is rejected |
| `REQ-RUN-009` | `test_req_run_009` | uncorrelated or locally optional redaction is rejected |
| `REQ-RUNTIME-001` | `test_runtime_decision_1` | alternate namespace or fat surface adapter is rejected |
| `REQ-RUNTIME-002` | `test_runtime_decision_2` | async framework in the domain core is rejected |
| `REQ-RUNTIME-003` | `test_runtime_decision_3` | implicit composition or silent setting default is rejected |
| `REQ-RUNTIME-004` | `test_runtime_decision_4` | broker state authority or unmapped error fallback is rejected |

`REQ-RUNTIME-001` and the error boundary are bound to the frozen contract foundation;
the thin-surface invariant is also checked against the frozen runtime profile.
`REQ-RUNTIME-004` preserves PostgreSQL/PostGIS as system of record and the broker as
transport only. The checkpoint materializes policy and proof, not a second runtime
authority.

## Ownership and containment

The production paths are capability-based and contain no issue identifier. The Tech
Lead role provides control-plane authority for the minimal TaskEnvelope correction;
the TaskEnvelope is not self-authorized in its payload allowlist. The correction adds
only the focused test and exact implementation evidence file already required by the
acceptance criteria. No shared registry, ADR, specification, or frozen contract is
modified.

## Contract impact, risks, and rollback

- **Contract impact:** the two frozen profiles are read, hash-pinned, and verified;
  no public contract or generated client changes.
- **Persistence/migrations:** no persistence implementation or migration is added;
  PostgreSQL/PostGIS authority is preserved as an executable governance invariant.
- **Runtime/Geo/IA:** no runtime, geometry, SGV, or AI implementation is introduced.
- **Residual risk:** the checkpoint proves policy conformance and negative behavior;
  downstream runtime/data-plane stories remain responsible for operational code.
- **Rollback:** revert this candidate before downstream consumption. After a consumer
  pins version `1.0.0`, preserve history and publish a successor checkpoint.
- **Review:** the implementer claims no approval; QA and Reviewer assess the same
  candidate commit independently.

## Focused command

```text
py -3.12 -m pytest -p no:cacheprovider tests/fnd/openapi-cliente-typescript-e-contratos-cli-jobs-evento/test_run_runtime_foundation.py -q
```
