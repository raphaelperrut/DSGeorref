# EPIC-101 — Relative Mosaic Verifier e promotion lifecycle

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-008 — Mosaico Relativo`
- **Sprint planejada:** `SPRINT-008`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0101`
- **Dependências:** Nenhuma
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-050

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-050`

## Resultado

Relative mosaic verifier e promotion lifecycle.

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

- Requisitos: REQ-RMV-001, REQ-RMV-002, REQ-RMV-003, REQ-RMV-004
- Issue: `ISSUE-0101`
- Sprint: `SPRINT-008`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0626` / `ISSUE-0736` / `TASK-0626` — Definir contrato científico e invariantes: Relative Mosaic Verifier e promotion lifecycle
- `STORY-0627` / `ISSUE-0737` / `TASK-0627` — Preparar corpus, fixtures e representação tipada: Relative Mosaic Verifier e promotion lifecycle
- `STORY-0628` / `ISSUE-0738` / `TASK-0628` — Implementar o núcleo algorítmico: Relative Mosaic Verifier e promotion lifecycle
- `STORY-0629` / `ISSUE-0739` / `TASK-0629` — Integrar ao ProcessingPlan e pipeline: Relative Mosaic Verifier e promotion lifecycle
- `STORY-0630` / `ISSUE-0740` / `TASK-0630` — Produzir métricas, diagnóstico e lineage: Relative Mosaic Verifier e promotion lifecycle
- `STORY-0631` / `ISSUE-0741` / `TASK-0631` — Executar benchmark, negativos e regressão científica: Relative Mosaic Verifier e promotion lifecycle
- `STORY-0632` / `ISSUE-0742` / `TASK-0632` — Auditar evidência científica e final: Relative Mosaic Verifier e promotion lifecycle

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
