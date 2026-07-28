# REQ-HW-001 — Toda release funciona em CPU; GPU é aceleração opcional, declarada e governada sem alterar silenciosamente qualidade ou algoritmo

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `HW`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-037`
- **Estado:** `PENDING`
- **Gate:** `Platform/AI`

## Requisito

Toda release funciona em CPU; GPU é aceleração opcional, declarada e governada sem alterar silenciosamente qualidade ou algoritmo

## Rastreabilidade

- **Épicos:** `EPIC-010`, `EPIC-082`
- **Evidência ou teste canônico:** `test_cpu_baseline_gpu_optional_no_silent_fallback`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Contexts consumidores:** `BC-002/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
