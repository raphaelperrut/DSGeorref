# EPIC-010 — autorização por projeto, operação, artefato e caminho

- **Domínio:** `PLT`
- **Bounded Context owner:** `BC-002 — Identidade e Controle de Acesso`
- **Sprint planejada:** `SPRINT-002`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0010`
- **Dependências:** EPIC-009
- **Release gate:** `G2`
- **Referências arquiteturais:** ADR-051, ADR-028

- ADRs: `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-037`, `ADR-043`, `ADR-055`

## Resultado

Autorização por projeto, operação, artefato e caminho.

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

- Requisitos: REQ-ACC-001, REQ-AUTH-IMPL-001, REQ-AUTH-IMPL-002, REQ-AUTH-IMPL-003, REQ-AUTH-IMPL-004, REQ-AUTH-IMPL-005, REQ-AUTH-IMPL-006, REQ-AUTH-IMPL-007, REQ-AUTH-IMPL-008, REQ-AUTH-IMPL-009, REQ-AUTH-IMPL-010, REQ-HW-001
- Issue: `ISSUE-0010`
- Sprint: `SPRINT-002`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0046` / `ISSUE-0156` / `TASK-0046` — Definir política, estados e contratos: autorização por projeto, operação, artefato e caminho
- `STORY-0047` / `ISSUE-0157` / `TASK-0047` — Consolidar slices e liberar integração: autorização por projeto, operação, artefato e caminho
- `STORY-0048` / `ISSUE-0158` / `TASK-0048` — Expor administração e fluxos de uso: autorização por projeto, operação, artefato e caminho
- `STORY-0049` / `ISSUE-0159` / `TASK-0049` — Validar ameaças, autorização e falhas: autorização por projeto, operação, artefato e caminho
- `STORY-0050` / `ISSUE-0160` / `TASK-0050` — Executar QA e auditoria final: autorização por projeto, operação, artefato e caminho
- `STORY-0716` / `ISSUE-0826` / `TASK-0716` — Slice 1/2 — Implementar domínio e persistência: autorização por projeto, operação, artefato e caminho [REQ-ACC, REQ-AUTH-IMPL]
- `STORY-0717` / `ISSUE-0827` / `TASK-0717` — Slice 2/2 — Implementar domínio e persistência: autorização por projeto, operação, artefato e caminho [REQ-HW]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-037`, `ADR-043`, `ADR-055`
- **Resultado:** `PASS`
