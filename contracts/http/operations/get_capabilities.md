# get_capabilities — GET /capabilities

- **API:** `API-004` — ProcessingPlan e capabilities
- **Estado do contrato:** `FROZEN`
- **Permissão:** `capability:list`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetCapabilitiesResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `Capability`;
- wrapper específico: `GetCapabilitiesResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
