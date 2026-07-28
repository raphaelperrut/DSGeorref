# API-003 — Workspace, roots e assets

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `4`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `GET` | `/workspace/roots` | `get_workspace_roots` | `—` | `GetWorkspaceRootsResponse` | `workspace_root:list` | `FROZEN` |
| `GET` | `/workspace/entries` | `get_workspace_entries` | `—` | `GetWorkspaceEntriesResponse` | `workspace_entry:list` | `FROZEN` |
| `POST` | `/projects/{projectId}/assets` | `post_projects_projectid_assets` | `PostProjectsProjectidAssetsRequest` | `PostProjectsProjectidAssetsResponse` | `asset:create` | `FROZEN` |
| `GET` | `/assets/{assetId}` | `get_assets_assetid` | `—` | `GetAssetsAssetidResponse` | `asset:read` | `FROZEN` |

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
