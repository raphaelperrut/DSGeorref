# get_workspace_entries — GET /workspace/entries

- **API:** `API-003` — Workspace, roots e assets
- **Estado do contrato:** `FROZEN`
- **Permissão:** `workspace_entry:list`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetWorkspaceEntriesResponse`

## Parâmetros de path

Nenhum.

## Query

- `rootId` **obrigatório**: `{"type": "string", "format": "uuid"}`
- `parentId`: `{"type": "string"}`
- `cursor`: `{"type": "string"}`
- `limit`: `{"type": "integer", "minimum": 1, "maximum": 200, "default": 100}`

## Request

Sem corpo.

## Response

- recurso: `WorkspaceEntry`;
- wrapper específico: `GetWorkspaceEntriesResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
