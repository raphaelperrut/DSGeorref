# get_assets_assetid — GET /assets/{assetId}

- **API:** `API-003` — Workspace, roots e assets
- **Estado do contrato:** `FROZEN`
- **Permissão:** `asset:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetAssetsAssetidResponse`

## Parâmetros de path

`assetId`

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `Asset`;
- wrapper específico: `GetAssetsAssetidResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
