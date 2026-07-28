# REQ-PLN-001 — representar roadmap por horizontes, outcomes e gates, usando datas somente quando justificadas por compromisso real

- **Tipo:** `FUNCIONAL`
- **Categoria:** `PLN`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-016`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

representar roadmap por horizontes, outcomes e gates, usando datas somente quando justificadas por compromisso real

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-110`
- **Evidência ou teste canônico:** `test_roadmap_horizons_outcomes_gates_and_date_exception`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
