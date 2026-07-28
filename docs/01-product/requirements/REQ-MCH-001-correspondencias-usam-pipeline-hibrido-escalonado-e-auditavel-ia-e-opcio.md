# REQ-MCH-001 — Correspondências usam pipeline híbrido escalonado e auditável; IA é opcional, explícita e submetida aos mesmos filtros e SGV

- **Tipo:** `FUNCIONAL`
- **Categoria:** `MCH`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-055`
- **Estado:** `PENDING`
- **Gate:** `Geo/AI`

## Requisito

Correspondências usam pipeline híbrido escalonado e auditável; IA é opcional, explícita e submetida aos mesmos filtros e SGV

## Rastreabilidade

- **Épicos:** `EPIC-023`, `EPIC-050`
- **Evidência ou teste canônico:** `test_hybrid_matcher_escalation_provenance_no_ai_installation`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Contexts consumidores:** `BC-006/BC-009`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
