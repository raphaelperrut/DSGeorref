# EPIC-017 — REST, SSE e polling de reconciliação com contratos versionados

- **Domínio:** `JOB`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Sprint planejada:** `SPRINT-003`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0017`
- **Dependências:** EPIC-014
- **Release gate:** `G1/G7`
- **Referências arquiteturais:** ADR-002, ADR-018, ADR-036, ADR-039, ADR-054

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-033`, `ADR-034`

## Resultado

Rest, sse e polling de reconciliação com contratos versionados.

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

- Requisitos: REQ-FS1-009, REQ-RUN-006, REQ-RUN-007, REQ-RUNTIME-005, REQ-WORKER-008
- Issue: `ISSUE-0017`
- Sprint: `SPRINT-003`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0089` / `ISSUE-0199` / `TASK-0089` — Definir estados, envelopes e invariantes: REST, SSE e polling de reconciliação com contratos versionados
- `STORY-0090` / `ISSUE-0200` / `TASK-0090` — Implementar modelo e application services: REST, SSE e polling de reconciliação com contratos versionados
- `STORY-0091` / `ISSUE-0201` / `TASK-0091` — Implementar runner, worker ou scheduler: REST, SSE e polling de reconciliação com contratos versionados
- `STORY-0092` / `ISSUE-0202` / `TASK-0092` — Expor comandos, progresso e reconciliação: REST, SSE e polling de reconciliação com contratos versionados
- `STORY-0093` / `ISSUE-0203` / `TASK-0093` — Automatizar testes de resiliência, retry e recuperação: REST, SSE e polling de reconciliação com contratos versionados
- `STORY-0094` / `ISSUE-0204` / `TASK-0094` — Executar integração real, carga e fault injection: REST, SSE e polling de reconciliação com contratos versionados
- `STORY-0095` / `ISSUE-0205` / `TASK-0095` — Auditar evidência e integração final: REST, SSE e polling de reconciliação com contratos versionados

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-033`, `ADR-034`
- **Resultado:** `PASS`
