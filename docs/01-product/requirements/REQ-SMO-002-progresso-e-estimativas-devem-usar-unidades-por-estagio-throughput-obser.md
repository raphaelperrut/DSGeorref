# REQ-SMO-002 — Progresso e estimativas devem usar unidades por estágio, throughput observado e incerteza explícita

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SMO`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-040`
- **Estado:** `PENDING`
- **Gate:** `Jobs/Web`

## Requisito

Progresso e estimativas devem usar unidades por estágio, throughput observado e incerteza explícita

## Rastreabilidade

- **Épicos:** `EPIC-034`, `EPIC-069`
- **Evidência ou teste canônico:** `test_stage_work_units_progress_eta_range_confidence_replanning_and_unknown_state`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
