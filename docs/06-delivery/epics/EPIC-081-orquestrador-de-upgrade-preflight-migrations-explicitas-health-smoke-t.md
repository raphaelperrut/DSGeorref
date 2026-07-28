# EPIC-081 — orquestrador de upgrade, preflight, migrations explícitas, health/smoke tests e rollback/restore

- **Domínio:** `REL`
- **Bounded Context owner:** `BC-015 — Release, Instalação e Supply Chain`
- **Sprint planejada:** `SPRINT-012`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0081`
- **Dependências:** EPIC-043, EPIC-071, EPIC-072, EPIC-080
- **Release gate:** `G7`
- **Referências arquiteturais:** ADR-034, ADR-026

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-035`

## Resultado

Orquestrador de upgrade, preflight, migrations explícitas, health/smoke tests e rollback/restore.

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

- Requisitos: REQ-INS-001, REQ-UPG-001
- Issue: `ISSUE-0081`
- Sprint: `SPRINT-012`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0505` / `ISSUE-0615` / `TASK-0505` — Definir gate, versão e critérios de release: orquestrador de upgrade, preflight, migrations explícitas, health/smoke tests e rollback/restore
- `STORY-0506` / `ISSUE-0616` / `TASK-0506` — Implementar pipeline e artifacts de release: orquestrador de upgrade, preflight, migrations explícitas, health/smoke tests e rollback/restore
- `STORY-0507` / `ISSUE-0617` / `TASK-0507` — Implementar upgrade, rollback e compatibilidade: orquestrador de upgrade, preflight, migrations explícitas, health/smoke tests e rollback/restore
- `STORY-0508` / `ISSUE-0618` / `TASK-0508` — Gerar evidências, SBOM e attestations: orquestrador de upgrade, preflight, migrations explícitas, health/smoke tests e rollback/restore
- `STORY-0509` / `ISSUE-0619` / `TASK-0509` — Executar instalação limpa e rehearsal: orquestrador de upgrade, preflight, migrations explícitas, health/smoke tests e rollback/restore
- `STORY-0510` / `ISSUE-0620` / `TASK-0510` — Auditar release candidata final: orquestrador de upgrade, preflight, migrations explícitas, health/smoke tests e rollback/restore

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-035`
- **Resultado:** `PASS`
