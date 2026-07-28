# API-007 — Resultados, artifacts e exports

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `4`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `GET` | `/results/{resultId}` | `get_results_resultid` | `—` | `GetResultsResultidResponse` | `result:read` | `FROZEN` |
| `GET` | `/artifact-sets/{artifactSetId}/manifest` | `get_artifact_sets_artifactsetid_manifest` | `—` | `GetArtifactSetsArtifactsetidManifestResponse` | `artifact_manifest:read` | `FROZEN` |
| `POST` | `/results/{resultId}/exports` | `post_results_resultid_exports` | `PostResultsResultidExportsRequest` | `PostResultsResultidExportsResponse` | `export:create` | `FROZEN` |
| `GET` | `/exports/{exportId}` | `get_exports_exportid` | `—` | `GetExportsExportidResponse` | `export:read` | `FROZEN` |

## Invariantes

- requests e responses são específicos por operação;
- toda mutação exige idempotência e, quando revision-aware, `If-Match`;
- erros usam `application/problem+json` e códigos enumerados no arquivo da operação;
- autorização é aplicada no application service, não duplicada em rotas;
- nenhuma implementação pode acrescentar campo, endpoint ou estado não presente no contrato congelado.

## Arquivos normativos

- `contracts/http/openapi.yaml`;
- `contracts/http/operations/`;
- `contracts/http/OPERATION_CATALOG.json`.
