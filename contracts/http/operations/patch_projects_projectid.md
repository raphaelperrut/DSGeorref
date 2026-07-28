# patch_projects_projectid — PATCH /projects/{projectId}

- **API:** `API-002` — Projetos, usuários e autorização
- **Estado do contrato:** `FROZEN`
- **Permissão:** `project:update`
- **Idempotência:** `Obrigatória`
- **Success status:** `200`
- **Request schema:** `PatchProjectsProjectidRequest`
- **Response schema:** `PatchProjectsProjectidResponse`

## Parâmetros de path

`projectId`

## Query

Nenhum.

## Request

- `name`: `{"type": "string", "minLength": 1, "maxLength": 160}`
- `description`: `{"type": "string", "maxLength": 2000}`

## Response

- recurso: `Project`;
- wrapper específico: `PatchProjectsProjectidResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
