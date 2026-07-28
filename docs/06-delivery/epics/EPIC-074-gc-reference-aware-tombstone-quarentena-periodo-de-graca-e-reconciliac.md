# EPIC-074 — GC reference-aware, tombstone, quarentena, período de graça e reconciliação

- **Domínio:** `DAT`
- **Bounded Context owner:** `BC-013 — Artifacts, Proveniência e Lifecycle`
- **Sprint planejada:** `SPRINT-011`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0074`
- **Dependências:** EPIC-049, EPIC-073
- **Release gate:** `G3/G5/G7`
- **Referências arquiteturais:** ADR-027

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`

## Resultado

Gc reference-aware, tombstone, quarentena, período de graça e reconciliação.

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

- Requisitos: REQ-GC-001
- Issue: `ISSUE-0074`
- Sprint: `SPRINT-011`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0463` / `ISSUE-0573` / `TASK-0463` — Definir modelo, invariantes e contratos de dados: GC reference-aware, tombstone, quarentena, período de graça e reconciliação
- `STORY-0464` / `ISSUE-0574` / `TASK-0464` — Implementar persistência e migrations: GC reference-aware, tombstone, quarentena, período de graça e reconciliação
- `STORY-0465` / `ISSUE-0575` / `TASK-0465` — Implementar armazenamento e lifecycle: GC reference-aware, tombstone, quarentena, período de graça e reconciliação
- `STORY-0466` / `ISSUE-0576` / `TASK-0466` — Expor serviços e integrar consumers: GC reference-aware, tombstone, quarentena, período de graça e reconciliação
- `STORY-0467` / `ISSUE-0577` / `TASK-0467` — Validar segurança, recuperação e concorrência: GC reference-aware, tombstone, quarentena, período de graça e reconciliação
- `STORY-0468` / `ISSUE-0578` / `TASK-0468` — Executar QA e auditoria final: GC reference-aware, tombstone, quarentena, período de graça e reconciliação

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-030`, `ADR-031`, `ADR-032`
- **Resultado:** `PASS`
