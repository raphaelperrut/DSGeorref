# REQ-DIS-001 — Componentes espaciais provisórios usam evidências multimodais versionadas e nunca são tratados como prova de overlap ou aceitação

- **Tipo:** `FUNCIONAL`
- **Categoria:** `DIS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-047`
- **Estado:** `PENDING`
- **Gate:** `Geo/Discovery`

## Requisito

Componentes espaciais provisórios usam evidências multimodais versionadas e nunca são tratados como prova de overlap ou aceitação

## Rastreabilidade

- **Épicos:** `EPIC-054`
- **Evidência ou teste canônico:** `test_provisional_components_never_create_operational_edge`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Contexts consumidores:** `BC-005`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
