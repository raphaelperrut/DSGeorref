# REQ-EST-001 — `USAC_MAGSAC` é o estimador padrão; RANSAC exige seleção antecipada, configuração própria e nunca atua como fallback silencioso

- **Tipo:** `FUNCIONAL`
- **Categoria:** `EST`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-045`
- **Estado:** `PENDING`
- **Gate:** `Geo/Quality`

## Requisito

`USAC_MAGSAC` é o estimador padrão; RANSAC exige seleção antecipada, configuração própria e nunca atua como fallback silencioso

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-051`
- **Evidência ou teste canônico:** `test_usac_magsac_default_explicit_ransac_no_silent_switch`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-006`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
