# EPIC-027 — gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-005 — Descoberta e Aquisição de Referências`
- **Sprint planejada:** `SPRINT-005`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0027`
- **Dependências:** EPIC-005, EPIC-041
- **Release gate:** `G5/G4`
- **Referências arquiteturais:** ADR-047

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`

## Resultado

Gateway de fontes, proteção ssrf, estados de disponibilidade e bloqueio de compra.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G5/G4` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-SRC-001, REQ-SRC-002
- Issue: `ISSUE-0027`
- Sprint: `SPRINT-005`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0157` / `ISSUE-0267` / `TASK-0157` — Definir contrato científico e invariantes: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0158` / `ISSUE-0268` / `TASK-0158` — Preparar corpus, fixtures e representação tipada: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0159` / `ISSUE-0269` / `TASK-0159` — Implementar o núcleo algorítmico: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0160` / `ISSUE-0270` / `TASK-0160` — Integrar ao ProcessingPlan e pipeline: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0161` / `ISSUE-0271` / `TASK-0161` — Produzir métricas, diagnóstico e lineage: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0162` / `ISSUE-0272` / `TASK-0162` — Executar benchmark, negativos e regressão científica: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0163` / `ISSUE-0273` / `TASK-0163` — Auditar evidência científica e final: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`
- **Resultado:** `PASS`
