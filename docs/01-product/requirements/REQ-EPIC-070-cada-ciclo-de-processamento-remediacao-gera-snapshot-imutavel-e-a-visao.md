# REQ-EPIC-070 — Cada ciclo de processamento/remediação gera snapshot imutável e a visão consolidada identifica o resultado vigente por imagem

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-002`
- **Estado:** `PENDING`
- **Gate:** `Data/UX`

## Requisito

Cada ciclo de processamento/remediação gera snapshot imutável e a visão consolidada identifica o resultado vigente por imagem

## Rastreabilidade

- **Épicos:** `EPIC-034`, `EPIC-037`, `EPIC-049`
- **Evidência ou teste canônico:** `test_immutable_snapshots_current_view_historical_metrics`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-012/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
