# EPIC-060 — policy de aquisição no ProcessingPlan, preview, consentimento e bloqueio fail-closed de ativos pagos/ambíguos

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-005 — Descoberta e Aquisição de Referências`
- **Sprint planejada:** `SPRINT-006`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0060`
- **Dependências:** EPIC-029, EPIC-058, EPIC-059
- **Release gate:** `G4/G5/G7`
- **Referências arquiteturais:** ADR-047

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`

## Resultado

Policy de aquisição no processingplan, preview, consentimento e bloqueio fail-closed de ativos pagos/ambíguos.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4/G5/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-PUB-003, REQ-SRC-005
- Issue: `ISSUE-0060`
- Sprint: `SPRINT-006`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0372` / `ISSUE-0482` / `TASK-0372` — Definir contrato científico e invariantes: policy de aquisição no ProcessingPlan, preview, consentimento e bloqueio fail-closed de ativos pagos/ambíguos
- `STORY-0373` / `ISSUE-0483` / `TASK-0373` — Preparar corpus, fixtures e representação tipada: policy de aquisição no ProcessingPlan, preview, consentimento e bloqueio fail-closed de ativos pagos/ambíguos
- `STORY-0374` / `ISSUE-0484` / `TASK-0374` — Implementar o núcleo algorítmico: policy de aquisição no ProcessingPlan, preview, consentimento e bloqueio fail-closed de ativos pagos/ambíguos
- `STORY-0375` / `ISSUE-0485` / `TASK-0375` — Integrar ao ProcessingPlan e pipeline: policy de aquisição no ProcessingPlan, preview, consentimento e bloqueio fail-closed de ativos pagos/ambíguos
- `STORY-0376` / `ISSUE-0486` / `TASK-0376` — Produzir métricas, diagnóstico e lineage: policy de aquisição no ProcessingPlan, preview, consentimento e bloqueio fail-closed de ativos pagos/ambíguos
- `STORY-0377` / `ISSUE-0487` / `TASK-0377` — Executar benchmark, negativos e regressão científica: policy de aquisição no ProcessingPlan, preview, consentimento e bloqueio fail-closed de ativos pagos/ambíguos
- `STORY-0378` / `ISSUE-0488` / `TASK-0378` — Auditar evidência científica e final: policy de aquisição no ProcessingPlan, preview, consentimento e bloqueio fail-closed de ativos pagos/ambíguos

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`
- **Resultado:** `PASS`
