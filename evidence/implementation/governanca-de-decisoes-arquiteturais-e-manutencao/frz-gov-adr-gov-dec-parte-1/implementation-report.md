# ISSUE-0798 — QA repair implementation evidence

## Candidate and boundary

This repair is layered on rejected candidate
0160efea15c84de1703bcd1df0e551376a1ce892; that commit remains an ancestor and
was not amended. The normative checkpoint remains
d7788e2b45802ddd71d422b440d63984ee8b70d0.

The implementation is limited to validation and evidence for Slice 1/2. It does
not implement ISSUE-0802, ISSUE-0803, ISSUE-0864, ISSUE-0867, ISSUE-0868, or
Slice 2.

## Effective-diff accounting

The rejected candidate's effective diff against origin/main contains 12 files,
not 10. One of those files is the TaskEnvelope control-plane mutation
.codex/tasks/TASK-0688.json, which is not an implementation-plane path in the
TaskEnvelope allowlist.

The repaired candidate is expected to contain 16 effective files:

- one Owner-authorized TaskEnvelope control-plane mutation;
- four contract, documentation, evidence, and mandatory-test files;
- eleven stable Python validation modules.

The control-plane file is governed by the Tech Lead ownership rule for
.codex/tasks/**, is frozen at the normative checkpoint, and is separately
verified by the effective-scope validator. All implementation-plane files
remain subject to the TaskEnvelope allow/deny paths. The validator does not add
the TaskEnvelope to its own allowlist and does not weaken global policy.

## HIGH finding repairs

1. Lifecycle authority and evidence are Git-resolved governed artifacts.
   Closure evidence has typed semantic linkage to the baseline and candidate,
   file-scope-bound authority, ancestry checks, a real Git merge, and an
   append-only closure ledger. Reopening requires a governed substantive
   trigger that resolves distinct candidate and evidence-set artifacts.
2. Decision governance derives classification, identifier history, normative
   owner, supersession, overlap, and Owner approval from governed ADR artifacts
   and history. An existing ADR's Owner gate comes from its accepted base
   authority; caller booleans or newly written approval text do not establish
   authority.
3. ISM validation binds prior/current state to distinct snapshot-history
   endpoints, resolves deltas and tombstones from governed revisions, and
   requires approval records in a Product Owner-authorized path. The applied
   delta must exactly explain the observed transition.
4. Sprint validation derives the canonical SPRINT-001 story selection from the
   governed backlog and AP-008, then computes dependency closure and stable
   topological ordering.
5. Effective TaskEnvelope scope is evaluated with separate, canonical
   control-plane authority and implementation-plane TaskEnvelope scope.

## Regression evidence

The mandatory test module contains nine tests, including negative assertions
for every QA HIGH bypass: nonexistent lifecycle authority, incomplete or
arbitrary closure/reopening evidence, role-shaped evidence outside the role's
governed scope, forged ADR classification, eligibility, Owner authority, early
identifier allocation, unexplained ISM mutation, disconnected snapshots,
invalid tombstones, duplicate or fake delta approval, arbitrary Sprint
selection, and the effective TaskEnvelope scope.

The final mandatory and independent adversarial run completed with 9 passed.
The complete FND run completed with 16 passed. The FND command required
execution outside the filesystem sandbox because the pre-existing ISSUE-0869
test creates a nested TemporaryDirectory at repository root; two sandboxed
attempts each reached 15 passed and failed before an assertion with Windows
permission errors in that temporary fixture.

## Python architecture coverage

tools/check_python_architecture.py scans src/**/*.py; it reports zero scanned
files for these governance modules and therefore is not evidence of their
architecture compliance.

An additional narrow review used the existing repository architecture policy
and the existing branch_points metric against all eleven Python modules in the
authorized implementation package. It scanned 11 files and reported zero
policy errors. This supplements, but does not alter, the global architecture
gate.

## Final validation

- repository validation: PASS;
- architecture review: PASS;
- requirements review: PASS;
- domain-driven design review: PASS;
- ADR review: PASS after removing ignored probe fixtures from workdir;
- specification review: PASS;
- sprint review: PASS;
- global Python architecture: PASS with 0 files scanned;
- narrow Python architecture: PASS with 11 files scanned and 0 findings;
- mandatory/adversarial tests: PASS, 9 tests;
- complete FND regressions: PASS, 16 tests;
- effective scope audit: PASS, 16 files and 0 findings;
- git diff --check: PASS;
- make verify: PASS.

## Schema correction

The rejected schema allowed unversioned caller bytes to stand in for governed
evidence. EvidenceReference now requires a repository path, full source
revision, and digest, and the validator resolves all three as one immutable Git
artifact. Because the new required fields are a breaking contract correction,
the lifecycle schema/profile version is 2.0.0, following SPEC-001 semantic
versioning.
