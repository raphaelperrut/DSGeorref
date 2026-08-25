# Portfolio materialization and runtime foundation

This slice materializes one candidate policy and a fail-closed validator for
the ten requirements owned by `STORY-0697`. The policy records only the named
portfolio materialization and runtime invariants. It does not mutate GitHub,
provision an operational Project, issue credentials, open a database
transaction, or claim that downstream repository integration is complete.

`policy_validation.load_policy` rejects missing, extra, mistyped, changed, or
unreadable controls without a permissive fallback. Portfolio controls require
evidence before operational convergence, an immutable and sanitized record for
every synchronization run, snapshot-based recovery with safe compensations and
forward reconciliation, and a dedicated least-privilege identity using
short-lived credentials. Runtime controls keep the domain core synchronous,
put asynchronous I/O at boundaries, require explicit constructor-injected
composition, typed layered settings, explicit short Unit of Work transactions,
persistent idempotency, and structured correlated logs with central redaction.

## Boundaries and handoff

- Contract impact: none; frozen public contracts, profiles, and ADRs are unchanged.
- Persistence, HTTP, broker, migration, live GitHub mutation, credential issuance,
  and operational Project provisioning are not applicable to this local foundation slice.
- Risk: downstream repository integration must consume all controls without
  weakening fail-closed materialization or runtime gates.
- Limitation: evidence schemas, record fields, snapshot formats, compensation
  procedures, credential lifetimes, storage adapters, and logging field catalogs
  remain with their authorized owners and are not inferred here.
- Review: this remains a candidate until independent QA and Reviewer validate
  the exact commit; no self-approval is claimed.
- Rollback: revert the candidate commit. No data migration or destructive
  rollback is required.
