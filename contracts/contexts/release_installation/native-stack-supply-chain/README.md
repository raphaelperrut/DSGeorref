# Native stack supply-chain contract

This directory contains the narrow, fail-closed contract authorized for Issue #973 in
SPRINT-001. It does not implement, satisfy, supersede, or close EPIC-080, Issue #720, or
Story #790.

`policy.yaml` is the normative instance. `policy.schema.json` validates its exact
administrative scope, publication identity, artifact linkage, verification, revocation,
and failure rules. Independent Architect/BC-015 and Security reviews must reference the
SHA-256 digest of the exact policy bytes they examined.

The delivery-approval authority, Prompt Bundle signatures, test keys, and this supply-chain
trust scope are distinct authorities. Cross-use is rejected.
