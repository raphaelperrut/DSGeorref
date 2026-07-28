# EPIC-061 — cache endereçado por conteúdo, deduplicação, quotas, retention, licença, GC e proteção de lineage

- **Domínio:** `DAT`
- **Bounded Context owner:** `BC-013 — Artifacts, Proveniência e Lifecycle`
- **Sprint planejada:** `SPRINT-010`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0061`
- **Dependências:** EPIC-012, EPIC-049, EPIC-058
- **Release gate:** `G3/G5/G7`
- **Referências arquiteturais:** ADR-047

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-047`

## Resultado

Cache endereçado por conteúdo, deduplicação, quotas, retention, licença, gc e proteção de lineage.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3/G5/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-CAC-001, REQ-PUB-003
- Issue: `ISSUE-0061`
- Sprint: `SPRINT-010`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0379` / `ISSUE-0489` / `TASK-0379` — Definir modelo, invariantes e contratos de dados: cache endereçado por conteúdo, deduplicação, quotas, retention, licença, GC e proteção de lineage
- `STORY-0380` / `ISSUE-0490` / `TASK-0380` — Implementar persistência e migrations: cache endereçado por conteúdo, deduplicação, quotas, retention, licença, GC e proteção de lineage
- `STORY-0381` / `ISSUE-0491` / `TASK-0381` — Implementar armazenamento e lifecycle: cache endereçado por conteúdo, deduplicação, quotas, retention, licença, GC e proteção de lineage
- `STORY-0382` / `ISSUE-0492` / `TASK-0382` — Expor serviços e integrar consumers: cache endereçado por conteúdo, deduplicação, quotas, retention, licença, GC e proteção de lineage
- `STORY-0383` / `ISSUE-0493` / `TASK-0383` — Validar segurança, recuperação e concorrência: cache endereçado por conteúdo, deduplicação, quotas, retention, licença, GC e proteção de lineage
- `STORY-0384` / `ISSUE-0494` / `TASK-0384` — Executar QA e auditoria final: cache endereçado por conteúdo, deduplicação, quotas, retention, licença, GC e proteção de lineage

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-047`
- **Resultado:** `PASS`
