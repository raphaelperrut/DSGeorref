# post_admin_restores_validate — POST /admin/restores/validate

- **API:** `API-011` — Backup, retenção e lifecycle
- **Estado do contrato:** `FROZEN`
- **Permissão:** `restore:validate`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostAdminRestoresValidateRequest`
- **Response schema:** `PostAdminRestoresValidateResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `backupSetId` **obrigatório**: `{"type": "string", "format": "uuid"}`
- `targetProfile`: `{"type": "string"}`

## Response

- recurso: `RestoreValidation`;
- wrapper específico: `PostAdminRestoresValidateResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
