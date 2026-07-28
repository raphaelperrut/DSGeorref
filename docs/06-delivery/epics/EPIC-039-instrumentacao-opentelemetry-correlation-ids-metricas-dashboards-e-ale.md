# EPIC-039 — instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers

- **Domínio:** `OPS`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0039`
- **Dependências:** EPIC-005, EPIC-015, EPIC-019, EPIC-067, EPIC-082
- **Release gate:** `G7`
- **Referências arquiteturais:** ADR-002, ADR-018, ADR-036, ADR-054

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-017`, `ADR-018`, `ADR-020`, `ADR-023`, `ADR-024`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-054`, `ADR-055`

## Resultado

Instrumentação opentelemetry, correlation ids, métricas, dashboards e alertas para api, rabbitmq e workers.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AIE-001, REQ-AIE-002, REQ-AIE-003, REQ-AIE-004, REQ-AIE-005, REQ-AIE-006, REQ-AIE-007, REQ-AIE-008, REQ-AIE-009, REQ-AIE-010, REQ-ARTLAYOUT-001, REQ-ARTLAYOUT-004, REQ-ARTLAYOUT-008, REQ-ARTLAYOUT-009, REQ-EPIC-018, REQ-LOG-001, REQ-MET-001, REQ-OBS-001, REQ-OBS-002, REQ-RUNTIME-009, REQ-RUNTIME-010, REQ-WORKER-001, REQ-WORKER-002, REQ-WORKER-003, REQ-WORKER-004, REQ-WORKER-005, REQ-WORKER-006, REQ-WORKER-007, REQ-WORKER-008, REQ-WORKER-009, REQ-WORKER-010
- Issue: `ISSUE-0039`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **8** histórias filhas:

- `STORY-0232` / `ISSUE-0342` / `TASK-0232` — Definir SLO, runbook e controles operacionais: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0233` / `ISSUE-0343` / `TASK-0233` — Consolidar slices e liberar integração: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0234` / `ISSUE-0344` / `TASK-0234` — Instrumentar sinais, dashboards e alertas: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0235` / `ISSUE-0345` / `TASK-0235` — Executar drills, fault injection e recuperação: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0236` / `ISSUE-0346` / `TASK-0236` — Validar acesso, redaction e exposição: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0237` / `ISSUE-0347` / `TASK-0237` — Auditar evidência operacional final: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0745` / `ISSUE-0855` / `TASK-0745` — Slice 1/2 — Implementar automação operacional: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers [REQ-AIE, REQ-ARTLAYOUT]
- `STORY-0746` / `ISSUE-0856` / `TASK-0746` — Slice 2/2 — Implementar automação operacional: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers [REQ-ARTLAYOUT, REQ-MET, REQ-WORKER]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-017`, `ADR-018`, `ADR-020`, `ADR-023`, `ADR-024`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-054`, `ADR-055`
- **Resultado:** `PASS`
