# EPIC-015 — runner direto e Celery/RabbitMQ sobre o mesmo núcleo

- **Domínio:** `JOB`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Sprint planejada:** `SPRINT-003`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0015`
- **Dependências:** EPIC-014
- **Release gate:** `G1`
- **Referências arquiteturais:** ADR-002, ADR-036

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-018`, `ADR-033`, `ADR-034`

## Resultado

Runner direto e celery/rabbitmq sobre o mesmo núcleo.

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

- Requisitos: REQ-EPIC-015, REQ-TOP-001
- Issue: `ISSUE-0015`
- Sprint: `SPRINT-003`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0075` / `ISSUE-0185` / `TASK-0075` — Definir estados, envelopes e invariantes: runner direto e Celery/RabbitMQ sobre o mesmo núcleo
- `STORY-0076` / `ISSUE-0186` / `TASK-0076` — Implementar modelo e application services: runner direto e Celery/RabbitMQ sobre o mesmo núcleo
- `STORY-0077` / `ISSUE-0187` / `TASK-0077` — Implementar runner, worker ou scheduler: runner direto e Celery/RabbitMQ sobre o mesmo núcleo
- `STORY-0078` / `ISSUE-0188` / `TASK-0078` — Expor comandos, progresso e reconciliação: runner direto e Celery/RabbitMQ sobre o mesmo núcleo
- `STORY-0079` / `ISSUE-0189` / `TASK-0079` — Automatizar testes de resiliência, retry e recuperação: runner direto e Celery/RabbitMQ sobre o mesmo núcleo
- `STORY-0080` / `ISSUE-0190` / `TASK-0080` — Executar integração real, carga e fault injection: runner direto e Celery/RabbitMQ sobre o mesmo núcleo
- `STORY-0081` / `ISSUE-0191` / `TASK-0081` — Auditar evidência e integração final: runner direto e Celery/RabbitMQ sobre o mesmo núcleo

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-018`, `ADR-033`, `ADR-034`
- **Resultado:** `PASS`
