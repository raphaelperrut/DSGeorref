# get_review_queue — GET /review-queue

- **API:** `API-008` — Revisão e correções
- **Estado do contrato:** `FROZEN`
- **Permissão:** `review_queue:list`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetReviewQueueResponse`

## Parâmetros de path

Nenhum.

## Query

- `projectId`: `{"type": "string", "format": "uuid"}`
- `state`: `{"type": "string", "enum": ["pending", "claimed", "resolved"]}`
- `cursor`: `{"type": "string"}`
- `limit`: `{"type": "integer", "minimum": 1, "maximum": 200, "default": 50}`

## Request

Sem corpo.

## Response

- recurso: `ReviewQueueItem`;
- wrapper específico: `GetReviewQueueResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
