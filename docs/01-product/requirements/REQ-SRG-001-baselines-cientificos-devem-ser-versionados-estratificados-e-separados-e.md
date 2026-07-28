# REQ-SRG-001 — Baselines científicos devem ser versionados, estratificados e separados entre desenvolvimento, sentinelas e promoção cega

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SRG`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Quality/Geo/AI`

## Requisito

Baselines científicos devem ser versionados, estratificados e separados entre desenvolvimento, sentinelas e promoção cega

## Rastreabilidade

- **Épicos:** `EPIC-028`
- **Evidência ou teste canônico:** `test_layered_versioned_stratified_scientific_baselines_sentinels_and_blind_promotion_set`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
