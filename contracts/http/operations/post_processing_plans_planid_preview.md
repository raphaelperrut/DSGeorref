# post_processing_plans_planid_preview — POST /processing-plans/{planId}/preview

- **API:** `API-004` — ProcessingPlan e capabilities
- **Estado do contrato:** `FROZEN`
- **Permissão:** `processing_plan:preview`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostProcessingPlansPlanidPreviewRequest`
- **Response schema:** `PostProcessingPlansPlanidPreviewResponse`

## Parâmetros de path

`planId`

## Query

Nenhum.

## Request

- `hardwareProfile`: `{"type": ["string", "null"]}`
- `includeProviderSearch`: `{"type": "boolean", "default": false}`

## Response

- recurso: `PlanPreview`;
- wrapper específico: `PostProcessingPlansPlanidPreviewResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
