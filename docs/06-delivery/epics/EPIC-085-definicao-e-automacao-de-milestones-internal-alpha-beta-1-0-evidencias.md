# EPIC-085 — definição e automação de milestones internal/alpha/beta/1.0, evidências e gate de abertura do repositório

- **Domínio:** `REL`
- **Bounded Context owner:** `BC-015 — Release, Instalação e Supply Chain`
- **Sprint planejada:** `SPRINT-012`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0085`
- **Dependências:** EPIC-002, EPIC-042, EPIC-043
- **Release gate:** `G6/G7`
- **Referências arquiteturais:** ADR-034, ADR-054, ADR-026

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-037`

## Resultado

Definição e automação de milestones internal/alpha/beta/1.0, evidências e gate de abertura do repositório.

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

- Requisitos: REQ-EPIC-043
- Issue: `ISSUE-0085`
- Sprint: `SPRINT-012`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0528` / `ISSUE-0638` / `TASK-0528` — Definir gate, versão e critérios de release: definição e automação de milestones internal/alpha/beta/1.0, evidências e gate de abertura do repositório
- `STORY-0529` / `ISSUE-0639` / `TASK-0529` — Implementar pipeline e artifacts de release: definição e automação de milestones internal/alpha/beta/1.0, evidências e gate de abertura do repositório
- `STORY-0530` / `ISSUE-0640` / `TASK-0530` — Implementar upgrade, rollback e compatibilidade: definição e automação de milestones internal/alpha/beta/1.0, evidências e gate de abertura do repositório
- `STORY-0531` / `ISSUE-0641` / `TASK-0531` — Gerar evidências, SBOM e attestations: definição e automação de milestones internal/alpha/beta/1.0, evidências e gate de abertura do repositório
- `STORY-0532` / `ISSUE-0642` / `TASK-0532` — Executar instalação limpa e rehearsal: definição e automação de milestones internal/alpha/beta/1.0, evidências e gate de abertura do repositório
- `STORY-0533` / `ISSUE-0643` / `TASK-0533` — Auditar release candidata final: definição e automação de milestones internal/alpha/beta/1.0, evidências e gate de abertura do repositório

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
