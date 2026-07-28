# EPIC-052 — seleção de GCPs por cobertura/qualidade/diversidade, exportando pontos usados e descartados

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-006 — Georreferenciamento`
- **Sprint planejada:** `SPRINT-006`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0052`
- **Dependências:** EPIC-023, EPIC-045, EPIC-051
- **Release gate:** `G4`
- **Referências arquiteturais:** ADR-044

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-048`

## Resultado

Seleção de gcps por cobertura/qualidade/diversidade, exportando pontos usados e descartados.

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

- Requisitos: REQ-GCP-001
- Issue: `ISSUE-0052`
- Sprint: `SPRINT-006`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0316` / `ISSUE-0426` / `TASK-0316` — Definir contrato científico e invariantes: seleção de GCPs por cobertura/qualidade/diversidade, exportando pontos usados e descartados
- `STORY-0317` / `ISSUE-0427` / `TASK-0317` — Preparar corpus, fixtures e representação tipada: seleção de GCPs por cobertura/qualidade/diversidade, exportando pontos usados e descartados
- `STORY-0318` / `ISSUE-0428` / `TASK-0318` — Implementar o núcleo algorítmico: seleção de GCPs por cobertura/qualidade/diversidade, exportando pontos usados e descartados
- `STORY-0319` / `ISSUE-0429` / `TASK-0319` — Integrar ao ProcessingPlan e pipeline: seleção de GCPs por cobertura/qualidade/diversidade, exportando pontos usados e descartados
- `STORY-0320` / `ISSUE-0430` / `TASK-0320` — Produzir métricas, diagnóstico e lineage: seleção de GCPs por cobertura/qualidade/diversidade, exportando pontos usados e descartados
- `STORY-0321` / `ISSUE-0431` / `TASK-0321` — Executar benchmark, negativos e regressão científica: seleção de GCPs por cobertura/qualidade/diversidade, exportando pontos usados e descartados
- `STORY-0322` / `ISSUE-0432` / `TASK-0322` — Auditar evidência científica e final: seleção de GCPs por cobertura/qualidade/diversidade, exportando pontos usados e descartados

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-048`
- **Resultado:** `PASS`
