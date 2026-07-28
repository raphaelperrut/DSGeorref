# REQ-PLN-006 — registrar capacidade por faixas, categoria e confiança, sem conversão automática em prazo

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `PLN`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-016`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

registrar capacidade por faixas, categoria e confiança, sem conversão automática em prazo

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-110`
- **Evidência ou teste canônico:** `test_capacity_ranges_availability_throughput_and_no_deadline_conversion`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
