# REQ-SRC-003 — Fontes externas são integradas por gateway de capacidades com adapters allowlisted, testes de contrato e estados explícitos de suporte

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SRC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-047`
- **Estado:** `PENDING`
- **Gate:** `Providers/Security`

## Requisito

Fontes externas são integradas por gateway de capacidades com adapters allowlisted, testes de contrato e estados explícitos de suporte

## Rastreabilidade

- **Épicos:** `EPIC-041`, `EPIC-058`
- **Evidência ou teste canônico:** `test_provider_capability_contract_allowlist_ssrf_no_purchase`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014/BC-005`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
