# REQ-ISM-009 — limitar spikes por pergunta, budget, evidência e decisão de saída

- **Tipo:** `GOVERNANCA`
- **Categoria:** `ISM`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-006`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

limitar spikes por pergunta, budget, evidência e decisão de saída

## Rastreabilidade

- **Épicos:** `EPIC-110`
- **Evidência ou teste canônico:** `test_req_ism_009`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
