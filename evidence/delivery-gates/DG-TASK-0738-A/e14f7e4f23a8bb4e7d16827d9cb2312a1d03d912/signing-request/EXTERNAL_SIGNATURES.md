# TASK-0738 — external DAA signature request

Status: EXTERNAL_SIGNATURE_REQUIRED. No draft is an authenticated authorization or
attestation. The operational trust manifest still selects the original signed profile.
All private operations must be performed by the existing Project Owner custodian,
`MANUAL_OUTSIDE_CODEX`, as recorded in
`evidence/implementation/issue-0974/adr-compatibility.json` and
`task-envelope-authorization.json`. No private material is requested for this repository.

Candidate: `e14f7e4f23a8bb4e7d16827d9cb2312a1d03d912`.
Manifest file SHA-256: `893b2dc9d4e74c52cfbf57ff05d5a980bdb58556d46f07c912d5d91118a80a8d`.
Final snapshot canonical/file SHA-256:
`f84908d577debb9bc3a4d014b8411d3b548648aebf97dcf63284868dba177270`.
Origin owner envelope canonical SHA-256:
`df3e8dbd025f5b477450b9d5333dd68e2cb73b9a502c02b9179880df9d5e167a`.
Profile pending payload canonical SHA-256:
`6910ceb514eb6dbd1eeca3d2327ec393e9f75dd1825bb0b8dba4074d3af59273`.
Profile signature message SHA-256:
`2e4ec40b99db833dd9d524a04ef5b729b1e7a678645143bb9ba9568bbcc3685f`.

## Operational revision

The existing DAA v2 schemas fix `profile_version` and `binding_version` to `2.0.0`.
This is an operational revision identified by its canonical payload digest and this
versioned candidate directory. It adds exactly TASK-0738 and the final acceptance snapshot
digest. TASK-0764 scopes are preserved verbatim, never reused to authorize TASK-0738.
Identity, accountable subject, public keys, roots, algorithms and validity windows are
unchanged. No ADR or DAA schema change is needed under ADR-059's change gate.

`*.pending.json` contains an empty signature and intentionally fails the signature-value
schema constraint. Everything else conforms to the existing DAA contract. `*.message.bin`
is the exact signature message: v2 domain, NUL, canonical payload with empty signature.

Required signatures, in order:

1. `profile.pending.json`: `daa2-operational-profile-root-2026`.
2. Four distinct bindings: `daa2-operational-binding-authority-2026`, one per role.
3. Executor DELIVERED: `daa2-operational-executor-2026`.
4. QA APPROVE: `daa2-operational-qa-2026`.
5. Reviewer APPROVE: `daa2-operational-reviewer-2026`.
6. Project Owner PASS (or NO_GO): `daa2-operational-project-owner-2026`.

The four attestation messages cannot be finalized together in advance: each successor
depends on the digest of the fully signed predecessor. Owner also binds the complete
verifier input-set digest. Preparing unsigned invented predecessor digests would violate
the contract. The public-only helper produces each next request after authentic preceding
records arrive. There are nine external signatures total, under six existing keys.

## Signature commands for the external custodian

Run from the repository root. The environment variables below must resolve to the
custodian's actual existing external PEM keys, if that is the authorized key format.
They are command parameters, not a claim that a signing service or key path exists.
For another custody interface, submit the exact `.message.bin` bytes and return the raw
64-byte Ed25519 signature. Never generate a replacement keypair.

```powershell
$requestRoot = 'evidence/delivery-gates/DG-TASK-0738-A/e14f7e4f23a8bb4e7d16827d9cb2312a1d03d912/signing-request'
openssl pkeyutl -sign -rawin -inkey $env:DAA2_PROFILE_ROOT_PEM -in "$requestRoot/profile.message.bin" -out "$requestRoot/profile.sig"
.venv/Scripts/python.exe -m tools.governance.delivery_approval_authority.signing_requests --root $requestRoot attach --name profile --kind profile --signature "$requestRoot/profile.sig"

foreach ($roleName in @('executor','qa','reviewer','project-owner')) {
    openssl pkeyutl -sign -rawin -inkey $env:DAA2_BINDING_AUTHORITY_PEM -in "$requestRoot/$roleName-binding.message.bin" -out "$requestRoot/$roleName-binding.sig"
    .venv/Scripts/python.exe -m tools.governance.delivery_approval_authority.signing_requests --root $requestRoot attach --name "$roleName-binding" --kind binding --signature "$requestRoot/$roleName-binding.sig"
}
```

