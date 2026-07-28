# EPIC-029 — etapas/capacidades canônicas e ProcessingPlan reproduzível

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-004 — Plano de Processamento e Workflow`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0029`
- **Dependências:** EPIC-004, EPIC-006, EPIC-021
- **Release gate:** `G1/G4`
- **Referências arquiteturais:** ADR-051, ADR-044, ADR-047

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`, `ADR-051`

## Resultado

Etapas/capacidades canônicas e processingplan reproduzível.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1/G4` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AI-008, REQ-AI-010, REQ-AI-011, REQ-AI-014, REQ-SRC-005, REQ-UX-002
- Issue: `ISSUE-0029`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0171` / `ISSUE-0281` / `TASK-0171` — Definir contrato científico e invariantes: etapas/capacidades canônicas e ProcessingPlan reproduzível
- `STORY-0172` / `ISSUE-0282` / `TASK-0172` — Preparar corpus, fixtures e representação tipada: etapas/capacidades canônicas e ProcessingPlan reproduzível
- `STORY-0173` / `ISSUE-0283` / `TASK-0173` — Implementar o núcleo algorítmico: etapas/capacidades canônicas e ProcessingPlan reproduzível
- `STORY-0174` / `ISSUE-0284` / `TASK-0174` — Integrar ao ProcessingPlan e pipeline: etapas/capacidades canônicas e ProcessingPlan reproduzível
- `STORY-0175` / `ISSUE-0285` / `TASK-0175` — Produzir métricas, diagnóstico e lineage: etapas/capacidades canônicas e ProcessingPlan reproduzível
- `STORY-0176` / `ISSUE-0286` / `TASK-0176` — Executar benchmark, negativos e regressão científica: etapas/capacidades canônicas e ProcessingPlan reproduzível
- `STORY-0177` / `ISSUE-0287` / `TASK-0177` — Auditar evidência científica e final: etapas/capacidades canônicas e ProcessingPlan reproduzível

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-004` — Plano de Processamento e Workflow.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`, `ADR-051`
- **Resultado:** `PASS`
