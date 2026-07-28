# EPIC-091 — ruleset de main, checks únicos, CODEOWNERS, política de branches e prova de bypass auditado

- **Domínio:** `FND`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Sprint planejada:** `SPRINT-001`
- **Papel responsável pela implementação:** `Tech Lead`
- **Issue principal:** `ISSUE-0091`
- **Dependências:** EPIC-002, EPIC-005
- **Release gate:** `G0/G1/G5`
- **Referências arquiteturais:** ADR-002, ADR-034, ADR-054

- ADRs: `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-057`

## Resultado

Ruleset de main, checks únicos, codeowners, política de branches e prova de bypass auditado.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G0/G1/G5` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-FRZ-003, REQ-GOV-004, REQ-ISS-003, REQ-ISS-006, REQ-PUB-002
- Issue: `ISSUE-0091`
- Sprint: `SPRINT-001`

## Histórias implementáveis


Este épico possui **5** histórias filhas:

- `STORY-0560` / `ISSUE-0670` / `TASK-0560` — Definir escopo, contratos e invariantes: ruleset de main, checks únicos, CODEOWNERS, política de branches e prova de bypass auditado
- `STORY-0561` / `ISSUE-0671` / `TASK-0561` — Materializar a fundação executável: ruleset de main, checks únicos, CODEOWNERS, política de branches e prova de bypass auditado
- `STORY-0562` / `ISSUE-0672` / `TASK-0562` — Automatizar validações e controles: ruleset de main, checks únicos, CODEOWNERS, política de branches e prova de bypass auditado
- `STORY-0563` / `ISSUE-0673` / `TASK-0563` — Integrar a capacidade ao fluxo do repositório: ruleset de main, checks únicos, CODEOWNERS, política de branches e prova de bypass auditado
- `STORY-0564` / `ISSUE-0674` / `TASK-0564` — Validar evidência e realizar auditoria final: ruleset de main, checks únicos, CODEOWNERS, política de branches e prova de bypass auditado

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-057`
- **Resultado:** `PASS`
