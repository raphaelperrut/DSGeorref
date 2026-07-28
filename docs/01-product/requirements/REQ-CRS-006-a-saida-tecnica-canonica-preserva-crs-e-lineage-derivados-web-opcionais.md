# REQ-CRS-006 — A saída técnica canônica preserva CRS e lineage; derivados Web opcionais não substituem o artifact técnico.

- **Tipo:** `CONTRATO`
- **Categoria:** `CRS`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-025`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

A saída técnica canônica preserva CRS e lineage; derivados Web opcionais não substituem o artifact técnico.

## Rastreabilidade

- **Épicos:** `EPIC-044`, `EPIC-096`
- **Evidência ou teste canônico:** `test_technical_canonical_output_and_optional_web_derivative_lineage`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Contexts consumidores:** `BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
