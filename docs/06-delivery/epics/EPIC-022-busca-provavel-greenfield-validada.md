# EPIC-022 — busca provável greenfield validada

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-005 — Descoberta e Aquisição de Referências`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0022`
- **Dependências:** EPIC-021
- **Release gate:** `G4`
- **Referências arquiteturais:** ADR-051, ADR-046, ADR-044, ADR-041

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-023`, `ADR-025`, `ADR-030`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`

## Resultado

Busca provável greenfield validada.

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

- Requisitos: REQ-AI-010, REQ-AIE-001, REQ-AIE-002, REQ-AIE-003, REQ-AIE-004, REQ-AIE-005, REQ-AIE-006, REQ-AIE-007, REQ-AIE-008, REQ-AIE-009, REQ-AIE-010, REQ-CLASSICPROFILE-001, REQ-CLASSICPROFILE-002, REQ-CLASSICPROFILE-003, REQ-CLASSICPROFILE-004, REQ-CLASSICPROFILE-005, REQ-CLASSICPROFILE-006, REQ-CLASSICPROFILE-007, REQ-CLASSICPROFILE-008, REQ-CLASSICPROFILE-009, REQ-CLASSICPROFILE-010, REQ-FS1-001, REQ-FS1-002, REQ-FS1-003, REQ-FS1-004, REQ-FS1-005, REQ-FS1-006, REQ-FS1-007, REQ-FS1-008, REQ-FS1-009, REQ-FS1-010, REQ-NATIVE-001, REQ-NATIVE-002, REQ-NATIVE-003, REQ-NATIVE-004, REQ-NATIVE-005, REQ-NATIVE-006, REQ-NATIVE-007, REQ-NATIVE-008, REQ-NATIVE-009, REQ-NATIVE-010, REQ-SGVCAL-001, REQ-SGVCAL-002, REQ-SGVCAL-003, REQ-SGVCAL-004, REQ-SGVCAL-005, REQ-SGVCAL-006, REQ-SGVCAL-007, REQ-SGVCAL-008, REQ-SGVCAL-009, REQ-SGVCAL-010
- Issue: `ISSUE-0022`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **11** histórias filhas:

- `STORY-0122` / `ISSUE-0232` / `TASK-0122` — Definir contrato científico e invariantes: busca provável greenfield validada
- `STORY-0123` / `ISSUE-0233` / `TASK-0123` — Consolidar slices e liberar integração: busca provável greenfield validada
- `STORY-0124` / `ISSUE-0234` / `TASK-0124` — Implementar o núcleo algorítmico: busca provável greenfield validada
- `STORY-0125` / `ISSUE-0235` / `TASK-0125` — Integrar ao ProcessingPlan e pipeline: busca provável greenfield validada
- `STORY-0126` / `ISSUE-0236` / `TASK-0126` — Produzir métricas, diagnóstico e lineage: busca provável greenfield validada
- `STORY-0127` / `ISSUE-0237` / `TASK-0127` — Executar benchmark, negativos e regressão científica: busca provável greenfield validada
- `STORY-0128` / `ISSUE-0238` / `TASK-0128` — Auditar evidência científica e final: busca provável greenfield validada
- `STORY-0725` / `ISSUE-0835` / `TASK-0725` — Slice 1/4 — Preparar corpus, fixtures e representação tipada: busca provável greenfield validada [REQ-AIE, REQ-CLASSICPROFILE]
- `STORY-0726` / `ISSUE-0836` / `TASK-0726` — Slice 2/4 — Preparar corpus, fixtures e representação tipada: busca provável greenfield validada [REQ-CLASSICPROFILE, REQ-FS1, REQ-NATIVE]
- `STORY-0727` / `ISSUE-0837` / `TASK-0727` — Slice 3/4 — Preparar corpus, fixtures e representação tipada: busca provável greenfield validada [REQ-NATIVE, REQ-SGVCAL]
- `STORY-0728` / `ISSUE-0838` / `TASK-0728` — Slice 4/4 — Preparar corpus, fixtures e representação tipada: busca provável greenfield validada [REQ-SGVCAL]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-023`, `ADR-025`, `ADR-030`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Resultado:** `PASS`
