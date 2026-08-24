# Project and portfolio materialization foundation

This slice materializes one candidate policy and a fail-closed validator for
the ten requirements owned by `STORY-0696`. The policy records only the named
Project and portfolio materialization invariants. It does not mutate GitHub,
provision an operational Project, select concrete dependency types or size
bands, or claim that later repository integration is complete.

`policy_validation.load_policy` rejects missing, extra, mistyped, changed, or
unreadable controls without a permissive fallback. Project controls require
typed dependencies with material-cycle detection, distinct derived priority
dimensions, relative sizing with confidence and a split rule, and automation
that preserves integrity without approving material decisions. Materialization
controls require representative staging, bounded waves, explicit per-field
sync governance, three-way drift reconciliation, approved destructive
ChangeSets with tombstones, and idempotent resumable operations.

## Boundaries and handoff

- Contract impact: none; frozen public contracts, profiles, and ADRs are unchanged.
- Persistence, HTTP, broker, migration, live GitHub mutation, and operational
  Project provisioning are not applicable to this local foundation slice.
- Risk: downstream repository integration must consume all controls without
  collapsing priority dimensions or weakening fail-closed materialization gates.
- Limitation: concrete edge types, relative size bands, field authorities, sync
  directions, wave sizes, retry timing, and checkpoint formats remain with their
  authorized operational owners and are not inferred here.
- Review: this remains a candidate until independent QA and Reviewer validate
  the exact commit; no self-approval is claimed.
- Rollback: revert the candidate commit. No data migration or destructive
  rollback is required.
