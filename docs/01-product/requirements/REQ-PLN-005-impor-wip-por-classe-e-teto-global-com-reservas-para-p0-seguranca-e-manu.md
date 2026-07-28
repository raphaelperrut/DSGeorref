# REQ-PLN-005 — impor WIP por classe e teto global com reservas para P0, segurança e manutenção

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `PLN`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-012`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

impor WIP por classe e teto global com reservas para P0, segurança e manutenção

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-110`
- **Evidência ou teste canônico:** `test_wip_class_limits_global_cap_and_emergency_reserve`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
