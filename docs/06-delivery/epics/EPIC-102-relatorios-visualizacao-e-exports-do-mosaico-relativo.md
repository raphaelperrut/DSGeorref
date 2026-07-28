# EPIC-102 — Relatórios, visualização e exports do mosaico relativo

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-008 — Mosaico Relativo`
- **Sprint planejada:** `SPRINT-008`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0102`
- **Dependências:** Nenhuma
- **Release gate:** `G3/G4/G7`
- **Referências arquiteturais:** ADR-050

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-050`

## Resultado

Relatórios, visualização e exports do mosaico relativo.

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

- Requisitos: REQ-RMR-001, REQ-RMR-002, REQ-RMR-003, REQ-RMR-004
- Issue: `ISSUE-0102`
- Sprint: `SPRINT-008`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0633` / `ISSUE-0743` / `TASK-0633` — Definir contrato científico e invariantes: Relatórios, visualização e exports do mosaico relativo
- `STORY-0634` / `ISSUE-0744` / `TASK-0634` — Preparar corpus, fixtures e representação tipada: Relatórios, visualização e exports do mosaico relativo
- `STORY-0635` / `ISSUE-0745` / `TASK-0635` — Implementar o núcleo algorítmico: Relatórios, visualização e exports do mosaico relativo
- `STORY-0636` / `ISSUE-0746` / `TASK-0636` — Integrar ao ProcessingPlan e pipeline: Relatórios, visualização e exports do mosaico relativo
- `STORY-0637` / `ISSUE-0747` / `TASK-0637` — Produzir métricas, diagnóstico e lineage: Relatórios, visualização e exports do mosaico relativo
- `STORY-0638` / `ISSUE-0748` / `TASK-0638` — Executar benchmark, negativos e regressão científica: Relatórios, visualização e exports do mosaico relativo
- `STORY-0639` / `ISSUE-0749` / `TASK-0639` — Auditar evidência científica e final: Relatórios, visualização e exports do mosaico relativo

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-008` — Mosaico Relativo.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-050`
- **Resultado:** `PASS`
