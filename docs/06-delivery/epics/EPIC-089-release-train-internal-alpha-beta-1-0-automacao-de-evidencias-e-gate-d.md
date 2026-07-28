# EPIC-089 — release train internal/alpha/beta/1.0, automação de evidências e gate de abertura pública

- **Domínio:** `REL`
- **Bounded Context owner:** `BC-015 — Release, Instalação e Supply Chain`
- **Sprint planejada:** `SPRINT-012`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0089`
- **Dependências:** EPIC-042, EPIC-072, EPIC-080, EPIC-085, EPIC-087
- **Release gate:** `G6/G7`
- **Referências arquiteturais:** ADR-034, ADR-054, ADR-053, ADR-026

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-037`

## Resultado

Release train internal/alpha/beta/1.0, automação de evidências e gate de abertura pública.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G6/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-EPIC-043, REQ-PUB-004
- Issue: `ISSUE-0089`
- Sprint: `SPRINT-012`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0549` / `ISSUE-0659` / `TASK-0549` — Definir gate, versão e critérios de release: release train internal/alpha/beta/1.0, automação de evidências e gate de abertura pública
- `STORY-0550` / `ISSUE-0660` / `TASK-0550` — Implementar pipeline e artifacts de release: release train internal/alpha/beta/1.0, automação de evidências e gate de abertura pública
- `STORY-0551` / `ISSUE-0661` / `TASK-0551` — Implementar upgrade, rollback e compatibilidade: release train internal/alpha/beta/1.0, automação de evidências e gate de abertura pública
- `STORY-0552` / `ISSUE-0662` / `TASK-0552` — Gerar evidências, SBOM e attestations: release train internal/alpha/beta/1.0, automação de evidências e gate de abertura pública
- `STORY-0553` / `ISSUE-0663` / `TASK-0553` — Executar instalação limpa e rehearsal: release train internal/alpha/beta/1.0, automação de evidências e gate de abertura pública
- `STORY-0554` / `ISSUE-0664` / `TASK-0554` — Auditar release candidata final: release train internal/alpha/beta/1.0, automação de evidências e gate de abertura pública

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-037`
- **Resultado:** `PASS`
