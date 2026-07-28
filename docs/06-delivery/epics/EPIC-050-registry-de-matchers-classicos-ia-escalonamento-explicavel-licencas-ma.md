# EPIC-050 — registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-009 — Recuperação Assistida por IA e Governança de Modelos`
- **Sprint planejada:** `SPRINT-006`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0050`
- **Dependências:** EPIC-004, EPIC-021, EPIC-047
- **Release gate:** `G4/G5`
- **Referências arquiteturais:** ADR-051, ADR-039, ADR-044, ADR-053

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-017`, `ADR-030`, `ADR-033`, `ADR-037`, `ADR-038`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`

## Resultado

Registry de matchers clássicos/ia, escalonamento explicável, licenças, manifests e benchmark.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4/G5` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AI-001, REQ-AI-005, REQ-AI-008, REQ-AI-009, REQ-AI-012, REQ-AI-013, REQ-AI-015, REQ-AI-017, REQ-AIE-001, REQ-AIE-002, REQ-AIE-003, REQ-AIE-004, REQ-AIE-005, REQ-AIE-006, REQ-AIE-007, REQ-AIE-008, REQ-AIE-009, REQ-AIE-010, REQ-EPIC-088, REQ-MCH-001, REQ-SCH-003, REQ-SDR-001, REQ-SDR-002, REQ-SDR-003
- Issue: `ISSUE-0050`
- Sprint: `SPRINT-006`

## Histórias implementáveis


Este épico possui **9** histórias filhas:

- `STORY-0302` / `ISSUE-0412` / `TASK-0302` — Definir contrato científico e invariantes: registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark
- `STORY-0303` / `ISSUE-0413` / `TASK-0303` — Consolidar slices e liberar integração: registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark
- `STORY-0304` / `ISSUE-0414` / `TASK-0304` — Implementar o núcleo algorítmico: registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark
- `STORY-0305` / `ISSUE-0415` / `TASK-0305` — Integrar ao ProcessingPlan e pipeline: registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark
- `STORY-0306` / `ISSUE-0416` / `TASK-0306` — Produzir métricas, diagnóstico e lineage: registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark
- `STORY-0307` / `ISSUE-0417` / `TASK-0307` — Executar benchmark, negativos e regressão científica: registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark
- `STORY-0308` / `ISSUE-0418` / `TASK-0308` — Auditar evidência científica e final: registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark
- `STORY-0750` / `ISSUE-0860` / `TASK-0750` — Slice 1/2 — Preparar corpus, fixtures e representação tipada: registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark [REQ-AI, REQ-AIE]
- `STORY-0751` / `ISSUE-0861` / `TASK-0751` — Slice 2/2 — Preparar corpus, fixtures e representação tipada: registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark [REQ-AIE, REQ-EPIC, REQ-SCH, REQ-SDR]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-009` — Recuperação Assistida por IA e Governança de Modelos.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-017`, `ADR-030`, `ADR-033`, `ADR-037`, `ADR-038`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Resultado:** `PASS`
