# EPIC-070 — snapshots imutáveis, regra de resultado vigente e comparação entre ciclos

- **Domínio:** `REP`
- **Bounded Context owner:** `BC-012 — Resultados, Diagnósticos e Exportação`
- **Sprint planejada:** `SPRINT-010`
- **Papel responsável pela implementação:** `Backend`
- **Issue principal:** `ISSUE-0070`
- **Dependências:** EPIC-037, EPIC-049, EPIC-062
- **Release gate:** `G3/G4/G7`
- **Referências arquiteturais:** ADR-018, ADR-048, ADR-050

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`

## Resultado

Snapshots imutáveis, regra de resultado vigente e comparação entre ciclos.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G3/G4/G7` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-EPIC-037, REQ-EPIC-070, REQ-PROV-001, REQ-RMR-001
- Issue: `ISSUE-0070`
- Sprint: `SPRINT-010`

## Histórias implementáveis


Este épico possui **6** histórias filhas:

- `STORY-0439` / `ISSUE-0549` / `TASK-0439` — Definir schemas, formatos e invariantes de resultado: snapshots imutáveis, regra de resultado vigente e comparação entre ciclos
- `STORY-0440` / `ISSUE-0550` / `TASK-0440` — Implementar persistência e snapshots: snapshots imutáveis, regra de resultado vigente e comparação entre ciclos
- `STORY-0441` / `ISSUE-0551` / `TASK-0441` — Implementar geração e exportação: snapshots imutáveis, regra de resultado vigente e comparação entre ciclos
- `STORY-0442` / `ISSUE-0552` / `TASK-0442` — Expor consulta, download e visualização: snapshots imutáveis, regra de resultado vigente e comparação entre ciclos
- `STORY-0443` / `ISSUE-0553` / `TASK-0443` — Validar escala, reprodutibilidade e integridade: snapshots imutáveis, regra de resultado vigente e comparação entre ciclos
- `STORY-0444` / `ISSUE-0554` / `TASK-0444` — Auditar lineage e evidência final: snapshots imutáveis, regra de resultado vigente e comparação entre ciclos

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`
- **Resultado:** `PASS`
