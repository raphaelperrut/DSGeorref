# REQ-MSK-002 — Faixas de voo, marcas fiduciais, datas, legendas e outros metadados marginais são preservados e distinguíveis de fundo vazio

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MSK`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-040`
- **Estado:** `PENDING`
- **Gate:** `Geo/Data`

## Requisito

Faixas de voo, marcas fiduciais, datas, legendas e outros metadados marginais são preservados e distinguíveis de fundo vazio

## Rastreabilidade

- **Épicos:** `EPIC-037`, `EPIC-045`
- **Evidência ou teste canônico:** `test_marginal_metadata_pixels_preserved_and_classified`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Contexts consumidores:** `BC-012/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
