# API-001 — Identidade e sessões

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `5`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `POST` | `/auth/bootstrap` | `post_auth_bootstrap` | `PostAuthBootstrapRequest` | `PostAuthBootstrapResponse` | `instance:bootstrap` | `FROZEN` |
| `POST` | `/auth/session` | `post_auth_session` | `PostAuthSessionRequest` | `PostAuthSessionResponse` | `session:create` | `FROZEN` |
| `DELETE` | `/auth/session` | `delete_auth_session` | `—` | `—` | `session:revoke` | `FROZEN` |
| `POST` | `/auth/tokens` | `post_auth_tokens` | `PostAuthTokensRequest` | `PostAuthTokensResponse` | `token:create` | `FROZEN` |
| `GET` | `/auth/oidc/callback` | `get_auth_oidc_callback` | `—` | `GetAuthOidcCallbackResponse` | `oidc:callback` | `FROZEN` |

## Invariantes

- requests e responses são específicos por operação;
- toda mutação exige idempotência e, quando revision-aware, `If-Match`;
- erros usam `application/problem+json` e códigos enumerados no arquivo da operação;
- autorização é aplicada no application service, não duplicada em rotas;
- nenhuma implementação pode acrescentar campo, endpoint ou estado não presente no contrato congelado.

## Arquivos normativos

- `contracts/http/openapi.yaml`;
- `contracts/http/operations/`;
- `contracts/http/OPERATION_CATALOG.json`.
