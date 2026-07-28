# REQ-RUNTIME-009 — Sinais operacionais aplicam cardinalidade limitada, redaction e correlação consistente.

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `RUNTIME`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-055`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Sinais operacionais aplicam cardinalidade limitada, redaction e correlação consistente.

## Rastreabilidade

- **Épicos:** `EPIC-039`, `EPIC-076`
- **Evidência ou teste canônico:** `test_runtime_decision_9`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
