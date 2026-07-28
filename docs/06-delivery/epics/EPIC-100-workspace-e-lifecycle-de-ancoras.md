# EPIC-100 — Workspace e lifecycle de âncoras

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-008 — Mosaico Relativo`
- **Sprint planejada:** `SPRINT-008`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0100`
- **Dependências:** Nenhuma
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-049

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-048`, `ADR-049`, `ADR-055`

## Resultado

Workspace e lifecycle de âncoras.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-ANC-005, REQ-ANC-006, REQ-ANC-007, REQ-ANC-008
- Issue: `ISSUE-0100`
- Sprint: `SPRINT-008`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0619` / `ISSUE-0729` / `TASK-0619` — Definir contrato científico e invariantes: Workspace e lifecycle de âncoras
- `STORY-0620` / `ISSUE-0730` / `TASK-0620` — Preparar corpus, fixtures e representação tipada: Workspace e lifecycle de âncoras
- `STORY-0621` / `ISSUE-0731` / `TASK-0621` — Implementar o núcleo algorítmico: Workspace e lifecycle de âncoras
- `STORY-0622` / `ISSUE-0732` / `TASK-0622` — Integrar ao ProcessingPlan e pipeline: Workspace e lifecycle de âncoras
- `STORY-0623` / `ISSUE-0733` / `TASK-0623` — Produzir métricas, diagnóstico e lineage: Workspace e lifecycle de âncoras
- `STORY-0624` / `ISSUE-0734` / `TASK-0624` — Executar benchmark, negativos e regressão científica: Workspace e lifecycle de âncoras
- `STORY-0625` / `ISSUE-0735` / `TASK-0625` — Auditar evidência científica e final: Workspace e lifecycle de âncoras

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-008` — Mosaico Relativo.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-048`, `ADR-049`, `ADR-055`
- **Resultado:** `PASS`
