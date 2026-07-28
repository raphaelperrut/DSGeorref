# get_auth_oidc_callback — GET /auth/oidc/callback

- **API:** `API-001` — Identidade e sessões
- **Estado do contrato:** `FROZEN`
- **Permissão:** `oidc:callback`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetAuthOidcCallbackResponse`

## Parâmetros de path

Nenhum.

## Query

- `code` **obrigatório**: `{"type": "string"}`
- `state` **obrigatório**: `{"type": "string"}`

## Request

Sem corpo.

## Response

- recurso: `OidcCallbackResult`;
- wrapper específico: `GetAuthOidcCallbackResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`oidc_state_invalid`, `oidc_exchange_failed`, `identity_link_conflict`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
