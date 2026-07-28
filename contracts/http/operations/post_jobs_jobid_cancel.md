# post_jobs_jobid_cancel — POST /jobs/{jobId}/cancel

- **API:** `API-005` — Jobs, attempts e progresso
- **Estado do contrato:** `FROZEN`
- **Permissão:** `job:cancel`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostJobsJobidCancelRequest`
- **Response schema:** `PostJobsJobidCancelResponse`

## Parâmetros de path

`jobId`

## Query

Nenhum.

## Request

- `reason`: `{"type": "string", "maxLength": 500}`

## Response

- recurso: `AcceptedOperation`;
- wrapper específico: `PostJobsJobidCancelResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
