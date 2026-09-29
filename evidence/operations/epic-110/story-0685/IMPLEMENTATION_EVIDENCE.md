# STORY-0685 implementation evidence

## Candidate binding

- `CANDIDATE_SHA: CONTAINING_COMMIT`.
- The authoritative SHA is the commit containing this evidence file and must equal
  the PR #1000 `headRefOid`.
- Verify with `git show <candidate-sha>:evidence/operations/epic-110/story-0685/IMPLEMENTATION_EVIDENCE.md`.
- This evidence supersedes the candidate rejected by Sentinel QA; no prior SHA is
  identified as the current candidate.
- Independent QA for this candidate: `NOT_PERFORMED`.
- Independent Review: `NOT_PERFORMED`.

## Corrected HIGH finding

- Finding: six requirement mappings and six proof entries could pass when the sixth
  item duplicated an existing value.
- Root cause: requirement entries were converted to a dictionary keyed by ID and
  proofs to a set before cardinality validation. Both transformations silently
  discarded duplicate occurrences.
- Correction: validate exact raw-list cardinality and emit a duplicate diagnostic
  before building the dictionary or set.
- Duplicate mapping diagnostic: `DUPLICATE_REQUIREMENT_MAPPING`, including the
  requirement ID, occurrence count, and remediation.
- Duplicate proof diagnostic: `DUPLICATE_PROOF`, including the proof name,
  occurrence count, and remediation.

## Acceptance criteria

| Criterion | Result | Evidence |
|---|---|---|
| AC-ISSUE-0795-01 | PASS | Deterministic read-only JSON report and focused CI workflow remain unchanged. |
| AC-ISSUE-0795-02 | PASS | Exactly five unique requirement/control/test bindings and five unique proofs are required. |
| AC-ISSUE-0795-03 | PASS | Duplicate mapping, duplicate proof, and combined 6/6 regression fail closed in validator and contract sentinel tests. |
| AC-ISSUE-0795-04 | PASS | Repeated invalid executions are byte-identical, do not write files, and emit artifact/code/detail/remediation diagnostics. |

## Commands and results

- Required `test_epic_110_automacao`: `1 passed`.
- Duplicate-focused tests: `4 passed`.
- Complete focused automation module: `11 passed`.
- Frozen contract module with exact cardinality assertions: `12 passed`.
- Valid manifest CLI: `PASS`, five unique requirement bindings, zero findings.
- Ruff format check on the production validator and automation test, plus Ruff lint
  on all three modified Python files: `PASS`.
- mypy on `manifest_validation.py`: `PASS`.
- Task/workflow syntax and `git diff --check`: `PASS`.

## Changed files

- `tools/quality/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/manifest_validation.py`:
  validates raw cardinality and duplicate IDs/proofs before lossy transformations.
- `tests/fnd/governanca-continua-do-backlog-e-decomposicao-de-epico/test_automation.py`:
  reproduces duplicate mapping, duplicate proof, and combined 6/6 behavior,
  including deterministic CLI rejection and actionable diagnostics.
- `tests/fnd/governanca-continua-do-backlog-e-decomposicao-de-epico/test_epic_110_contract.py`:
  requires exact cardinality and uniqueness in the frozen contract sentinel.
- `evidence/operations/epic-110/story-0685/IMPLEMENTATION_EVIDENCE.md`:
  replaces the invalidated evidence for the new containing commit.

## CI finding kept separate

- `validate-epic-110-governance`: `PASS` on the prior candidate after the workflow
  was limited to its three direct dependencies.
- `validate-main-ruleset-controls`: external/preexisting failure in its own global
  dependency installation. Two attempts timed out resolving `python-dateutil>=2.8.2`
  pulled by Celery from `requirements-validation.txt`.
- `verify-foundation`, which used the same global requirements file, passed in the
  same PR run. The ruleset workflow/path is outside ISSUE-0795 ownership, so this
  correction does not mask or modify it.

## Impact and residual risk

- Fail-closed: `VALID` for missing/invalid inputs and duplicate cardinality.
- Diagnostics: `VALID`; duplicate identity/name, occurrence count, and remediation
  are explicit.
- Idempotency: `VALID`; repeated valid and invalid execution is deterministic and
  preserves filesystem snapshots.
- Dry-run: `NOT_APPLICABLE_READ_ONLY`; no mutation path exists.
- Contract impact: `NONE`; the frozen `backlog-governance-profile` `1.0.0` is only
  consumed and validated.
- Migration/rollback: `NOT_APPLICABLE`; no persistent schema/state/deployment change.
- New prerequisite: `NO`.
- Residual risk: the unrelated ruleset gate remains exposed to external package-index
  availability; resolving its global dependency strategy is outside this issue.
