# ISSUE-0798 — Targeted QA repair implementation evidence

## Candidate and boundary

This targeted repair is layered on rejected candidate
58e91cb4b83fa9f92140d51e3a20c94d568b36ae; that commit remains the direct
ancestor and was not amended, reset or rebased. The normative checkpoint remains
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

## Targeted HIGH finding repairs

1. Lifecycle QA evidence must match task, issue and story identity from a
   candidate-resident QA TaskEnvelope. Both the global role policy and that
   TaskEnvelope must authorize the exact evidence path, and the TaskEnvelope must
   govern STORY-0688. A role-shaped file elsewhere under `evidence/qa/**` fails
   closed.
2. Decision governance derives material overlap from candidate ADR decision
   clauses, owned requirements, explicit supersession, the canonical ADR index
   and repository history. Caller-provided `overlapping_adr_ids` is combined with,
   not substituted for, that derived set; an empty list cannot conceal overlap.
3. ISM approval must match task, issue and story identity from a pre-existing
   Product Owner TaskEnvelope. Global product-path ownership, role text and exact
   delta metadata are insufficient without task scope and REQ-ISM-010 authority.
4. Sprint validation derives the canonical SPRINT-001 story selection from the
   governed backlog and AP-008, then computes dependency closure and stable
   topological ordering.
5. Effective TaskEnvelope scope is evaluated with separate, canonical
   control-plane authority and implementation-plane TaskEnvelope scope.

## Regression evidence

The mandatory test module retains nine tests and adds one focused negative
assertion for each remaining bypass: a forged QA record inside `evidence/qa/**`,
a materially overlapping ADR change with an empty caller list, and a forged
Product Owner approval inside `docs/01-product/**`.

## Python architecture coverage

tools/check_python_architecture.py scans src/**/*.py; it reports zero scanned
files for these governance modules and therefore is not evidence of their
architecture compliance.

An additional narrow review used the existing repository architecture policy
and the existing branch_points metric against all eleven Python modules in the
authorized implementation package. It scanned 11 files and reported zero
policy errors. This supplements, but does not alter, the global architecture
gate.

## Targeted validation

- mandatory/adversarial tests: PASS, 9 tests;
- applicable FND regression: PASS, 16 tests (the repository-root temporary
  fixture required the established outside-sandbox Windows rerun);
- three independent attack probes: PASS, all three attacks failed closed;
- TaskEnvelope/file-scope audit: PASS, 7 repair files and 0 findings;
- `git diff --check`: PASS;
- repository-required `make verify`: PASS with `PYTHONUTF8=1` (the initial
  default-Python invocation stopped at its pre-existing Windows cp1252 decoding
  mismatch before completing the architecture review).

## Schema correction

The rejected schema allowed unversioned caller bytes to stand in for governed
evidence. EvidenceReference now requires a repository path, full source
revision, and digest, and the validator resolves all three as one immutable Git
artifact. Because the new required fields are a breaking contract correction,
the lifecycle schema/profile version is 2.0.0, following SPEC-001 semantic
versioning.
