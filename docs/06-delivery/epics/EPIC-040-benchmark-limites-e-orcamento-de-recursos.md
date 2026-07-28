# EPIC-040 — benchmark, limites e orçamento de recursos

- **Domínio:** `OPS`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0040`
- **Dependências:** EPIC-024, EPIC-039, EPIC-068, EPIC-069
- **Release gate:** `G7`
- **Referências arquiteturais:** ADR-039, ADR-041, ADR-050

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-036`, `ADR-039`, `ADR-040`, `ADR-042`, `ADR-053`

## Resultado

Benchmark, limites e orçamento de recursos.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-NFR-001, REQ-OUT-001, REQ-RES-001, REQ-RMQ-001, REQ-SCH-004, REQ-SCL-001, REQ-SMO-001, REQ-SMO-003, REQ-SRP-001
- Issue: `ISSUE-0040`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0238` / `ISSUE-0348` / `TASK-0238` — Definir SLO, runbook e controles operacionais: benchmark, limites e orçamento de recursos
- `STORY-0239` / `ISSUE-0349` / `TASK-0239` — Implementar automação operacional: benchmark, limites e orçamento de recursos
- `STORY-0240` / `ISSUE-0350` / `TASK-0240` — Instrumentar sinais, dashboards e alertas: benchmark, limites e orçamento de recursos
- `STORY-0241` / `ISSUE-0351` / `TASK-0241` — Executar drills, fault injection e recuperação: benchmark, limites e orçamento de recursos
- `STORY-0242` / `ISSUE-0352` / `TASK-0242` — Validar acesso, redaction e exposição: benchmark, limites e orçamento de recursos
- `STORY-0243` / `ISSUE-0353` / `TASK-0243` — Auditar evidência operacional final: benchmark, limites e orçamento de recursos

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-036`, `ADR-039`, `ADR-040`, `ADR-042`, `ADR-053`
- **Resultado:** `PASS`
