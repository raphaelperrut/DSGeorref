# EPIC-014 — modelo de job e máquina de estados no PostgreSQL

- **Domínio:** `JOB`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Sprint planejada:** `SPRINT-003`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0014`
- **Dependências:** EPIC-004, EPIC-005
- **Release gate:** `G1`
- **Referências arquiteturais:** ADR-002, ADR-018, ADR-036

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-015`, `ADR-016`, `ADR-018`, `ADR-019`, `ADR-020`, `ADR-023`, `ADR-030`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`

## Resultado

Modelo de job e máquina de estados no postgresql.

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

- Requisitos: REQ-AIE-001, REQ-AIE-002, REQ-AIE-003, REQ-AIE-004, REQ-AIE-005, REQ-AIE-006, REQ-AIE-007, REQ-AIE-008, REQ-AIE-009, REQ-AIE-010, REQ-DBSCHEMA-008, REQ-DBSCHEMA-009, REQ-EPIC-014, REQ-FS1-001, REQ-FS1-002, REQ-FS1-003, REQ-FS1-004, REQ-FS1-005, REQ-FS1-006, REQ-FS1-007, REQ-FS1-008, REQ-FS1-009, REQ-FS1-010, REQ-RUNTIME-002, REQ-WORKER-001, REQ-WORKER-002, REQ-WORKER-003, REQ-WORKER-004, REQ-WORKER-005, REQ-WORKER-006, REQ-WORKER-007, REQ-WORKER-008, REQ-WORKER-009, REQ-WORKER-010
- Issue: `ISSUE-0014`
- Sprint: `SPRINT-003`

## Histórias implementáveis


Este épico possui **9** histórias filhas:

- `STORY-0068` / `ISSUE-0178` / `TASK-0068` — Definir estados, envelopes e invariantes: modelo de job e máquina de estados no PostgreSQL
- `STORY-0069` / `ISSUE-0179` / `TASK-0069` — Consolidar slices e liberar integração: modelo de job e máquina de estados no PostgreSQL
- `STORY-0070` / `ISSUE-0180` / `TASK-0070` — Implementar runner, worker ou scheduler: modelo de job e máquina de estados no PostgreSQL
- `STORY-0071` / `ISSUE-0181` / `TASK-0071` — Expor comandos, progresso e reconciliação: modelo de job e máquina de estados no PostgreSQL
- `STORY-0072` / `ISSUE-0182` / `TASK-0072` — Automatizar testes de resiliência, retry e recuperação: modelo de job e máquina de estados no PostgreSQL
- `STORY-0073` / `ISSUE-0183` / `TASK-0073` — Executar integração real, carga e fault injection: modelo de job e máquina de estados no PostgreSQL
- `STORY-0074` / `ISSUE-0184` / `TASK-0074` — Auditar evidência e integração final: modelo de job e máquina de estados no PostgreSQL
- `STORY-0721` / `ISSUE-0831` / `TASK-0721` — Slice 1/2 — Implementar modelo e application services: modelo de job e máquina de estados no PostgreSQL [REQ-AIE, REQ-DBSCHEMA, REQ-FS1]
- `STORY-0722` / `ISSUE-0832` / `TASK-0722` — Slice 2/2 — Implementar modelo e application services: modelo de job e máquina de estados no PostgreSQL [REQ-FS1, REQ-RUNTIME, REQ-WORKER]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-015`, `ADR-016`, `ADR-018`, `ADR-019`, `ADR-020`, `ADR-023`, `ADR-030`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Resultado:** `PASS`
