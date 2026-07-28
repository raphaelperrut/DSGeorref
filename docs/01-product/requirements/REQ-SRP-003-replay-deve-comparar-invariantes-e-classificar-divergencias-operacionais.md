# REQ-SRP-003 — Replay deve comparar invariantes e classificar divergências operacionais separadamente de resultados científicos

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SRP`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Jobs/Quality/Reporting`

## Requisito

Replay deve comparar invariantes e classificar divergências operacionais separadamente de resultados científicos

## Rastreabilidade

- **Épicos:** `EPIC-037`, `EPIC-104`
- **Evidência ou teste canônico:** `test_invariant_equivalence_divergence_classification_and_first_causal_event`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Contexts consumidores:** `BC-012/BC-010`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
