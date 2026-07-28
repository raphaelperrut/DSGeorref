# EPIC-095 — Validade raster explícita

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-006 — Georreferenciamento`
- **Sprint planejada:** `SPRINT-007`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0095`
- **Dependências:** Nenhuma
- **Release gate:** `G3/G4`
- **Referências arquiteturais:** ADR-041, ADR-049

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-049`

## Resultado

Validade raster explícita.

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

- Requisitos: REQ-MOS-006, REQ-RAS-004
- Issue: `ISSUE-0095`
- Sprint: `SPRINT-007`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0584` / `ISSUE-0694` / `TASK-0584` — Definir contrato científico e invariantes: Validade raster explícita
- `STORY-0585` / `ISSUE-0695` / `TASK-0585` — Preparar corpus, fixtures e representação tipada: Validade raster explícita
- `STORY-0586` / `ISSUE-0696` / `TASK-0586` — Implementar o núcleo algorítmico: Validade raster explícita
- `STORY-0587` / `ISSUE-0697` / `TASK-0587` — Integrar ao ProcessingPlan e pipeline: Validade raster explícita
- `STORY-0588` / `ISSUE-0698` / `TASK-0588` — Produzir métricas, diagnóstico e lineage: Validade raster explícita
- `STORY-0589` / `ISSUE-0699` / `TASK-0589` — Executar benchmark, negativos e regressão científica: Validade raster explícita
- `STORY-0590` / `ISSUE-0700` / `TASK-0590` — Auditar evidência científica e final: Validade raster explícita

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-049`
- **Resultado:** `PASS`
