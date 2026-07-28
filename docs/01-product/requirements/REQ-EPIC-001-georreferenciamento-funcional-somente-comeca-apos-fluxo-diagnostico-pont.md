# REQ-EPIC-001 — Georreferenciamento funcional somente começa após fluxo diagnóstico ponta a ponta, migrations, contratos, CI, segurança mínima e clean-room bootstrap comprovados

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `EPIC`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-002`
- **Estado:** `PENDING`
- **Gate:** `Foundation`

## Requisito

Georreferenciamento funcional somente começa após fluxo diagnóstico ponta a ponta, migrations, contratos, CI, segurança mínima e clean-room bootstrap comprovados

## Rastreabilidade

- **Épicos:** `EPIC-086`, `EPIC-092`
- **Evidência ou teste canônico:** `test_executable_foundation_gate_clean_room_end_to_end`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
