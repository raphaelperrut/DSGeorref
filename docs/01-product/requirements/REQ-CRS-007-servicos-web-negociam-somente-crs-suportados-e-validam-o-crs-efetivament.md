# REQ-CRS-007 — Serviços Web negociam somente CRS suportados e validam o CRS efetivamente retornado pelo provider.

- **Tipo:** `CONTRATO`
- **Categoria:** `CRS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-034`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

Serviços Web negociam somente CRS suportados e validam o CRS efetivamente retornado pelo provider.

## Rastreabilidade

- **Épicos:** `EPIC-058`, `EPIC-096`
- **Evidência ou teste canônico:** `test_web_service_capability_crs_negotiation_and_actual_response_validation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Contexts consumidores:** `BC-005/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
