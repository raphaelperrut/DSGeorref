# API-005 — Jobs, attempts e progresso

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `5`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `POST` | `/projects/{projectId}/jobs` | `post_projects_projectid_jobs` | `PostProjectsProjectidJobsRequest` | `PostProjectsProjectidJobsResponse` | `job:create` | `FROZEN` |
| `GET` | `/jobs/{jobId}` | `get_jobs_jobid` | `—` | `GetJobsJobidResponse` | `job:read` | `FROZEN` |
| `POST` | `/jobs/{jobId}/cancel` | `post_jobs_jobid_cancel` | `PostJobsJobidCancelRequest` | `PostJobsJobidCancelResponse` | `job:cancel` | `FROZEN` |
| `GET` | `/jobs/{jobId}/events` | `get_jobs_jobid_events` | `—` | `GetJobsJobidEventsResponse` | `job_event:list` | `FROZEN` |
| `GET` | `/jobs/{jobId}/results` | `get_jobs_jobid_results` | `—` | `GetJobsJobidResultsResponse` | `result:list` | `FROZEN` |

## Invariantes

- requests e responses são específicos por operação;
- toda mutação exige idempotência e, quando revision-aware, `If-Match`;
- erros usam `application/problem+json` e códigos enumerados no arquivo da operação;
- autorização é aplicada no application service, não duplicada em rotas;
- nenhuma implementação pode acrescentar campo, endpoint ou estado não presente no contrato congelado.

## Arquivos normativos

- `contracts/http/openapi.yaml`;
- `contracts/http/operations/`;
- `contracts/http/OPERATION_CATALOG.json`.
