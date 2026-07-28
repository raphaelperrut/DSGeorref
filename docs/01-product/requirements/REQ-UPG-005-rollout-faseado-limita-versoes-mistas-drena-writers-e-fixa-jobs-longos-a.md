# REQ-UPG-005 — Rollout faseado limita versões mistas, drena writers e fixa jobs longos à versão compatível até a conclusão.

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `UPG`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-035`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Rollout faseado limita versões mistas, drena writers e fixa jobs longos à versão compatível até a conclusão.

## Rastreabilidade

- **Épicos:** `EPIC-004`, `EPIC-105`, `EPIC-107`
- **Evidência ou teste canônico:** `test_phased_rollout_limited_mixed_version_window_drain_and_long_job_pinning`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-013/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
