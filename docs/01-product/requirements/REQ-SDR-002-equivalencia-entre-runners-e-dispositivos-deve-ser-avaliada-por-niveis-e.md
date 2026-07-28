# REQ-SDR-002 — Equivalência entre runners e dispositivos deve ser avaliada por níveis e tolerâncias versionadas

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SDR`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Geo/AI/Quality`

## Requisito

Equivalência entre runners e dispositivos deve ser avaliada por níveis e tolerâncias versionadas

## Rastreabilidade

- **Épicos:** `EPIC-024`, `EPIC-028`, `EPIC-050`
- **Evidência ou teste canônico:** `test_tiered_cpu_gpu_runner_numerical_decision_and_artifact_equivalence`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Contexts consumidores:** `BC-007/BC-009`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
