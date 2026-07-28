# EPIC-062 — workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático

- **Domínio:** `REV`
- **Bounded Context owner:** `BC-011 — Revisão e Correção`
- **Sprint planejada:** `SPRINT-009`
- **Papel responsável pela implementação:** `Frontend`
- **Issue principal:** `ISSUE-0062`
- **Dependências:** EPIC-024, EPIC-032, EPIC-034, EPIC-035
- **Release gate:** `G4/G5/G7`
- **Referências arquiteturais:** ADR-048

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-048`

## Resultado

Workspace visual assistido, correctionsets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático.

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

- Requisitos: REQ-EPIC-062, REQ-REV-003, REQ-REV-004
- Issue: `ISSUE-0062`
- Sprint: `SPRINT-009`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0385` / `ISSUE-0495` / `TASK-0385` — Definir fluxo de revisão e decisões permitidas: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático
- `STORY-0386` / `ISSUE-0496` / `TASK-0386` — Definir contratos de correção e nova tentativa: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático
- `STORY-0387` / `ISSUE-0497` / `TASK-0387` — Implementar workspace e comparação: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático
- `STORY-0388` / `ISSUE-0498` / `TASK-0388` — Implementar lifecycle e auditoria: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático
- `STORY-0389` / `ISSUE-0499` / `TASK-0389` — Executar testes de revisão, hard gates e concorrência: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático
- `STORY-0390` / `ISSUE-0500` / `TASK-0390` — Auditar rastreabilidade e evidência final: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-011` — Revisão e Correção.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-048`
- **Resultado:** `PASS`
