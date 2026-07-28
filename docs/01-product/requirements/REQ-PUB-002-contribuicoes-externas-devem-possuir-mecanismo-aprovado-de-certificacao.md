# REQ-PUB-002 — Contribuições externas devem possuir mecanismo aprovado de certificação de origem e verificação automatizada

- **Tipo:** `FUNCIONAL`
- **Categoria:** `PUB`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-057`
- **Estado:** `PENDING`
- **Gate:** `Governance/Engineering`

## Requisito

Contribuições externas devem possuir mecanismo aprovado de certificação de origem e verificação automatizada

## Rastreabilidade

- **Épicos:** `EPIC-007`, `EPIC-091`
- **Evidência ou teste canônico:** `test_contribution_origin_dco_signoff_and_inbound_outbound_policy`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
