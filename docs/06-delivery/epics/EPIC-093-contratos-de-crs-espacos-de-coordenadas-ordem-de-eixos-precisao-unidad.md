# EPIC-093 — contratos de CRS, espaços de coordenadas, ordem de eixos, precisão/unidades e validade raster

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-006 — Georreferenciamento`
- **Sprint planejada:** `SPRINT-007`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0093`
- **Dependências:** EPIC-044, EPIC-047, EPIC-063, EPIC-092
- **Release gate:** `G1/G3/G4`
- **Referências arquiteturais:** ADR-041

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`

## Resultado

Contratos de crs, espaços de coordenadas, ordem de eixos, precisão/unidades e validade raster.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1/G3/G4` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-CRS-001, REQ-CRS-002, REQ-CRS-003, REQ-CRS-004, REQ-RAS-001
- Issue: `ISSUE-0093`
- Sprint: `SPRINT-007`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0570` / `ISSUE-0680` / `TASK-0570` — Definir contrato científico e invariantes: contratos de CRS, espaços de coordenadas, ordem de eixos, precisão/unidades e validade raster
- `STORY-0571` / `ISSUE-0681` / `TASK-0571` — Preparar corpus, fixtures e representação tipada: contratos de CRS, espaços de coordenadas, ordem de eixos, precisão/unidades e validade raster
- `STORY-0572` / `ISSUE-0682` / `TASK-0572` — Implementar o núcleo algorítmico: contratos de CRS, espaços de coordenadas, ordem de eixos, precisão/unidades e validade raster
- `STORY-0573` / `ISSUE-0683` / `TASK-0573` — Integrar ao ProcessingPlan e pipeline: contratos de CRS, espaços de coordenadas, ordem de eixos, precisão/unidades e validade raster
- `STORY-0574` / `ISSUE-0684` / `TASK-0574` — Produzir métricas, diagnóstico e lineage: contratos de CRS, espaços de coordenadas, ordem de eixos, precisão/unidades e validade raster
- `STORY-0575` / `ISSUE-0685` / `TASK-0575` — Executar benchmark, negativos e regressão científica: contratos de CRS, espaços de coordenadas, ordem de eixos, precisão/unidades e validade raster
- `STORY-0576` / `ISSUE-0686` / `TASK-0576` — Auditar evidência científica e final: contratos de CRS, espaços de coordenadas, ordem de eixos, precisão/unidades e validade raster

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`
- **Resultado:** `PASS`
