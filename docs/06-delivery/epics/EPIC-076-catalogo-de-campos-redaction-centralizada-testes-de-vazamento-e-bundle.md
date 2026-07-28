# EPIC-076 — catálogo de campos, redaction centralizada, testes de vazamento e bundles de suporte sanitizados

- **Domínio:** `SEC`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `Security`
- **Issue principal:** `ISSUE-0076`
- **Dependências:** EPIC-005, EPIC-039, EPIC-075
- **Release gate:** `G5/G7`
- **Referências arquiteturais:** ADR-034, ADR-039, ADR-054

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-053`, `ADR-055`

## Resultado

Catálogo de campos, redaction centralizada, testes de vazamento e bundles de suporte sanitizados.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G5/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-INS-002, REQ-LOG-001, REQ-RUNTIME-009, REQ-SRP-004
- Issue: `ISSUE-0076`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0475` / `ISSUE-0585` / `TASK-0475` — Modelar ameaças e requisitos de controle: catálogo de campos, redaction centralizada, testes de vazamento e bundles de suporte sanitizados
- `STORY-0476` / `ISSUE-0586` / `TASK-0476` — Definir políticas e contratos fail-closed: catálogo de campos, redaction centralizada, testes de vazamento e bundles de suporte sanitizados
- `STORY-0477` / `ISSUE-0587` / `TASK-0477` — Implementar controles e enforcement: catálogo de campos, redaction centralizada, testes de vazamento e bundles de suporte sanitizados
- `STORY-0478` / `ISSUE-0588` / `TASK-0478` — Executar testes negativos e ofensivos: catálogo de campos, redaction centralizada, testes de vazamento e bundles de suporte sanitizados
- `STORY-0479` / `ISSUE-0589` / `TASK-0479` — Instrumentar detecção, resposta e runbook: catálogo de campos, redaction centralizada, testes de vazamento e bundles de suporte sanitizados
- `STORY-0480` / `ISSUE-0590` / `TASK-0480` — Auditar evidência de segurança final: catálogo de campos, redaction centralizada, testes de vazamento e bundles de suporte sanitizados

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-053`, `ADR-055`
- **Resultado:** `PASS`
