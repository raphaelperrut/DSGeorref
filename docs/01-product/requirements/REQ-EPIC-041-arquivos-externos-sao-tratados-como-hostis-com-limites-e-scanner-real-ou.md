# REQ-EPIC-041 — Arquivos externos são tratados como hostis com limites e scanner real ou fail-closed

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-002`
- **Estado:** `PENDING`
- **Gate:** `Security`

## Requisito

Arquivos externos são tratados como hostis com limites e scanner real ou fail-closed

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-041`
- **Evidência ou teste canônico:** `malicious_file_suite`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
