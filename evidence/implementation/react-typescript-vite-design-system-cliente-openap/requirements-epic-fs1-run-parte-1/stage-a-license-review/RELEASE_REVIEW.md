# TASK-0738 Stage A — direct dependency release review

Scope justification: release/license compliance required by dependencies explicitly approved for Stage A.

The exact baseline/candidate comparison introduces nine direct npm dependencies. Installed package.json versions/licenses and upstream LICENSE files were inspected; the JSON report records their exact hashes and lock integrity. All Python declarations remain unchanged. No manifest/lock classification correction is required.

| Package | Exact pin | Classification | Declared license | Included in application build |
|---|---|---|---|---|
| @hey-api/client-fetch | 0.13.1 | runtime | MIT | yes |
| react | 19.2.4 | runtime | MIT | yes |
| react-dom | 19.2.4 | runtime | MIT | yes |
| @hey-api/openapi-ts | 0.87.5 | development_and_validation | MIT | no |
| @oasdiff-js/oasdiff-js | 1.0.0 | development_and_validation | Apache-2.0 | no |
| @types/react | 19.2.14 | development_and_validation | MIT | no |
| @types/react-dom | 19.2.3 | development_and_validation | MIT | no |
| vite | 8.1.5 | development_and_validation | MIT | no |
| yaml | 2.8.3 | development_and_validation | ISC | no |

The direct inventory contains 23 records: three runtime npm dependencies and 20 development/validation dependencies (eight Python and 12 npm). It preserves DIRECT_DECLARED_DEPENDENCIES; transitive dependencies are not presented as direct declarations. The explicit package/license allow-list and runtime set reject unknown packages/licenses, unpinned versions, stale records, scope drift, resolved lock drift and notice drift. Optional/peer dependency declarations also require review.

The canonical notice table adds only the nine new direct packages. Its prior no-redistribution prose and the inventory redistribution field were factually corrected for the Stage A frontend build. Runtime MIT copyright/permission notices must be preserved for redistribution; the reference table is not a substitute for those texts. No additional standalone upstream NOTICE file was found for these direct packages. Vite’s LICENSE.md also describes code bundled into the tool itself; the tool is not shipped in the application bundle.

All 28 added tracked paths in the exact Stage A diff are classified unambiguously by existing license patterns. DEP5 and license-inventory are unchanged and remain equivalent.

The 49 focused governance tests preserve the historical tests and cover every requested failure mode, including unknown packages even when their manifest/inventory/lock agree. Results and exact commands are in license-governance-tests.log and execution-results.json.

[GHSA-hhx9-57xq-r5rw](https://github.com/hey-api/hey-api/security/advisories/GHSA-hhx9-57xq-r5rw), CVE-2026-48819, is MODERATE for @hey-api/openapi-ts 0.87.5. The affected template exists locally. The precompiled Fetch package also contains the vulnerable unused helper; bundle=false alone is not proof of safety. The generated SDK never imports/calls buildClientParams and emits no params.gen.ts. An AST inspection detects the prefix-controlled indexed assignment in the installed transport and zero such assignments in both production and readable inspection builds. The remaining prefix-map expression is unused. Stage A mounts a static shell without forwarding user input or issuing backend requests. The advisory is not applicable to the current output/execution; future imports, configuration, regeneration, bundling or redistribution of unbundled packages require reassessment. No dependency upgrade was made.

This is implementation evidence for foundation validation, not independent QA/reviewer approval or publication approval. The ISSUE-0142 checkpoint remains unchanged with current_decision=BLOCKED. DEPENDENCY_INVENTORY_AND_SBOM remains REQUIRED_AT_RELEASE_CANDIDATE; LEGAL_REVIEW_BEFORE_G6 and SECURITY_LICENSE_RESTORE_COMPATIBILITY_SCIENTIFIC_GATES remain NOT_PROVIDED. DCO candidate-range review is also pending. DG-TASK-0738-A remains PENDING, with no AcceptanceManifest or integration receipt.

Rollback: revert the compliance candidate and its append-only binding record. This restores the historical blocker and does not change frontend behavior, contracts or generated outputs.

Local revalidation: OpenAPI check, semantic diff, typecheck, 17 frontend tests, Chromium tooling test, build, runtime smoke, 55 delivery-gate tests, repository validation, architecture/requirements/DDD/ADR/specification/sprint reviews, dependency/license inventory validation and 49 governance tests all PASS. make verify exits 2 only at the pre-existing FOUNDATION_INTEGRATION=1 requirement for pinned PostgreSQL/RabbitMQ; classification is ENVIRONMENTAL / NONBLOCKING for this compliance pass. No service-dependent completion or release/publication approval is claimed. The initial wrong Chromium environment attempt is retained separately, followed by the successful frontend rerun.
