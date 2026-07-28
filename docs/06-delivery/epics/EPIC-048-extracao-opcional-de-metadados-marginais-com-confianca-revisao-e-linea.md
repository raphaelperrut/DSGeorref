# EPIC-048 — extração opcional de metadados marginais com confiança, revisão e lineage

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-006 — Georreferenciamento`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0048`
- **Dependências:** EPIC-012, EPIC-045
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-044

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`

## Resultado

Extração opcional de metadados marginais com confiança, revisão e lineage.

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

- Requisitos: REQ-MTD-001
- Issue: `ISSUE-0048`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0289` / `ISSUE-0399` / `TASK-0289` — Definir contrato científico e invariantes: extração opcional de metadados marginais com confiança, revisão e lineage
- `STORY-0290` / `ISSUE-0400` / `TASK-0290` — Preparar corpus, fixtures e representação tipada: extração opcional de metadados marginais com confiança, revisão e lineage
- `STORY-0291` / `ISSUE-0401` / `TASK-0291` — Implementar o núcleo algorítmico: extração opcional de metadados marginais com confiança, revisão e lineage
- `STORY-0292` / `ISSUE-0402` / `TASK-0292` — Integrar ao ProcessingPlan e pipeline: extração opcional de metadados marginais com confiança, revisão e lineage
- `STORY-0293` / `ISSUE-0403` / `TASK-0293` — Produzir métricas, diagnóstico e lineage: extração opcional de metadados marginais com confiança, revisão e lineage
- `STORY-0294` / `ISSUE-0404` / `TASK-0294` — Executar benchmark, negativos e regressão científica: extração opcional de metadados marginais com confiança, revisão e lineage
- `STORY-0295` / `ISSUE-0405` / `TASK-0295` — Auditar evidência científica e final: extração opcional de metadados marginais com confiança, revisão e lineage

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`
- **Resultado:** `PASS`
