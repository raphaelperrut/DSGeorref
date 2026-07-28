# EPIC-077 — budgets de cardinalidade, sampling, retenção por sinal e dashboards de perda/overhead

- **Domínio:** `OPS`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0077`
- **Dependências:** EPIC-039, EPIC-073
- **Release gate:** `G7`
- **Referências arquiteturais:** ADR-054

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-054`

## Resultado

Budgets de cardinalidade, sampling, retenção por sinal e dashboards de perda/overhead.

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

- Requisitos: REQ-MET-001
- Issue: `ISSUE-0077`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0481` / `ISSUE-0591` / `TASK-0481` — Definir SLO, runbook e controles operacionais: budgets de cardinalidade, sampling, retenção por sinal e dashboards de perda/overhead
- `STORY-0482` / `ISSUE-0592` / `TASK-0482` — Implementar automação operacional: budgets de cardinalidade, sampling, retenção por sinal e dashboards de perda/overhead
- `STORY-0483` / `ISSUE-0593` / `TASK-0483` — Instrumentar sinais, dashboards e alertas: budgets de cardinalidade, sampling, retenção por sinal e dashboards de perda/overhead
- `STORY-0484` / `ISSUE-0594` / `TASK-0484` — Executar drills, fault injection e recuperação: budgets de cardinalidade, sampling, retenção por sinal e dashboards de perda/overhead
- `STORY-0485` / `ISSUE-0595` / `TASK-0485` — Validar acesso, redaction e exposição: budgets de cardinalidade, sampling, retenção por sinal e dashboards de perda/overhead
- `STORY-0486` / `ISSUE-0596` / `TASK-0486` — Auditar evidência operacional final: budgets de cardinalidade, sampling, retenção por sinal e dashboards de perda/overhead

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-054`
- **Resultado:** `PASS`
