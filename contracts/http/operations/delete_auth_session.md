# delete_auth_session — DELETE /auth/session

- **API:** `API-001` — Identidade e sessões
- **Estado do contrato:** `FROZEN`
- **Permissão:** `session:revoke`
- **Idempotência:** `Obrigatória`
- **Success status:** `204`
- **Request schema:** `sem corpo`
- **Response schema:** `sem corpo`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `Session`;
- wrapper específico: `sem corpo`;
- content type de sucesso: `application/json`.

## Erros permitidos

`unauthorized`, `session_not_found`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
