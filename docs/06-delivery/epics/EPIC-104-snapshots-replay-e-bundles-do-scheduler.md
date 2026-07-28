# EPIC-104 — Snapshots, replay e bundles do scheduler

- **Domínio:** `JOB`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Sprint planejada:** `SPRINT-004`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0104`
- **Dependências:** Nenhuma
- **Release gate:** `G1/G7`
- **Referências arquiteturais:** ADR-039

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-053`

## Resultado

Snapshots, replay e bundles do scheduler.

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

- Requisitos: REQ-SRP-001, REQ-SRP-002, REQ-SRP-003, REQ-SRP-004
- Issue: `ISSUE-0104`
- Sprint: `SPRINT-004`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0647` / `ISSUE-0757` / `TASK-0647` — Definir estados, envelopes e invariantes: Snapshots, replay e bundles do scheduler
- `STORY-0648` / `ISSUE-0758` / `TASK-0648` — Implementar modelo e application services: Snapshots, replay e bundles do scheduler
- `STORY-0649` / `ISSUE-0759` / `TASK-0649` — Implementar runner, worker ou scheduler: Snapshots, replay e bundles do scheduler
- `STORY-0650` / `ISSUE-0760` / `TASK-0650` — Expor comandos, progresso e reconciliação: Snapshots, replay e bundles do scheduler
- `STORY-0651` / `ISSUE-0761` / `TASK-0651` — Automatizar testes de resiliência, retry e recuperação: Snapshots, replay e bundles do scheduler
- `STORY-0652` / `ISSUE-0762` / `TASK-0652` — Executar integração real, carga e fault injection: Snapshots, replay e bundles do scheduler
- `STORY-0653` / `ISSUE-0763` / `TASK-0653` — Auditar evidência e integração final: Snapshots, replay e bundles do scheduler

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-053`
- **Resultado:** `PASS`
