# EPIC-007 — LICENSE, CITATION.cff, contribuição, DCO/CLA e gate de publicação definidos

- **Domínio:** `FND`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Sprint planejada:** `SPRINT-001`
- **Papel responsável pela implementação:** `Tech Lead`
- **Issue principal:** `ISSUE-0007`
- **Dependências:** EPIC-001
- **Release gate:** `G0/G6`
- **Referências arquiteturais:** ADR-034, ADR-047, ADR-054

- ADRs: `ADR-002`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-056`, `ADR-057`

## Resultado

License, citation.cff, contribuição, dco/cla e gate de publicação definidos.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G0/G6` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-CIT-001, REQ-EPIC-042, REQ-OSS-001, REQ-PUB-002
- Issue: `ISSUE-0007`
- Sprint: `SPRINT-001`

## Histórias implementáveis


Este épico possui **5** histórias filhas:

- `STORY-0031` / `ISSUE-0141` / `TASK-0031` — Definir escopo, contratos e invariantes: LICENSE, CITATION.cff, contribuição, DCO/CLA e gate de publicação definidos
- `STORY-0032` / `ISSUE-0142` / `TASK-0032` — Materializar a fundação executável: LICENSE, CITATION.cff, contribuição, DCO/CLA e gate de publicação definidos
- `STORY-0033` / `ISSUE-0143` / `TASK-0033` — Automatizar validações e controles: LICENSE, CITATION.cff, contribuição, DCO/CLA e gate de publicação definidos
- `STORY-0034` / `ISSUE-0144` / `TASK-0034` — Integrar a capacidade ao fluxo do repositório: LICENSE, CITATION.cff, contribuição, DCO/CLA e gate de publicação definidos
- `STORY-0035` / `ISSUE-0145` / `TASK-0035` — Validar evidência e realizar auditoria final: LICENSE, CITATION.cff, contribuição, DCO/CLA e gate de publicação definidos

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-056`, `ADR-057`
- **Resultado:** `PASS`
