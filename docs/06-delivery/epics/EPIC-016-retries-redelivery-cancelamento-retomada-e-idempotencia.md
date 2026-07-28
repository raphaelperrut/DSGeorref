# EPIC-016 — retries, redelivery, cancelamento, retomada e idempotência

- **Domínio:** `JOB`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Sprint planejada:** `SPRINT-003`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0016`
- **Dependências:** EPIC-015
- **Release gate:** `G1/G4`
- **Referências arquiteturais:** ADR-002, ADR-036

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-018`, `ADR-033`, `ADR-034`, `ADR-038`

## Resultado

Retries, redelivery, cancelamento, retomada e idempotência.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1/G4` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-EPIC-014, REQ-EPIC-015, REQ-EPIC-016, REQ-EPIC-018
- Issue: `ISSUE-0016`
- Sprint: `SPRINT-003`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0082` / `ISSUE-0192` / `TASK-0082` — Definir estados, envelopes e invariantes: retries, redelivery, cancelamento, retomada e idempotência
- `STORY-0083` / `ISSUE-0193` / `TASK-0083` — Implementar modelo e application services: retries, redelivery, cancelamento, retomada e idempotência
- `STORY-0084` / `ISSUE-0194` / `TASK-0084` — Implementar runner, worker ou scheduler: retries, redelivery, cancelamento, retomada e idempotência
- `STORY-0085` / `ISSUE-0195` / `TASK-0085` — Expor comandos, progresso e reconciliação: retries, redelivery, cancelamento, retomada e idempotência
- `STORY-0086` / `ISSUE-0196` / `TASK-0086` — Automatizar testes de resiliência, retry e recuperação: retries, redelivery, cancelamento, retomada e idempotência
- `STORY-0087` / `ISSUE-0197` / `TASK-0087` — Executar integração real, carga e fault injection: retries, redelivery, cancelamento, retomada e idempotência
- `STORY-0088` / `ISSUE-0198` / `TASK-0088` — Auditar evidência e integração final: retries, redelivery, cancelamento, retomada e idempotência

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-018`, `ADR-033`, `ADR-034`, `ADR-038`
- **Resultado:** `PASS`
