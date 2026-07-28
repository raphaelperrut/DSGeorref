# REQ-OBS-002 — Telemetria usa contratos OpenTelemetry/backends substituíveis e correlation IDs de request até ArtifactSet, sem se tornar fonte autoritativa

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `OBS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-054`
- **Estado:** `PENDING`
- **Gate:** `Ops`

## Requisito

Telemetria usa contratos OpenTelemetry/backends substituíveis e correlation IDs de request até ArtifactSet, sem se tornar fonte autoritativa

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-039`
- **Evidência ou teste canônico:** `test_opentelemetry_context_propagation_exporter_outage`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
