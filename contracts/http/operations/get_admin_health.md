# get_admin_health — GET /admin/health

- **API:** `API-010` — Administração e operação
- **Estado do contrato:** `FROZEN`
- **Permissão:** `admin_health:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetAdminHealthResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `HealthStatus`;
- wrapper específico: `GetAdminHealthResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
