# EPIC-035 — workflow de revisão com gates revisáveis, hard gates imutáveis, checklist e auditoria

- **Domínio:** `REV`
- **Bounded Context owner:** `BC-011 — Revisão e Correção`
- **Sprint planejada:** `SPRINT-009`
- **Papel responsável pela implementação:** `Frontend`
- **Issue principal:** `ISSUE-0035`
- **Dependências:** EPIC-010, EPIC-025, EPIC-034
- **Release gate:** `G4/G5/G7`
- **Referências arquiteturais:** ADR-048

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-046`

## Resultado

Workflow de revisão com gates revisáveis, hard gates imutáveis, checklist e auditoria.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4/G5/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-EPIC-035
- Issue: `ISSUE-0035`
- Sprint: `SPRINT-009`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0209` / `ISSUE-0319` / `TASK-0209` — Definir fluxo de revisão e decisões permitidas: workflow de revisão com gates revisáveis, hard gates imutáveis, checklist e auditoria
- `STORY-0210` / `ISSUE-0320` / `TASK-0210` — Definir contratos de correção e nova tentativa: workflow de revisão com gates revisáveis, hard gates imutáveis, checklist e auditoria
- `STORY-0211` / `ISSUE-0321` / `TASK-0211` — Implementar workspace e comparação: workflow de revisão com gates revisáveis, hard gates imutáveis, checklist e auditoria
- `STORY-0212` / `ISSUE-0322` / `TASK-0212` — Implementar lifecycle e auditoria: workflow de revisão com gates revisáveis, hard gates imutáveis, checklist e auditoria
- `STORY-0213` / `ISSUE-0323` / `TASK-0213` — Executar testes de revisão, hard gates e concorrência: workflow de revisão com gates revisáveis, hard gates imutáveis, checklist e auditoria
- `STORY-0214` / `ISSUE-0324` / `TASK-0214` — Auditar rastreabilidade e evidência final: workflow de revisão com gates revisáveis, hard gates imutáveis, checklist e auditoria

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-011` — Revisão e Correção.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-046`
- **Resultado:** `PASS`
