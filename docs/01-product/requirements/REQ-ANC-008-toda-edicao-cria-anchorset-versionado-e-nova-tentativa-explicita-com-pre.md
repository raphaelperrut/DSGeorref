# REQ-ANC-008 — Toda edição cria AnchorSet versionado e nova tentativa explícita, com preview de impacto e preservação do histórico

- **Tipo:** `FUNCIONAL`
- **Categoria:** `ANC`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-048`
- **Estado:** `PENDING`
- **Gate:** `Geo/Data/Jobs`

## Requisito

Toda edição cria AnchorSet versionado e nova tentativa explícita, com preview de impacto e preservação do histórico

## Rastreabilidade

- **Épicos:** `EPIC-066`, `EPIC-100`
- **Evidência ou teste canônico:** `test_immutable_anchorset_impact_preview_scoped_reoptimization_and_history`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
