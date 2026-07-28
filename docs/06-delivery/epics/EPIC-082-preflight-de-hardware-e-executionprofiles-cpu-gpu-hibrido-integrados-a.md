# EPIC-082 — preflight de hardware e ExecutionProfiles CPU/GPU/híbrido integrados ao Resource Governor

- **Domínio:** `PLT`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Sprint planejada:** `SPRINT-002`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0082`
- **Dependências:** EPIC-010
- **Release gate:** `G1/G4/G7`
- **Referências arquiteturais:** ADR-051, ADR-039, ADR-053

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-037`, `ADR-053`

## Resultado

Preflight de hardware e executionprofiles cpu/gpu/híbrido integrados ao resource governor.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1/G4/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-HW-001, REQ-SCH-003, REQ-SDR-003
- Issue: `ISSUE-0082`
- Sprint: `SPRINT-002`

## Histórias implementáveis


Este épico possui **5** histórias filhas:

- `STORY-0511` / `ISSUE-0621` / `TASK-0511` — Definir política, estados e contratos: preflight de hardware e ExecutionProfiles CPU/GPU/híbrido integrados ao Resource Governor
- `STORY-0512` / `ISSUE-0622` / `TASK-0512` — Implementar domínio e persistência: preflight de hardware e ExecutionProfiles CPU/GPU/híbrido integrados ao Resource Governor
- `STORY-0513` / `ISSUE-0623` / `TASK-0513` — Expor administração e fluxos de uso: preflight de hardware e ExecutionProfiles CPU/GPU/híbrido integrados ao Resource Governor
- `STORY-0514` / `ISSUE-0624` / `TASK-0514` — Validar ameaças, autorização e falhas: preflight de hardware e ExecutionProfiles CPU/GPU/híbrido integrados ao Resource Governor
- `STORY-0515` / `ISSUE-0625` / `TASK-0515` — Executar QA e auditoria final: preflight de hardware e ExecutionProfiles CPU/GPU/híbrido integrados ao Resource Governor

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-037`, `ADR-053`
- **Resultado:** `PASS`
