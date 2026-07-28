# REQ-ANC-004 — Ancoragem parcial, divisão de subcomponentes e produtos intermediários são representados explicitamente e imutavelmente

- **Tipo:** `FUNCIONAL`
- **Categoria:** `ANC`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-049`
- **Estado:** `PENDING`
- **Gate:** `Geo/Data`

## Requisito

Ancoragem parcial, divisão de subcomponentes e produtos intermediários são representados explicitamente e imutavelmente

## Rastreabilidade

- **Épicos:** `EPIC-046`, `EPIC-099`
- **Evidência ou teste canônico:** `test_partial_anchor_states_subcomponents_and_immutable_artifacts`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
