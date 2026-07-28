# REQ-QUAL-002 — Cada imagem possui métricas, thresholds, gates e versão do QualityProfile auditáveis

- **Tipo:** `FUNCIONAL`
- **Categoria:** `QUAL`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-046`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

Cada imagem possui métricas, thresholds, gates e versão do QualityProfile auditáveis

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-037`
- **Evidência ou teste canônico:** `test_quality_profile_metric_threshold_gate_lineage`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-012`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
