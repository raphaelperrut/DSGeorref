# EPIC-096 — Seletor e validador de CRS

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-006 — Georreferenciamento`
- **Sprint planejada:** `SPRINT-007`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0096`
- **Dependências:** Nenhuma
- **Release gate:** `G3/G4`
- **Referências arquiteturais:** ADR-041

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-025`, `ADR-034`, `ADR-041`, `ADR-042`, `ADR-043`

## Resultado

Seletor e validador de crs.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3/G4` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-CRS-004, REQ-CRS-005, REQ-CRS-006, REQ-CRS-007
- Issue: `ISSUE-0096`
- Sprint: `SPRINT-007`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0591` / `ISSUE-0701` / `TASK-0591` — Definir contrato científico e invariantes: Seletor e validador de CRS
- `STORY-0592` / `ISSUE-0702` / `TASK-0592` — Preparar corpus, fixtures e representação tipada: Seletor e validador de CRS
- `STORY-0593` / `ISSUE-0703` / `TASK-0593` — Implementar o núcleo algorítmico: Seletor e validador de CRS
- `STORY-0594` / `ISSUE-0704` / `TASK-0594` — Integrar ao ProcessingPlan e pipeline: Seletor e validador de CRS
- `STORY-0595` / `ISSUE-0705` / `TASK-0595` — Produzir métricas, diagnóstico e lineage: Seletor e validador de CRS
- `STORY-0596` / `ISSUE-0706` / `TASK-0596` — Executar benchmark, negativos e regressão científica: Seletor e validador de CRS
- `STORY-0597` / `ISSUE-0707` / `TASK-0597` — Auditar evidência científica e final: Seletor e validador de CRS

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-025`, `ADR-034`, `ADR-041`, `ADR-042`, `ADR-043`
- **Resultado:** `PASS`
