# EPIC-090 — Issue Forms, templates e taxonomia de tipos com validação de campos obrigatórios

- **Domínio:** `FND`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Sprint planejada:** `SPRINT-001`
- **Papel responsável pela implementação:** `Tech Lead`
- **Issue principal:** `ISSUE-0090`
- **Dependências:** EPIC-002
- **Release gate:** `G0/G1`
- **Referências arquiteturais:** ADR-002, ADR-054

- ADRs: `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-033`, `ADR-034`

## Resultado

Issue forms, templates e taxonomia de tipos com validação de campos obrigatórios.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G0/G1` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-GOV-002
- Issue: `ISSUE-0090`
- Sprint: `SPRINT-001`

## Histórias implementáveis


Este épico possui **5** histórias filhas:

- `STORY-0555` / `ISSUE-0665` / `TASK-0555` — Definir escopo, contratos e invariantes: Issue Forms, templates e taxonomia de tipos com validação de campos obrigatórios
- `STORY-0556` / `ISSUE-0666` / `TASK-0556` — Materializar a fundação executável: Issue Forms, templates e taxonomia de tipos com validação de campos obrigatórios
- `STORY-0557` / `ISSUE-0667` / `TASK-0557` — Automatizar validações e controles: Issue Forms, templates e taxonomia de tipos com validação de campos obrigatórios
- `STORY-0558` / `ISSUE-0668` / `TASK-0558` — Integrar a capacidade ao fluxo do repositório: Issue Forms, templates e taxonomia de tipos com validação de campos obrigatórios
- `STORY-0559` / `ISSUE-0669` / `TASK-0559` — Validar evidência e realizar auditoria final: Issue Forms, templates e taxonomia de tipos com validação de campos obrigatórios

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-033`, `ADR-034`
- **Resultado:** `PASS`
