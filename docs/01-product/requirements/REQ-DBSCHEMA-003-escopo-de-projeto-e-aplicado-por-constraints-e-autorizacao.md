# REQ-DBSCHEMA-003 — escopo de projeto é aplicado por constraints e autorização

- **Tipo:** `CONTRATO`
- **Categoria:** `DBSCHEMA`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-043`
- **Estado:** `ACCEPTED`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

escopo de projeto é aplicado por constraints e autorização

## Rastreabilidade

- **Épicos:** `EPIC-008`, `EPIC-012`
- **Evidência ou teste canônico:** `test_req_dbschema_003`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Contexts consumidores:** `BC-002/BC-003`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
