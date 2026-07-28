# EPIC-032 — workspace OpenLayers, configuração, acompanhamento e revisão

- **Domínio:** `WEB`
- **Bounded Context owner:** `BC-016 — Experiência e Orientação do Operador`
- **Sprint planejada:** `SPRINT-009`
- **Papel responsável pela implementação:** `Frontend`
- **Issue principal:** `ISSUE-0032`
- **Dependências:** EPIC-024, EPIC-031
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-002, ADR-044, ADR-049, ADR-050

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-040`, `ADR-042`, `ADR-049`, `ADR-055`

## Resultado

Workspace openlayers, configuração, acompanhamento e revisão.

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

- Requisitos: REQ-ANC-005, REQ-MSK-003, REQ-MTD-001, REQ-RMR-002, REQ-UX-001
- Issue: `ISSUE-0032`
- Sprint: `SPRINT-009`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0191` / `ISSUE-0301` / `TASK-0191` — Definir jornada, estados e acessibilidade: workspace OpenLayers, configuração, acompanhamento e revisão
- `STORY-0192` / `ISSUE-0302` / `TASK-0192` — Integrar contratos e cliente tipado: workspace OpenLayers, configuração, acompanhamento e revisão
- `STORY-0193` / `ISSUE-0303` / `TASK-0193` — Implementar componentes e interação: workspace OpenLayers, configuração, acompanhamento e revisão
- `STORY-0194` / `ISSUE-0304` / `TASK-0194` — Integrar mapa, fluxo e estados de erro: workspace OpenLayers, configuração, acompanhamento e revisão
- `STORY-0195` / `ISSUE-0305` / `TASK-0195` — Executar testes de componente, acessibilidade e E2E: workspace OpenLayers, configuração, acompanhamento e revisão
- `STORY-0196` / `ISSUE-0306` / `TASK-0196` — Auditar UX, contrato e evidência final: workspace OpenLayers, configuração, acompanhamento e revisão

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-040`, `ADR-042`, `ADR-049`, `ADR-055`
- **Resultado:** `PASS`
