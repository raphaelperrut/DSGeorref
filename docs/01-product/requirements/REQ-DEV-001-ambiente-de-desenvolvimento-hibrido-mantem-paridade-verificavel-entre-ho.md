# REQ-DEV-001 — Ambiente de desenvolvimento híbrido mantém paridade verificável entre host suportado, containers e CI, sem downloads implícitos

- **Tipo:** `FUNCIONAL`
- **Categoria:** `DEV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-001`
- **Estado:** `PENDING`
- **Gate:** `Foundation`

## Requisito

Ambiente de desenvolvimento híbrido mantém paridade verificável entre host suportado, containers e CI, sem downloads implícitos

## Rastreabilidade

- **Épicos:** `EPIC-003`, `EPIC-092`
- **Evidência ou teste canônico:** `test_host_container_ci_contract_and_no_implicit_downloads`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
