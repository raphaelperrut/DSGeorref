# API-009 — Providers e aquisição

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `5`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `GET` | `/providers` | `get_providers` | `—` | `GetProvidersResponse` | `provider:list` | `FROZEN` |
| `POST` | `/provider-searches` | `post_provider_searches` | `PostProviderSearchesRequest` | `PostProviderSearchesResponse` | `provider_search:create` | `FROZEN` |
| `GET` | `/provider-searches/{id}` | `get_provider_searches_id` | `—` | `GetProviderSearchesIdResponse` | `provider_search:read` | `FROZEN` |
| `POST` | `/acquisitions` | `post_acquisitions` | `PostAcquisitionsRequest` | `PostAcquisitionsResponse` | `acquisition:create` | `FROZEN` |
| `GET` | `/acquisitions/{id}` | `get_acquisitions_id` | `—` | `GetAcquisitionsIdResponse` | `acquisition:read` | `FROZEN` |

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
