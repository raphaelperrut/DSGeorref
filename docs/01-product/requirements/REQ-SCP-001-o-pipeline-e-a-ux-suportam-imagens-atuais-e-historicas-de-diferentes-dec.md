# REQ-SCP-001 — O pipeline e a UX suportam imagens atuais e históricas de diferentes décadas, sem restringir o produto ao caso inicial dos anos 1960

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SCP`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Product/Geo`

## Requisito

O pipeline e a UX suportam imagens atuais e históricas de diferentes décadas, sem restringir o produto ao caso inicial dos anos 1960

## Rastreabilidade

- **Épicos:** `EPIC-021`, `EPIC-028`
- **Evidência ou teste canônico:** `test_cross_decade_corpus_and_no_temporal_hardcode`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
