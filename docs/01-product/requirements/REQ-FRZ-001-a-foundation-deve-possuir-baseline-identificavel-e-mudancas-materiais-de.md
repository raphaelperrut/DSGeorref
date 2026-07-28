# REQ-FRZ-001 — A Foundation deve possuir baseline identificável e mudanças materiais devem ser orientadas por evidências e supersession explícita

- **Tipo:** `GOVERNANCA`
- **Categoria:** `FRZ`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-057`
- **Estado:** `PENDING`
- **Gate:** `Governance/Architecture`

## Requisito

A Foundation deve possuir baseline identificável e mudanças materiais devem ser orientadas por evidências e supersession explícita

## Rastreabilidade

- **Épicos:** `EPIC-001`, `EPIC-092`
- **Evidência ou teste canônico:** `test_foundation_baseline_digest_controlled_change_and_adr_supersession`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
