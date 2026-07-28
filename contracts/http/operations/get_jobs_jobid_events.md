# get_jobs_jobid_events — GET /jobs/{jobId}/events

- **API:** `API-005` — Jobs, attempts e progresso
- **Estado do contrato:** `FROZEN`
- **Permissão:** `job_event:list`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetJobsJobidEventsResponse`

## Parâmetros de path

`jobId`

## Query

- `afterSequence`: `{"type": "integer", "minimum": 0}`
- `limit`: `{"type": "integer", "minimum": 1, "maximum": 500, "default": 100}`

## Request

Sem corpo.

## Response

- recurso: `JobEvent`;
- wrapper específico: `GetJobsJobidEventsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
