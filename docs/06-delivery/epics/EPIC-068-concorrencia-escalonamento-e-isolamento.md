# EPIC-068 — Concorrência, escalonamento e isolamento

- **Domínio:** `JOB`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Sprint planejada:** `SPRINT-004`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0068`
- **Dependências:** EPIC-018, EPIC-019, EPIC-082
- **Release gate:** `G1/G7`
- **Referências arquiteturais:** ADR-039

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`

## Resultado

Concorrência, escalonamento e isolamento.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-BEX-001, REQ-BEX-002, REQ-BEX-003, REQ-BEX-004, REQ-BEX-005, REQ-BEX-006, REQ-BEX-007, REQ-BEX-008, REQ-BEX-009, REQ-BEX-010, REQ-SCH-001, REQ-SCH-002, REQ-SCH-003, REQ-SCH-004
- Issue: `ISSUE-0068`
- Sprint: `SPRINT-004`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0425` / `ISSUE-0535` / `TASK-0425` — Definir estados, envelopes e invariantes: Concorrência, escalonamento e isolamento
- `STORY-0426` / `ISSUE-0536` / `TASK-0426` — Implementar modelo e application services: Concorrência, escalonamento e isolamento
- `STORY-0427` / `ISSUE-0537` / `TASK-0427` — Implementar runner, worker ou scheduler: Concorrência, escalonamento e isolamento
- `STORY-0428` / `ISSUE-0538` / `TASK-0428` — Expor comandos, progresso e reconciliação: Concorrência, escalonamento e isolamento
- `STORY-0429` / `ISSUE-0539` / `TASK-0429` — Automatizar testes de resiliência, retry e recuperação: Concorrência, escalonamento e isolamento
- `STORY-0430` / `ISSUE-0540` / `TASK-0430` — Executar integração real, carga e fault injection: Concorrência, escalonamento e isolamento
- `STORY-0431` / `ISSUE-0541` / `TASK-0431` — Auditar evidência e integração final: Concorrência, escalonamento e isolamento

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`
- **Resultado:** `PASS`
