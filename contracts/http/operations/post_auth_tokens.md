# post_auth_tokens — POST /auth/tokens

- **API:** `API-001` — Identidade e sessões
- **Estado do contrato:** `FROZEN`
- **Permissão:** `token:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `201`
- **Request schema:** `PostAuthTokensRequest`
- **Response schema:** `PostAuthTokensResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `name` **obrigatório**: `{"type": "string", "minLength": 1, "maxLength": 100}`
- `scopes` **obrigatório**: `{"type": "array", "items": {"type": "string"}, "minItems": 1}`
- `expiresAt`: `{"type": ["string", "null"], "format": "date-time"}`

## Response

- recurso: `PersonalAccessToken`;
- wrapper específico: `PostAuthTokensResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
