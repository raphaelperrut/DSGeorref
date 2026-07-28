# EPIC-065 — taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos

- **Domínio:** `JOB`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Sprint planejada:** `SPRINT-004`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0065`
- **Dependências:** EPIC-014, EPIC-015
- **Release gate:** `G1/G4/G7`
- **Referências arquiteturais:** ADR-036, ADR-039, ADR-053

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`

## Resultado

Taxonomia de retry técnico, orçamento, backoff, idempotência e planvariants algorítmicos.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1/G4/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-BEX-001, REQ-BEX-002, REQ-BEX-003, REQ-BEX-004, REQ-BEX-005, REQ-BEX-006, REQ-BEX-007, REQ-BEX-008, REQ-BEX-009, REQ-BEX-010
- Issue: `ISSUE-0065`
- Sprint: `SPRINT-004`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0404` / `ISSUE-0514` / `TASK-0404` — Definir estados, envelopes e invariantes: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0405` / `ISSUE-0515` / `TASK-0405` — Implementar modelo e application services: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0406` / `ISSUE-0516` / `TASK-0406` — Implementar runner, worker ou scheduler: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0407` / `ISSUE-0517` / `TASK-0407` — Expor comandos, progresso e reconciliação: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0408` / `ISSUE-0518` / `TASK-0408` — Automatizar testes de resiliência, retry e recuperação: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0409` / `ISSUE-0519` / `TASK-0409` — Executar integração real, carga e fault injection: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0410` / `ISSUE-0520` / `TASK-0410` — Auditar evidência e integração final: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos

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
