# EPIC-041 — threat model validado, scanning e testes ofensivos

- **Domínio:** `SEC`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Sprint planejada:** `SPRINT-002`
- **Papel responsável pela implementação:** `Security`
- **Issue principal:** `ISSUE-0041`
- **Dependências:** EPIC-012
- **Release gate:** `G5`
- **Referências arquiteturais:** ADR-002, ADR-018, ADR-028, ADR-034, ADR-047

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-014`, `ADR-016`, `ADR-023`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-038`, `ADR-046`, `ADR-047`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`

## Resultado

Threat model validado, scanning e testes ofensivos.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G5` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AIE-001, REQ-AIE-002, REQ-AIE-003, REQ-AIE-004, REQ-AIE-005, REQ-AIE-006, REQ-AIE-007, REQ-AIE-008, REQ-AIE-009, REQ-AIE-010, REQ-ARTLAYOUT-010, REQ-AUTH-IMPL-001, REQ-AUTH-IMPL-002, REQ-AUTH-IMPL-003, REQ-AUTH-IMPL-004, REQ-AUTH-IMPL-005, REQ-AUTH-IMPL-006, REQ-AUTH-IMPL-007, REQ-AUTH-IMPL-008, REQ-AUTH-IMPL-009, REQ-AUTH-IMPL-010, REQ-EPIC-041, REQ-FS-001, REQ-NET-001, REQ-SRC-002, REQ-SRC-003
- Issue: `ISSUE-0041`
- Sprint: `SPRINT-002`

## Histórias implementáveis


Este épico possui **9** histórias filhas:

- `STORY-0244` / `ISSUE-0354` / `TASK-0244` — Modelar ameaças e requisitos de controle: threat model validado, scanning e testes ofensivos
- `STORY-0245` / `ISSUE-0355` / `TASK-0245` — Consolidar slices e liberar integração: threat model validado, scanning e testes ofensivos
- `STORY-0246` / `ISSUE-0356` / `TASK-0246` — Implementar controles e enforcement: threat model validado, scanning e testes ofensivos
- `STORY-0247` / `ISSUE-0357` / `TASK-0247` — Executar testes negativos e ofensivos: threat model validado, scanning e testes ofensivos
- `STORY-0248` / `ISSUE-0358` / `TASK-0248` — Instrumentar detecção, resposta e runbook: threat model validado, scanning e testes ofensivos
- `STORY-0249` / `ISSUE-0359` / `TASK-0249` — Auditar evidência de segurança final: threat model validado, scanning e testes ofensivos
- `STORY-0747` / `ISSUE-0857` / `TASK-0747` — Slice 1/3 — Definir políticas e contratos fail-closed: threat model validado, scanning e testes ofensivos [REQ-AIE]
- `STORY-0748` / `ISSUE-0858` / `TASK-0748` — Slice 2/3 — Definir políticas e contratos fail-closed: threat model validado, scanning e testes ofensivos [REQ-ARTLAYOUT, REQ-AUTH-IMPL]
- `STORY-0749` / `ISSUE-0859` / `TASK-0749` — Slice 3/3 — Definir políticas e contratos fail-closed: threat model validado, scanning e testes ofensivos [REQ-AUTH-IMPL, REQ-EPIC, REQ-FS, REQ-SRC]

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-014`, `ADR-016`, `ADR-023`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-038`, `ADR-046`, `ADR-047`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Resultado:** `PASS`
