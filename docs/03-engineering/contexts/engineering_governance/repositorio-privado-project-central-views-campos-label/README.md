# EPIC-002 repository integration

`STORY-0009` integrates the already published and consolidated engineering-
governance capability into the repository validation flow. The implementation
is read-only: it does not mutate GitHub, Project, repository configuration,
contracts, database, broker, or product runtime state.

The entry point is
`tools/governance/repositorio-privado-project-central-views-campos-label/repository_integration.py`.
It composes the existing contract validator from `STORY-0008`, requires the
consolidation surface from `STORY-0007`, and derives scope and dependency state
from `TASK-0009` and the canonical story graph. Scientific and product rules
remain owned by their requirements, ADRs, and published contracts; this
integration does not restate or reinterpret them.

## Governing requirement evidence

| Requirement | Normative owner | Canonical test in this integration |
|---|---|---|
| `REQ-CLASSICPROFILE-006` | `ADR-044` | `test_req_classicprofile_006` |
| `REQ-CLASSICPROFILE-008` | `ADR-045` | `test_req_classicprofile_008` |
| `REQ-CLASSICPROFILE-010` | `ADR-044` | `test_req_classicprofile_0010` |
| `REQ-NATIVE-001` | `ADR-042` | `test_req_native_001` |
| `REQ-NATIVE-004` | `ADR-042` | `test_req_native_004` |

Each test verifies the existing requirement document, TaskEnvelope reference,
story assignment, traceability-matrix row, owner, status, and canonical test
identity. It proves integration traceability without creating a second source
of truth for matching, homography, Rasterio/GDAL, or `RasterTile` behavior.

## Fail-closed behavior

Validation returns sorted findings and no success when any required document or
upstream surface is absent; TaskEnvelope, story, matrix, dependency, contract,
or workflow state drifts; a requirement reference or implementation is
duplicated; or a cycle appears in the story DAG or local Python imports. The
negative fixtures execute every case twice and require identical findings.

The workflow runs the existing frozen-contract validator before this entry
point, then executes all requirement and integration tests. Permissions remain
`contents: read`.

Contract, API, persistence, migration, frontend, geospatial runtime, AI, and
broker impact are not applicable. Rollback is a revert of the candidate commit.
Independent QA and Reviewer approval remain required on that exact commit; the
implementation does not self-approve or release `STORY-0010`.
