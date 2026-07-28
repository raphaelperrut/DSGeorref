# post_projects_projectid_members — POST /projects/{projectId}/members

- **API:** `API-002` — Projetos, usuários e autorização
- **Estado do contrato:** `FROZEN`
- **Permissão:** `project_member:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `201`
- **Request schema:** `PostProjectsProjectidMembersRequest`
- **Response schema:** `PostProjectsProjectidMembersResponse`

## Parâmetros de path

`projectId`

## Query

Nenhum.

## Request

- `userId` **obrigatório**: `{"type": "string", "format": "uuid"}`
- `role` **obrigatório**: `{"type": "string", "enum": ["owner", "editor", "reviewer", "viewer"]}`

## Response

- recurso: `ProjectMember`;
- wrapper específico: `PostProjectsProjectidMembersResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
