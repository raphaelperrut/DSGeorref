# get_results_id_comparisons — GET /results/{id}/comparisons

- **API:** `API-008` — Revisão e correções
- **Estado do contrato:** `FROZEN`
- **Permissão:** `result_comparison:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetResultsIdComparisonsResponse`

## Parâmetros de path

`id`

## Query

- `leftSnapshotId` **obrigatório**: `{"type": "string", "format": "uuid"}`
- `rightSnapshotId` **obrigatório**: `{"type": "string", "format": "uuid"}`

## Request

Sem corpo.

## Response

- recurso: `ResultComparison`;
- wrapper específico: `GetResultsIdComparisonsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
