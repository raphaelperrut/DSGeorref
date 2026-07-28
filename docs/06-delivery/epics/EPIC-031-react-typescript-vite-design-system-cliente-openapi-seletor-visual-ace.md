# EPIC-031 — React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E

- **Domínio:** `WEB`
- **Bounded Context owner:** `BC-016 — Experiência e Orientação do Operador`
- **Sprint planejada:** `SPRINT-009`
- **Papel responsável pela implementação:** `Frontend`
- **Issue principal:** `ISSUE-0031`
- **Dependências:** EPIC-004, EPIC-011, EPIC-017
- **Release gate:** `G2/G7`
- **Referências arquiteturais:** ADR-002

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-017`, `ADR-023`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-055`

## Resultado

React/typescript/vite, design system, cliente openapi, seletor visual, acessibilidade e e2e.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G2/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-EPIC-031, REQ-FS-001, REQ-FS1-001, REQ-FS1-002, REQ-FS1-003, REQ-FS1-004, REQ-FS1-005, REQ-FS1-006, REQ-FS1-007, REQ-FS1-008, REQ-FS1-009, REQ-FS1-010, REQ-RUN-001, REQ-RUN-002, REQ-RUN-003, REQ-RUN-004, REQ-RUN-005, REQ-RUN-006, REQ-RUN-007, REQ-RUN-008, REQ-RUN-009, REQ-RUN-010, REQ-RUNTIME-008, REQ-TOOL-008, REQ-TOOL-009, REQ-UX-001
- Issue: `ISSUE-0031`
- Sprint: `SPRINT-009`

## Histórias implementáveis


Este épico possui **9** histórias filhas:

- `STORY-0185` / `ISSUE-0295` / `TASK-0185` — Definir jornada, estados e acessibilidade: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0186` / `ISSUE-0296` / `TASK-0186` — Consolidar slices e liberar integração: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0187` / `ISSUE-0297` / `TASK-0187` — Implementar componentes e interação: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0188` / `ISSUE-0298` / `TASK-0188` — Integrar mapa, fluxo e estados de erro: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0189` / `ISSUE-0299` / `TASK-0189` — Executar testes de componente, acessibilidade e E2E: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0190` / `ISSUE-0300` / `TASK-0190` — Auditar UX, contrato e evidência final: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0738` / `ISSUE-0848` / `TASK-0738` — Slice 1/3 — Integrar contratos e cliente tipado: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E [REQ-EPIC, REQ-FS1, REQ-RUN]
- `STORY-0739` / `ISSUE-0849` / `TASK-0739` — Slice 2/3 — Integrar contratos e cliente tipado: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E [REQ-RUN, REQ-RUNTIME]
- `STORY-0740` / `ISSUE-0850` / `TASK-0740` — Slice 3/3 — Integrar contratos e cliente tipado: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E [REQ-UX]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-017`, `ADR-023`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-055`
- **Resultado:** `PASS`
