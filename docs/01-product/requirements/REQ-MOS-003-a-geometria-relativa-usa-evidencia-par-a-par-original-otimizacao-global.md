# REQ-MOS-003 — A geometria relativa usa evidência par a par original, otimização global e controles de ciclo, drift, foldover e pontes fracas

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MOS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-049`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

A geometria relativa usa evidência par a par original, otimização global e controles de ciclo, drift, foldover e pontes fracas

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-098`
- **Evidência ou teste canônico:** `test_global_relative_alignment_cycle_drift_foldover_and_weak_bridge_split`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
