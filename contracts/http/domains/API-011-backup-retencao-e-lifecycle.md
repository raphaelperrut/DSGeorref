# API-011 — Backup, retenção e lifecycle

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `5`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `POST` | `/admin/backups` | `post_admin_backups` | `PostAdminBackupsRequest` | `PostAdminBackupsResponse` | `backup:create` | `FROZEN` |
| `POST` | `/admin/restores/validate` | `post_admin_restores_validate` | `PostAdminRestoresValidateRequest` | `PostAdminRestoresValidateResponse` | `restore:validate` | `FROZEN` |
| `GET` | `/admin/retention-policies` | `get_admin_retention_policies` | `—` | `GetAdminRetentionPoliciesResponse` | `retention_policy:read` | `FROZEN` |
| `PATCH` | `/admin/retention-policies` | `patch_admin_retention_policies` | `PatchAdminRetentionPoliciesRequest` | `PatchAdminRetentionPoliciesResponse` | `retention_policy:update` | `FROZEN` |
| `POST` | `/admin/gc/previews` | `post_admin_gc_previews` | `PostAdminGcPreviewsRequest` | `PostAdminGcPreviewsResponse` | `gc:preview` | `FROZEN` |

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
