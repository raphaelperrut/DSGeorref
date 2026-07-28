# EPIC-009 — usuários e papéis da instância

- **Domínio:** `PLT`
- **Bounded Context owner:** `BC-002 — Identidade e Controle de Acesso`
- **Sprint planejada:** `SPRINT-002`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0009`
- **Dependências:** EPIC-005, EPIC-008
- **Release gate:** `G2`
- **Referências arquiteturais:** ADR-028

- ADRs: `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-043`, `ADR-055`

## Resultado

Usuários e papéis da instância.

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

- Requisitos: REQ-ACC-001, REQ-AUTH-IMPL-001, REQ-AUTH-IMPL-002, REQ-AUTH-IMPL-003, REQ-AUTH-IMPL-004, REQ-AUTH-IMPL-005, REQ-AUTH-IMPL-006, REQ-AUTH-IMPL-007, REQ-AUTH-IMPL-008, REQ-AUTH-IMPL-009, REQ-AUTH-IMPL-010, REQ-ID-002
- Issue: `ISSUE-0009`
- Sprint: `SPRINT-002`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0041` / `ISSUE-0151` / `TASK-0041` — Definir política, estados e contratos: usuários e papéis da instância
- `STORY-0042` / `ISSUE-0152` / `TASK-0042` — Consolidar slices e liberar integração: usuários e papéis da instância
- `STORY-0043` / `ISSUE-0153` / `TASK-0043` — Expor administração e fluxos de uso: usuários e papéis da instância
- `STORY-0044` / `ISSUE-0154` / `TASK-0044` — Validar ameaças, autorização e falhas: usuários e papéis da instância
- `STORY-0045` / `ISSUE-0155` / `TASK-0045` — Executar QA e auditoria final: usuários e papéis da instância
- `STORY-0714` / `ISSUE-0824` / `TASK-0714` — Slice 1/2 — Implementar domínio e persistência: usuários e papéis da instância [REQ-ACC, REQ-AUTH-IMPL]
- `STORY-0715` / `ISSUE-0825` / `TASK-0715` — Slice 2/2 — Implementar domínio e persistência: usuários e papéis da instância [REQ-ID]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-043`, `ADR-055`
- **Resultado:** `PASS`
