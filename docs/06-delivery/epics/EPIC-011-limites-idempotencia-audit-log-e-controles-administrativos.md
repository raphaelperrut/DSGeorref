# EPIC-011 — limites, idempotência, audit log e controles administrativos

- **Domínio:** `PLT`
- **Bounded Context owner:** `BC-002 — Identidade e Controle de Acesso`
- **Sprint planejada:** `SPRINT-002`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0011`
- **Dependências:** EPIC-010
- **Release gate:** `G2`
- **Referências arquiteturais:** ADR-002, ADR-028, ADR-054

- ADRs: `ADR-002`, `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-017`, `ADR-021`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-055`

## Resultado

Limites, idempotência, audit log e controles administrativos.

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

- Requisitos: REQ-AUD-001, REQ-AUTH-IMPL-001, REQ-AUTH-IMPL-002, REQ-AUTH-IMPL-003, REQ-AUTH-IMPL-004, REQ-AUTH-IMPL-005, REQ-AUTH-IMPL-006, REQ-AUTH-IMPL-007, REQ-AUTH-IMPL-008, REQ-AUTH-IMPL-009, REQ-AUTH-IMPL-010, REQ-RUNTIME-006, REQ-RUNTIME-007, REQ-RUNTIME-010
- Issue: `ISSUE-0011`
- Sprint: `SPRINT-002`

## Histórias implementáveis


Este épico possui **5** histórias filhas:

- `STORY-0051` / `ISSUE-0161` / `TASK-0051` — Definir política, estados e contratos: limites, idempotência, audit log e controles administrativos
- `STORY-0052` / `ISSUE-0162` / `TASK-0052` — Implementar domínio e persistência: limites, idempotência, audit log e controles administrativos
- `STORY-0053` / `ISSUE-0163` / `TASK-0053` — Expor administração e fluxos de uso: limites, idempotência, audit log e controles administrativos
- `STORY-0054` / `ISSUE-0164` / `TASK-0054` — Validar ameaças, autorização e falhas: limites, idempotência, audit log e controles administrativos
- `STORY-0055` / `ISSUE-0165` / `TASK-0055` — Executar QA e auditoria final: limites, idempotência, audit log e controles administrativos

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-017`, `ADR-021`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-055`
- **Resultado:** `PASS`
