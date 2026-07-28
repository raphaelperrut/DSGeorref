# EPIC-021 — corpus versionado com décadas e condições distintas

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-007 — Verificação Geométrica e Qualidade`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0021`
- **Dependências:** EPIC-006
- **Release gate:** `G4`
- **Referências arquiteturais:** ADR-046, ADR-044, ADR-047, ADR-041

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-023`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-053`, `ADR-055`

## Resultado

Corpus versionado com décadas e condições distintas.

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

- Requisitos: REQ-DBSCHEMA-005, REQ-EPIC-021, REQ-FS1-001, REQ-FS1-002, REQ-FS1-003, REQ-FS1-004, REQ-FS1-005, REQ-FS1-006, REQ-FS1-007, REQ-FS1-008, REQ-FS1-009, REQ-FS1-010, REQ-NATIVE-001, REQ-NATIVE-002, REQ-NATIVE-003, REQ-NATIVE-004, REQ-NATIVE-005, REQ-NATIVE-006, REQ-NATIVE-007, REQ-NATIVE-008, REQ-NATIVE-009, REQ-NATIVE-010, REQ-SCP-001
- Issue: `ISSUE-0021`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **9** histórias filhas:

- `STORY-0115` / `ISSUE-0225` / `TASK-0115` — Definir contrato científico e invariantes: corpus versionado com décadas e condições distintas
- `STORY-0116` / `ISSUE-0226` / `TASK-0116` — Consolidar slices e liberar integração: corpus versionado com décadas e condições distintas
- `STORY-0117` / `ISSUE-0227` / `TASK-0117` — Implementar o núcleo algorítmico: corpus versionado com décadas e condições distintas
- `STORY-0118` / `ISSUE-0228` / `TASK-0118` — Integrar ao ProcessingPlan e pipeline: corpus versionado com décadas e condições distintas
- `STORY-0119` / `ISSUE-0229` / `TASK-0119` — Produzir métricas, diagnóstico e lineage: corpus versionado com décadas e condições distintas
- `STORY-0120` / `ISSUE-0230` / `TASK-0120` — Executar benchmark, negativos e regressão científica: corpus versionado com décadas e condições distintas
- `STORY-0121` / `ISSUE-0231` / `TASK-0121` — Auditar evidência científica e final: corpus versionado com décadas e condições distintas
- `STORY-0723` / `ISSUE-0833` / `TASK-0723` — Slice 1/2 — Preparar corpus, fixtures e representação tipada: corpus versionado com décadas e condições distintas [REQ-EPIC, REQ-FS1, REQ-NATIVE]
- `STORY-0724` / `ISSUE-0834` / `TASK-0724` — Slice 2/2 — Preparar corpus, fixtures e representação tipada: corpus versionado com décadas e condições distintas [REQ-NATIVE, REQ-SCP]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-023`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-053`, `ADR-055`
- **Resultado:** `PASS`
