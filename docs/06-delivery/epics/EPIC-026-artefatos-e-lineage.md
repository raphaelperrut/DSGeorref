# EPIC-026 — artefatos e lineage

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-013 — Artifacts, Proveniência e Lifecycle`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0026`
- **Dependências:** EPIC-012, EPIC-024
- **Release gate:** `G3/G4`
- **Referências arquiteturais:** ADR-051, ADR-018, ADR-044, ADR-027, ADR-041

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-015`, `ADR-019`, `ADR-023`, `ADR-024`, `ADR-025`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-052`, `ADR-055`

## Resultado

Artefatos e lineage.

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

- Requisitos: REQ-AI-005, REQ-ART-001, REQ-ARTLAYOUT-001, REQ-ARTLAYOUT-002, REQ-ARTLAYOUT-003, REQ-ARTLAYOUT-004, REQ-ARTLAYOUT-005, REQ-ARTLAYOUT-006, REQ-ARTLAYOUT-007, REQ-ARTLAYOUT-008, REQ-ARTLAYOUT-009, REQ-ARTLAYOUT-010, REQ-DBSCHEMA-006, REQ-FS1-001, REQ-FS1-002, REQ-FS1-003, REQ-FS1-004, REQ-FS1-005, REQ-FS1-006, REQ-FS1-007, REQ-FS1-008, REQ-FS1-009, REQ-FS1-010, REQ-NATIVE-001, REQ-NATIVE-002, REQ-NATIVE-003, REQ-NATIVE-004, REQ-NATIVE-005, REQ-NATIVE-006, REQ-NATIVE-007, REQ-NATIVE-008, REQ-NATIVE-009, REQ-NATIVE-010
- Issue: `ISSUE-0026`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **10** histórias filhas:

- `STORY-0150` / `ISSUE-0260` / `TASK-0150` — Definir contrato científico e invariantes: artefatos e lineage
- `STORY-0151` / `ISSUE-0261` / `TASK-0151` — Consolidar slices e liberar integração: artefatos e lineage
- `STORY-0152` / `ISSUE-0262` / `TASK-0152` — Implementar o núcleo algorítmico: artefatos e lineage
- `STORY-0153` / `ISSUE-0263` / `TASK-0153` — Integrar ao ProcessingPlan e pipeline: artefatos e lineage
- `STORY-0154` / `ISSUE-0264` / `TASK-0154` — Produzir métricas, diagnóstico e lineage: artefatos e lineage
- `STORY-0155` / `ISSUE-0265` / `TASK-0155` — Executar benchmark, negativos e regressão científica: artefatos e lineage
- `STORY-0156` / `ISSUE-0266` / `TASK-0156` — Auditar evidência científica e final: artefatos e lineage
- `STORY-0732` / `ISSUE-0842` / `TASK-0732` — Slice 1/3 — Preparar corpus, fixtures e representação tipada: artefatos e lineage [REQ-ART, REQ-ARTLAYOUT]
- `STORY-0733` / `ISSUE-0843` / `TASK-0733` — Slice 2/3 — Preparar corpus, fixtures e representação tipada: artefatos e lineage [REQ-ARTLAYOUT, REQ-DBSCHEMA, REQ-FS1, REQ-NATIVE]
- `STORY-0734` / `ISSUE-0844` / `TASK-0734` — Slice 3/3 — Preparar corpus, fixtures e representação tipada: artefatos e lineage [REQ-NATIVE]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-015`, `ADR-019`, `ADR-023`, `ADR-024`, `ADR-025`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-052`, `ADR-055`
- **Resultado:** `PASS`
