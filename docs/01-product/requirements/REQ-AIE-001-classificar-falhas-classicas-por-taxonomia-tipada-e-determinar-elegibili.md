# REQ-AIE-001 — classificar falhas clássicas por taxonomia tipada e determinar elegibilidade neural de forma versionada

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AIE`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-051`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

classificar falhas clássicas por taxonomia tipada e determinar elegibilidade neural de forma versionada

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-014`, `EPIC-022`, `EPIC-024`, `EPIC-028`, `EPIC-039`, `EPIC-041`, `EPIC-050`
- **Evidência ou teste canônico:** `test_ai_escalation_decision_01`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-010/BC-005/BC-007/BC-014/BC-009`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
