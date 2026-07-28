# get_exports_exportid — GET /exports/{exportId}

- **API:** `API-007` — Resultados, artifacts e exports
- **Estado do contrato:** `FROZEN`
- **Permissão:** `export:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetExportsExportidResponse`

## Parâmetros de path

`exportId`

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `ExportJob`;
- wrapper específico: `GetExportsExportidResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
