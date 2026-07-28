# REQ-WORKER-001 — `TaskEnvelope` é mínimo, versionado e contém somente IDs, versão e contexto técnico indispensável

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `WORKER`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-006`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

`TaskEnvelope` é mínimo, versionado e contém somente IDs, versão e contexto técnico indispensável

## Rastreabilidade

- **Épicos:** `EPIC-002`, `EPIC-014`, `EPIC-039`
- **Evidência ou teste canônico:** `test_req_worker_001`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-010/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
