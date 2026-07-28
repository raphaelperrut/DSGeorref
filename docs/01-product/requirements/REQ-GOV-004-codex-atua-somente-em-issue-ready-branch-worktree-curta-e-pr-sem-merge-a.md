# REQ-GOV-004 — Codex atua somente em issue Ready, branch/worktree curta e PR, sem merge autônomo ou decisão sobre gates sensíveis

- **Tipo:** `GOVERNANCA`
- **Categoria:** `GOV`
- **Prioridade:** `P0`
- **Owner normativo:** `ADR-007`
- **Estado:** `PENDING`
- **Gate:** `Governance/Security`

## Requisito

Codex atua somente em issue Ready, branch/worktree curta e PR, sem merge autônomo ou decisão sobre gates sensíveis

## Rastreabilidade

- **Épicos:** `EPIC-005`, `EPIC-091`
- **Evidência ou teste canônico:** `test_codex_issue_scope_required_pr_no_direct_main_or_automerge`
- **Fonte de produto:** `docs/01-product/PRD.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é considerado atendido somente quando o teste ou evidência canônica passa no commit candidato e a história responsável referencia este arquivo.
