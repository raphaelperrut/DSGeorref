# EPIC-067 — cancelamento cooperativo, supervisão de subprocessos, contenção e reconciliação

- **Domínio:** `JOB`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Sprint planejada:** `SPRINT-004`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0067`
- **Dependências:** EPIC-016, EPIC-019
- **Release gate:** `G1/G7`
- **Referências arquiteturais:** ADR-036, ADR-039, ADR-054

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`

## Resultado

Cancelamento cooperativo, supervisão de subprocessos, contenção e reconciliação.

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

- Requisitos: REQ-BEX-001, REQ-BEX-002, REQ-BEX-003, REQ-BEX-004, REQ-BEX-005, REQ-BEX-006, REQ-BEX-007, REQ-BEX-008, REQ-BEX-009, REQ-BEX-010
- Issue: `ISSUE-0067`
- Sprint: `SPRINT-004`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0418` / `ISSUE-0528` / `TASK-0418` — Definir estados, envelopes e invariantes: cancelamento cooperativo, supervisão de subprocessos, contenção e reconciliação
- `STORY-0419` / `ISSUE-0529` / `TASK-0419` — Implementar modelo e application services: cancelamento cooperativo, supervisão de subprocessos, contenção e reconciliação
- `STORY-0420` / `ISSUE-0530` / `TASK-0420` — Implementar runner, worker ou scheduler: cancelamento cooperativo, supervisão de subprocessos, contenção e reconciliação
- `STORY-0421` / `ISSUE-0531` / `TASK-0421` — Expor comandos, progresso e reconciliação: cancelamento cooperativo, supervisão de subprocessos, contenção e reconciliação
- `STORY-0422` / `ISSUE-0532` / `TASK-0422` — Automatizar testes de resiliência, retry e recuperação: cancelamento cooperativo, supervisão de subprocessos, contenção e reconciliação
- `STORY-0423` / `ISSUE-0533` / `TASK-0423` — Executar integração real, carga e fault injection: cancelamento cooperativo, supervisão de subprocessos, contenção e reconciliação
- `STORY-0424` / `ISSUE-0534` / `TASK-0424` — Auditar evidência e integração final: cancelamento cooperativo, supervisão de subprocessos, contenção e reconciliação

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
