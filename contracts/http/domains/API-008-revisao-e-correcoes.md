# API-008 — Revisão e correções

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `4`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `GET` | `/review-queue` | `get_review_queue` | `—` | `GetReviewQueueResponse` | `review_queue:list` | `FROZEN` |
| `POST` | `/attempts/{attemptId}/correction-sets` | `post_attempts_attemptid_correction_sets` | `PostAttemptsAttemptidCorrectionSetsRequest` | `PostAttemptsAttemptidCorrectionSetsResponse` | `correction_set:create` | `FROZEN` |
| `POST` | `/correction-sets/{id}/attempts` | `post_correction_sets_id_attempts` | `PostCorrectionSetsIdAttemptsRequest` | `PostCorrectionSetsIdAttemptsResponse` | `attempt:create` | `FROZEN` |
| `GET` | `/results/{id}/comparisons` | `get_results_id_comparisons` | `—` | `GetResultsIdComparisonsResponse` | `result_comparison:read` | `FROZEN` |

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
