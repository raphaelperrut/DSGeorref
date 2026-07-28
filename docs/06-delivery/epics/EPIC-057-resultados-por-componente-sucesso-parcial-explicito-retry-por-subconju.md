# EPIC-057 — resultados por componente, sucesso parcial explícito, retry por subconjunto e UX de componentes não resolvidos

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-012 — Resultados, Diagnósticos e Exportação`
- **Sprint planejada:** `SPRINT-006`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0057`
- **Dependências:** EPIC-030, EPIC-053, EPIC-056
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-036, ADR-046, ADR-039, ADR-048

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-039`, `ADR-041`, `ADR-042`, `ADR-043`

## Resultado

Resultados por componente, sucesso parcial explícito, retry por subconjunto e ux de componentes não resolvidos.

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

- Requisitos: REQ-BAT-001
- Issue: `ISSUE-0057`
- Sprint: `SPRINT-006`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0351` / `ISSUE-0461` / `TASK-0351` — Definir contrato científico e invariantes: resultados por componente, sucesso parcial explícito, retry por subconjunto e UX de componentes não resolvidos
- `STORY-0352` / `ISSUE-0462` / `TASK-0352` — Preparar corpus, fixtures e representação tipada: resultados por componente, sucesso parcial explícito, retry por subconjunto e UX de componentes não resolvidos
- `STORY-0353` / `ISSUE-0463` / `TASK-0353` — Implementar o núcleo algorítmico: resultados por componente, sucesso parcial explícito, retry por subconjunto e UX de componentes não resolvidos
- `STORY-0354` / `ISSUE-0464` / `TASK-0354` — Integrar ao ProcessingPlan e pipeline: resultados por componente, sucesso parcial explícito, retry por subconjunto e UX de componentes não resolvidos
- `STORY-0355` / `ISSUE-0465` / `TASK-0355` — Produzir métricas, diagnóstico e lineage: resultados por componente, sucesso parcial explícito, retry por subconjunto e UX de componentes não resolvidos
- `STORY-0356` / `ISSUE-0466` / `TASK-0356` — Executar benchmark, negativos e regressão científica: resultados por componente, sucesso parcial explícito, retry por subconjunto e UX de componentes não resolvidos
- `STORY-0357` / `ISSUE-0467` / `TASK-0357` — Auditar evidência científica e final: resultados por componente, sucesso parcial explícito, retry por subconjunto e UX de componentes não resolvidos

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-039`, `ADR-041`, `ADR-042`, `ADR-043`
- **Resultado:** `PASS`
