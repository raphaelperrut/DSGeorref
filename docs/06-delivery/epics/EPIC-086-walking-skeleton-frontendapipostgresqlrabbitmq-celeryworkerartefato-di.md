# EPIC-086 — walking skeleton frontend→API→PostgreSQL→RabbitMQ/Celery→worker→artefato diagnóstico, executável e testado ponta a ponta

- **Domínio:** `FND`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Sprint planejada:** `SPRINT-001`
- **Papel responsável pela implementação:** `Tech Lead`
- **Issue principal:** `ISSUE-0086`
- **Dependências:** EPIC-002, EPIC-003, EPIC-004, EPIC-005
- **Release gate:** `G1`
- **Referências arquiteturais:** ADR-002, ADR-018, ADR-036, ADR-034, ADR-054

- ADRs: `ADR-002`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-057`

## Resultado

Walking skeleton frontend→api→postgresql→rabbitmq/celery→worker→artefato diagnóstico, executável e testado ponta a ponta.

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

- Requisitos: REQ-DEL-001, REQ-DEL-002, REQ-EPIC-001, REQ-ISM-003, REQ-SPRINT-001-001, REQ-SPRINT-001-002, REQ-SPRINT-001-003, REQ-SPRINT-001-004, REQ-SPRINT-001-005, REQ-SPRINT-001-006, REQ-SPRINT-001-007, REQ-SPRINT-001-008, REQ-SPRINT-001-009, REQ-SPRINT-001-010
- Issue: `ISSUE-0086`
- Sprint: `SPRINT-001`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0534` / `ISSUE-0644` / `TASK-0534` — Definir escopo, contratos e invariantes: walking skeleton frontend→API→PostgreSQL→RabbitMQ/Celery→worker→artefato diagnóstico, executável e testado ponta a ponta
- `STORY-0535` / `ISSUE-0645` / `TASK-0535` — Consolidar slices e liberar integração: walking skeleton frontend→API→PostgreSQL→RabbitMQ/Celery→worker→artefato diagnóstico, executável e testado ponta a ponta
- `STORY-0536` / `ISSUE-0646` / `TASK-0536` — Automatizar validações e controles: walking skeleton frontend→API→PostgreSQL→RabbitMQ/Celery→worker→artefato diagnóstico, executável e testado ponta a ponta
- `STORY-0537` / `ISSUE-0647` / `TASK-0537` — Integrar a capacidade ao fluxo do repositório: walking skeleton frontend→API→PostgreSQL→RabbitMQ/Celery→worker→artefato diagnóstico, executável e testado ponta a ponta
- `STORY-0538` / `ISSUE-0648` / `TASK-0538` — Validar evidência e realizar auditoria final: walking skeleton frontend→API→PostgreSQL→RabbitMQ/Celery→worker→artefato diagnóstico, executável e testado ponta a ponta
- `STORY-0752` / `ISSUE-0862` / `TASK-0752` — Slice 1/2 — Materializar a fundação executável: walking skeleton frontend→API→PostgreSQL→RabbitMQ/Celery→worker→artefato diagnóstico, executável e testado ponta a ponta [REQ-DEL, REQ-ISM, REQ-SPRINT-001]
- `STORY-0753` / `ISSUE-0863` / `TASK-0753` — Slice 2/2 — Materializar a fundação executável: walking skeleton frontend→API→PostgreSQL→RabbitMQ/Celery→worker→artefato diagnóstico, executável e testado ponta a ponta [REQ-SPRINT-001]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-057`
- **Resultado:** `PASS`
