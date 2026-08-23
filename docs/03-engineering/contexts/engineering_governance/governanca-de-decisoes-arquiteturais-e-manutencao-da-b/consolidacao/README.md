# Slice consolidation validator

This package is the local, read-only consolidation owned by `STORY-0002`.
It evaluates `STORY-0688` and `STORY-0689` from one full Git candidate revision.

The validator derives dependencies and downstream releases from the canonical
story graph, derives requirement ownership from the child TaskEnvelopes and the
requirements-review matrix, and reads all slice outputs from the same revision.
It rejects missing outputs, baseline drift, overlapping scopes, duplicate
requirement ownership, byte-identical Python implementations, invalid Python,
and the absence of the established Slice 2 reuse of the Slice 1 boundary.

A slice is complete only when its canonical state is `Done`, or when the
Reviewer supplies governed completion artifact references accepted by the
existing Sprint graph completion validator. The consolidation package delegates
those references without redefining them. That canonical validator enforces the
completed story/task/candidate binding, immutable reference lineage, QA and
Reviewer assurance, and Delivery Approval Authority verification. Ready,
Ready-after-authorization, Planned, In Progress, Blocked, unknown, missing, and
locally asserted path/hash records are never completion by themselves.

Dependent stories are never released implicitly. A reviewer record must bind the
exact candidate, list residual risks (an empty list is explicit), name the exact
graph-derived dependents, and identify a reviewer distinct from the executor.
The record is an input to this local validator; it does not replace repository or
GitHub review evidence and the implementation candidate does not self-approve.

The mandatory test is `test_story_0002_slice_consolidation`, colocated with the
validator inside its Phase-F scope. Rollback is a revert of the candidate commit;
the validator is read-only and adds no database, broker, runtime, migration,
shared contract, or product state.
