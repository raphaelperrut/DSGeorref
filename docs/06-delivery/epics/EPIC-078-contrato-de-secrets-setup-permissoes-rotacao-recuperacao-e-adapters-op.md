# EPIC-078 — contrato de secrets, setup, permissões, rotação, recuperação e adapters opcionais de vault

- **Domínio:** `SEC`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `Security`
- **Issue principal:** `ISSUE-0078`
- **Dependências:** EPIC-005, EPIC-008
- **Release gate:** `G5/G7`
- **Referências arquiteturais:** ADR-018, ADR-034

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-023`, `ADR-024`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-040`, `ADR-045`

## Resultado

Contrato de secrets, setup, permissões, rotação, recuperação e adapters opcionais de vault.

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

- Requisitos: REQ-ARTLAYOUT-005, REQ-ARTLAYOUT-006, REQ-ARTLAYOUT-007, REQ-EPIC-076, REQ-RUNTIME-004
- Issue: `ISSUE-0078`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0487` / `ISSUE-0597` / `TASK-0487` — Modelar ameaças e requisitos de controle: contrato de secrets, setup, permissões, rotação, recuperação e adapters opcionais de vault
- `STORY-0488` / `ISSUE-0598` / `TASK-0488` — Definir políticas e contratos fail-closed: contrato de secrets, setup, permissões, rotação, recuperação e adapters opcionais de vault
- `STORY-0489` / `ISSUE-0599` / `TASK-0489` — Implementar controles e enforcement: contrato de secrets, setup, permissões, rotação, recuperação e adapters opcionais de vault
- `STORY-0490` / `ISSUE-0600` / `TASK-0490` — Executar testes negativos e ofensivos: contrato de secrets, setup, permissões, rotação, recuperação e adapters opcionais de vault
- `STORY-0491` / `ISSUE-0601` / `TASK-0491` — Instrumentar detecção, resposta e runbook: contrato de secrets, setup, permissões, rotação, recuperação e adapters opcionais de vault
- `STORY-0492` / `ISSUE-0602` / `TASK-0492` — Auditar evidência de segurança final: contrato de secrets, setup, permissões, rotação, recuperação e adapters opcionais de vault

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-023`, `ADR-024`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-040`, `ADR-045`
- **Resultado:** `PASS`
