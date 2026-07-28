# REQ-SPRINT-001-010 — liberar primeira fatia funcional somente por cutover explícito após Foundation Gate aprovado

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SPRINT`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-035`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

liberar primeira fatia funcional somente por cutover explícito após Foundation Gate aprovado

## Rastreabilidade

- **Épicos:** `EPIC-001`, `EPIC-002`, `EPIC-086`, `EPIC-110`
- **Evidência ou teste canônico:** `test_sprint_zero_baseline_decision_10`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
