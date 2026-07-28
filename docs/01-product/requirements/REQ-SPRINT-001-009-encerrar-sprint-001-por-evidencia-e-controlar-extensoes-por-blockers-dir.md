# REQ-SPRINT-001-009 — encerrar SPRINT-001 por evidência e controlar extensões por blockers diretos

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SPRINT`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-008`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

encerrar SPRINT-001 por evidência e controlar extensões por blockers diretos

## Rastreabilidade

- **Épicos:** `EPIC-001`, `EPIC-002`, `EPIC-086`, `EPIC-110`
- **Evidência ou teste canônico:** `test_sprint_zero_baseline_decision_09`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
