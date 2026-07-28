# get_processing_plans_planid — GET /processing-plans/{planId}

- **API:** `API-004` — ProcessingPlan e capabilities
- **Estado do contrato:** `FROZEN`
- **Permissão:** `processing_plan:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetProcessingPlansPlanidResponse`

## Parâmetros de path

`planId`

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `ProcessingPlan`;
- wrapper específico: `GetProcessingPlansPlanidResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
