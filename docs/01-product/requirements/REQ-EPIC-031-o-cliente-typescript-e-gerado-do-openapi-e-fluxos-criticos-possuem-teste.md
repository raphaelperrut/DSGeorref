# REQ-EPIC-031 — O cliente TypeScript é gerado do OpenAPI e fluxos críticos possuem testes de componente, acessibilidade e E2E

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-013`
- **Estado:** `PENDING`
- **Gate:** `Foundation/UX`

## Requisito

O cliente TypeScript é gerado do OpenAPI e fluxos críticos possuem testes de componente, acessibilidade e E2E

## Rastreabilidade

- **Épicos:** `EPIC-004`, `EPIC-031`
- **Evidência ou teste canônico:** `generated_client_component_accessibility_e2e`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-016`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
