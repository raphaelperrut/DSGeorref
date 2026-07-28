# REQ-TST-001 — Dados de teste seguem pirâmide de fixtures, integração externa, validação protegida e teste cego com origem/licença/hash

- **Tipo:** `FUNCIONAL`
- **Categoria:** `TST`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-053`
- **Estado:** `PENDING`
- **Gate:** `Quality/Data`

## Requisito

Dados de teste seguem pirâmide de fixtures, integração externa, validação protegida e teste cego com origem/licença/hash

## Rastreabilidade

- **Épicos:** `EPIC-006`, `EPIC-028`, `EPIC-092`
- **Evidência ou teste canônico:** `test_corpus_license_hash_split_and_access_integrity`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-007`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
