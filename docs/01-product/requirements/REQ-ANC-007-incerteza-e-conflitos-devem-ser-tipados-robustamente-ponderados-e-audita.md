# REQ-ANC-007 — Incerteza e conflitos devem ser tipados, robustamente ponderados e auditáveis, sem média silenciosa ou confiança ilimitada

- **Tipo:** `FUNCIONAL`
- **Categoria:** `ANC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-055`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

Incerteza e conflitos devem ser tipados, robustamente ponderados e auditáveis, sem média silenciosa ou confiança ilimitada

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-100`
- **Evidência ou teste canônico:** `test_anchor_uncertainty_robust_weighting_conflict_quarantine_and_split`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
