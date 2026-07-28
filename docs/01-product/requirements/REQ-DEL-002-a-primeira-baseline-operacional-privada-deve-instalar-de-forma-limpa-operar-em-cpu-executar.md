# REQ-DEL-002 — A primeira baseline operacional privada deve instalar de forma limpa, operar em CPU, executar o fluxo vertical aprovado e produzir evidências reproduzíveis antes de qualquer claim público.

- **Tipo:** `FUNCIONAL`
- **Categoria:** `DEL`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-057`
- **Estado:** `PENDING`
- **Gate:** `Definido pelo épico vinculado`

## Requisito

A primeira baseline operacional privada deve instalar de forma limpa, operar em CPU, executar o fluxo vertical aprovado e produzir evidências reproduzíveis antes de qualquer claim público.

## Rastreabilidade

- **Épicos:** `EPIC-086`, `EPIC-087`
- **Evidência ou teste canônico:** `test_private_operational_baseline_scope_cpu_only_clean_install`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001/BC-015`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
