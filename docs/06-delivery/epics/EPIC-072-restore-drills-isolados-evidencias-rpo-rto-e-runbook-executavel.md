# EPIC-072 — restore drills isolados, evidências, RPO/RTO e runbook executável

- **Domínio:** `OPS`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0072`
- **Dependências:** EPIC-039, EPIC-071
- **Release gate:** `G7`
- **Referências arquiteturais:** ADR-027, ADR-026

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-025`, `ADR-027`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-035`

## Resultado

Restore drills isolados, evidências, rpo/rto e runbook executável.

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

- Requisitos: REQ-BKP-002, REQ-EPIC-039, REQ-SCM-004, REQ-UPG-001, REQ-UPG-004
- Issue: `ISSUE-0072`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0451` / `ISSUE-0561` / `TASK-0451` — Definir SLO, runbook e controles operacionais: restore drills isolados, evidências, RPO/RTO e runbook executável
- `STORY-0452` / `ISSUE-0562` / `TASK-0452` — Implementar automação operacional: restore drills isolados, evidências, RPO/RTO e runbook executável
- `STORY-0453` / `ISSUE-0563` / `TASK-0453` — Instrumentar sinais, dashboards e alertas: restore drills isolados, evidências, RPO/RTO e runbook executável
- `STORY-0454` / `ISSUE-0564` / `TASK-0454` — Executar drills, fault injection e recuperação: restore drills isolados, evidências, RPO/RTO e runbook executável
- `STORY-0455` / `ISSUE-0565` / `TASK-0455` — Validar acesso, redaction e exposição: restore drills isolados, evidências, RPO/RTO e runbook executável
- `STORY-0456` / `ISSUE-0566` / `TASK-0456` — Auditar evidência operacional final: restore drills isolados, evidências, RPO/RTO e runbook executável

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-025`, `ADR-027`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-035`
- **Resultado:** `PASS`
