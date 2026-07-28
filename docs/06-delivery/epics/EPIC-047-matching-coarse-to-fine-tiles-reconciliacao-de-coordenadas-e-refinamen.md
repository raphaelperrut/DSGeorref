# EPIC-047 — matching coarse-to-fine, tiles, reconciliação de coordenadas e refinamento em resolução adequada

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-006 — Georreferenciamento`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0047`
- **Dependências:** EPIC-019, EPIC-021, EPIC-023
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-044

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`

## Resultado

Matching coarse-to-fine, tiles, reconciliação de coordenadas e refinamento em resolução adequada.

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

- Requisitos: REQ-MAT-001
- Issue: `ISSUE-0047`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0282` / `ISSUE-0392` / `TASK-0282` — Definir contrato científico e invariantes: matching coarse-to-fine, tiles, reconciliação de coordenadas e refinamento em resolução adequada
- `STORY-0283` / `ISSUE-0393` / `TASK-0283` — Preparar corpus, fixtures e representação tipada: matching coarse-to-fine, tiles, reconciliação de coordenadas e refinamento em resolução adequada
- `STORY-0284` / `ISSUE-0394` / `TASK-0284` — Implementar o núcleo algorítmico: matching coarse-to-fine, tiles, reconciliação de coordenadas e refinamento em resolução adequada
- `STORY-0285` / `ISSUE-0395` / `TASK-0285` — Integrar ao ProcessingPlan e pipeline: matching coarse-to-fine, tiles, reconciliação de coordenadas e refinamento em resolução adequada
- `STORY-0286` / `ISSUE-0396` / `TASK-0286` — Produzir métricas, diagnóstico e lineage: matching coarse-to-fine, tiles, reconciliação de coordenadas e refinamento em resolução adequada
- `STORY-0287` / `ISSUE-0397` / `TASK-0287` — Executar benchmark, negativos e regressão científica: matching coarse-to-fine, tiles, reconciliação de coordenadas e refinamento em resolução adequada
- `STORY-0288` / `ISSUE-0398` / `TASK-0288` — Auditar evidência científica e final: matching coarse-to-fine, tiles, reconciliação de coordenadas e refinamento em resolução adequada

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`
- **Resultado:** `PASS`
