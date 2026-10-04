# Identity/access surface — ISSUE-0148 / TASK-0038

This BC-002 feature mounts through `mountFrontendShell` and calls the eight
published SDK functions through the foundation public boundary. It exports
`IdentitySurface` and `mountIdentitySurface`. It creates no client, DTO, schema,
router, provider or authorization policy.

Start the canonical development server with `pnpm --dir src/frontend dev` and
open `/src/contexts/identity_access/features/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/index.html`.
The root Stage A shell remains owned by BC-016; this explicit HTML entrypoint
makes the consumer reachable without changing that owner’s files.

## Published operation mapping

| Operation ID / generated function | UI | Valid success | Failure |
| --- | --- | --- | --- |
| post_auth_bootstrap / postAuthBootstrap | Bootstrap único | 202 + BootstrapStatus; first administrator displayed; does not infer authenticated Session | 409 repeated, 422 invalid, 500; defensive rejection of unauthorized/forbidden and malformed responses |
| post_auth_session / postAuthSession | Sessão local | 202 + complete unexpired Session | 401, 422, 429, 500; no session on failure |
| delete_auth_session / deleteAuthSession | Encerrar sessão | 204; generated Idempotency-Key and If-Match supplied | 401, 404, 500; local confirmation cleared before request, failure never claims server revocation |
| post_auth_tokens / postAuthTokens | Emitir token pessoal | 201 + generated PAT metadata; optional one-time value handled using PersonalAccessTokenWritable | 401, 403, 404, 409, 412, 422, 429, 500; no issuance claim on failure |
| get_auth_oidc_callback / getAuthOidcCallback | Callback OIDC | 200 + linked boolean and complete unexpired Session | 400, 409, 500, 502; no local authentication fallback |
| get_projects_projectid_members / getProjectsProjectidMembers | Membros locais do projeto | 200 + members matching requested project and PageMeta | Published Problem Details, unauthorized/forbidden and malformed data |
| post_projects_projectid_members / postProjectsProjectidMembers | Vincular conta local existente | 201 + matching ProjectMember | Published Problem Details; no general account CRUD |
| get_authorization_check / getAuthorizationCheck | Consultar autorização | 200 + boolean decision, policyVersion, reasonCode; false remains denied | Published Problem Details; no permission inferred from error/unknown data |

The latter three operations have published failures 401, 403, 404, 409, 412,
422, 429 and 500. The shared presentation preserves type, title, status, detail
and instance as text. Reflected submitted secrets and stack traces are redacted;
unstructured or inconsistent errors receive a fixed fail-closed message.

## State and secrets

- API responses, not visual flags, establish the session. Protected actions
  require that response and remain subject to server-side authorization.
- Bootstrap is an attempt, never an availability assertion. A rejected repeat
  stays rejected. No availability endpoint is called.
- Unchanged failed retries retain their idempotency key; editing input or a
  successful new intention creates a new key. The backend owns replay semantics.
- Logout uses the API ETag if received, otherwise an explicitly supplied
  If-Match. The frontend never fabricates a revision.
- No PAT revoke operation exists in this feature. Discarding the displayed
  value does not claim to revoke the server credential.
- Passwords/OIDC parameters stay in form memory only as needed for the attempt;
  successful forms reset. PAT plaintext is kept only for ephemeral display,
  masked initially, and removed on discard, page hide, next operation, logout
  or session expiry. No localStorage/sessionStorage, logging or trace capture.
- Cookies use the generated transport with same-origin credentials. Session
  expiry and auth rejection clear local confirmation and protected results.
  An unknown response, interrupted request or redirect cannot establish access.

## Reproduction

Run from the repository root:

```text
pnpm --dir src/frontend exec vitest run src/contexts/identity_access/features/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/surface.test.tsx --environment jsdom
pnpm --dir src/frontend exec vitest run src/contexts/identity_access/features/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/surface.test.tsx --environment jsdom -t test_epic_008_superficie
pnpm --dir src/frontend typecheck
pnpm --dir src/frontend build
pnpm --dir src/frontend exec playwright test --config src/contexts/identity_access/features/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/playwright.config.ts
```

The canonical build verifies the shared shell. Build this feature's own entry
with Vite's root argument (absolute output under the repository's ignored cache):

```text
pnpm --dir src/frontend exec vite build src/contexts/identity_access/features/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter --outDir <absolute-repo>/node_modules/.cache/identity-access-dist --base ./ --emptyOutDir
```

Unit tests isolate Fetch while consuming the same actual generated SDK. The
browser smoke does not intercept requests: React/Vite sends a real published
session request and verifies fail-closed behavior against the host without an
identity API. This proves executable composition, not backend integration.
The feature adds no backend HTTP adapter. A configured identity HTTP host,
server-side CSRF transport enforcement, TLS/cookies and authoritative services
remain necessary to validate successful backend integration independently.

Independent QA and Reviewer must consume the candidate and implementation
evidence under `evidence/implementation/epic-008/story-0038/`; this implementation
does not approve itself. Rollback is reverting this feature candidate; no
contract or migration changed.
