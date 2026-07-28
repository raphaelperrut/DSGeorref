# EPIC-033 — assistente guiado, recomendação explicável, consentimentos e modo avançado

- **Domínio:** `WEB`
- **Bounded Context owner:** `BC-016 — Experiência e Orientação do Operador`
- **Sprint planejada:** `SPRINT-009`
- **Papel responsável pela implementação:** `Frontend`
- **Issue principal:** `ISSUE-0033`
- **Dependências:** EPIC-029, EPIC-031, EPIC-059
- **Release gate:** `G4/G7`
- **Referências arquiteturais:** ADR-051, ADR-044, ADR-047

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-047`, `ADR-051`

## Resultado

Assistente guiado, recomendação explicável, consentimentos e modo avançado.

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

- Requisitos: REQ-AI-011, REQ-SRC-004, REQ-UX-002
- Issue: `ISSUE-0033`
- Sprint: `SPRINT-009`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0197` / `ISSUE-0307` / `TASK-0197` — Definir jornada, estados e acessibilidade: assistente guiado, recomendação explicável, consentimentos e modo avançado
- `STORY-0198` / `ISSUE-0308` / `TASK-0198` — Integrar contratos e cliente tipado: assistente guiado, recomendação explicável, consentimentos e modo avançado
- `STORY-0199` / `ISSUE-0309` / `TASK-0199` — Implementar componentes e interação: assistente guiado, recomendação explicável, consentimentos e modo avançado
- `STORY-0200` / `ISSUE-0310` / `TASK-0200` — Integrar mapa, fluxo e estados de erro: assistente guiado, recomendação explicável, consentimentos e modo avançado
- `STORY-0201` / `ISSUE-0311` / `TASK-0201` — Executar testes de componente, acessibilidade e E2E: assistente guiado, recomendação explicável, consentimentos e modo avançado
- `STORY-0202` / `ISSUE-0312` / `TASK-0202` — Auditar UX, contrato e evidência final: assistente guiado, recomendação explicável, consentimentos e modo avançado

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-047`, `ADR-051`
- **Resultado:** `PASS`
