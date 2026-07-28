# get_attempts_attemptid_diagnostics — GET /attempts/{attemptId}/diagnostics

- **API:** `API-006` — Qualidade, SGV e diagnósticos
- **Estado do contrato:** `FROZEN`
- **Permissão:** `diagnostic:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetAttemptsAttemptidDiagnosticsResponse`

## Parâmetros de path

`attemptId`

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `FailureDiagnostic`;
- wrapper específico: `GetAttemptsAttemptidDiagnosticsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
