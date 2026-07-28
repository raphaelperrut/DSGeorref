# REQ-EPIC-015 — Mensagens de fila contêm apenas IDs/versionamento; PostgreSQL preserva estado autoritativo e histórico

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-018`
- **Estado:** `PENDING`
- **Gate:** `Core/Data`

## Requisito

Mensagens de fila contêm apenas IDs/versionamento; PostgreSQL preserva estado autoritativo e histórico

## Rastreabilidade

- **Épicos:** `EPIC-015`, `EPIC-016`
- **Evidência ou teste canônico:** `test_small_messages_duplicate_redelivery_authoritative_state`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
