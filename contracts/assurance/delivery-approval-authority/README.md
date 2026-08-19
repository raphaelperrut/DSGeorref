# Delivery Approval Authority contract

- Contract version: `1.0.0`
- Owner: `BC-001`
- Normative decision: `ADR-058`
- Canonicalization: `JCS-RFC8785-PROFILE-1`
- Hash: `SHA-256`
- Signature algorithm: `Ed25519`
- Trust scope: `DSGEOREF-DELIVERY-APPROVAL-AUTHORITY-V1`

This directory is the machine-readable boundary for delivery approval evidence. It is
independent from product identity, GitHub, supply-chain signing and the `SPEC-001` Prompt
Bundle authority. A Prompt Bundle signature is never accepted for any purpose in this
contract.

## Authoritative inputs

The verifier is initialized with a locally pinned `trust-anchor-set` and a profile selected
from its trusted profile repository. Neither object is accepted from the untrusted
verification request. The delivery gate supplies the validated TaskEnvelope bytes and the
current expected candidate SHA as trusted verification context. The untrusted evidence
request contains only binding and attestation records. Identifiers in those records are
lookup hints; they never create an issuer, key, role, scope or authority.

The trust profile is valid only when its signature verifies against a non-revoked,
temporally valid anchor with purpose `DELIVERY_TRUST_PROFILE_SIGNING` and this contract's
trust scope. The profile then supplies the complete allowlist of identity issuers, role
binding authorities and principal attestation keys. Missing or ambiguous trusted material
is a failure.

## Stable identity and authorization

A principal is the ordered pair `issuer + subject`. It is distinct from the
`accountable_subject`, which identifies the human or organization accountable for a
workload. Authentication of a principal does not grant a role.

A role is granted only by a valid `role-binding` signed by a trusted key whose purpose is
`DELIVERY_ROLE_BINDING`. Its principal, accountable subject, role, TaskEnvelope scope,
policy reference and validity window are immutable signed fields. The binding and all keys
and issuers used by it must be unrevoked and valid at the attestation time.

## Canonical bytes and domain separation

JSON is parsed with duplicate-key rejection, UTF-8 without BOM, NFC strings, finite JSON
numbers and no unknown normative fields. Canonical bytes use sorted object keys, no
insignificant whitespace and UTF-8. The project implementation of
`JCS-RFC8785-PROFILE-1` is reused only as a canonicalization primitive.

Each signature covers its document after replacing only `/signature/value` with the empty
string. The signed message is the ASCII domain below, one NUL byte, then the canonical JSON
bytes of that projection:

| Record | Signature domain |
|---|---|
| trust profile | `DSGEOREF-DELIVERY-APPROVAL-TRUST-PROFILE-V1` |
| role binding | `DSGEOREF-DELIVERY-APPROVAL-ROLE-BINDING-V1` |
| approval attestation | `DSGEOREF-DELIVERY-APPROVAL-ATTESTATION-V1` |

These domains and the trust scope differ from
`DSGEOREF-PROMPT-BUNDLE-V1`/`SPEC-001`. A key without the exact delivery purpose and scope
is rejected even if an Ed25519 signature is mathematically valid.

## Approval verification

Verification receives an explicit UTC `verification_time`; the wall clock is not implicit.
The TaskEnvelope must validate against `.codex/tasks/TASK_ENVELOPE.schema.json`. Its digest
is SHA-256 of its canonical JSON bytes and must match every attestation. The expected
candidate SHA is supplied by the verifier's calling gate and must match every attestation.

For one TaskEnvelope/candidate pair, a complete PASS requires a non-empty attestation set
for every required role:

- one or more `Executor` attestations with decision `DELIVERED`;
- one or more `QA` attestations with decision `APPROVE`;
- one or more `Reviewer` attestations with decision `APPROVE`.

No required role has an upper cardinality bound in this contract. Multiple attestations for
a role are accepted when every attestation is valid and the resulting accountable-subject
sets remain pairwise disjoint across the three roles.

Every attestation must have a valid signature from the principal key selected from the
trusted profile, an exact valid binding digest, matching principal/role/accountable subject,
compatible validity windows, exact policy and scope, and an `issued_at` not after the
verification time. Reject decisions fail the set. The accountable-subject sets of Executor,
QA and Reviewer must be pairwise disjoint. Distinct issuers, subjects, keys or accounts do
not compensate for an overlap.

The verifier returns a `verification-verdict` and never a partial approval. On failure,
`status=FAIL`, `validated_roles=[]` and no caller-controlled value is promoted to trusted
state. At minimum it distinguishes schema, trust, signature, temporal, revocation, scope,
binding, TaskEnvelope digest, candidate replay, approval completeness, role mismatch and
independence failures.

## Conformance material

`test-vectors/conformance-suite.json` contains a deterministic golden path and mutation
probes. Its deterministic test keys have no authority outside the suite. The suite's trust
anchors are harness configuration, not request data. A conforming implementation must
reproduce the PASS and every fail-closed result, including cross-use of the `SPEC-001`
signature domain and trust scope.

This contract adds no API, database, service, GitHub integration or product runtime.
