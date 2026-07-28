# REQ-SRC-004 — Busca espaciotemporal usa AOI/época/incerteza, expansão limitada, orçamento e ranking explicável persistidos no ProcessingPlan

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SRC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-047`
- **Estado:** `PENDING`
- **Gate:** `Providers/Geo`

## Requisito

Busca espaciotemporal usa AOI/época/incerteza, expansão limitada, orçamento e ranking explicável persistidos no ProcessingPlan

## Rastreabilidade

- **Épicos:** `EPIC-033`, `EPIC-059`
- **Evidência ou teste canônico:** `test_guided_bounded_search_ranking_uncertainty_reproducible`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-005`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
