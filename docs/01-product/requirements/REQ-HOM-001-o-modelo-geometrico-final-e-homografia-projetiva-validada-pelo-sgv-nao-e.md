# REQ-HOM-001 — O modelo geométrico final é homografia projetiva validada pelo SGV; não existe fallback oculto para modelos alternativos

- **Tipo:** `FUNCIONAL`
- **Categoria:** `HOM`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-043`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

O modelo geométrico final é homografia projetiva validada pelo SGV; não existe fallback oculto para modelos alternativos

## Rastreabilidade

- **Épicos:** `EPIC-023`, `EPIC-024`
- **Evidência ou teste canônico:** `test_projective_homography_only_no_hidden_fallback`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Contexts consumidores:** `BC-006/BC-007`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
