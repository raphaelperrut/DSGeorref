# Executable foundation slice consolidation

This read-only package is owned by `STORY-0017`. It evaluates `STORY-0703`,
`STORY-0704`, and `STORY-0705` from one full Git candidate revision and does not
mutate contracts, repository state, PostgreSQL, RabbitMQ, or published artifacts.

The validator derives slices and dependents from the canonical dependency graph.
It requires the same Phase F, specification, and Phase G baselines; disjoint tool
and document scopes; and one validator, checkpoint, and handoff document per
slice. The three checkpoints must retain unique identities and controls, bind the
same frozen upstream consolidation, match their TaskEnvelope tests, and resolve
every pinned canonical contract without digest drift. Validator sources must be
valid Python and cannot be byte-identical implementations.

Requirement ownership is read from each slice story and compared with the
requirements-review matrix. The candidate is rejected on missing coverage or
duplicate normative ownership. The current slices cover 24 distinct requirements.

Slice completion is accepted only through the existing governed completion
authority, which binds immutable evidence to QA, Reviewer, and Delivery Approval
Authority decisions. Local status text, file presence, and self-asserted hashes do
not prove completion.

Dependent release is fail-closed. A distinct Reviewer must bind the exact
candidate, record residual risks explicitly, and name the exact graph-derived
dependent. Without that record, or while any other finding remains, the validator
returns no released dependents and cannot self-approve.

The mandatory test is `test_story_0017_slice_consolidation`, colocated with the
validator inside the TaskEnvelope scope. Shared contracts, migrations, runtime,
and persistence are unchanged. Rollback is a revert of the candidate commit.
