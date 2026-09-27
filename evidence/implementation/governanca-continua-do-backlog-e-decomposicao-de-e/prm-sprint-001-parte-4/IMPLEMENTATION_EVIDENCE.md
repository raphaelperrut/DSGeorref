# Implementation evidence — ISSUE-0867 / slice 4/5

## Candidate identity

This evidence belongs to the commit that contains this file. Its immutable SHA is
recorded in the pull request and implementation handoff; QA and Reviewer must use
that exact candidate. This record is implementation evidence, not independent
approval.

## Scope and changed files

- `.codex/tasks/TASK-0757.json` — administrative correction adding the already
  required evidence directory to `allow_paths` and the mirrored Phase F file scope.
- `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/prm-sprint-001-parte-4/foundation-policy.json`
  — local `BC-001` controls for the ten assigned requirements.
- `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/prm-sprint-001-parte-4/HANDOFF.md`
  — traceability, contract impact, risks, limitations and rollback.
- `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/prm-sprint-001-parte-4/policy_validation.py`
  — strict, digest-locked, fail-closed validator.
- `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/prm-sprint-001-parte-4/test_policy_validation.py`
  — ten mandatory tests plus strict-input hardening.
- this append-only evidence record.

No file outside the corrected TaskEnvelope scope is changed. No deny path is
touched. No other slice, requirement, contract, ADR, API, database, queue, frontend,
geo, AI runtime or SGV behavior is implemented.

## Requirement and acceptance evidence

| Requirement | Evidence | Result |
|---|---|---|
| `REQ-PRM-002` | `test_portfolio_materialization_decision_02` | PASS |
| `REQ-PRM-003` | `test_portfolio_materialization_decision_03` | PASS |
| `REQ-PRM-004` | `test_portfolio_materialization_decision_04` | PASS |
| `REQ-PRM-005` | `test_portfolio_materialization_decision_05` | PASS |
| `REQ-PRM-006` | `test_portfolio_materialization_decision_06` | PASS |
| `REQ-PRM-007` | `test_portfolio_materialization_decision_07` | PASS |
| `REQ-PRM-008` | `test_portfolio_materialization_decision_08` | PASS |
| `REQ-PRM-009` | `test_portfolio_materialization_decision_09` | PASS |
| `REQ-PRM-010` | `test_portfolio_materialization_decision_10` | PASS |
| `REQ-SPRINT-001-001` | `test_sprint_zero_baseline_decision_01` | PASS |

- `AC-ISSUE-0867-01`: PASS — all ten requirements have explicit policy and tests.
- `AC-ISSUE-0867-02`: PASS — stable capability path; no production path uses a
  ticket identifier.
- `AC-ISSUE-0867-03`: PASS — each mandatory test mutates its control into a denied
  state; the additional test covers unknown/missing input, duplicate keys, invalid
  root and unavailable file.
- `AC-ISSUE-0867-04`: PASS — `HANDOFF.md` records contracts, risks and rollback.

## Validation results

- Focused slice suite: `11 passed` (ten mandatory tests plus one hardening test).
- Existing canonical evidence rerun: `10 passed` for the exact ten TaskEnvelope test
  names across the established PRM and SPRINT-001 suites.
- Ruff on both new Python files: PASS.
- Mypy on the validator: PASS.
- JSON parsing for TaskEnvelope and policy: PASS.
- `git diff --check`: PASS.
- `make verify PYTHON="py -3.12"`: ENVIRONMENTAL FAIL after Ruff, mypy, frontend
  typecheck/unit/browser, repository validation, architecture, requirements, DDD,
  ADR, specification, sprint, Python architecture, licensing checks and validators
  passed. The unchanged walking-skeleton E2E then stopped before entering its body
  because this host has neither `FOUNDATION_INTEGRATION=1` nor the pinned PostgreSQL
  and RabbitMQ services. Hosted PR CI owns that existing service-backed gate.

The Node engine warning (`22.14.0` locally versus pinned `24.20.0`) did not fail the
frontend gates. The pytest-asyncio default-scope deprecation warning is pre-existing
and did not affect test results.

## Contract impact, risks and rollback

No frozen or public contract is changed. The versioned policy is local
implementation evidence for existing decisions. It does not perform operational
portfolio synchronization; adapters and approved credentials remain outside this
slice. Rollback is a joint revert of the six files above, with no database,
migration, endpoint, queue or Project rollback required.
