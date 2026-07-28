# REQ-SMO-004 — Dashboard role-based deve explicar bloqueios, prioridade efetiva e ações seguras com auditoria

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `SMO`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-030`
- **Estado:** `PENDING`
- **Gate:** `Web/Operations/Security`

## Requisito

Dashboard role-based deve explicar bloqueios, prioridade efetiva e ações seguras com auditoria

## Rastreabilidade

- **Épicos:** `EPIC-034`, `EPIC-069`, `EPIC-075`
- **Evidência ou teste canônico:** `test_role_based_scheduler_diagnostics_safe_controls_and_append_only_audit`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Contexts consumidores:** `BC-016/BC-010/BC-014`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
