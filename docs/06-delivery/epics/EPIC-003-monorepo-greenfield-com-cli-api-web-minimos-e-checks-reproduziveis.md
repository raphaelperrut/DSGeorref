# EPIC-003 — monorepo greenfield com CLI/API/Web mínimos e checks reproduzíveis

- **Domínio:** `FND`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Sprint planejada:** `SPRINT-001`
- **Papel responsável pela implementação:** `Tech Lead`
- **Issue principal:** `ISSUE-0003`
- **Dependências:** EPIC-001
- **Release gate:** `G1`
- **Referências arquiteturais:** ADR-002

- ADRs: `ADR-001`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-033`, `ADR-034`

## Resultado

Monorepo greenfield com cli/api/web mínimos e checks reproduzíveis.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-DEL-001, REQ-DEV-001, REQ-TOP-001
- Issue: `ISSUE-0003`
- Sprint: `SPRINT-001`

## Histórias implementáveis


Este épico possui **5** histórias filhas:

- `STORY-0011` / `ISSUE-0121` / `TASK-0011` — Definir escopo, contratos e invariantes: monorepo greenfield com CLI/API/Web mínimos e checks reproduzíveis
- `STORY-0012` / `ISSUE-0122` / `TASK-0012` — Materializar a fundação executável: monorepo greenfield com CLI/API/Web mínimos e checks reproduzíveis
- `STORY-0013` / `ISSUE-0123` / `TASK-0013` — Automatizar validações e controles: monorepo greenfield com CLI/API/Web mínimos e checks reproduzíveis
- `STORY-0014` / `ISSUE-0124` / `TASK-0014` — Integrar a capacidade ao fluxo do repositório: monorepo greenfield com CLI/API/Web mínimos e checks reproduzíveis
- `STORY-0015` / `ISSUE-0125` / `TASK-0015` — Validar evidência e realizar auditoria final: monorepo greenfield com CLI/API/Web mínimos e checks reproduzíveis

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-001`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-033`, `ADR-034`
- **Resultado:** `PASS`
