# REQ-INS-002 — Primeira identidade deve ser criada por bootstrap único sem credenciais padrão e com secrets protegidos

- **Tipo:** `FUNCIONAL`
- **Categoria:** `INS`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-034`
- **Estado:** `PENDING`
- **Gate:** `Security/Identity/Operations`

## Requisito

Primeira identidade deve ser criada por bootstrap único sem credenciais padrão e com secrets protegidos

## Rastreabilidade

- **Épicos:** `EPIC-008`, `EPIC-076`, `EPIC-108`
- **Evidência ou teste canônico:** `test_one_time_bootstrap_no_default_credentials_secret_generation_expiry_and_recovery`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Contexts consumidores:** `BC-002/BC-014/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
