# EPIC-083 — modos offline/restricted/connected, egress enforcement, mirrors e testes air-gapped

- **Domínio:** `OPS`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0083`
- **Dependências:** EPIC-058, EPIC-079, EPIC-080
- **Release gate:** `G5/G7`
- **Referências arquiteturais:** ADR-051

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-052`

## Resultado

Modos offline/restricted/connected, egress enforcement, mirrors e testes air-gapped.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G5/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-OFF-001
- Issue: `ISSUE-0083`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0516` / `ISSUE-0626` / `TASK-0516` — Definir SLO, runbook e controles operacionais: modos offline/restricted/connected, egress enforcement, mirrors e testes air-gapped
- `STORY-0517` / `ISSUE-0627` / `TASK-0517` — Implementar automação operacional: modos offline/restricted/connected, egress enforcement, mirrors e testes air-gapped
- `STORY-0518` / `ISSUE-0628` / `TASK-0518` — Instrumentar sinais, dashboards e alertas: modos offline/restricted/connected, egress enforcement, mirrors e testes air-gapped
- `STORY-0519` / `ISSUE-0629` / `TASK-0519` — Executar drills, fault injection e recuperação: modos offline/restricted/connected, egress enforcement, mirrors e testes air-gapped
- `STORY-0520` / `ISSUE-0630` / `TASK-0520` — Validar acesso, redaction e exposição: modos offline/restricted/connected, egress enforcement, mirrors e testes air-gapped
- `STORY-0521` / `ISSUE-0631` / `TASK-0521` — Auditar evidência operacional final: modos offline/restricted/connected, egress enforcement, mirrors e testes air-gapped

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-052`
- **Resultado:** `PASS`
