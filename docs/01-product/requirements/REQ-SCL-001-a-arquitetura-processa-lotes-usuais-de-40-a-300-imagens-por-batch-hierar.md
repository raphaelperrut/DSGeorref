# REQ-SCL-001 — A arquitetura processa lotes usuais de 40 a 300 imagens por batch hierárquico, retomável e com concorrência limitada/adaptativa aos recursos

- **Tipo:** `FUNCIONAL`
- **Categoria:** `SCL`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Jobs/Scale`

## Requisito

A arquitetura processa lotes usuais de 40 a 300 imagens por batch hierárquico, retomável e com concorrência limitada/adaptativa aos recursos

## Rastreabilidade

- **Épicos:** `EPIC-018`, `EPIC-019`, `EPIC-040`
- **Evidência ou teste canônico:** `test_batches_40_100_300_memory_checkpoint_backpressure`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Contexts consumidores:** `BC-010/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
