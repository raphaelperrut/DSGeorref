# ISSUE-0124 implementation evidence

## Outcome and scope

The repository integration is a deterministic, read-only composition of the
merged `STORY-0012` executable foundation and `STORY-0013` control validator.
It emits a machine-readable JSON result for the four `ISSUE-0124` acceptance
criteria and the three EPIC-003 requirements without creating a second owner
for foundation, contract, or automation rules.

The TaskEnvelope control plane was amended first and separately to authorize
the mandatory integration test, workflow checkpoint, and this evidence path.
No prerequisite, issue, contract, ADR, product state, API, schema, migration,
queue, or reusable runtime primitive was created or changed.

## Acceptance evidence

- `AC-ISSUE-0124-01`: the integration CLI emits canonical JSON with issue,
  dependencies, requirements, acceptance criteria, findings, and status.
- `AC-ISSUE-0124-02`: the CLI requires the existing read-only automation proof
  for `REQ-DEL-001`, `REQ-DEV-001`, and `REQ-TOP-001` to pass exactly.
- `AC-ISSUE-0124-03`: negative fixtures cover scope drift, dependency drift,
  disconnected control plane, silent fallback, import cycles, and exact rule
  duplication; each case must fail identically on two executions.
- `AC-ISSUE-0124-04`: integration calls the existing `STORY-0013` validator and
  only adds boundary checks for composition, so foundation business rules are
  not reimplemented; the local import graph and duplicate digests are checked.

## Changed files and scope rationale

- `.codex/tasks/TASK-0014.json`: minimal control-plane authorization, committed
  separately before implementation.
- `.github/workflows/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r.yaml`:
  repository checkpoint for the integration CLI and focused test.
- `tools/governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/repository_integration.py`:
  read-only integration entry point.
- `tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_integration.py`:
  required acceptance and fail-closed coverage.
- `docs/03-engineering/contexts/engineering_governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/README.md`:
  invocation, boundaries, failure semantics, and rollback.
- `evidence/implementation/epic-003/story-0014/implementation-report.md`:
  candidate evidence and handoff record.

## Contract, migration, and operational impact

Contract and migration impact are not applicable. PostgreSQL remains the state
authority and RabbitMQ remains transport-only because this integration does not
write either. The workflow retains `contents: read`; rollback is a revert of
the candidate commit.

## Focused verification results

- `py -3.12 -B tools/governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/repository_integration.py`
  returned `PASS` with zero findings.
- `py -3.12 -B -m pytest -q -p no:cacheprovider tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_integration.py::test_epic_003_integracao`
  returned `1 passed` after hardening.
- `py -3.12 -B -m pytest -q -p no:cacheprovider tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_automation.py::test_epic_003_automacao`
  returned `1 passed`, proving the upstream control surface still passes.
- `git diff --check` returned no whitespace errors.

The Python 3.12 environment emitted the repository-wide pre-existing
`pytest-asyncio` deprecation warning for an unset default fixture loop scope;
it did not change test collection, execution, or status.

## Limitations and next gate

This implementation does not claim independent approval, release G1, or finish
`STORY-0015`. QA and Reviewer must independently validate the exact candidate
SHA. Focused command results and the candidate SHA are reported on the pull
request that carries this file.
