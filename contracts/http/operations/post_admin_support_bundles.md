# post_admin_support_bundles — POST /admin/support-bundles

- **API:** `API-012` — Release, upgrade e suporte
- **Estado do contrato:** `FROZEN`
- **Permissão:** `support_bundle:create`
- **Idempotência:** `Obrigatória`
- **Success status:** `202`
- **Request schema:** `PostAdminSupportBundlesRequest`
- **Response schema:** `PostAdminSupportBundlesResponse`

## Parâmetros de path

Nenhum.

## Query

Nenhum.

## Request

- `redactionProfile` **obrigatório**: `{"type": "string"}`
- `includeLogsHours`: `{"type": "integer", "minimum": 1, "maximum": 168, "default": 24}`

## Response

- recurso: `SupportBundle`;
- wrapper específico: `PostAdminSupportBundlesResponse`;
- content type de sucesso: `application/json`.

## Erros permitidos

`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `precondition_failed`, `rate_limited`, `internal_error`

## Regras

- Nenhum campo não documentado pode ser inferido pelo implementador.
- Falha usa `application/problem+json` e um dos códigos acima.
- Alteração incompatível após freeze segue ADR-026 e ADR-010.
