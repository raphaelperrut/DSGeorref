# post_admin_drain — POST /admin/drain

- **API:** `API-010` — Administração e operação
- **Estado do contrato:** `FROZEN`
- **Permissão:** `admin_drain:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostAdminDrainRequest`
- **Response schema:** `PostAdminDrainResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `deadlineSeconds` **obrigatório**: `{"type": "integer", "minimum": 30, "maximum": 86400}`
- `reason`: `{"type": "string", "maxLength": 500}`

## Response

- recurso: `DrainOperation`;
- wrapper específico: `PostAdminDrainResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
