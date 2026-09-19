# Issue #972 / REMEDIATION-01 — ruleset reconciliation evidence

Date: 2026-09-19  
Repository: `raphaelperrut/DSGeorref`  
Ruleset: `main` / ID `19942009`

## Visibility decision

- Effective repository state: `visibility=public`, `private=false`.
- The Owner confirmed that public visibility is intentional at present.
- The discrepancy between the earlier declaration and the API state is resolved.
- The historical EPIC-002 requirement for a private repository remains unsatisfied.
- Maintaining or replacing that historical requirement requires formal baseline reconciliation; this remediation does not claim it as implemented.
- The decision is recorded in Issue #972 at <https://github.com/raphaelperrut/DSGeorref/issues/972#issuecomment-5745178186>.

## Preconditions

- Default branch: `main`.
- Local starting SHA and remote `main`: `acc30e5edadb3f3c7888dc57af48ee9df0ee1d61`.
- Administrative access: API returned `permissions.admin=true`.
- Worktree was clean before the dedicated branch `codex/issue-0972-ruleset-remediation` was created.
- Concurrent-edit guard: immediately before PUT, `updated_at` still equalled `2026-09-19T14:22:11.830-03:00`; the update would have stopped on mismatch.
- Lockout check: required approvals remained `0`, Code Owner review remained disabled, bypass remained empty, and both required contexts had a successful GitHub Actions producer before the update.

## Required-check producers

Both contexts were present exactly once on PR candidate SHA `ad082015b8a260c90b8b5cb4d7e5423bf7c7a35e`, were emitted by GitHub Actions (`integration_id=15368`), and completed successfully:

| Context | Versioned producer | Successful hosted run |
|---|---|---|
| `verify-foundation` | `.github/workflows/ci.yml`, job `verify-foundation` | <https://github.com/raphaelperrut/DSGeorref/actions/runs/35466249595> |
| `validate-main-ruleset-controls` | `.github/workflows/ruleset-de-main-checks-unicos-codeowners-politica-de-b.yaml`, job `validate-main-ruleset-controls` | <https://github.com/raphaelperrut/DSGeorref/actions/runs/35466249698> |

The check-runs API returned one check run for each context on that SHA. No integration ID was inferred or invented.

## Before and after

The complete pre-update snapshot is preserved in the Issue #972 comment linked above.

| Field | Before | After |
|---|---|---|
| `enforcement` | `active` | `active` |
| `target` | `branch` | `branch` |
| include | `~DEFAULT_BRANCH` | `~DEFAULT_BRANCH` |
| deletion | enabled | enabled |
| non-fast-forward / force-push block | enabled | enabled |
| pull request | required | required |
| conversation resolution | required | required |
| required approvals | `0` | `0` |
| Code Owner review | disabled | disabled |
| bypass actors | empty | empty |
| `verify-foundation` | required, integration `15368` | required, integration `15368` |
| `validate-main-ruleset-controls` | absent | required, integration `15368` |
| linear history | required | absent |

Effective post-update `updated_at`: `2026-09-19T17:46:52.119-03:00`.

## Ruleset diff and rationale

```diff
 required_status_checks:
   - context: verify-foundation
     integration_id: 15368
+  - context: validate-main-ruleset-controls
+    integration_id: 15368
-required_linear_history
```

All other rules and parameters were copied from the immediately preceding remote snapshot into the full PUT payload.

`required_linear_history` was removed because the hardening guide permits it only when merge commits are not used. The repository has `allow_merge_commit=true`, the pull-request rule allows `merge`, and recent first-parent history contains canonical merge commits. No later conflicting decision was found in the artifacts scoped by Issue #972.

## Independent post-update verification

A fresh GET of `/repos/raphaelperrut/DSGeorref/rulesets/19942009` confirmed the post-update state rather than relying on the PUT response. A separate GET of `/repos/raphaelperrut/DSGeorref/rules/branches/main` showed that ruleset `19942009` effectively applies to `main` and exposes deletion, non-fast-forward, pull-request, conversation-resolution, solo-mode, and both required-check controls.

## Enforcement evidence

PR <https://github.com/raphaelperrut/DSGeorref/pull/983> is the dedicated enforcement proof. On its first candidate, `validate-main-ruleset-controls` passed and `verify-foundation` failed because the initial TaskEnvelope location was interpreted as an invalid extension of the historical 761-task catalog. The ruleset kept the PR blocked. The envelope was then moved into this issue-scoped evidence directory without modifying the historical catalog; final hosted results are recorded on the PR and Issue #972.

Direct push, force push, deletion, and unauthorized bypass are configured fail-closed and are shown as effective rules on `main`. Destructive negative operations against `main` were not attempted. Until an independently safe rejection trace exists, actual rejection for those operations is classified `NOT_PROVEN`; configuration and applicability are `PROVEN_BY_API`.

## Residual risks and owner decision

- Historical private-repository requirement: `OPEN`; the Owner must formally retain or replace it in the normative baseline.
- Safe operational rejection traces for direct push, force push, deletion, and bypass: `NOT_PROVEN`; no destructive action was attempted against `main`.
- No change was made to EPIC #2, EPIC #10, EPIC-110 status, secret scanning, push protection, workflows, or product code.

## Focused validations

- TaskEnvelope schema validation: passed.
- Versioned ruleset artifacts and workflow producers: inspected.
- Remote precondition and concurrent-edit guards: passed.
- Independent ruleset GET: passed.
- Effective rules for `main` GET: passed.
- Focused automation and integration tests: `2 passed`.
- Hosted PR checks: see PR #983 final candidate and Issue #972.
