# EPIC-003 executable foundation candidate

This candidate materializes the BC-001 engineering foundation defined by the
frozen `MONOREPO-FOUNDATION-CONTRACT`. It provides a machine-readable plan and
an offline validator for the minimum CLI/API/Web topology, the walking-skeleton
stage order, authoritative-state boundary, fail-closed behavior, and host,
container, and CI command parity required by `STORY-0012`.

Run the same command on a configured host, in a container runner, and in CI:

```text
make verify
```

The command runs the deterministic offline validator and the focused ISSUE-0122
tests. The executable integration test uses the PostgreSQL, RabbitMQ, Celery,
and Python versions pinned by the repository; CI provides those services and
sets `FOUNDATION_INTEGRATION=1`. Missing or reordered stages, failed broker
delivery, absent worker execution, and missing or corrupt diagnostic artifacts
fail the canonical test.

This BC-001 artifact is executable engineering evidence, not the product
runtime. Its issue-specific probe proves the CLI-to-artifact path against real
PostgreSQL and RabbitMQ/Celery services without publishing a reusable job,
queue, API, or persistence primitive. The later EPIC-086 implementation still
owns the product vertical slice. No frozen contract, public HTTP operation, or
ADR is changed here.

## Handoff boundaries

- Contract impact: none; the frozen STORY-0011 contract is consumed read-only.
- Migration and operational rollback: not applicable; rollback is reverting
  this candidate commit.
- Residual risk: independent QA and Reviewer must validate the same candidate
  SHA before any approval or merge claim.

## Repository integration

`STORY-0014` composes the already merged foundation and automation surfaces
without restating their rules. Run the deterministic read-only entry point:

```text
python tools/governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/repository_integration.py
```

The JSON report exposes the four `ISSUE-0124` acceptance criteria, the declared
`STORY-0012`/`STORY-0013` dependencies, and explicit evidence coverage for
`REQ-DEL-001`, `REQ-DEV-001`, and `REQ-TOP-001`. It succeeds only when the
existing `STORY-0013` validator passes in dry-run mode, the TaskEnvelope and
story graph agree, the read-only workflow invokes both validation layers, and
the local Python modules contain neither a dependency cycle nor an exact rule
duplicate.

Missing or drifted upstream evidence, a disconnected workflow, scope drift,
silent fallback, dependency drift, import cycles, and duplicated rule modules
produce sorted findings and a non-zero exit. The integration adds no API,
database, broker, frontend, geospatial, AI, migration, or public contract.
Rollback is a revert of the candidate commit. Independent QA and Reviewer must
still validate the same candidate SHA.
