# EPIC-098 — Mosaico relativo de recuperação

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-008 — Mosaico Relativo`
- **Sprint planejada:** `SPRINT-007`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0098`
- **Dependências:** Nenhuma
- **Release gate:** `G3/G4/G7`
- **Referências arquiteturais:** ADR-049, ADR-050

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-036`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-049`, `ADR-050`

## Resultado

Mosaico relativo de recuperação.

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

- Requisitos: REQ-MOS-001, REQ-MOS-002, REQ-MOS-003, REQ-MOS-004, REQ-MOS-005, REQ-MOS-006, REQ-RMQ-003, REQ-RMR-004
- Issue: `ISSUE-0098`
- Sprint: `SPRINT-007`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0605` / `ISSUE-0715` / `TASK-0605` — Definir contrato científico e invariantes: Mosaico relativo de recuperação
- `STORY-0606` / `ISSUE-0716` / `TASK-0606` — Preparar corpus, fixtures e representação tipada: Mosaico relativo de recuperação
- `STORY-0607` / `ISSUE-0717` / `TASK-0607` — Implementar o núcleo algorítmico: Mosaico relativo de recuperação
- `STORY-0608` / `ISSUE-0718` / `TASK-0608` — Integrar ao ProcessingPlan e pipeline: Mosaico relativo de recuperação
- `STORY-0609` / `ISSUE-0719` / `TASK-0609` — Produzir métricas, diagnóstico e lineage: Mosaico relativo de recuperação
- `STORY-0610` / `ISSUE-0720` / `TASK-0610` — Executar benchmark, negativos e regressão científica: Mosaico relativo de recuperação
- `STORY-0611` / `ISSUE-0721` / `TASK-0611` — Auditar evidência científica e final: Mosaico relativo de recuperação

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-008` — Mosaico Relativo.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-036`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-049`, `ADR-050`
- **Resultado:** `PASS`
