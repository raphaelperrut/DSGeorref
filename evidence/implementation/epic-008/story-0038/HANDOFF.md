# ISSUE-0148 / TASK-0038 implementation handoff

Final verification: 42 focused tests, mandatory surface test, frontend typecheck,
canonical/feature builds, real Chromium dev/production smoke, repository
validation and full `make verify` PASS (raw exit 0). Successful identity HTTP-host
integration remains `ENVIRONMENTAL_NOT_AVAILABLE`, as detailed below.

This is implementation evidence for independent QA and Reviewer. It records no
approval, merge, issue closure or production readiness decision.

Baseline: `7d60a213a9286aa34ad20f5204890ece13e2f35f`.
Branch: `codex/issue-0148-task-0038`.
The candidate is the single commit containing this handoff, the validation
report and the feature. Resolve its exact SHA with:

```text
git log -1 --format=%H -- evidence/implementation/epic-008/story-0038/VALIDATION-REPORT.json
```

The same SHA is reported in the implementation response. The containing-commit
binding avoids an impossible self-referential Git hash. Any subsequent code
change needs new QA/review evidence for its new candidate.

## Delivered surface and published boundaries

The BC-002 entrypoint exports `IdentitySurface` and `mountIdentitySurface`, uses
the existing public `mountFrontendShell`, and consumes the canonical public
`api`/`client`. No foundation ownership was acquired. The generated artifact,
HTTP contract, backend, TASK-0738, DG-TASK-0738-A and Stage A evidence are unchanged.

All eight flows are reachable in the actual React app. Start the canonical Vite
server and open:

```text
/src/contexts/identity_access/features/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/index.html
```

The feature has its own production HTML entrypoint because the root shell is
outside the consumer write scope. The feature build and production preview were
tested separately from the canonical root shell build.

| Generated operation | Observable flow | Authority / failure handling |
| --- | --- | --- |
| postAuthBootstrap | Attempt initial administrator creation | 202 BootstrapStatus shown; no implicit session; repeat/invalid attempts remain rejected; no availability query |
| postAuthSession | Start local session | Only complete, unexpired Session in a valid 202 response confirms local session |
| deleteAuthSession | End session | Idempotency-Key and explicit/API ETag If-Match; local confirmation cleared before request; only 204 confirms server completion |
| postAuthTokens | Issue PAT | 201 metadata; optional one-time value masked and ephemeral; no revoke flow |
| getAuthOidcCallback | Validate server OIDC callback parameters | 200 callback with complete Session; no provider, discovery, client secret or local fallback |
| getProjectsProjectidMembers | List project members | Valid 200 page scoped to requested project; server authorization remains authoritative |
| postProjectsProjectidMembers | Link existing local account to project | Explicit selected role; valid matching 201 member; no invented account CRUD |
| getAuthorizationCheck | Inspect authorization decision | Boolean false stays denied; no success on unknown/malformed decision |

The [feature README](../../../../src/frontend/src/contexts/identity_access/features/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/README.md)
maps operation IDs, success statuses, published errors and reproduction commands.

## Acceptance evidence

| Criterion | Implementation evidence |
| --- | --- |
| AC-ISSUE-0148-01 | Mandatory surface render test, all eight forms, built feature, Chromium dev/production smoke and recorded visual inspection |
| AC-ISSUE-0148-02 | This candidate-bound handoff, validation report, actual command logs and SHA-256 manifest |
| AC-ISSUE-0148-03 | 42 focused tests cover auth rejection, repeated bootstrap, session expiry, token errors, OIDC failure, denied authorization, malformed data and no secret logging/storage |
| AC-ISSUE-0148-04 | Same generated client; stable keys for unchanged failed mutation retries; server If-Match; authorization remains server-owned; structured Problem Details preserved |

These criteria are architectural controls in the current acceptance traceability
CSV; it associates no additional individual requirement IDs with this issue.
This handoff does not fabricate such mappings.

Problem Details retain available `type`, `title`, `status`, `detail`, `instance`
and contract `code`. Known reflected submitted secrets and stack traces are
redacted. Malformed/unstructured responses cannot authenticate or authorize.
401/403, malformed results, session expiry and logout clear local confirmation
and protected results. Other structured operation errors cannot grant access or
claim completion. Authorization is checked again by the backend per operation.

Tokens are never logged or stored persistently. The optional generated writable
PAT value exists only for explicit one-time display, masked initially, and is
discarded on page hide, another operation, logout, expiry or user discard. The local-cache
screenshot was captured before filling any credentials and visually inspected;
no PNG asset is delivered in canonical evidence. Browser traces and
videos are disabled. No token value or real credential is included in evidence.

## Runtime limits and independent QA

The browser tests use no request interception or API stubs. They execute a real
`POST /api/v1/auth/session` through the canonical SDK against Vite/preview, observe
HTTP 404 without an API host, and prove that protected controls stay disabled.
They prove executable UI-to-generated-client-to-published-HTTP-path composition.
They do not prove successful identity backend integration.

`RUNTIME_BACKEND_INTEGRATION = ENVIRONMENTAL_NOT_AVAILABLE`: this checkout has
identity application/domain/database adapters but no configured identity HTTP
host composing these published routes. The engineering walking skeleton is not
an identity API. Starting PostgreSQL/RabbitMQ alone cannot provide that host.
No backend adapter or endpoint was invented to hide this limitation.

QA must validate successful flows against the authorized identity HTTP host,
including same-origin TLS/cookies, authoritative session expiry, server CSRF
transport/enforcement, logout ETag/If-Match and OIDC state/exchange rejection.
The published response has a csrfToken but no specified frontend request-header
mapping; this feature does not invent one. Unit tests demonstrate contract
success/error composition with Fetch isolated while keeping the real SDK.

See [VALIDATION-REPORT.json](VALIDATION-REPORT.json) for final command outcomes,
make verification classification, baseline readiness, cleanup audit, changed
paths and content digests. The original make attempt's environmental failure and the corrected optional
screenshot asset-license failure are retained. A final attempt uses disposable
pinned foundation services where available. No Stage A-only failure classifier is applied to this consumer.

Rollback is reverting this feature candidate. No migration, contract or generated
client rollback is needed. No production or operational gate is claimed.
