# REQ-EPIC-037 — Toda imagem do lote possui resultado consultável com nome, diretório relativo, caminho relativo, status e lineage, seja sucesso ou falha

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-002`
- **Estado:** `PENDING`
- **Gate:** `Data/UX`

## Requisito

Toda imagem do lote possui resultado consultável com nome, diretório relativo, caminho relativo, status e lineage, seja sucesso ou falha

## Rastreabilidade

- **Épicos:** `EPIC-030`, `EPIC-034`, `EPIC-037`
- **Evidência ou teste canônico:** `test_success_failure_name_relative_path_exports`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Contexts consumidores:** `BC-012/BC-016`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
