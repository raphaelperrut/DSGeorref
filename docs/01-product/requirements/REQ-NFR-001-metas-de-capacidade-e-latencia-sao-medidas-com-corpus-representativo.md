# REQ-NFR-001 — Metas de capacidade e latência são medidas com corpus representativo

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `NFR`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-040`
- **Estado:** `PENDING`
- **Gate:** `Release`

## Requisito

Metas de capacidade e latência são medidas com corpus representativo

## Rastreabilidade

- **Épicos:** `EPIC-040`
- **Evidência ou teste canônico:** `test_req_nfr_001`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Contexts consumidores:** `BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
