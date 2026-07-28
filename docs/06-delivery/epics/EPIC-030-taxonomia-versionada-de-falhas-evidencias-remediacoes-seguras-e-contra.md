# EPIC-030 — taxonomia versionada de falhas, evidências, remediações seguras e contratos de resultado por imagem

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-012 — Resultados, Diagnósticos e Exportação`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0030`
- **Dependências:** EPIC-004, EPIC-024
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-036, ADR-046, ADR-048

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-038`, `ADR-041`, `ADR-042`, `ADR-043`

## Resultado

Taxonomia versionada de falhas, evidências, remediações seguras e contratos de resultado por imagem.

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

- Requisitos: REQ-EPIC-016, REQ-EPIC-037, REQ-EPIC-038
- Issue: `ISSUE-0030`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0178` / `ISSUE-0288` / `TASK-0178` — Definir contrato científico e invariantes: taxonomia versionada de falhas, evidências, remediações seguras e contratos de resultado por imagem
- `STORY-0179` / `ISSUE-0289` / `TASK-0179` — Preparar corpus, fixtures e representação tipada: taxonomia versionada de falhas, evidências, remediações seguras e contratos de resultado por imagem
- `STORY-0180` / `ISSUE-0290` / `TASK-0180` — Implementar o núcleo algorítmico: taxonomia versionada de falhas, evidências, remediações seguras e contratos de resultado por imagem
- `STORY-0181` / `ISSUE-0291` / `TASK-0181` — Integrar ao ProcessingPlan e pipeline: taxonomia versionada de falhas, evidências, remediações seguras e contratos de resultado por imagem
- `STORY-0182` / `ISSUE-0292` / `TASK-0182` — Produzir métricas, diagnóstico e lineage: taxonomia versionada de falhas, evidências, remediações seguras e contratos de resultado por imagem
- `STORY-0183` / `ISSUE-0293` / `TASK-0183` — Executar benchmark, negativos e regressão científica: taxonomia versionada de falhas, evidências, remediações seguras e contratos de resultado por imagem
- `STORY-0184` / `ISSUE-0294` / `TASK-0184` — Auditar evidência científica e final: taxonomia versionada de falhas, evidências, remediações seguras e contratos de resultado por imagem

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-038`, `ADR-041`, `ADR-042`, `ADR-043`
- **Resultado:** `PASS`
