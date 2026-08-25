# Worker progress and cancellation foundation

This slice materializes candidate governance evidence for `REQ-WORKER-008` and
`REQ-WORKER-009`. It consumes frozen authorities without implementing a worker,
endpoint, database model, broker flow, or artifact publisher.

The policy requires PostgreSQL-authoritative, typed, work-unit progress that is
monotonic and exposed to SSE only after persistence. Polling remains a mandatory
reconciliation path, and transport signals never become product state.
Cancellation is cooperative, uses a persisted token, takes effect only at safe
points, revalidates lease ownership before effects, and cannot expose staged or
partial output as current. The validator rejects missing references, invalid
checkpoints, policy drift, unknown fields, incomplete configuration, scope drift,
and silent fallback.

## Handoff boundaries

- Contract impact: none; frozen ADRs and application profiles are consumed read-only.
- Runtime and migration impact: none; this is governance evidence and validation tooling.
- Risk: operational progress/cancellation behavior remains owned by downstream runtime stories.
- Rollback: revert the candidate commit; no migration or destructive action is required.
- Review: independent QA and Reviewer must validate the same candidate commit.
