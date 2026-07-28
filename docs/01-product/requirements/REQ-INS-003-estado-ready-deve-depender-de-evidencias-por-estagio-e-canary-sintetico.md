# REQ-INS-003 — Estado `ready` deve depender de evidências por estágio e canary sintético ponta a ponta

- **Tipo:** `FUNCIONAL`
- **Categoria:** `INS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-034`
- **Estado:** `PENDING`
- **Gate:** `Quality/Operations/Platform`

## Requisito

Estado `ready` deve depender de evidências por estágio e canary sintético ponta a ponta

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-108`
- **Evidência ou teste canônico:** `test_installation_evidence_set_synthetic_canary_offline_readiness_and_failure_codes`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
