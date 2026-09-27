# Executable backlog-governance foundation

This BC-001 control-plane package binds the slice to the frozen
`backlog-governance-profile` version `1.0.0` and makes the ten assigned invariants
executable. The JSON policy is strict: missing, unknown or permissive values fail
closed. The validators cover repository-stable identity, canonical domains,
evidence-based epic closure, thin sequenced slices, traceability and bounded
spikes. The existing BC-001 portfolio validator supplies governed snapshot,
delta, approval and tombstone checks for this slice.

The package is not a runtime service. It creates no endpoint, database table,
queue, state machine, shared registry or GitHub writer. Repository content remains
the control-plane authority; GitHub number and title remain non-authoritative
metadata. The frozen contract is consumed without modification.

The domain taxonomy is a versioned local registry of the domain codes already
present in both delivery indexes. Its loader rejects drift, duplicates and
unknown codes. The backlog validators receive this taxonomy and known source
and evidence IDs from their caller; they reject unknown entries and duplicate
issue identities. The caller must obtain source and evidence IDs from versioned
repository authorities.

Rollback is a revert of the candidate commit. No external or runtime state is
mutated. Independent QA and Reviewer validation remain separate gates on the same
candidate commit.
