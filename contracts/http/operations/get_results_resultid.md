# get_results_resultid — GET /results/{resultId}

- **API:** `API-007` — Resultados, artifacts e exports
- **Estado do contrato:** `FROZEN`
- **Permissão:** `result:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetResultsResultidResponse`

## Parâmetros de path

`resultId`

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `ResultSnapshot`;
- wrapper específico: `GetResultsResultidResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
