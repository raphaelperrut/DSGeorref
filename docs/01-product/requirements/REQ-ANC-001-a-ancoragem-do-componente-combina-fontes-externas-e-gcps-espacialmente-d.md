# REQ-ANC-001 — A ancoragem do componente combina fontes externas e GCPs espacialmente distribuídos com provenance e incerteza

- **Tipo:** `FUNCIONAL`
- **Categoria:** `ANC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-049`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

A ancoragem do componente combina fontes externas e GCPs espacialmente distribuídos com provenance e incerteza

## Rastreabilidade

- **Épicos:** `EPIC-058`, `EPIC-099`
- **Evidência ou teste canônico:** `test_distributed_external_anchor_sources_provenance_uncertainty_and_coverage`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Contexts consumidores:** `BC-005/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
