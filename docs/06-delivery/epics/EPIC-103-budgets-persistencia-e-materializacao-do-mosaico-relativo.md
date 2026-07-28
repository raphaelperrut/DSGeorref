# EPIC-103 — Budgets, persistência e materialização do mosaico relativo

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-008 — Mosaico Relativo`
- **Sprint planejada:** `SPRINT-008`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0103`
- **Dependências:** Nenhuma
- **Release gate:** `G3/G4/G7`
- **Referências arquiteturais:** ADR-050

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-036`, `ADR-039`, `ADR-041`, `ADR-042`, `ADR-043`

## Resultado

Budgets, persistência e materialização do mosaico relativo.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3/G4/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-RMQ-001, REQ-RMQ-002, REQ-RMQ-003, REQ-RMQ-004
- Issue: `ISSUE-0103`
- Sprint: `SPRINT-008`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0640` / `ISSUE-0750` / `TASK-0640` — Definir contrato científico e invariantes: Budgets, persistência e materialização do mosaico relativo
- `STORY-0641` / `ISSUE-0751` / `TASK-0641` — Preparar corpus, fixtures e representação tipada: Budgets, persistência e materialização do mosaico relativo
- `STORY-0642` / `ISSUE-0752` / `TASK-0642` — Implementar o núcleo algorítmico: Budgets, persistência e materialização do mosaico relativo
- `STORY-0643` / `ISSUE-0753` / `TASK-0643` — Integrar ao ProcessingPlan e pipeline: Budgets, persistência e materialização do mosaico relativo
- `STORY-0644` / `ISSUE-0754` / `TASK-0644` — Produzir métricas, diagnóstico e lineage: Budgets, persistência e materialização do mosaico relativo
- `STORY-0645` / `ISSUE-0755` / `TASK-0645` — Executar benchmark, negativos e regressão científica: Budgets, persistência e materialização do mosaico relativo
- `STORY-0646` / `ISSUE-0756` / `TASK-0646` — Auditar evidência científica e final: Budgets, persistência e materialização do mosaico relativo

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-008` — Mosaico Relativo.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-036`, `ADR-039`, `ADR-041`, `ADR-042`, `ADR-043`
- **Resultado:** `PASS`
