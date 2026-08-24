# Issue and portfolio governance foundation

This slice materializes one candidate policy and a fail-closed validator for
the ten requirements owned by `STORY-0693`. The policy records only invariants
already owned by the cited requirements and ADRs. It does not mutate GitHub,
choose a new domain taxonomy, define geospatial serialization, or create a
second ADR-governance authority.

`policy_validation.load_policy` rejects missing, extra, mistyped, or changed
controls without a permissive fallback. ADR classification and overlap remain
owned by the existing `decision_governance` validators. The issue controls keep
the canonical domain taxonomy, a single primary issue for cross-domain work,
idempotent dry-run synchronization restricted by a managed-field registry,
portfolio skeleton rules, and bounded spike exits explicit. The native geometry
control keeps Shapely in domain logic and parsing/serialization in explicit I/O
adapters.

## Boundaries and handoff

- Contract impact: none; frozen public contracts and ADRs are unchanged.
- Persistence, HTTP, broker, migration, live GitHub mutation, and geospatial
  runtime materialization: not applicable to this local foundation slice.
- Risk: this remains a candidate until independent QA and Reviewer validate the
  exact commit; later EPIC-002 integration stories own repository automation.
- Rollback: revert the candidate commit. No data migration or destructive
  rollback is required.
