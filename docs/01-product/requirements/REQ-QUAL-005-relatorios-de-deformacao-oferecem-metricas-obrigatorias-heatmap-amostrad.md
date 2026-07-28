# REQ-QUAL-005 — Relatórios de deformação oferecem métricas obrigatórias, heatmap amostrado e diagnóstico denso sob demanda

- **Tipo:** `FUNCIONAL`
- **Categoria:** `QUAL`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-046`
- **Estado:** `PENDING`
- **Gate:** `Geo/UX`

## Requisito

Relatórios de deformação oferecem métricas obrigatórias, heatmap amostrado e diagnóstico denso sob demanda

## Rastreabilidade

- **Épicos:** `EPIC-034`, `EPIC-038`
- **Evidência ou teste canônico:** `test_deformation_summary_heatmap_dense_consistency`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-007`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
