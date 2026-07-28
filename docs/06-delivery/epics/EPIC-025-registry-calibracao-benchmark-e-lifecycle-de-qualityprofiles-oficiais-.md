# EPIC-025 — registry, calibração, benchmark e lifecycle de QualityProfiles oficiais/customizados

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-007 — Verificação Geométrica e Qualidade`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0025`
- **Dependências:** EPIC-021, EPIC-024
- **Release gate:** `G4`
- **Referências arquiteturais:** ADR-046

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-046`

## Resultado

Registry, calibração, benchmark e lifecycle de qualityprofiles oficiais/customizados.

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

- Requisitos: REQ-QUAL-004
- Issue: `ISSUE-0025`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0143` / `ISSUE-0253` / `TASK-0143` — Definir contrato científico e invariantes: registry, calibração, benchmark e lifecycle de QualityProfiles oficiais/customizados
- `STORY-0144` / `ISSUE-0254` / `TASK-0144` — Preparar corpus, fixtures e representação tipada: registry, calibração, benchmark e lifecycle de QualityProfiles oficiais/customizados
- `STORY-0145` / `ISSUE-0255` / `TASK-0145` — Implementar o núcleo algorítmico: registry, calibração, benchmark e lifecycle de QualityProfiles oficiais/customizados
- `STORY-0146` / `ISSUE-0256` / `TASK-0146` — Integrar ao ProcessingPlan e pipeline: registry, calibração, benchmark e lifecycle de QualityProfiles oficiais/customizados
- `STORY-0147` / `ISSUE-0257` / `TASK-0147` — Produzir métricas, diagnóstico e lineage: registry, calibração, benchmark e lifecycle de QualityProfiles oficiais/customizados
- `STORY-0148` / `ISSUE-0258` / `TASK-0148` — Executar benchmark, negativos e regressão científica: registry, calibração, benchmark e lifecycle de QualityProfiles oficiais/customizados
- `STORY-0149` / `ISSUE-0259` / `TASK-0149` — Auditar evidência científica e final: registry, calibração, benchmark e lifecycle de QualityProfiles oficiais/customizados

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-046`
- **Resultado:** `PASS`
