# EPIC-094 — Registry e transformações de CRS

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-006 — Georreferenciamento`
- **Sprint planejada:** `SPRINT-007`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0094`
- **Dependências:** Nenhuma
- **Release gate:** `G3/G4`
- **Referências arquiteturais:** ADR-041

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`

## Resultado

Registry e transformações de crs.

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

- Requisitos: REQ-CRS-001, REQ-CRS-002, REQ-CRS-003, REQ-CRS-004, REQ-CRS-005, REQ-CRS-006, REQ-CRS-007, REQ-NATIVE-002
- Issue: `ISSUE-0094`
- Sprint: `SPRINT-007`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0577` / `ISSUE-0687` / `TASK-0577` — Definir contrato científico e invariantes: Registry e transformações de CRS
- `STORY-0578` / `ISSUE-0688` / `TASK-0578` — Preparar corpus, fixtures e representação tipada: Registry e transformações de CRS
- `STORY-0579` / `ISSUE-0689` / `TASK-0579` — Implementar o núcleo algorítmico: Registry e transformações de CRS
- `STORY-0580` / `ISSUE-0690` / `TASK-0580` — Integrar ao ProcessingPlan e pipeline: Registry e transformações de CRS
- `STORY-0581` / `ISSUE-0691` / `TASK-0581` — Produzir métricas, diagnóstico e lineage: Registry e transformações de CRS
- `STORY-0582` / `ISSUE-0692` / `TASK-0582` — Executar benchmark, negativos e regressão científica: Registry e transformações de CRS
- `STORY-0583` / `ISSUE-0693` / `TASK-0583` — Auditar evidência científica e final: Registry e transformações de CRS

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
