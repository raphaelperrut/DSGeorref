# REQ-ISS-003 — Toda issue deve apontar ADRs/requisitos/riscos/gates ou justificar decisão local reversível

- **Tipo:** `GOVERNANCA`
- **Categoria:** `ISS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-008`
- **Estado:** `PENDING`
- **Gate:** `Governance/Quality`

## Requisito

Toda issue deve apontar ADRs/requisitos/riscos/gates ou justificar decisão local reversível

## Rastreabilidade

- **Épicos:** `EPIC-091`, `EPIC-110`
- **Evidência ou teste canônico:** `test_no_orphan_issue_without_adr_or_local_decision_justification`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
