# get_provider_searches_id — GET /provider-searches/{id}

- **API:** `API-009` — Providers e aquisição
- **Estado do contrato:** `FROZEN`
- **Permissão:** `provider_search:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetProviderSearchesIdResponse`

## Parâmetros de path

`id`

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `ProviderSearch`;
- wrapper específico: `GetProviderSearchesIdResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
