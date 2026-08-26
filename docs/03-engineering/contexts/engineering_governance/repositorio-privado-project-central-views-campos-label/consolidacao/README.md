# Executable foundation slice consolidation

This package is the local, read-only consolidation owned by `STORY-0007`. It
evaluates the nine linked implementation slices from one full Git candidate
revision and never mutates repository, Project, issue, database, or broker
state.

The validator derives slice and downstream identities from the canonical story
graph. It checks common Phase F, specification, and Phase G baselines; disjoint
owned scopes; presence and syntax of every governed output; unique policy/map
identities; absence of byte-identical Python implementations; and the exact
requirement coverage approved in the requirements-review matrix. The current
nine slices cover 82 distinct requirements without normative duplication.

Slice completion is accepted only through the existing governed completion
authority. That authority binds each story and TaskEnvelope to an immutable
candidate, QA and Reviewer assurance, and Delivery Approval Authority evidence.
Local state labels, implementation reports, or path/hash assertions are not
completion proof.

Dependent release remains fail-closed. A distinct Reviewer must bind the exact
consolidation candidate, record residual risks explicitly, and name the exact
graph-derived dependent. Until then the validator returns no released
dependents; this implementation does not self-approve or anticipate Sentinel QA.

The mandatory test is `test_story_0007_slice_consolidation`, colocated with the
validator inside its TaskEnvelope scope. Contract, migration, persistence, and
runtime impact are not applicable. Rollback is a revert of the candidate commit.
