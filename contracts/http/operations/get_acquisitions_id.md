# get_acquisitions_id — GET /acquisitions/{id}

- **API:** `API-009` — Providers e aquisição
- **Estado do contrato:** `FROZEN`
- **Permissão:** `acquisition:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetAcquisitionsIdResponse`

## Parâmetros de path

`id`

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `Acquisition`;
- wrapper específico: `GetAcquisitionsIdResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
