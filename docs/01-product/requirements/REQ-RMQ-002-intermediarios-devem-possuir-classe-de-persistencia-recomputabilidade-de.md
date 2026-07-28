# REQ-RMQ-002 — Intermediários devem possuir classe de persistência, recomputabilidade, dependências, retenção e custo estimado

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `RMQ`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-009`
- **Estado:** `PENDING`
- **Gate:** `Data/Operations`

## Requisito

Intermediários devem possuir classe de persistência, recomputabilidade, dependências, retenção e custo estimado

## Rastreabilidade

- **Épicos:** `EPIC-049`, `EPIC-103`
- **Evidência ou teste canônico:** `test_persistence_classes_recomputability_lineage_retention_and_resume`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
