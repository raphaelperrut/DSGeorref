# post_admin_backups — POST /admin/backups

- **API:** `API-011` — Backup, retenção e lifecycle
- **Estado do contrato:** `FROZEN`
- **Permissão:** `backup:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostAdminBackupsRequest`
- **Response schema:** `PostAdminBackupsResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `classes`: `{"type": "array", "items": {"type": "string"}}`
- `label`: `{"type": "string", "maxLength": 160}`

## Response

- recurso: `BackupSet`;
- wrapper específico: `PostAdminBackupsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
