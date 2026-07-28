# post_projects — POST /projects

- **API:** `API-002` — Projetos, usuários e autorização
- **Estado do contrato:** `FROZEN`
- **Permissão:** `project:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `201`
- **Request schema:** `PostProjectsRequest`
- **Response schema:** `PostProjectsResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `name` **obrigatório**: `{"type": "string", "minLength": 1, "maxLength": 160}`
- `description`: `{"type": "string", "maxLength": 2000}`

## Response

- recurso: `Project`;
- wrapper específico: `PostProjectsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
