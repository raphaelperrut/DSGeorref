# EPIC-064 — fila de revisão explicável, filtros, priorização, impacto em descendentes e operações em lote permitidas

- **Domínio:** `WEB`
- **Bounded Context owner:** `BC-011 — Revisão e Correção`
- **Sprint planejada:** `SPRINT-009`
- **Papel responsável pela implementação:** `Frontend`
- **Issue principal:** `ISSUE-0064`
- **Dependências:** EPIC-030, EPIC-034, EPIC-053, EPIC-062
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-048

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-048`

## Resultado

Fila de revisão explicável, filtros, priorização, impacto em descendentes e operações em lote permitidas.

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

- Requisitos: REQ-REV-004
- Issue: `ISSUE-0064`
- Sprint: `SPRINT-009`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0398` / `ISSUE-0508` / `TASK-0398` — Definir jornada, estados e acessibilidade: fila de revisão explicável, filtros, priorização, impacto em descendentes e operações em lote permitidas
- `STORY-0399` / `ISSUE-0509` / `TASK-0399` — Integrar contratos e cliente tipado: fila de revisão explicável, filtros, priorização, impacto em descendentes e operações em lote permitidas
- `STORY-0400` / `ISSUE-0510` / `TASK-0400` — Implementar componentes e interação: fila de revisão explicável, filtros, priorização, impacto em descendentes e operações em lote permitidas
- `STORY-0401` / `ISSUE-0511` / `TASK-0401` — Integrar mapa, fluxo e estados de erro: fila de revisão explicável, filtros, priorização, impacto em descendentes e operações em lote permitidas
- `STORY-0402` / `ISSUE-0512` / `TASK-0402` — Executar testes de componente, acessibilidade e E2E: fila de revisão explicável, filtros, priorização, impacto em descendentes e operações em lote permitidas
- `STORY-0403` / `ISSUE-0513` / `TASK-0403` — Auditar UX, contrato e evidência final: fila de revisão explicável, filtros, priorização, impacto em descendentes e operações em lote permitidas

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-011` — Revisão e Correção.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-048`
- **Resultado:** `PASS`
