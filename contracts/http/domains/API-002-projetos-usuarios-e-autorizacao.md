# API-002 — Projetos, usuários e autorização

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `7`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `GET` | `/projects` | `get_projects` | `—` | `GetProjectsResponse` | `project:list` | `FROZEN` |
| `POST` | `/projects` | `post_projects` | `PostProjectsRequest` | `PostProjectsResponse` | `project:create` | `FROZEN` |
| `GET` | `/projects/{projectId}` | `get_projects_projectid` | `—` | `GetProjectsProjectidResponse` | `project:read` | `FROZEN` |
| `PATCH` | `/projects/{projectId}` | `patch_projects_projectid` | `PatchProjectsProjectidRequest` | `PatchProjectsProjectidResponse` | `project:update` | `FROZEN` |
| `GET` | `/projects/{projectId}/members` | `get_projects_projectid_members` | `—` | `GetProjectsProjectidMembersResponse` | `project_member:list` | `FROZEN` |
| `POST` | `/projects/{projectId}/members` | `post_projects_projectid_members` | `PostProjectsProjectidMembersRequest` | `PostProjectsProjectidMembersResponse` | `project_member:create` | `FROZEN` |
| `GET` | `/authorization/check` | `get_authorization_check` | `—` | `GetAuthorizationCheckResponse` | `authorization:check` | `FROZEN` |

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
