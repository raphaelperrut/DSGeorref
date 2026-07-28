# post_projects_projectid_assets — POST /projects/{projectId}/assets

- **API:** `API-003` — Workspace, roots e assets
- **Estado do contrato:** `FROZEN`
- **Permissão:** `asset:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `201`
- **Request schema:** `PostProjectsProjectidAssetsRequest`
- **Response schema:** `PostProjectsProjectidAssetsResponse`

## Parâmetros de path

`projectId`

## Query

Nenhum.

## Request

- `workspaceEntryId` **obrigatório**: `{"type": "string"}`
- `expectedSha256`: `{"type": ["string", "null"], "pattern": "^[a-f0-9]{64}$"}`

## Response

- recurso: `Asset`;
- wrapper específico: `PostProjectsProjectidAssetsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
