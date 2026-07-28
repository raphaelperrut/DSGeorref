# EPIC-006 — catálogo de conhecimento técnico e decomposição das capacidades de processamento

- **Domínio:** `FND`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Sprint planejada:** `SPRINT-001`
- **Papel responsável pela implementação:** `Tech Lead`
- **Issue principal:** `ISSUE-0006`
- **Dependências:** EPIC-001
- **Release gate:** `G0`
- **Referências arquiteturais:** ADR-051

- ADRs: `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-033`, `ADR-034`, `ADR-051`, `ADR-053`

## Resultado

Catálogo de conhecimento técnico e decomposição das capacidades de processamento.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G0` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-AI-007, REQ-TST-001
- Issue: `ISSUE-0006`
- Sprint: `SPRINT-001`

## Histórias implementáveis


Este épico possui **5** histórias filhas:

- `STORY-0026` / `ISSUE-0136` / `TASK-0026` — Definir escopo, contratos e invariantes: catálogo de conhecimento técnico e decomposição das capacidades de processamento
- `STORY-0027` / `ISSUE-0137` / `TASK-0027` — Materializar a fundação executável: catálogo de conhecimento técnico e decomposição das capacidades de processamento
- `STORY-0028` / `ISSUE-0138` / `TASK-0028` — Automatizar validações e controles: catálogo de conhecimento técnico e decomposição das capacidades de processamento
- `STORY-0029` / `ISSUE-0139` / `TASK-0029` — Integrar a capacidade ao fluxo do repositório: catálogo de conhecimento técnico e decomposição das capacidades de processamento
- `STORY-0030` / `ISSUE-0140` / `TASK-0030` — Validar evidência e realizar auditoria final: catálogo de conhecimento técnico e decomposição das capacidades de processamento

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-033`, `ADR-034`, `ADR-051`, `ADR-053`
- **Resultado:** `PASS`
