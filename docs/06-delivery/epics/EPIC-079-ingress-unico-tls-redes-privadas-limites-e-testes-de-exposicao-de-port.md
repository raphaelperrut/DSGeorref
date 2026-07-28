# EPIC-079 — ingress único, TLS, redes privadas, limites e testes de exposição de portas

- **Domínio:** `OPS`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0079`
- **Dependências:** EPIC-003, EPIC-008, EPIC-078
- **Release gate:** `G5/G7`
- **Referências arquiteturais:** ADR-034

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`

## Resultado

Ingress único, tls, redes privadas, limites e testes de exposição de portas.

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

- Requisitos: REQ-NET-001
- Issue: `ISSUE-0079`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0493` / `ISSUE-0603` / `TASK-0493` — Definir SLO, runbook e controles operacionais: ingress único, TLS, redes privadas, limites e testes de exposição de portas
- `STORY-0494` / `ISSUE-0604` / `TASK-0494` — Implementar automação operacional: ingress único, TLS, redes privadas, limites e testes de exposição de portas
- `STORY-0495` / `ISSUE-0605` / `TASK-0495` — Instrumentar sinais, dashboards e alertas: ingress único, TLS, redes privadas, limites e testes de exposição de portas
- `STORY-0496` / `ISSUE-0606` / `TASK-0496` — Executar drills, fault injection e recuperação: ingress único, TLS, redes privadas, limites e testes de exposição de portas
- `STORY-0497` / `ISSUE-0607` / `TASK-0497` — Validar acesso, redaction e exposição: ingress único, TLS, redes privadas, limites e testes de exposição de portas
- `STORY-0498` / `ISSUE-0608` / `TASK-0498` — Auditar evidência operacional final: ingress único, TLS, redes privadas, limites e testes de exposição de portas

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`
- **Resultado:** `PASS`
