# get_admin_retention_policies — GET /admin/retention-policies

- **API:** `API-011` — Backup, retenção e lifecycle
- **Estado do contrato:** `FROZEN`
- **Permissão:** `retention_policy:read`
- **Idempotência:** `Não aplicável`
- **Success status:** `200`
- **Request schema:** `sem corpo`
- **Response schema:** `GetAdminRetentionPoliciesResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

Sem corpo.

## Response

- recurso: `RetentionPolicy`;
- wrapper específico: `GetAdminRetentionPoliciesResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
