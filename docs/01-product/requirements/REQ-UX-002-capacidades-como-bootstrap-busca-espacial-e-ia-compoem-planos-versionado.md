# REQ-UX-002 — Capacidades como bootstrap, busca espacial e IA compõem planos versionados e não aparecem como modos duplicados sem justificativa

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `UX`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-014`
- **Estado:** `PENDING`
- **Gate:** `UX/Core`

## Requisito

Capacidades como bootstrap, busca espacial e IA compõem planos versionados e não aparecem como modos duplicados sem justificativa

## Rastreabilidade

- **Épicos:** `EPIC-004`, `EPIC-029`, `EPIC-033`
- **Evidência ou teste canônico:** `test_no_duplicate_modes_processing_plan_roundtrip`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-004/BC-016`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
