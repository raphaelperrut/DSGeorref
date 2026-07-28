# API-010 — Administração e operação

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `5`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `GET` | `/admin/health` | `get_admin_health` | `—` | `GetAdminHealthResponse` | `admin_health:read` | `FROZEN` |
| `GET` | `/admin/readiness` | `get_admin_readiness` | `—` | `GetAdminReadinessResponse` | `admin_readiness:read` | `FROZEN` |
| `GET` | `/admin/resources` | `get_admin_resources` | `—` | `GetAdminResourcesResponse` | `admin_resource:read` | `FROZEN` |
| `POST` | `/admin/drain` | `post_admin_drain` | `PostAdminDrainRequest` | `PostAdminDrainResponse` | `admin_drain:create` | `FROZEN` |
| `GET` | `/admin/audit` | `get_admin_audit` | `—` | `GetAdminAuditResponse` | `audit:list` | `FROZEN` |

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
