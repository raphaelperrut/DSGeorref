# post_admin_upgrades — POST /admin/upgrades

- **API:** `API-012` — Release, upgrade e suporte
- **Estado do contrato:** `FROZEN`
- **Permissão:** `upgrade:execute`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostAdminUpgradesRequest`
- **Response schema:** `PostAdminUpgradesResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `preflightId` **obrigatório**: `{"type": "string", "format": "uuid"}`
- `maintenanceWindowId`: `{"type": "string"}`

## Response

- recurso: `UpgradeOperation`;
- wrapper específico: `PostAdminUpgradesResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
