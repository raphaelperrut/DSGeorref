# EPIC-019 — Resource Governor, admission control e orçamento adaptativo de RAM/CPU/GPU/disco

- **Domínio:** `JOB`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Sprint planejada:** `SPRINT-003`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0019`
- **Dependências:** EPIC-018
- **Release gate:** `G1/G7`
- **Referências arquiteturais:** ADR-039, ADR-044, ADR-049

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-044`, `ADR-046`, `ADR-047`, `ADR-053`

## Resultado

Resource governor, admission control e orçamento adaptativo de ram/cpu/gpu/disco.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-BEX-001, REQ-BEX-002, REQ-BEX-003, REQ-BEX-004, REQ-BEX-005, REQ-BEX-006, REQ-BEX-007, REQ-BEX-008, REQ-BEX-009, REQ-BEX-010, REQ-DIS-002, REQ-MAT-001, REQ-MOS-004, REQ-RES-001, REQ-SCH-001, REQ-SCL-001
- Issue: `ISSUE-0019`
- Sprint: `SPRINT-003`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0103` / `ISSUE-0213` / `TASK-0103` — Definir estados, envelopes e invariantes: Resource Governor, admission control e orçamento adaptativo de RAM/CPU/GPU/disco
- `STORY-0104` / `ISSUE-0214` / `TASK-0104` — Implementar modelo e application services: Resource Governor, admission control e orçamento adaptativo de RAM/CPU/GPU/disco
- `STORY-0105` / `ISSUE-0215` / `TASK-0105` — Implementar runner, worker ou scheduler: Resource Governor, admission control e orçamento adaptativo de RAM/CPU/GPU/disco
- `STORY-0106` / `ISSUE-0216` / `TASK-0106` — Expor comandos, progresso e reconciliação: Resource Governor, admission control e orçamento adaptativo de RAM/CPU/GPU/disco
- `STORY-0107` / `ISSUE-0217` / `TASK-0107` — Automatizar testes de resiliência, retry e recuperação: Resource Governor, admission control e orçamento adaptativo de RAM/CPU/GPU/disco
- `STORY-0108` / `ISSUE-0218` / `TASK-0108` — Executar integração real, carga e fault injection: Resource Governor, admission control e orçamento adaptativo de RAM/CPU/GPU/disco
- `STORY-0109` / `ISSUE-0219` / `TASK-0109` — Auditar evidência e integração final: Resource Governor, admission control e orçamento adaptativo de RAM/CPU/GPU/disco

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-044`, `ADR-046`, `ADR-047`, `ADR-053`
- **Resultado:** `PASS`
