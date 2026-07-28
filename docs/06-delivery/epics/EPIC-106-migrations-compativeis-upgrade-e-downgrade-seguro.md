# EPIC-106 — Migrations compatíveis, upgrade e downgrade seguro

- **Domínio:** `REL`
- **Bounded Context owner:** `BC-015 — Release, Instalação e Supply Chain`
- **Sprint planejada:** `SPRINT-012`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0106`
- **Dependências:** Nenhuma
- **Release gate:** `G7`
- **Referências arquiteturais:** ADR-026

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-026`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-035`

## Resultado

Migrations compatíveis, upgrade e downgrade seguro.

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

- Requisitos: REQ-SCM-002, REQ-SCM-004, REQ-UPG-002
- Issue: `ISSUE-0106`
- Sprint: `SPRINT-012`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0660` / `ISSUE-0770` / `TASK-0660` — Definir gate, versão e critérios de release: Migrations compatíveis, upgrade e downgrade seguro
- `STORY-0661` / `ISSUE-0771` / `TASK-0661` — Implementar pipeline e artifacts de release: Migrations compatíveis, upgrade e downgrade seguro
- `STORY-0662` / `ISSUE-0772` / `TASK-0662` — Implementar upgrade, rollback e compatibilidade: Migrations compatíveis, upgrade e downgrade seguro
- `STORY-0663` / `ISSUE-0773` / `TASK-0663` — Gerar evidências, SBOM e attestations: Migrations compatíveis, upgrade e downgrade seguro
- `STORY-0664` / `ISSUE-0774` / `TASK-0664` — Executar instalação limpa e rehearsal: Migrations compatíveis, upgrade e downgrade seguro
- `STORY-0665` / `ISSUE-0775` / `TASK-0665` — Auditar release candidata final: Migrations compatíveis, upgrade e downgrade seguro

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-026`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-035`
- **Resultado:** `PASS`
