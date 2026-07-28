# EPIC-066 — checkpoints canônicos, manifests de compatibilidade, retomada e lifecycle de intermediários

- **Domínio:** `JOB`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Sprint planejada:** `SPRINT-004`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0066`
- **Dependências:** EPIC-018
- **Release gate:** `G1/G3/G7`
- **Referências arquiteturais:** ADR-049

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-048`

## Resultado

Checkpoints canônicos, manifests de compatibilidade, retomada e lifecycle de intermediários.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G1/G3/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-ANC-008, REQ-BEX-001, REQ-BEX-002, REQ-BEX-003, REQ-BEX-004, REQ-BEX-005, REQ-BEX-006, REQ-BEX-007, REQ-BEX-008, REQ-BEX-009, REQ-BEX-010
- Issue: `ISSUE-0066`
- Sprint: `SPRINT-004`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0411` / `ISSUE-0521` / `TASK-0411` — Definir estados, envelopes e invariantes: checkpoints canônicos, manifests de compatibilidade, retomada e lifecycle de intermediários
- `STORY-0412` / `ISSUE-0522` / `TASK-0412` — Implementar modelo e application services: checkpoints canônicos, manifests de compatibilidade, retomada e lifecycle de intermediários
- `STORY-0413` / `ISSUE-0523` / `TASK-0413` — Implementar runner, worker ou scheduler: checkpoints canônicos, manifests de compatibilidade, retomada e lifecycle de intermediários
- `STORY-0414` / `ISSUE-0524` / `TASK-0414` — Expor comandos, progresso e reconciliação: checkpoints canônicos, manifests de compatibilidade, retomada e lifecycle de intermediários
- `STORY-0415` / `ISSUE-0525` / `TASK-0415` — Automatizar testes de resiliência, retry e recuperação: checkpoints canônicos, manifests de compatibilidade, retomada e lifecycle de intermediários
- `STORY-0416` / `ISSUE-0526` / `TASK-0416` — Executar integração real, carga e fault injection: checkpoints canônicos, manifests de compatibilidade, retomada e lifecycle de intermediários
- `STORY-0417` / `ISSUE-0527` / `TASK-0417` — Auditar evidência e integração final: checkpoints canônicos, manifests de compatibilidade, retomada e lifecycle de intermediários

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-048`
- **Resultado:** `PASS`
