# get_projects_projectid — GET /projects/{projectId}

- **API:** `API-002` — Projetos, usuários e autorização
- **Estado do contrato:** `FROZEN`
- **Permissão:** `project:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetProjectsProjectidResponse`

## Parâmetros de path

`projectId`

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `Project`;
- wrapper específico: `GetProjectsProjectidResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
