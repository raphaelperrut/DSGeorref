# post_auth_bootstrap — POST /auth/bootstrap

- **API:** `API-001` — Identidade e sessões
- **Estado do contrato:** `FROZEN`
- **Permissão:** `instance:bootstrap`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostAuthBootstrapRequest`
- **Response schema:** `PostAuthBootstrapResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `username` **obrigatório**: `{"type": "string", "minLength": 3}`
- `password` **obrigatório**: `{"type": "string", "minLength": 12}`
- `displayName` **obrigatório**: `{"type": "string", "minLength": 1}`

## Response

- recurso: `BootstrapStatus`;
- wrapper específico: `PostAuthBootstrapResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`bootstrap_already_completed`, `password_policy_failed`, `validation_failed`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
