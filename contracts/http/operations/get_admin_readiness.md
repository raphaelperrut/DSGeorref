# get_admin_readiness — GET /admin/readiness

- **API:** `API-010` — Administração e operação
- **Estado do contrato:** `FROZEN`
- **Permissão:** `admin_readiness:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetAdminReadinessResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `ReadinessStatus`;
- wrapper específico: `GetAdminReadinessResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`dependency_unavailable`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
