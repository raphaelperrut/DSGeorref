# EPIC-084 — UX guiada de IA, explicação do plano, capacidades instaladas/bloqueadas e laboratório separado

- **Domínio:** `WEB`
- **Bounded Context owner:** `BC-016 — Experiência e Orientação do Operador`
- **Sprint planejada:** `SPRINT-009`
- **Papel responsável pela implementação:** `Frontend`
- **Issue principal:** `ISSUE-0084`
- **Dependências:** EPIC-029, EPIC-033, EPIC-050
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-051

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-014`

## Resultado

Ux guiada de ia, explicação do plano, capacidades instaladas/bloqueadas e laboratório separado.

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

- Requisitos: REQ-AI-016
- Issue: `ISSUE-0084`
- Sprint: `SPRINT-009`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0522` / `ISSUE-0632` / `TASK-0522` — Definir jornada, estados e acessibilidade: UX guiada de IA, explicação do plano, capacidades instaladas/bloqueadas e laboratório separado
- `STORY-0523` / `ISSUE-0633` / `TASK-0523` — Integrar contratos e cliente tipado: UX guiada de IA, explicação do plano, capacidades instaladas/bloqueadas e laboratório separado
- `STORY-0524` / `ISSUE-0634` / `TASK-0524` — Implementar componentes e interação: UX guiada de IA, explicação do plano, capacidades instaladas/bloqueadas e laboratório separado
- `STORY-0525` / `ISSUE-0635` / `TASK-0525` — Integrar mapa, fluxo e estados de erro: UX guiada de IA, explicação do plano, capacidades instaladas/bloqueadas e laboratório separado
- `STORY-0526` / `ISSUE-0636` / `TASK-0526` — Executar testes de componente, acessibilidade e E2E: UX guiada de IA, explicação do plano, capacidades instaladas/bloqueadas e laboratório separado
- `STORY-0527` / `ISSUE-0637` / `TASK-0527` — Auditar UX, contrato e evidência final: UX guiada de IA, explicação do plano, capacidades instaladas/bloqueadas e laboratório separado

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-014`
- **Resultado:** `PASS`
