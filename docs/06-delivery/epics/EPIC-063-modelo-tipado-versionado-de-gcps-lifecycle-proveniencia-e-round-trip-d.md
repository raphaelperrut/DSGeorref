# EPIC-063 — modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-011 — Revisão e Correção`
- **Sprint planejada:** `SPRINT-006`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0063`
- **Dependências:** EPIC-012, EPIC-052
- **Release gate:** `G3/G4/G6`
- **Referências arquiteturais:** ADR-048, ADR-041

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-048`

## Resultado

Modelo tipado/versionado de gcps, lifecycle, proveniência e round-trip dos exports.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3/G4/G6` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-CRS-001, REQ-GCP-002
- Issue: `ISSUE-0063`
- Sprint: `SPRINT-006`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0391` / `ISSUE-0501` / `TASK-0391` — Definir contrato científico e invariantes: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0392` / `ISSUE-0502` / `TASK-0392` — Preparar corpus, fixtures e representação tipada: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0393` / `ISSUE-0503` / `TASK-0393` — Implementar o núcleo algorítmico: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0394` / `ISSUE-0504` / `TASK-0394` — Integrar ao ProcessingPlan e pipeline: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0395` / `ISSUE-0505` / `TASK-0395` — Produzir métricas, diagnóstico e lineage: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0396` / `ISSUE-0506` / `TASK-0396` — Executar benchmark, negativos e regressão científica: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0397` / `ISSUE-0507` / `TASK-0397` — Auditar evidência científica e final: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-011` — Revisão e Correção.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-048`
- **Resultado:** `PASS`
