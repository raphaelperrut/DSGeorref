# EPIC-003 executable foundation candidate

This candidate materializes the BC-001 engineering foundation defined by the
frozen `MONOREPO-FOUNDATION-CONTRACT`. It provides a machine-readable plan and
an offline validator for the minimum CLI/API/Web topology, the walking-skeleton
stage order, authoritative-state boundary, fail-closed behavior, and host,
container, and CI command parity required by `STORY-0012`.

Run the same command locally and in CI:

```text
python tools/governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/foundation_validation.py --foundation docs/03-engineering/contexts/engineering_governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/foundation-plan.json --contract contracts/contexts/engineering_governance/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/examples/monorepo-foundation.json
```

The command uses only the Python standard library, performs no dependency or
network discovery, emits deterministic JSON, returns `0` only for a conforming
candidate, and returns `2` on unreadable input or contract drift. Unknown
fields, semantic-authority drift, reordered or missing stages, command drift,
implicit downloads, and silent fallback are rejected.

This BC-001 artifact is executable engineering evidence, not the product
runtime. It does not claim that PostgreSQL, RabbitMQ/Celery, worker, or frontend
services have been deployed; the later EPIC-086 implementation owns that live
vertical slice. No frozen contract, HTTP operation, persistence schema, or ADR
is changed here.

## Handoff boundaries

- Contract impact: none; the frozen STORY-0011 contract is consumed read-only.
- Migration and operational rollback: not applicable; rollback is reverting
  this candidate commit.
- Residual risk: independent QA and Reviewer must validate the same candidate
  SHA before any approval or merge claim.
