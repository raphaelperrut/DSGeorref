# EPIC-001 — governança de decisões arquiteturais e manutenção da baseline normativa

- **Domínio:** `FND`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Sprint planejada:** `SPRINT-001`
- **Papel responsável pela implementação:** `Tech Lead`
- **Issue principal:** `ISSUE-0001`
- **Dependências:** Nenhuma
- **Release gate:** `G0`
- **Referências arquiteturais:** ADR-002, ADR-054, ADR-053, ADR-026

- ADRs: `ADR-001`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-040`, `ADR-057`

## Resultado

Governança de decisões arquiteturais e manutenção da baseline normativa.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G0` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-FRZ-001, REQ-FRZ-004, REQ-GOV-ADR-002, REQ-GOV-ADR-003, REQ-GOV-ADR-018, REQ-GOV-DEC-001, REQ-GOV-DEC-002, REQ-ISM-004, REQ-ISM-010, REQ-ISS-002, REQ-SPRINT-001-001, REQ-SPRINT-001-002, REQ-SPRINT-001-003, REQ-SPRINT-001-004, REQ-SPRINT-001-005, REQ-SPRINT-001-006, REQ-SPRINT-001-007, REQ-SPRINT-001-008, REQ-SPRINT-001-009, REQ-SPRINT-001-010, REQ-TOOL-001, REQ-TOOL-002, REQ-TOOL-010
- Issue: `ISSUE-0001`
- Sprint: `SPRINT-001`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0001` / `ISSUE-0111` / `TASK-0001` — Definir escopo, contratos e invariantes: governança de decisões arquiteturais e manutenção da baseline normativa
- `STORY-0002` / `ISSUE-0112` / `TASK-0002` — Consolidar slices e liberar integração: governança de decisões arquiteturais e manutenção da baseline normativa
- `STORY-0003` / `ISSUE-0113` / `TASK-0003` — Automatizar validações e controles: governança de decisões arquiteturais e manutenção da baseline normativa
- `STORY-0004` / `ISSUE-0114` / `TASK-0004` — Integrar a capacidade ao fluxo do repositório: governança de decisões arquiteturais e manutenção da baseline normativa
- `STORY-0005` / `ISSUE-0115` / `TASK-0005` — Validar evidência e realizar auditoria final: governança de decisões arquiteturais e manutenção da baseline normativa
- `STORY-0688` / `ISSUE-0798` / `TASK-0688` — Slice 1/2 — Materializar a fundação executável: governança de decisões arquiteturais e manutenção da baseline normativa [REQ-FRZ, REQ-GOV-ADR, REQ-GOV-DEC, REQ-ISM, REQ-SPRINT-001]
- `STORY-0689` / `ISSUE-0799` / `TASK-0689` — Slice 2/2 — Materializar a fundação executável: governança de decisões arquiteturais e manutenção da baseline normativa [REQ-SPRINT-001, REQ-TOOL]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-001`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-040`, `ADR-057`
- **Resultado:** `PASS`
