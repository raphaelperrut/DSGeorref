# EPIC-058 — gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-005 — Descoberta e Aquisição de Referências`
- **Sprint planejada:** `SPRINT-006`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0058`
- **Dependências:** EPIC-004, EPIC-027, EPIC-041
- **Release gate:** `G4/G5`
- **Referências arquiteturais:** ADR-051, ADR-047, ADR-041, ADR-049

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-034`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`, `ADR-049`, `ADR-052`

## Resultado

Gateway por capacidades, adapters stac/api oficial, testes de contrato, allowlist, ssrf/egress e estados de licença/disponibilidade.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4/G5` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-ANC-001, REQ-CRS-005, REQ-CRS-007, REQ-OFF-001, REQ-PUB-003, REQ-SRC-003
- Issue: `ISSUE-0058`
- Sprint: `SPRINT-006`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0358` / `ISSUE-0468` / `TASK-0358` — Definir contrato científico e invariantes: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0359` / `ISSUE-0469` / `TASK-0359` — Preparar corpus, fixtures e representação tipada: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0360` / `ISSUE-0470` / `TASK-0360` — Implementar o núcleo algorítmico: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0361` / `ISSUE-0471` / `TASK-0361` — Integrar ao ProcessingPlan e pipeline: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0362` / `ISSUE-0472` / `TASK-0362` — Produzir métricas, diagnóstico e lineage: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0363` / `ISSUE-0473` / `TASK-0363` — Executar benchmark, negativos e regressão científica: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0364` / `ISSUE-0474` / `TASK-0364` — Auditar evidência científica e final: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-034`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`, `ADR-049`, `ADR-052`
- **Resultado:** `PASS`
