# RUNTIME/TOOL/UPG executable foundation

- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Candidate:** `STORY-0705` / `TASK-0705`
- **Checkpoint version:** `1.0.0`
- **State:** implementation candidate; independent QA and review pending

## Scope

This slice materializes an executable governance checkpoint for the four requirements
assigned to `STORY-0705`. The checkpoint binds only frozen artifacts already present
in the approved baseline: the slice consolidation, foundation and runtime profiles,
OpenAPI, version-and-rollback matrix, and lock-and-queue policy. Every binding is
path-exact and SHA-256 pinned with normalized line endings.

`validate_runtime_tool_upgrade_foundation.py` emits `PASS` only when the checkpoint
shape is exact, `STORY-0705` remains eligible, every binding retains its digest and
frozen semantics, and all four controls remain fail-closed. Missing, unknown,
permissive, inconsistent, unreadable, root-escaping, or digest-divergent input
returns a non-zero result without fallback.

## Requirement-to-evidence mapping

| Requirement | Canonical test | Materialized control | Negative evidence |
|---|---|---|---|
| `REQ-RUNTIME-006` | `test_runtime_decision_6` | browser consumes only the published HTTP contract; host paths, raw broker payloads, and direct persistence are prohibited | exposure, raw forwarding, direct access, and OpenAPI binding drift are rejected |
| `REQ-RUNTIME-007` | `test_runtime_decision_7` | selection is limited to registered authorized roots and opaque root/entry identifiers | arbitrary roots, host-path identifiers, and absolute paths are rejected |
| `REQ-TOOL-005` | `test_model_boundary_architecture` | domain, HTTP transport, and persistence models stay separate; the frozen explicit mapping is retained | implicit mapping, shared boundary model, and missing control are rejected |
| `REQ-UPG-005` | `test_phased_rollout_limited_mixed_version_window_drain_and_long_job_pinning` | mixed versions are limited to one upgrade operation, writers are single-version and explicitly drained before cutover, and long jobs remain pinned to a compatible version until completion | unbounded windows, implicit drain, in-place job migration, and ineligible dependency are rejected |

The validator additionally verifies that the frozen runtime profile keeps the
frontend as a published-contract consumer, transport models inside the HTTP adapter,
explicit transport/domain/persistence mapping, and direct ORM/filesystem/broker
dependencies forbidden. The frozen OpenAPI workspace schemas expose only opaque IDs
and metadata, and the drain and upgrade operations remain frozen.

## Contract impact

No public contract is created or changed. The checkpoint reads and hash-pins existing
frozen contracts; OpenAPI, the generated TypeScript client, domain/event/artifact
schemas, persistence, migrations, and central registries are unchanged. The
TaskEnvelope correction adds only the exact focused-test and implementation-evidence
paths required by the acceptance contract.

## Risks, rollback, and explicit limits

- **Residual risk:** this checkpoint proves declared contract conformance and
  fail-closed behavior, not operational behavior under a live mixed-version rollout.
- **Rollback:** before downstream consumption, revert the candidate. After a consumer
  pins version `1.0.0`, preserve the checkpoint and publish a successor rather than
  mutating reviewed evidence.
- **Not implemented:** browser/API/filesystem/persistence behavior, broker or job data
  plane, `UpgradeController`, rollout orchestration, writer drain execution, long-job
  migration, new endpoint/state/event/table/schema, or a public contract.
- **Review boundary:** the implementer claims no QA or Reviewer approval. Independent
  QA and Reviewer must assess the same PR-head SHA.

## Focused commands

```text
py -3.12 -m pytest -p no:cacheprovider tests/fnd/openapi-cliente-typescript-e-contratos-cli-jobs-evento/test_runtime_tool_upgrade_foundation.py -q
py -3.12 tools/governance/openapi-cliente-typescript-e-contratos-cli-jobs-evento/runtime-tool-upg-parte-3/validate_runtime_tool_upgrade_foundation.py --repo-root .
```
