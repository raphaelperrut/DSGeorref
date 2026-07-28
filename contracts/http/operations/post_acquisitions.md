# post_acquisitions — POST /acquisitions

- **API:** `API-009` — Providers e aquisição
- **Estado do contrato:** `FROZEN`
- **Permissão:** `acquisition:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostAcquisitionsRequest`
- **Response schema:** `PostAcquisitionsResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `searchId`: `{"type": "string", "format": "uuid"}`
- `providerId` **obrigatório**: `{"type": "string"}`
- `providerAssetId` **obrigatório**: `{"type": "string"}`
- `projectId` **obrigatório**: `{"type": "string", "format": "uuid"}`

## Response

- recurso: `Acquisition`;
- wrapper específico: `PostAcquisitionsResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
