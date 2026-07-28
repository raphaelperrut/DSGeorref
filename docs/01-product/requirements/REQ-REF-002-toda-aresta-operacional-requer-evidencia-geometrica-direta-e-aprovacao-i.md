# REQ-REF-002 — Toda aresta operacional requer evidência geométrica direta e aprovação independente da imagem dependente pelo SGV

- **Tipo:** `FUNCIONAL`
- **Categoria:** `REF`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-040`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

Toda aresta operacional requer evidência geométrica direta e aprovação independente da imagem dependente pelo SGV

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-056`
- **Evidência ou teste canônico:** `test_direct_edge_evidence_and_independent_dependent_sgv`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-005`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
