# API-006 — Qualidade, SGV e diagnósticos

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `4`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `GET` | `/attempts/{attemptId}/quality` | `get_attempts_attemptid_quality` | `—` | `GetAttemptsAttemptidQualityResponse` | `quality:read` | `FROZEN` |
| `GET` | `/attempts/{attemptId}/sgv` | `get_attempts_attemptid_sgv` | `—` | `GetAttemptsAttemptidSgvResponse` | `sgv:read` | `FROZEN` |
| `GET` | `/attempts/{attemptId}/deformation` | `get_attempts_attemptid_deformation` | `—` | `GetAttemptsAttemptidDeformationResponse` | `deformation:read` | `FROZEN` |
| `GET` | `/attempts/{attemptId}/diagnostics` | `get_attempts_attemptid_diagnostics` | `—` | `GetAttemptsAttemptidDiagnosticsResponse` | `diagnostic:read` | `FROZEN` |

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
