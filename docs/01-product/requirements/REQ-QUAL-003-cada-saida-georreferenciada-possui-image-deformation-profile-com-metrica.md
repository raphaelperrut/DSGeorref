# REQ-QUAL-003 — Cada saída georreferenciada possui Image Deformation Profile com métricas de deformação entrada→saída, flags críticas e diagnóstico visual sob demanda

- **Tipo:** `FUNCIONAL`
- **Categoria:** `QUAL`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-046`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

Cada saída georreferenciada possui Image Deformation Profile com métricas de deformação entrada→saída, flags críticas e diagnóstico visual sob demanda

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-034`, `EPIC-037`
- **Evidência ou teste canônico:** `test_input_output_deformation_profile_and_heatmap`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-016/BC-012`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
