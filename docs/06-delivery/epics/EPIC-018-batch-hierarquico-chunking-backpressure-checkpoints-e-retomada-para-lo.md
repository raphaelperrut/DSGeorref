# EPIC-018 — batch hierárquico, chunking, backpressure, checkpoints e retomada para lotes usuais de 40–300 imagens

- **Domínio:** `JOB`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Sprint planejada:** `SPRINT-003`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0018`
- **Dependências:** EPIC-012, EPIC-015, EPIC-016
- **Release gate:** `G1/G7`
- **Referências arquiteturais:** ADR-036, ADR-039, ADR-048, ADR-049

- ADRs: `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-049`, `ADR-053`

## Resultado

Batch hierárquico, chunking, backpressure, checkpoints e retomada para lotes usuais de 40–300 imagens.

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

- Requisitos: REQ-BEX-001, REQ-BEX-002, REQ-BEX-003, REQ-BEX-004, REQ-BEX-005, REQ-BEX-006, REQ-BEX-007, REQ-BEX-008, REQ-BEX-009, REQ-BEX-010, REQ-EPIC-017, REQ-EPIC-018, REQ-EPIC-062, REQ-MOS-001, REQ-SCH-002, REQ-SCL-001
- Issue: `ISSUE-0018`
- Sprint: `SPRINT-003`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0096` / `ISSUE-0206` / `TASK-0096` — Definir estados, envelopes e invariantes: batch hierárquico, chunking, backpressure, checkpoints e retomada para lotes usuais de 40–300 imagens
- `STORY-0097` / `ISSUE-0207` / `TASK-0097` — Implementar modelo e application services: batch hierárquico, chunking, backpressure, checkpoints e retomada para lotes usuais de 40–300 imagens
- `STORY-0098` / `ISSUE-0208` / `TASK-0098` — Implementar runner, worker ou scheduler: batch hierárquico, chunking, backpressure, checkpoints e retomada para lotes usuais de 40–300 imagens
- `STORY-0099` / `ISSUE-0209` / `TASK-0099` — Expor comandos, progresso e reconciliação: batch hierárquico, chunking, backpressure, checkpoints e retomada para lotes usuais de 40–300 imagens
- `STORY-0100` / `ISSUE-0210` / `TASK-0100` — Automatizar testes de resiliência, retry e recuperação: batch hierárquico, chunking, backpressure, checkpoints e retomada para lotes usuais de 40–300 imagens
- `STORY-0101` / `ISSUE-0211` / `TASK-0101` — Executar integração real, carga e fault injection: batch hierárquico, chunking, backpressure, checkpoints e retomada para lotes usuais de 40–300 imagens
- `STORY-0102` / `ISSUE-0212` / `TASK-0102` — Auditar evidência e integração final: batch hierárquico, chunking, backpressure, checkpoints e retomada para lotes usuais de 40–300 imagens

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-049`, `ADR-053`
- **Resultado:** `PASS`
