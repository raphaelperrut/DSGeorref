# REQ-RMR-003 — Exports devem separar resumo, dados técnicos, visualização e bundle de reprodução, preservando lineage e limites de tamanho/licença

- **Tipo:** `FUNCIONAL`
- **Categoria:** `RMR`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-050`
- **Estado:** `PENDING`
- **Gate:** `Reporting/Data`

## Requisito

Exports devem separar resumo, dados técnicos, visualização e bundle de reprodução, preservando lineage e limites de tamanho/licença

## Rastreabilidade

- **Épicos:** `EPIC-037`, `EPIC-102`
- **Evidência ou teste canônico:** `test_layered_summary_technical_visual_reproducibility_export_profiles`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Contexts consumidores:** `BC-012/BC-008`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
