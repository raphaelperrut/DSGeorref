# patch_admin_retention_policies — PATCH /admin/retention-policies

- **API:** `API-011` — Backup, retenção e lifecycle
- **Estado do contrato:** `FROZEN`
- **Permissão:** `retention_policy:update`
- **Idempotência:** `Obrigatória`
- **Success status:** `200`
- **Request schema:** `PatchAdminRetentionPoliciesRequest`
- **Response schema:** `PatchAdminRetentionPoliciesResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `classes` **obrigatório**: `{"type": "object", "additionalProperties": {"type": "object", "title": "RetentionClass", "additionalProperties": false, "properties": {"minimumDays": {"type": "integer", "minimum": 0}, "maximumDays": {"type": ["integer", "null"], "minimum": 0}, "requiresNoReferences": {"type": "boolean"}}, "required": ["minimumDays", "requiresNoReferences"]}}`

## Response

- recurso: `RetentionPolicy`;
- wrapper específico: `PatchAdminRetentionPoliciesResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
