# REQ-EPIC-042 — Cada tipo de código, documentação, dado, modelo e fixture deve possuir licença explícita, SPDX e notices compatíveis

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-002`
- **Estado:** `PENDING`
- **Gate:** `Governance/Release/Security`

## Requisito

Cada tipo de código, documentação, dado, modelo e fixture deve possuir licença explícita, SPDX e notices compatíveis

## Rastreabilidade

- **Épicos:** `EPIC-007`, `EPIC-042`, `EPIC-080`
- **Evidência ou teste canônico:** `test_layered_spdx_reuse_license_notices_dependency_and_asset_compatibility`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
