# post_admin_upgrades_preflight — POST /admin/upgrades/preflight

- **API:** `API-012` — Release, upgrade e suporte
- **Estado do contrato:** `FROZEN`
- **Permissão:** `upgrade:preflight`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostAdminUpgradesPreflightRequest`
- **Response schema:** `PostAdminUpgradesPreflightResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `targetVersion` **obrigatório**: `{"type": "string"}`
- `imageDigest` **obrigatório**: `{"type": "string", "pattern": "^sha256:[a-f0-9]{64}$"}`

## Response

- recurso: `UpgradePreflight`;
- wrapper específico: `PostAdminUpgradesPreflightResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
