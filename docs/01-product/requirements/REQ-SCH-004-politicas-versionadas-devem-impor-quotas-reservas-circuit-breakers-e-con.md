# REQ-SCH-004 — Políticas versionadas devem impor quotas, reservas, circuit breakers e contenção sem relaxar gates

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SCH`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-039`
- **Estado:** `PENDING`
- **Gate:** `Operations/Security`

## Requisito

Políticas versionadas devem impor quotas, reservas, circuit breakers e contenção sem relaxar gates

## Rastreabilidade

- **Épicos:** `EPIC-040`, `EPIC-068`
- **Evidência ou teste canônico:** `test_policy_quotas_reservations_circuit_breakers_containment_and_effective_priority_audit`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014/BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
