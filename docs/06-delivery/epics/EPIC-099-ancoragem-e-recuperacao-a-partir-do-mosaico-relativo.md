# EPIC-099 — Ancoragem e recuperação a partir do mosaico relativo

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-008 — Mosaico Relativo`
- **Sprint planejada:** `SPRINT-008`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0099`
- **Dependências:** Nenhuma
- **Release gate:** `G4`
- **Referências arquiteturais:** ADR-049, ADR-050

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-045`, `ADR-049`, `ADR-050`

## Resultado

Ancoragem e recuperação a partir do mosaico relativo.

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

- Requisitos: REQ-ANC-001, REQ-ANC-002, REQ-ANC-003, REQ-ANC-004, REQ-RMV-004
- Issue: `ISSUE-0099`
- Sprint: `SPRINT-008`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0612` / `ISSUE-0722` / `TASK-0612` — Definir contrato científico e invariantes: Ancoragem e recuperação a partir do mosaico relativo
- `STORY-0613` / `ISSUE-0723` / `TASK-0613` — Preparar corpus, fixtures e representação tipada: Ancoragem e recuperação a partir do mosaico relativo
- `STORY-0614` / `ISSUE-0724` / `TASK-0614` — Implementar o núcleo algorítmico: Ancoragem e recuperação a partir do mosaico relativo
- `STORY-0615` / `ISSUE-0725` / `TASK-0615` — Integrar ao ProcessingPlan e pipeline: Ancoragem e recuperação a partir do mosaico relativo
- `STORY-0616` / `ISSUE-0726` / `TASK-0616` — Produzir métricas, diagnóstico e lineage: Ancoragem e recuperação a partir do mosaico relativo
- `STORY-0617` / `ISSUE-0727` / `TASK-0617` — Executar benchmark, negativos e regressão científica: Ancoragem e recuperação a partir do mosaico relativo
- `STORY-0618` / `ISSUE-0728` / `TASK-0618` — Auditar evidência científica e final: Ancoragem e recuperação a partir do mosaico relativo

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-008` — Mosaico Relativo.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-045`, `ADR-049`, `ADR-050`
- **Resultado:** `PASS`
