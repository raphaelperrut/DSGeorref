# REQ-OSS-001 — Código novo publicado sob licença open source aprovada, com notices e inventário de dependências

- **Tipo:** `GOVERNANCA`
- **Categoria:** `OSS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-056`
- **Estado:** `PENDING`
- **Gate:** `Governance`

## Requisito

Código novo publicado sob licença open source aprovada, com notices e inventário de dependências

## Rastreabilidade

- **Épicos:** `EPIC-007`, `EPIC-042`
- **Evidência ou teste canônico:** `license_and_dependency_inventory`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
