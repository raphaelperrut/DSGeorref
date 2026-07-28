# post_auth_session — POST /auth/session

- **API:** `API-001` — Identidade e sessões
- **Estado do contrato:** `FROZEN`
- **Permissão:** `session:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostAuthSessionRequest`
- **Response schema:** `PostAuthSessionResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `username` **obrigatório**: `{"type": "string"}`
- `password` **obrigatório**: `{"type": "string"}`

## Response

- recurso: `Session`;
- wrapper específico: `PostAuthSessionResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`invalid_credentials`, `account_locked`, `rate_limited`, `validation_failed`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
