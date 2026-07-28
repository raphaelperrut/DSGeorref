# get_authorization_check — GET /authorization/check

- **API:** `API-002` — Projetos, usuários e autorização
- **Estado do contrato:** `FROZEN`
- **Permissão:** `authorization:check`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetAuthorizationCheckResponse`

## Parâmetros de path

Nenhum.

## Query

- `action` **obrigatório**: `{"type": "string"}`
- `resourceType` **obrigatório**: `{"type": "string"}`
- `resourceId`: `{"type": "string"}`

## Request

Sem corpo.

## Response

- recurso: `AuthorizationDecision`;
- wrapper específico: `GetAuthorizationCheckResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
