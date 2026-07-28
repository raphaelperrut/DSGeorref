# EPIC-108 — Instalador, bootstrap, readiness e suporte diagnóstico

- **Domínio:** `REL`
- **Bounded Context owner:** `BC-015 — Release, Instalação e Supply Chain`
- **Sprint planejada:** `SPRINT-012`
- **Papel responsável pela implementação:** `DevOps`
- **Issue principal:** `ISSUE-0108`
- **Dependências:** Nenhuma
- **Release gate:** `G1/G7`
- **Referências arquiteturais:** ADR-034, ADR-054

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`

## Resultado

Instalador, bootstrap, readiness e suporte diagnóstico.

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

- Requisitos: REQ-INS-001, REQ-INS-002, REQ-INS-003, REQ-INS-004
- Issue: `ISSUE-0108`
- Sprint: `SPRINT-012`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0672` / `ISSUE-0782` / `TASK-0672` — Definir gate, versão e critérios de release: Instalador, bootstrap, readiness e suporte diagnóstico
- `STORY-0673` / `ISSUE-0783` / `TASK-0673` — Implementar pipeline e artifacts de release: Instalador, bootstrap, readiness e suporte diagnóstico
- `STORY-0674` / `ISSUE-0784` / `TASK-0674` — Implementar upgrade, rollback e compatibilidade: Instalador, bootstrap, readiness e suporte diagnóstico
- `STORY-0675` / `ISSUE-0785` / `TASK-0675` — Gerar evidências, SBOM e attestations: Instalador, bootstrap, readiness e suporte diagnóstico
- `STORY-0676` / `ISSUE-0786` / `TASK-0676` — Executar instalação limpa e rehearsal: Instalador, bootstrap, readiness e suporte diagnóstico
- `STORY-0677` / `ISSUE-0787` / `TASK-0677` — Auditar release candidata final: Instalador, bootstrap, readiness e suporte diagnóstico

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-015` — Release, Instalação e Supply Chain.
- **Classificação:** `Generic`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`
- **Resultado:** `PASS`
