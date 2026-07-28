# post_projects_projectid_processing_plans — POST /projects/{projectId}/processing-plans

- **API:** `API-004` — ProcessingPlan e capabilities
- **Estado do contrato:** `FROZEN`
- **Permissão:** `processing_plan:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `201`
- **Request schema:** `PostProjectsProjectidProcessingPlansRequest`
- **Response schema:** `PostProjectsProjectidProcessingPlansResponse`

## Parâmetros de path

`projectId`

## Query

Nenhum.

## Request

- `assetIds` **obrigatório**: `{"type": "array", "items": {"type": "string", "format": "uuid"}, "minItems": 1}`
- `profileIds`: `{"type": "array", "items": {"type": "string"}}`
- `providerPolicy`: `{"type": ["string", "null"]}`

## Response

- recurso: `ProcessingPlan`;
- wrapper específico: `PostProjectsProjectidProcessingPlansResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
