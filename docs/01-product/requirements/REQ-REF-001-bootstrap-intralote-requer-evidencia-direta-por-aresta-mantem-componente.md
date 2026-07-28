# REQ-REF-001 — Bootstrap intralote requer evidência direta por aresta, mantém componentes desconectados e nunca força georreferenciamento entre imagens disjuntas

- **Tipo:** `FUNCIONAL`
- **Categoria:** `REF`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-040`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

Bootstrap intralote requer evidência direta por aresta, mantém componentes desconectados e nunca força georreferenciamento entre imagens disjuntas

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-053`
- **Evidência ou teste canônico:** `test_disjoint_components_no_forced_edge_per_image_sgv`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-005`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
