# REQ-ARTLAYOUT-007 — execução usa identidade dedicada e impede escape do root

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `ARTLAYOUT`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-023`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

execução usa identidade dedicada e impede escape do root

## Rastreabilidade

- **Épicos:** `EPIC-026`, `EPIC-078`
- **Evidência ou teste canônico:** `test_req_artlayout_007`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Contexts consumidores:** `BC-013/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
