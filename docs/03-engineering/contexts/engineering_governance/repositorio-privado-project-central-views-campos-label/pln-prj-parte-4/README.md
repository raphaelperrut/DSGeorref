# Planning and Project governance foundation

This slice materializes one candidate policy and a fail-closed validator for
the ten requirements owned by `STORY-0695`. It records only the qualitative
planning and Project invariants named by the requirements and their canonical
tests. It does not set quantitative WIP/capacity values, invent issue types or
fields, mutate GitHub, or claim that repository integration is complete.

`policy_validation.load_policy` rejects missing, extra, mistyped, changed, or
unreadable controls without a permissive fallback. Planning controls require
class and global WIP limits with the named reserves, range/category/confidence
capacity records without automatic deadline conversion, pull flow, classified
carryover, separated authorities, and immutable versioned reforecast snapshots.
Project controls require canonical registered types and forms, core plus
per-type fields, one primary parent with limited operational hierarchy, and
fail-closed Ready/Done gates tied to the repository definitions.

## Boundaries and handoff

- Contract impact: none; frozen public contracts, profiles, and ADRs are unchanged.
- Persistence, HTTP, broker, migration, live GitHub mutation, and Project field
  provisioning are not applicable to this local foundation slice.
- Risk: concrete WIP/capacity numbers and the registered type/field catalog must
  remain owned by their applicable operational configuration; this slice does
  not silently supply them.
- Review: this is a candidate until independent QA and Reviewer validate the
  exact commit; no self-approval is claimed.
- Rollback: revert the candidate commit. No data migration or destructive
  rollback is required.
