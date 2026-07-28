# REQ-SCH-003 — GPUs devem usar leases device-aware, budgets de VRAM e fallback somente quando autorizado e explicável

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SCH`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-037`
- **Estado:** `PENDING`
- **Gate:** `AI/Platform`

## Requisito

GPUs devem usar leases device-aware, budgets de VRAM e fallback somente quando autorizado e explicável

## Rastreabilidade

- **Épicos:** `EPIC-050`, `EPIC-068`, `EPIC-082`
- **Evidência ou teste canônico:** `test_device_aware_gpu_leases_vram_budgets_model_residency_and_explicit_fallback`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-009` — Recuperação Assistida por IA e Governança de Modelos.
- **Contexts consumidores:** `BC-009/BC-010/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
