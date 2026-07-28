# EPIC-059 — busca espaciotemporal guiada, ranking explicável, incerteza e expansão limitada por orçamento

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-005 — Descoberta e Aquisição de Referências`
- **Sprint planejada:** `SPRINT-006`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0059`
- **Dependências:** EPIC-022, EPIC-058
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-047

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`

## Resultado

Busca espaciotemporal guiada, ranking explicável, incerteza e expansão limitada por orçamento.

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

- Requisitos: REQ-SRC-004
- Issue: `ISSUE-0059`
- Sprint: `SPRINT-006`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0365` / `ISSUE-0475` / `TASK-0365` — Definir contrato científico e invariantes: busca espaciotemporal guiada, ranking explicável, incerteza e expansão limitada por orçamento
- `STORY-0366` / `ISSUE-0476` / `TASK-0366` — Preparar corpus, fixtures e representação tipada: busca espaciotemporal guiada, ranking explicável, incerteza e expansão limitada por orçamento
- `STORY-0367` / `ISSUE-0477` / `TASK-0367` — Implementar o núcleo algorítmico: busca espaciotemporal guiada, ranking explicável, incerteza e expansão limitada por orçamento
- `STORY-0368` / `ISSUE-0478` / `TASK-0368` — Integrar ao ProcessingPlan e pipeline: busca espaciotemporal guiada, ranking explicável, incerteza e expansão limitada por orçamento
- `STORY-0369` / `ISSUE-0479` / `TASK-0369` — Produzir métricas, diagnóstico e lineage: busca espaciotemporal guiada, ranking explicável, incerteza e expansão limitada por orçamento
- `STORY-0370` / `ISSUE-0480` / `TASK-0370` — Executar benchmark, negativos e regressão científica: busca espaciotemporal guiada, ranking explicável, incerteza e expansão limitada por orçamento
- `STORY-0371` / `ISSUE-0481` / `TASK-0371` — Auditar evidência científica e final: busca espaciotemporal guiada, ranking explicável, incerteza e expansão limitada por orçamento

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