Each `attach` checks the existing schema and Ed25519 signature against the existing public
key before writing a new `.signed.json`. It cannot sign and does not activate a profile.
After all five signatures verify, publish `profile.signed.json` at the verifier's already
pinned `contracts/assurance/delivery-approval-authority/trust/profiles/dsgeorref-daa-operational-2.0.0.json`
and update only its SHA-256 reference in the operational trust manifest. Keep the old profile
in immutable Git history. The original TASK-0764 policies, bindings and signatures remain
unchanged. This publication must be committed before the public verifier API can resolve
the revised profile; it reads governed HEAD blobs, never caller-supplied trust.

## Incremental formal sessions

Prior implementation, QA PASS and Reviewer PASS at the candidate are retained as functional
decisions, attributed to the Owner's explicit instructions in `../functional-approvals.json`.
They are not fabricated cryptographic approvals. No technical test is repeated.

The final manifest-bound snapshot did not exist during those earlier sessions. The custodian
must conduct sequential incremental formal ratification sessions on the final snapshot.
Each request is issued at invocation time with a fresh session ID; no retrospective session
or timestamp is asserted. The function confirms its existing decision and the new snapshot
binding, signs with its own key, then passes the signed digest to the next function.
`SOLO_FUNCTIONAL_SEGREGATION_V1` and `PERSONAL_INDEPENDENCE=ABSENT_DECLARED` are mandatory.
The code author must not use this process to approve its own governance changes.

Execute and complete each block before the next:

```powershell
.venv/Scripts/python.exe -m tools.governance.delivery_approval_authority.signing_requests --root $requestRoot prepare-attestation --role Executor --decision DELIVERED
openssl pkeyutl -sign -rawin -inkey $env:DAA2_EXECUTOR_PEM -in "$requestRoot/executor-attestation.message.bin" -out "$requestRoot/executor-attestation.sig"
.venv/Scripts/python.exe -m tools.governance.delivery_approval_authority.signing_requests --root $requestRoot attach --name executor-attestation --kind attestation --signature "$requestRoot/executor-attestation.sig"

.venv/Scripts/python.exe -m tools.governance.delivery_approval_authority.signing_requests --root $requestRoot prepare-attestation --role QA --decision APPROVE
openssl pkeyutl -sign -rawin -inkey $env:DAA2_QA_PEM -in "$requestRoot/qa-attestation.message.bin" -out "$requestRoot/qa-attestation.sig"
.venv/Scripts/python.exe -m tools.governance.delivery_approval_authority.signing_requests --root $requestRoot attach --name qa-attestation --kind attestation --signature "$requestRoot/qa-attestation.sig"

.venv/Scripts/python.exe -m tools.governance.delivery_approval_authority.signing_requests --root $requestRoot prepare-attestation --role Reviewer --decision APPROVE
openssl pkeyutl -sign -rawin -inkey $env:DAA2_REVIEWER_PEM -in "$requestRoot/reviewer-attestation.message.bin" -out "$requestRoot/reviewer-attestation.sig"
.venv/Scripts/python.exe -m tools.governance.delivery_approval_authority.signing_requests --root $requestRoot attach --name reviewer-attestation --kind attestation --signature "$requestRoot/reviewer-attestation.sig"

.venv/Scripts/python.exe -m tools.governance.delivery_approval_authority.signing_requests --root $requestRoot prepare-attestation --role 'Project Owner' --decision PASS
openssl pkeyutl -sign -rawin -inkey $env:DAA2_PROJECT_OWNER_PEM -in "$requestRoot/project-owner-attestation.message.bin" -out "$requestRoot/project-owner-attestation.sig"
.venv/Scripts/python.exe -m tools.governance.delivery_approval_authority.signing_requests --root $requestRoot attach --name project-owner-attestation --kind attestation --signature "$requestRoot/project-owner-attestation.sig"

.venv/Scripts/python.exe -m tools.governance.delivery_approval_authority.signing_requests --root $requestRoot verify
```

The last command calls the real governed verifier. It emits a bundle only for PASS. Before
the revised profile and signatures exist, FAIL/GOVERNANCE_MODE_UNAUTHORIZED is expected;
the delivery work remains PENDING_EXTERNAL_SIGNATURES. Do not replace that result with PASS.

The manifest records the reused functional QA/Reviewer decisions; actual authenticated
approval remains mandatory in the existing receipt evaluator. Content/schema validation
alone does not release the delivery gate. No IntegrationReceipt is created before canonical
human merge and verified ancestry. STORY-0738 remains open; TASK-0038 remains NOT READY.
