# EPIC-054 — componentes provisórios multimodais, scores versionados, preview e correção sem equivalência com prova geométrica

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-005 — Descoberta e Aquisição de Referências`
- **Sprint planejada:** `SPRINT-006`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0054`
- **Dependências:** EPIC-012, EPIC-021, EPIC-053
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-044

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`

## Resultado

Componentes provisórios multimodais, scores versionados, preview e correção sem equivalência com prova geométrica.

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

- Requisitos: REQ-DIS-001
- Issue: `ISSUE-0054`
- Sprint: `SPRINT-006`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0330` / `ISSUE-0440` / `TASK-0330` — Definir contrato científico e invariantes: componentes provisórios multimodais, scores versionados, preview e correção sem equivalência com prova geométrica
- `STORY-0331` / `ISSUE-0441` / `TASK-0331` — Preparar corpus, fixtures e representação tipada: componentes provisórios multimodais, scores versionados, preview e correção sem equivalência com prova geométrica
- `STORY-0332` / `ISSUE-0442` / `TASK-0332` — Implementar o núcleo algorítmico: componentes provisórios multimodais, scores versionados, preview e correção sem equivalência com prova geométrica
- `STORY-0333` / `ISSUE-0443` / `TASK-0333` — Integrar ao ProcessingPlan e pipeline: componentes provisórios multimodais, scores versionados, preview e correção sem equivalência com prova geométrica
- `STORY-0334` / `ISSUE-0444` / `TASK-0334` — Produzir métricas, diagnóstico e lineage: componentes provisórios multimodais, scores versionados, preview e correção sem equivalência com prova geométrica
- `STORY-0335` / `ISSUE-0445` / `TASK-0335` — Executar benchmark, negativos e regressão científica: componentes provisórios multimodais, scores versionados, preview e correção sem equivalência com prova geométrica
- `STORY-0336` / `ISSUE-0446` / `TASK-0336` — Auditar evidência científica e final: componentes provisórios multimodais, scores versionados, preview e correção sem equivalência com prova geométrica

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`
- **Resultado:** `PASS`
