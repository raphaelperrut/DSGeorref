# REQ-TOOL-008 — frontend usa Node 24 LTS e pnpm frozen

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `TOOL`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-014`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

frontend usa Node 24 LTS e pnpm frozen

## Rastreabilidade

- **Épicos:** `EPIC-031`, `EPIC-043`
- **Evidência ou teste canônico:** `test_node_pnpm_lock`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
