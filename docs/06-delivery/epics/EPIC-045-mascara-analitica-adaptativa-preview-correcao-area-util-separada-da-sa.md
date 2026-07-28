# EPIC-045 — máscara analítica adaptativa, preview/correção, área útil separada da saída e preservação de metadados marginais

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-006 — Georreferenciamento`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0045`
- **Dependências:** EPIC-021, EPIC-023, EPIC-044
- **Release gate:** `G4`
- **Referências arquiteturais:** ADR-044, ADR-041

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-055`

## Resultado

Máscara analítica adaptativa, preview/correção, área útil separada da saída e preservação de metadados marginais.

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

- Requisitos: REQ-MSK-001, REQ-MSK-002, REQ-MSK-003, REQ-RAS-001
- Issue: `ISSUE-0045`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0268` / `ISSUE-0378` / `TASK-0268` — Definir contrato científico e invariantes: máscara analítica adaptativa, preview/correção, área útil separada da saída e preservação de metadados marginais
- `STORY-0269` / `ISSUE-0379` / `TASK-0269` — Preparar corpus, fixtures e representação tipada: máscara analítica adaptativa, preview/correção, área útil separada da saída e preservação de metadados marginais
- `STORY-0270` / `ISSUE-0380` / `TASK-0270` — Implementar o núcleo algorítmico: máscara analítica adaptativa, preview/correção, área útil separada da saída e preservação de metadados marginais
- `STORY-0271` / `ISSUE-0381` / `TASK-0271` — Integrar ao ProcessingPlan e pipeline: máscara analítica adaptativa, preview/correção, área útil separada da saída e preservação de metadados marginais
- `STORY-0272` / `ISSUE-0382` / `TASK-0272` — Produzir métricas, diagnóstico e lineage: máscara analítica adaptativa, preview/correção, área útil separada da saída e preservação de metadados marginais
- `STORY-0273` / `ISSUE-0383` / `TASK-0273` — Executar benchmark, negativos e regressão científica: máscara analítica adaptativa, preview/correção, área útil separada da saída e preservação de metadados marginais
- `STORY-0274` / `ISSUE-0384` / `TASK-0274` — Auditar evidência científica e final: máscara analítica adaptativa, preview/correção, área útil separada da saída e preservação de metadados marginais

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-006` — Georreferenciamento.
- **Classificação:** `Core`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-055`
- **Resultado:** `PASS`
