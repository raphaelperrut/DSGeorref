# REQ-AI-005 — Modelos são executados por contrato ModelRunner versionado, com runner, dispositivo, precisão e preprocessamento registrados

- **Tipo:** `FUNCIONAL`
- **Categoria:** `AI`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-052`
- **Estado:** `PENDING`
- **Gate:** `AI/Architecture`

## Requisito

Modelos são executados por contrato ModelRunner versionado, com runner, dispositivo, precisão e preprocessamento registrados

## Rastreabilidade

- **Épicos:** `EPIC-026`, `EPIC-050`
- **Evidência ou teste canônico:** `test_modelrunner_manifest_equivalence_device_precision`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-009`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
