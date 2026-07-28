# REQ-MET-001 — Métricas possuem budget de cardinalidade; resultados científicos permanecem no banco/exports e alertas são orientados a sintomas/SLOs

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `MET`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-054`
- **Estado:** `PENDING`
- **Gate:** `Ops/Scale`

## Requisito

Métricas possuem budget de cardinalidade; resultados científicos permanecem no banco/exports e alertas são orientados a sintomas/SLOs

## Rastreabilidade

- **Épicos:** `EPIC-039`, `EPIC-077`
- **Evidência ou teste canônico:** `test_metric_cardinality_budget_and_signal_retention`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
