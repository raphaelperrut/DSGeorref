# REQ-MTD-001 — Extração de metadados marginais é opcional, registra confiança/proveniência e não altera automaticamente o georreferenciamento

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MTD`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-040`
- **Estado:** `PENDING`
- **Gate:** `Metadata/Research`

## Requisito

Extração de metadados marginais é opcional, registra confiança/proveniência e não altera automaticamente o georreferenciamento

## Rastreabilidade

- **Épicos:** `EPIC-032`, `EPIC-048`
- **Evidência ou teste canônico:** `test_optional_metadata_extraction_no_geometry_side_effect`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
