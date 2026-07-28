# EPIC-107 — Controlador e rollout coordenado de upgrades

- **Domínio:** `REL`
- **Bounded Context owner:** `BC-015 — Release, Instalação e Supply Chain`
- **Sprint planejada:** `SPRINT-012`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0107`
- **Dependências:** Nenhuma
- **Release gate:** `G7`
- **Referências arquiteturais:** ADR-026

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-026`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-035`

## Resultado

Controlador e rollout coordenado de upgrades.

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

- Requisitos: REQ-DBSCHEMA-010, REQ-UPG-002, REQ-UPG-003, REQ-UPG-004, REQ-UPG-005
- Issue: `ISSUE-0107`
- Sprint: `SPRINT-012`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0666` / `ISSUE-0776` / `TASK-0666` — Definir gate, versão e critérios de release: Controlador e rollout coordenado de upgrades
- `STORY-0667` / `ISSUE-0777` / `TASK-0667` — Implementar pipeline e artifacts de release: Controlador e rollout coordenado de upgrades
- `STORY-0668` / `ISSUE-0778` / `TASK-0668` — Implementar upgrade, rollback e compatibilidade: Controlador e rollout coordenado de upgrades
- `STORY-0669` / `ISSUE-0779` / `TASK-0669` — Gerar evidências, SBOM e attestations: Controlador e rollout coordenado de upgrades
- `STORY-0670` / `ISSUE-0780` / `TASK-0670` — Executar instalação limpa e rehearsal: Controlador e rollout coordenado de upgrades
- `STORY-0671` / `ISSUE-0781` / `TASK-0671` — Auditar release candidata final: Controlador e rollout coordenado de upgrades

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
