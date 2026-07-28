# get_admin_audit — GET /admin/audit

- **API:** `API-010` — Administração e operação
- **Estado do contrato:** `FROZEN`
- **Permissão:** `audit:list`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetAdminAuditResponse`

## Parâmetros de path

Nenhum.

## Query

- `after`: `{"type": "string", "format": "date-time"}`
- `actorId`: `{"type": "string", "format": "uuid"}`
- `action`: `{"type": "string"}`
- `cursor`: `{"type": "string"}`
- `limit`: `{"type": "integer", "minimum": 1, "maximum": 200, "default": 100}`

## Request

Sem corpo.

## Response

- recurso: `AuditEvent`;
- wrapper específico: `GetAdminAuditResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
