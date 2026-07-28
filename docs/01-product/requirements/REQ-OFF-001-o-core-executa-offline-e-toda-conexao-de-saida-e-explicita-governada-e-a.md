# REQ-OFF-001 — O core executa offline e toda conexão de saída é explícita, governada e auditável

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `OFF`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-052`
- **Estado:** `PENDING`
- **Gate:** `Platform/Security`

## Requisito

O core executa offline e toda conexão de saída é explícita, governada e auditável

## Rastreabilidade

- **Épicos:** `EPIC-058`, `EPIC-083`
- **Evidência ou teste canônico:** `test_offline_zero_egress_restricted_allowlist_connected_audit`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Contexts consumidores:** `BC-005/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
