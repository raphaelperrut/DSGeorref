# REQ-BEX-004 — aplicar classes, fairness, aging e overrides auditados

- **Tipo:** `FUNCIONAL`
- **Categoria:** `BEX`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-012`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

aplicar classes, fairness, aging e overrides auditados

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-018`, `EPIC-019`, `EPIC-034`, `EPIC-037`, `EPIC-065`, `EPIC-066`, `EPIC-067`, `EPIC-068`, `EPIC-069`
- **Evidência ou teste canônico:** `test_batch_execution_decision_04`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-010/BC-016/BC-012`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
