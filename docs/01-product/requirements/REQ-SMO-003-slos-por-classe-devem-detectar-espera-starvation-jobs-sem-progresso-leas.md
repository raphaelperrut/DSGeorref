# REQ-SMO-003 — SLOs por classe devem detectar espera, starvation, jobs sem progresso, leases presos e breakers persistentes

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SMO`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-012`
- **Estado:** `PENDING`
- **Gate:** `Operations/Reliability`

## Requisito

SLOs por classe devem detectar espera, starvation, jobs sem progresso, leases presos e breakers persistentes

## Rastreabilidade

- **Épicos:** `EPIC-040`, `EPIC-069`
- **Evidência ou teste canônico:** `test_class_slos_wait_starvation_stalled_jobs_gpu_lease_and_breaker_recovery_alerts`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014/BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
