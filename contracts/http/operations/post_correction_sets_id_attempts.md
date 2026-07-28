# post_correction_sets_id_attempts — POST /correction-sets/{id}/attempts

- **API:** `API-008` — Revisão e correções
- **Estado do contrato:** `FROZEN`
- **Permissão:** `attempt:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `201`
- **Request schema:** `PostCorrectionSetsIdAttemptsRequest`
- **Response schema:** `PostCorrectionSetsIdAttemptsResponse`

## Parâmetros de path

`id`

## Query

Nenhum.

## Request

- `processingPlanId` **obrigatório**: `{"type": "string", "format": "uuid"}`

## Response

- recurso: `Attempt`;
- wrapper específico: `PostCorrectionSetsIdAttemptsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
