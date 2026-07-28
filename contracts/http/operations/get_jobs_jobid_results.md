# get_jobs_jobid_results — GET /jobs/{jobId}/results

- **API:** `API-005` — Jobs, attempts e progresso
- **Estado do contrato:** `FROZEN`
- **Permissão:** `result:list`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetJobsJobidResultsResponse`

## Parâmetros de path

`jobId`

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `ResultSummary`;
- wrapper específico: `GetJobsJobidResultsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
