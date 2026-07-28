# post_projects_projectid_jobs — POST /projects/{projectId}/jobs

- **API:** `API-005` — Jobs, attempts e progresso
- **Estado do contrato:** `FROZEN`
- **Permissão:** `job:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `201`
- **Request schema:** `PostProjectsProjectidJobsRequest`
- **Response schema:** `PostProjectsProjectidJobsResponse`

## Parâmetros de path

`projectId`

## Query

Nenhum.

## Request

- `planId` **obrigatório**: `{"type": "string", "format": "uuid"}`
- `executionMode`: `{"type": "string", "enum": ["direct", "worker"], "default": "worker"}`

## Response

- recurso: `Job`;
- wrapper específico: `PostProjectsProjectidJobsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
