# Delivery Approval Authority operational verifier

The reusable entry point is
`tools.governance.delivery_approval_authority.verify_delivery_approval`. It derives the
governed repository and exact `HEAD` revision from the trusted verifier installation, then
receives only validated TaskEnvelope context, expected candidate SHA, explicit verification
time and untrusted evidence. It never receives a repository, revision, verifier, anchor
set, trust profile, issuer, key or policy as caller-configurable input.

The resolver reads the manifest, schemas, anchors and signed profile from Git objects at
the derived full commit SHA. The operational anchor path and SHA-256 digest are pinned in
the verifier, outside the manifest-controlled trust data. It rejects an unresolved runtime
checkout, a substituted anchor, paths outside the governed trust directory, any path under
`test-vectors`, digest divergence, missing objects and ambiguous trusted identifiers.
Working-tree content and manifest-declared repository identity are never authority.

## Operational trust lifecycle

The 1.0.0 profile is a fail-closed bootstrap: it publishes the profile-signing anchor and
the role-binding authority public key for `TASK-0761`, but deliberately publishes no
principal approval key. Consequently, no approval set can pass until independent
Executor, QA and Reviewer public keys are issued in a later signed profile revision. This
is not a missing prerequisite or manual fallback; it prevents the implementer from
inventing accountable identities or storing private keys.

Rotation adds a new signed profile/anchor version and updates the manifest digests in the
same governed commit. Revocation sets `revoked_at`; historical verification remains
available when the trusted operational context checks out the original repository revision
and supplies the explicit historical verification time. Recovery requires a new
anchor/profile revision issued from external key custody; this candidate does not claim
that production custody exists. No credential or private key belongs in this repository.
Rollback is performed by the trusted operational context and never by caller-supplied trust.

Compatibility is contract 1.0.0 only. The verifier introduces no API, database, service,
GitHub integration or product runtime. Residual production readiness depends on external
private-key custody and independent signer issuance; this candidate claims only the
repository prerequisite defined by `TASK-0761`.
