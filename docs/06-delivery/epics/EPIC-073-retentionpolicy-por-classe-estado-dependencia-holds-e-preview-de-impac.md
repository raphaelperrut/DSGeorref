# EPIC-073 — RetentionPolicy por classe/estado/dependência, holds e preview de impacto

- **Domínio:** `DAT`
- **Bounded Context owner:** `BC-013 — Artifacts, Proveniência e Lifecycle`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0073`
- **Dependências:** EPIC-049, EPIC-061
- **Release gate:** `G3/G5`
- **Referências arquiteturais:** ADR-039, ADR-027

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-053`

## Resultado

Retentionpolicy por classe/estado/dependência, holds e preview de impacto.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3/G5` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-GC-001, REQ-RET-001, REQ-SRP-004
- Issue: `ISSUE-0073`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0457` / `ISSUE-0567` / `TASK-0457` — Definir modelo, invariantes e contratos de dados: RetentionPolicy por classe/estado/dependência, holds e preview de impacto
- `STORY-0458` / `ISSUE-0568` / `TASK-0458` — Implementar persistência e migrations: RetentionPolicy por classe/estado/dependência, holds e preview de impacto
- `STORY-0459` / `ISSUE-0569` / `TASK-0459` — Implementar armazenamento e lifecycle: RetentionPolicy por classe/estado/dependência, holds e preview de impacto
- `STORY-0460` / `ISSUE-0570` / `TASK-0460` — Expor serviços e integrar consumers: RetentionPolicy por classe/estado/dependência, holds e preview de impacto
- `STORY-0461` / `ISSUE-0571` / `TASK-0461` — Validar segurança, recuperação e concorrência: RetentionPolicy por classe/estado/dependência, holds e preview de impacto
- `STORY-0462` / `ISSUE-0572` / `TASK-0462` — Executar QA e auditoria final: RetentionPolicy por classe/estado/dependência, holds e preview de impacto

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-053`
- **Resultado:** `PASS`
