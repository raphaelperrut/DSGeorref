# REQ-GOV-DEC-002 — somente escolhas arquiteturais independentes, duráveis e caras de reverter recebem ADR própria

- **Tipo:** `GOVERNANCA`
- **Categoria:** `GOV`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-006`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

somente escolhas arquiteturais independentes, duráveis e caras de reverter recebem ADR própria

## Rastreabilidade

- **Épicos:** `EPIC-001`
- **Evidência ou teste canônico:** `test_req_gov_dec_002`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
