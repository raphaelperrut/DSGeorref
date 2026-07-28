# REQ-PROV-001 — Resultados possuem lineage normalizado, manifesto versionado e bundle de reprodução sob demanda

- **Tipo:** `FUNCIONAL`
- **Categoria:** `PROV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-025`
- **Estado:** `PENDING`
- **Gate:** `Data/Research`

## Requisito

Resultados possuem lineage normalizado, manifesto versionado e bundle de reprodução sob demanda

## Rastreabilidade

- **Épicos:** `EPIC-037`, `EPIC-049`
- **Evidência ou teste canônico:** `test_manifest_lineage_reproduction_bundle`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Contexts consumidores:** `BC-012/BC-013`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
