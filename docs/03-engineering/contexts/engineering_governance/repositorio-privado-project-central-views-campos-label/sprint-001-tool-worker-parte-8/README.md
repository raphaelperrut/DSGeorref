# Toolchain and worker foundation evidence

This slice records the exact evidence for the ten requirements owned by
`STORY-0699`. The policy is declarative: it points to existing requirements,
authorities, and executable checkpoints without changing frozen contracts,
ADRs, runtime behavior, or GitHub state.

`foundation_validation.load_policy` fails closed when coverage is incomplete,
a reference or checkpoint is missing or unsafe, policy fields drift, the
TaskEnvelope allow and review scopes differ, deny paths change, or the frozen
Python/worker authorities contradict the candidate policy. Unknown fields and
silent fallback are rejected.

## Handoff boundaries

- Contract impact: none; existing frozen contracts are consumed read-only.
- Runtime impact: none; this is governance evidence and validation tooling.
- Risk: future tuning remains owned by `BP-004` and cannot be inferred here.
- Rollback: revert the candidate commit; no migration or destructive action.
- Review: independent QA and Reviewer validate the same candidate commit.
