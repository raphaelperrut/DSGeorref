# post_provider_searches — POST /provider-searches

- **API:** `API-009` — Providers e aquisição
- **Estado do contrato:** `FROZEN`
- **Permissão:** `provider_search:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostProviderSearchesRequest`
- **Response schema:** `PostProviderSearchesResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `projectId` **obrigatório**: `{"type": "string", "format": "uuid"}`
- `geometry` **obrigatório**: `{"type": "object", "additionalProperties": true}`
- `timeRange`: `{"type": "object", "title": "TimeRange", "additionalProperties": false, "properties": {"start": {"type": ["string", "null"], "format": "date-time"}, "end": {"type": ["string", "null"], "format": "date-time"}}}`
- `providerIds`: `{"type": "array", "items": {"type": "string"}}`

## Response

- recurso: `ProviderSearch`;
- wrapper específico: `PostProviderSearchesResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
