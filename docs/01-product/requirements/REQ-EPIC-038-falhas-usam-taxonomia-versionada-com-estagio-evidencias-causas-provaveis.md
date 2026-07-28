# REQ-EPIC-038 — Falhas usam taxonomia versionada com estágio, evidências, causas prováveis, retryability e ações recomendadas seguras

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-002`
- **Estado:** `PENDING`
- **Gate:** `Quality/UX`

## Requisito

Falhas usam taxonomia versionada com estágio, evidências, causas prováveis, retryability e ações recomendadas seguras

## Rastreabilidade

- **Épicos:** `EPIC-030`, `EPIC-036`
- **Evidência ou teste canônico:** `test_failure_taxonomy_evidence_remediation_versioning`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Contexts consumidores:** `BC-012/BC-016`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
