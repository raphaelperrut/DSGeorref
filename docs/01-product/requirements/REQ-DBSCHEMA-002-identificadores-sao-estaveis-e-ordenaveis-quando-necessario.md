# REQ-DBSCHEMA-002 — identificadores são estáveis e ordenáveis quando necessário

- **Tipo:** `CONTRATO`
- **Categoria:** `DBSCHEMA`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-019`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

identificadores são estáveis e ordenáveis quando necessário

## Rastreabilidade

- **Épicos:** `EPIC-004`, `EPIC-012`
- **Evidência ou teste canônico:** `test_req_dbschema_002`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-003`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
