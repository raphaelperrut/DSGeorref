# EPIC-023 — correspondências e estimação robusta da homografia projetiva validadas

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-006 — Georreferenciamento`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0023`
- **Dependências:** EPIC-021
- **Release gate:** `G4`
- **Referências arquiteturais:** ADR-044, ADR-053

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-023`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-053`, `ADR-055`

## Resultado

Correspondências e estimação robusta da homografia projetiva validadas.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-FS1-001, REQ-FS1-002, REQ-FS1-003, REQ-FS1-004, REQ-FS1-005, REQ-FS1-006, REQ-FS1-007, REQ-FS1-008, REQ-FS1-009, REQ-FS1-010, REQ-HOM-001, REQ-MCH-001, REQ-SDR-001
- Issue: `ISSUE-0023`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0129` / `ISSUE-0239` / `TASK-0129` — Definir contrato científico e invariantes: correspondências e estimação robusta da homografia projetiva validadas
- `STORY-0130` / `ISSUE-0240` / `TASK-0130` — Preparar corpus, fixtures e representação tipada: correspondências e estimação robusta da homografia projetiva validadas
- `STORY-0131` / `ISSUE-0241` / `TASK-0131` — Implementar o núcleo algorítmico: correspondências e estimação robusta da homografia projetiva validadas
- `STORY-0132` / `ISSUE-0242` / `TASK-0132` — Integrar ao ProcessingPlan e pipeline: correspondências e estimação robusta da homografia projetiva validadas
- `STORY-0133` / `ISSUE-0243` / `TASK-0133` — Produzir métricas, diagnóstico e lineage: correspondências e estimação robusta da homografia projetiva validadas
- `STORY-0134` / `ISSUE-0244` / `TASK-0134` — Executar benchmark, negativos e regressão científica: correspondências e estimação robusta da homografia projetiva validadas
- `STORY-0135` / `ISSUE-0245` / `TASK-0135` — Auditar evidência científica e final: correspondências e estimação robusta da homografia projetiva validadas

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-023`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-053`, `ADR-055`
- **Resultado:** `PASS`
