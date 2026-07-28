# EPIC-105 — Registry de schemas e compatibilidade de artifacts

- **Domínio:** `DAT`
- **Bounded Context owner:** `BC-013 — Artifacts, Proveniência e Lifecycle`
- **Sprint planejada:** `SPRINT-010`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0105`
- **Dependências:** Nenhuma
- **Release gate:** `G3/G7`
- **Referências arquiteturais:** ADR-026

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-035`, `ADR-053`

## Resultado

Registry de schemas e compatibilidade de artifacts.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-SCM-001, REQ-SCM-003, REQ-UPG-004, REQ-UPG-005
- Issue: `ISSUE-0105`
- Sprint: `SPRINT-010`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0654` / `ISSUE-0764` / `TASK-0654` — Definir modelo, invariantes e contratos de dados: Registry de schemas e compatibilidade de artifacts
- `STORY-0655` / `ISSUE-0765` / `TASK-0655` — Implementar persistência e migrations: Registry de schemas e compatibilidade de artifacts
- `STORY-0656` / `ISSUE-0766` / `TASK-0656` — Implementar armazenamento e lifecycle: Registry de schemas e compatibilidade de artifacts
- `STORY-0657` / `ISSUE-0767` / `TASK-0657` — Expor serviços e integrar consumers: Registry de schemas e compatibilidade de artifacts
- `STORY-0658` / `ISSUE-0768` / `TASK-0658` — Validar segurança, recuperação e concorrência: Registry de schemas e compatibilidade de artifacts
- `STORY-0659` / `ISSUE-0769` / `TASK-0659` — Executar QA e auditoria final: Registry de schemas e compatibilidade de artifacts

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-035`, `ADR-053`
- **Resultado:** `PASS`
