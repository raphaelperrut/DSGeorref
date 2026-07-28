# EPIC-002 — repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível

- **Domínio:** `FND`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Sprint planejada:** `SPRINT-001`
- **Papel responsável pela implementação:** `Tech Lead`
- **Issue principal:** `ISSUE-0002`
- **Dependências:** EPIC-001
- **Release gate:** `G0/G1`
- **Referências arquiteturais:** ADR-002, ADR-044, ADR-041

- ADRs: `ADR-001`, `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-012`, `ADR-013`, `ADR-015`, `ADR-016`, `ADR-017`, `ADR-018`, `ADR-020`, `ADR-022`, `ADR-025`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-050`, `ADR-053`, `ADR-055`

## Resultado

Repositório privado, project central/views/campos, labels, issue forms, templates, ruleset, checks e configuração reproduzível.

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

- Requisitos: REQ-CLASSICPROFILE-001, REQ-CLASSICPROFILE-002, REQ-CLASSICPROFILE-003, REQ-CLASSICPROFILE-004, REQ-CLASSICPROFILE-005, REQ-CLASSICPROFILE-006, REQ-CLASSICPROFILE-007, REQ-CLASSICPROFILE-008, REQ-CLASSICPROFILE-009, REQ-CLASSICPROFILE-010, REQ-GOV-001, REQ-GOV-002, REQ-GOV-003, REQ-GOV-ADR-002, REQ-GOV-ADR-003, REQ-GOV-ADR-018, REQ-ISM-001, REQ-ISM-006, REQ-ISM-008, REQ-ISS-001, REQ-ISS-004, REQ-ISS-006, REQ-ISS-007, REQ-ISS-009, REQ-NATIVE-001, REQ-NATIVE-002, REQ-NATIVE-003, REQ-NATIVE-004, REQ-NATIVE-005, REQ-NATIVE-006, REQ-NATIVE-007, REQ-NATIVE-008, REQ-NATIVE-009, REQ-NATIVE-010, REQ-PLN-001, REQ-PLN-002, REQ-PLN-003, REQ-PLN-004, REQ-PLN-005, REQ-PLN-006, REQ-PLN-007, REQ-PLN-008, REQ-PLN-009, REQ-PLN-010, REQ-PRJ-001, REQ-PRJ-002, REQ-PRJ-003, REQ-PRJ-004, REQ-PRJ-005, REQ-PRJ-006, REQ-PRJ-007, REQ-PRJ-008, REQ-PRJ-009, REQ-PRJ-010, REQ-PRM-001, REQ-PRM-002, REQ-PRM-003, REQ-PRM-004, REQ-PRM-005, REQ-PRM-006, REQ-PRM-007, REQ-PRM-008, REQ-PRM-009, REQ-PRM-010, REQ-RUN-001, REQ-RUN-002, REQ-RUN-003, REQ-RUN-004, REQ-RUN-005, REQ-RUN-006, REQ-RUN-007, REQ-RUN-008, REQ-RUN-009, REQ-RUN-010, REQ-RUNTIME-001, REQ-RUNTIME-002, REQ-SPRINT-001-001, REQ-SPRINT-001-002, REQ-SPRINT-001-003, REQ-SPRINT-001-004, REQ-SPRINT-001-005, REQ-SPRINT-001-006, REQ-SPRINT-001-007, REQ-SPRINT-001-008, REQ-SPRINT-001-009, REQ-SPRINT-001-010, REQ-TOOL-001, REQ-TOOL-002, REQ-TOOL-005, REQ-WORKER-001, REQ-WORKER-002, REQ-WORKER-003, REQ-WORKER-004, REQ-WORKER-005, REQ-WORKER-006, REQ-WORKER-007, REQ-WORKER-008, REQ-WORKER-009, REQ-WORKER-010
- Issue: `ISSUE-0002`
- Sprint: `SPRINT-001`

## Histórias implementáveis


Este épico possui **16** histórias filhas:

- `STORY-0006` / `ISSUE-0116` / `TASK-0006` — Consolidar slices e liberar integração: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível
- `STORY-0007` / `ISSUE-0117` / `TASK-0007` — Consolidar slices e liberar integração: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível
- `STORY-0008` / `ISSUE-0118` / `TASK-0008` — Automatizar validações e controles: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível
- `STORY-0009` / `ISSUE-0119` / `TASK-0009` — Integrar a capacidade ao fluxo do repositório: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível
- `STORY-0010` / `ISSUE-0120` / `TASK-0010` — Validar evidência e realizar auditoria final: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível
- `STORY-0690` / `ISSUE-0800` / `TASK-0690` — Slice 1/2 — Definir escopo, contratos e invariantes: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-CLASSICPROFILE, REQ-ISS, REQ-NATIVE, REQ-PLN, REQ-PRJ, REQ-RUN, REQ-SPRINT-001]
- `STORY-0691` / `ISSUE-0801` / `TASK-0691` — Slice 2/2 — Definir escopo, contratos e invariantes: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-WORKER]
- `STORY-0692` / `ISSUE-0802` / `TASK-0692` — Slice 1/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-CLASSICPROFILE, REQ-GOV, REQ-GOV-ADR]
- `STORY-0693` / `ISSUE-0803` / `TASK-0693` — Slice 2/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-GOV-ADR, REQ-ISM, REQ-ISS, REQ-NATIVE]
- `STORY-0694` / `ISSUE-0804` / `TASK-0694` — Slice 3/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-NATIVE, REQ-PLN]
- `STORY-0695` / `ISSUE-0805` / `TASK-0695` — Slice 4/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-PLN, REQ-PRJ]
- `STORY-0696` / `ISSUE-0806` / `TASK-0696` — Slice 5/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-PRJ, REQ-PRM]
- `STORY-0697` / `ISSUE-0807` / `TASK-0697` — Slice 6/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-PRM, REQ-RUN]
- `STORY-0698` / `ISSUE-0808` / `TASK-0698` — Slice 7/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-RUNTIME, REQ-SPRINT-001]
- `STORY-0699` / `ISSUE-0809` / `TASK-0699` — Slice 8/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-SPRINT-001, REQ-TOOL, REQ-WORKER]
- `STORY-0700` / `ISSUE-0810` / `TASK-0700` — Slice 9/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-WORKER]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-001`, `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-012`, `ADR-013`, `ADR-015`, `ADR-016`, `ADR-017`, `ADR-018`, `ADR-020`, `ADR-022`, `ADR-025`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-050`, `ADR-053`, `ADR-055`
- **Resultado:** `PASS`
