# API-004 — ProcessingPlan e capabilities

- **Estado:** `FROZEN`
- **ADR normativa:** `ADR-010`
- **Operações:** `4`

## Operações

| Método | Path | Operation ID | Request | Response | Permissão | Estado |
|---|---|---|---|---|---|---|
| `POST` | `/projects/{projectId}/processing-plans` | `post_projects_projectid_processing_plans` | `PostProjectsProjectidProcessingPlansRequest` | `PostProjectsProjectidProcessingPlansResponse` | `processing_plan:create` | `FROZEN` |
| `GET` | `/processing-plans/{planId}` | `get_processing_plans_planid` | `—` | `GetProcessingPlansPlanidResponse` | `processing_plan:read` | `FROZEN` |
| `GET` | `/capabilities` | `get_capabilities` | `—` | `GetCapabilitiesResponse` | `capability:list` | `FROZEN` |
| `POST` | `/processing-plans/{planId}/preview` | `post_processing_plans_planid_preview` | `PostProcessingPlansPlanidPreviewRequest` | `PostProcessingPlansPlanidPreviewResponse` | `processing_plan:preview` | `FROZEN` |

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
