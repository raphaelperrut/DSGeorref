# API-012 — Release, upgrade e suporte

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `4`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `GET` | `/admin/version` | `get_admin_version` | `—` | `GetAdminVersionResponse` | `version:read` | `FROZEN` |
| `POST` | `/admin/upgrades/preflight` | `post_admin_upgrades_preflight` | `PostAdminUpgradesPreflightRequest` | `PostAdminUpgradesPreflightResponse` | `upgrade:preflight` | `FROZEN` |
| `POST` | `/admin/upgrades` | `post_admin_upgrades` | `PostAdminUpgradesRequest` | `PostAdminUpgradesResponse` | `upgrade:execute` | `FROZEN` |
| `POST` | `/admin/support-bundles` | `post_admin_support_bundles` | `PostAdminSupportBundlesRequest` | `PostAdminSupportBundlesResponse` | `support_bundle:create` | `FROZEN` |

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
