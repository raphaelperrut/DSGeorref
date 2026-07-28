# EPIC-008 — contas locais, bootstrap único, sessões, tokens e adapter OIDC

- **Domínio:** `PLT`
- **Bounded Context owner:** `BC-002 — Identidade e Controle de Acesso`
- **Sprint planejada:** `SPRINT-002`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0008`
- **Dependências:** EPIC-004
- **Release gate:** `G2`
- **Referências arquiteturais:** ADR-018, ADR-028, ADR-034

- ADRs: `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-034`, `ADR-043`, `ADR-055`

## Resultado

Contas locais, bootstrap único, sessões, tokens e adapter oidc.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G2` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AUTH-IMPL-001, REQ-AUTH-IMPL-002, REQ-AUTH-IMPL-003, REQ-AUTH-IMPL-004, REQ-AUTH-IMPL-005, REQ-AUTH-IMPL-006, REQ-AUTH-IMPL-007, REQ-AUTH-IMPL-008, REQ-AUTH-IMPL-009, REQ-AUTH-IMPL-010, REQ-DBSCHEMA-003, REQ-EPIC-076, REQ-ID-001, REQ-ID-002, REQ-INS-002
- Issue: `ISSUE-0008`
- Sprint: `SPRINT-002`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0036` / `ISSUE-0146` / `TASK-0036` — Definir política, estados e contratos: contas locais, bootstrap único, sessões, tokens e adapter OIDC
- `STORY-0037` / `ISSUE-0147` / `TASK-0037` — Consolidar slices e liberar integração: contas locais, bootstrap único, sessões, tokens e adapter OIDC
- `STORY-0038` / `ISSUE-0148` / `TASK-0038` — Expor administração e fluxos de uso: contas locais, bootstrap único, sessões, tokens e adapter OIDC
- `STORY-0039` / `ISSUE-0149` / `TASK-0039` — Validar ameaças, autorização e falhas: contas locais, bootstrap único, sessões, tokens e adapter OIDC
- `STORY-0040` / `ISSUE-0150` / `TASK-0040` — Executar QA e auditoria final: contas locais, bootstrap único, sessões, tokens e adapter OIDC
- `STORY-0712` / `ISSUE-0822` / `TASK-0712` — Slice 1/2 — Implementar domínio e persistência: contas locais, bootstrap único, sessões, tokens e adapter OIDC [REQ-AUTH-IMPL, REQ-DBSCHEMA]
- `STORY-0713` / `ISSUE-0823` / `TASK-0713` — Slice 2/2 — Implementar domínio e persistência: contas locais, bootstrap único, sessões, tokens e adapter OIDC [REQ-ID]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-034`, `ADR-043`, `ADR-055`
- **Resultado:** `PASS`
