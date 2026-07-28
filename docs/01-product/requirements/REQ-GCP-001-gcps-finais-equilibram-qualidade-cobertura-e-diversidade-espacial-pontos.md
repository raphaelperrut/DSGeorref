# REQ-GCP-001 — GCPs finais equilibram qualidade, cobertura e diversidade espacial; pontos usados/descartados e motivos são exportados

- **Tipo:** `FUNCIONAL`
- **Categoria:** `GCP`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-048`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

GCPs finais equilibram qualidade, cobertura e diversidade espacial; pontos usados/descartados e motivos são exportados

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-052`
- **Evidência ou teste canônico:** `test_spatial_gcp_balance_discard_reasons_conditioning`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
