# post_attempts_attemptid_correction_sets — POST /attempts/{attemptId}/correction-sets

- **API:** `API-008` — Revisão e correções
- **Estado do contrato:** `FROZEN`
- **Permissão:** `correction_set:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `201`
- **Request schema:** `PostAttemptsAttemptidCorrectionSetsRequest`
- **Response schema:** `PostAttemptsAttemptidCorrectionSetsResponse`

## Parâmetros de path

`attemptId`

## Query

Nenhum.

## Request

- `gcps` **obrigatório**: `{"type": "array", "items": {"type": "object", "title": "GcpInput", "additionalProperties": false, "properties": {"source": {"type": "array", "prefixItems": [{"type": "number"}, {"type": "number"}], "minItems": 2, "maxItems": 2}, "target": {"type": "array", "prefixItems": [{"type": "number"}, {"type": "number"}], "minItems": 2, "maxItems": 2}, "uncertainty": {"type": ["number", "null"], "minimum": 0}}, "required": ["source", "target"]}, "minItems": 1}`
- `comment`: `{"type": "string", "maxLength": 2000}`

## Response

- recurso: `CorrectionSet`;
- wrapper específico: `PostAttemptsAttemptidCorrectionSetsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
