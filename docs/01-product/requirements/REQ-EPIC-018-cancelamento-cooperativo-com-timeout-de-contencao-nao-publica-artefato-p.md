# REQ-EPIC-018 — Cancelamento cooperativo com timeout de contenção não publica artefato parcial e preserva resultados não afetados

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-038`
- **Estado:** `PENDING`
- **Gate:** `Jobs/Ops`

## Requisito

Cancelamento cooperativo com timeout de contenção não publica artefato parcial e preserva resultados não afetados

## Rastreabilidade

- **Épicos:** `EPIC-016`, `EPIC-018`, `EPIC-039`
- **Evidência ou teste canônico:** `test_cooperative_cancel_containment_no_partial_publish`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
