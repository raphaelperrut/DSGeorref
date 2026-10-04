# TASK-0738 Stage A — implementation only

Owner: Frontend / ISSUE-0848. Branch: `codex/issue-0848-stage-a`.
Baseline: `6d52ea0ea5f587e9ee6b57e478c3720282cb7062` (`origin/main`).
Gate: `DG-TASK-0738-A`, definition digest
`5ec3611d42cc10d28564c6f9da2b136043cfdf5c313beddff7613ae84e3bb0f2`.

The Stage A scope was validated using the canonical delivery-gate readiness mode
for TASK-0738 against this baseline. ADR-006/SAR-120 authorize its empty stage
dependency list; the full STORY-0185 dependency remains intact. The clean initial
checkout had one worktree and no other active Codex lane in the observed inventory.
The gate remains PENDING: no independent approval, acceptance manifest, snapshot
of approval, integration receipt or integration has been produced. STORY-0738
remains open; Stage B and ISSUE-0148/TASK-0038 were not implemented. TASK-0038 remains
blocked by this unsatisfied gate.

The minimal React shell mounts from `src/frontend/src/main.tsx`. Consumers use
`contexts/operator_experience/contracts/frontend-shell/index.ts`, which exposes
mount/teardown, optional React content, and the single generated client/SDK.
There are no product workflows, identity screens, map features or manual DTOs.
The shell reads its transport configuration from the generated client at runtime.

Selection and exact pins are recorded in `src/frontend/openapi-client.config.json`
and `pnpm-lock.yaml`: @hey-api/openapi-ts 0.87.5, official precompiled Fetch
transport 0.13.1, and @oasdiff-js/oasdiff-js 1.0.0 / oasdiff 1.15.0. Fetch is not
bundled as TypeScript source because that template fails the existing strict
exactOptionalPropertyTypes gate. The precompiled transport retains that gate;
all DTOs and operation wrappers are generated. No generated file was manually
patched. A scoped js-yaml 4.3.2 override fixes the newly introduced HIGH advisories.

Generation reads only the committed OpenAPI Git blob and rejects working-tree
contract changes (apart from Git line-ending normalization). External references
are rejected before the generator sees the parsed document. The four generated
TypeScript files are versioned in the single authorized generated directory.
`openapi:check` regenerates in an isolated temporary directory and rejects edited,
missing or extra files. Comparisons normalize only Git CRLF/LF text checkout
differences. Production and contract tests import the same generated modules;
temporary generation outputs are never imported by the application or its
contract-consumption tests.

`make-verify.log` records passing generation reproducibility, semantic diff,
strict typecheck, 17 unit/foundation tests (16 foundation), the existing Chromium
tooling test, Vite production build, and the actual shell Chromium smoke. The
smoke opened the production build via Vite preview, observed DSGeorref and the
generated `/api/v1` configuration, and observed no exceptions or API requests.
It required no backend, PostgreSQL or RabbitMQ. It is the actual application,
not a separate test application. Negative semantic tests mutate only isolated
copies: removed operation, newly required request field, removed required response
property and expanded response enum. Identical and documentation-only changes pass.
Missing source, invalid configuration and generated drift fail closed.

Repository/schema, architecture, requirements, DDD, ADR, specification and sprint
validators passed. The existing delivery-gate suite passed 55 tests in make verify.
Additional focused execution, install and read-only contract validation results
are in `execution-results.json` and its referenced logs.

## Blocking finding

`make verify` exits 2 at
`tools/governance/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/foundation_validation.py:543`:
`runtime npm dependencies require release review`.
The same validator additionally requires exact equality with the canonical
dependency inventory and corresponding third-party notices (lines 550–566).
The validator, inventory and THIRD_PARTY_NOTICES.md are outside this task's write
scope. No release review was fabricated and no control was weakened, skipped or
removed. This is GOVERNANCE / BLOCKING, not ENVIRONMENTAL / NONBLOCKING.
The PostgreSQL/RabbitMQ integration checks later in make verify were not reached.
The implementation is preserved as a blocked candidate, not ready for gate acceptance.

## Remaining limits and handoff

Node 24.20.0 and pnpm 10.26.1 were used for final gates. The available Python venv
is 3.12.10 instead of the repository's exact 3.12.13 pin. Initial sandbox failures
(symlinks, temporary renames and browser startup) were rerun outside the Windows
sandbox; they are not substituted for passing gate evidence. CI is configured
in the single authorized workflow; remote CI execution has not occurred.

The dependency audit has one MODERATE advisory for the generator's parameter
template. That template is not emitted with bundle=false, and generated SDK calls
do not use buildClientParams. The official precompiled transport is deprecated;
its eventual replacement requires compatibility testing. The newer generator /
external-transport combinations checked during selection did not preserve the
existing strict typecheck, so they were not adopted. These are disclosed residual
risks, not independent Security/QA/Reviewer approval. The semantic gate implements
the pinned upstream engine's checks; it does not claim exhaustive compatibility
for every OpenAPI/JSON Schema extension or generated-name change.

No HTTP contract, migration, ADR, Owner Decision, Delivery Gate primitive, Story
status or unrelated functional implementation changed. Rollback is a revert of
this isolated implementation candidate and its evidence-only binding commit.
The immutable candidate SHA, complete changed-file list, Git-byte output digests
and execution-log digests are bound after candidate creation under
`evidence/delivery-gates/DG-TASK-0738-A/<candidate_sha>/implementation-evidence.json`.
That record is implementation evidence only, not an AcceptanceManifest.
