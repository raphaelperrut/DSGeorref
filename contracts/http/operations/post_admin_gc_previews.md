# post_admin_gc_previews — POST /admin/gc/previews

- **API:** `API-011` — Backup, retenção e lifecycle
- **Estado do contrato:** `FROZEN`
- **Permissão:** `gc:preview`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostAdminGcPreviewsRequest`
- **Response schema:** `PostAdminGcPreviewsResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `policyVersion` **obrigatório**: `{"type": "string"}`
- `classes`: `{"type": "array", "items": {"type": "string"}}`

## Response

- recurso: `GcPreview`;
- wrapper específico: `PostAdminGcPreviewsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
