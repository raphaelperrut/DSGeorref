# REQ-SRG-002 — Seleção de testes deve usar grafo de impacto com tiers obrigatórios e matriz completa em promotion candidates

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SRG`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Quality/Engineering`

## Requisito

Seleção de testes deve usar grafo de impacto com tiers obrigatórios e matriz completa em promotion candidates

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-028`
- **Evidência ou teste canônico:** `test_change_impact_graph_mandatory_tiers_and_full_promotion_matrix`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-007`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
