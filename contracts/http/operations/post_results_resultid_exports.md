# post_results_resultid_exports — POST /results/{resultId}/exports

- **API:** `API-007` — Resultados, artifacts e exports
- **Estado do contrato:** `FROZEN`
- **Permissão:** `export:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostResultsResultidExportsRequest`
- **Response schema:** `PostResultsResultidExportsResponse`

## Parâmetros de path

`resultId`

## Query

Nenhum.

## Request

- `profile` **obrigatório**: `{"type": "string"}`
- `includeReport`: `{"type": "boolean", "default": true}`

## Response

- recurso: `ExportJob`;
- wrapper específico: `PostResultsResultidExportsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
