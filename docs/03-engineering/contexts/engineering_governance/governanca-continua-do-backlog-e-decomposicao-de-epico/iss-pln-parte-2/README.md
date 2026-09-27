# Backlog and planning governance foundation

This slice materializes one candidate policy and a fail-closed validator for
the ten requirements assigned to the backlog and planning foundation. The
policy records only the qualitative invariants already established by those
requirements and their canonical tests. It does not set quantitative WIP or
capacity values, mutate GitHub, create a service boundary, or publish cost,
scale, latency, GPU, recovery, or security claims.

`policy_validation.load_policy` rejects missing, extra, mistyped, changed,
duplicate-key, non-finite, or unreadable policy input without a permissive
fallback. The controls require a complete portfolio skeleton with progressive
detail, roadmap and milestone layers, auditable sequencing, critical dependency
classification, WIP and capacity governance, pull flow, separated authorities,
and immutable reforecast snapshots.

## Boundaries and handoff

- Contract impact: none; frozen public contracts and ADRs are unchanged.
- Domain model impact: `LOCAL_MODEL` in `BC-001`; no new boundary, primitive,
  registry, checker layer, persistence model, endpoint, broker, or migration.
- Limitation: this is a declarative repository control-plane foundation; live
  portfolio automation and concrete quantitative configuration are not included.
- Risk: downstream integration must preserve the fail-closed semantics, and
  independent QA and Reviewer validation remain required on the exact commit.
- Rollback: revert the candidate commit; no data migration or destructive state
  rollback is required.
