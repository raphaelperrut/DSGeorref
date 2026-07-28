# REQ-QUAL-001 — O Strong Geometric Verifier opera fail-closed e nenhum resultado é aceito automaticamente quando gate crítico falha ou métrica obrigatória está ausente

- **Tipo:** `FUNCIONAL`
- **Categoria:** `QUAL`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-046`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

O Strong Geometric Verifier opera fail-closed e nenhum resultado é aceito automaticamente quando gate crítico falha ou métrica obrigatória está ausente

## Rastreabilidade

- **Épicos:** `EPIC-024`
- **Evidência ou teste canônico:** `test_fail_closed_missing_metric_and_critical_gate_rejection`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
