# REQ-EPIC-017 — Checkpoints somente são reutilizados em fronteiras canônicas quando hashes, schemas, profiles, versões e inputs forem compatíveis

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-038`
- **Estado:** `PENDING`
- **Gate:** `Jobs/Data`

## Requisito

Checkpoints somente são reutilizados em fronteiras canônicas quando hashes, schemas, profiles, versões e inputs forem compatíveis

## Rastreabilidade

- **Épicos:** `EPIC-018`, `EPIC-049`
- **Evidência ou teste canônico:** `test_checkpoint_compatibility_invalidation_lineage`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
