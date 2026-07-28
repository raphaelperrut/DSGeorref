# EPIC-056 — máquina de estados de arestas, evidência direta, lineage e SGV independente da imagem dependente

- **Domínio:** `GEO`
- **Bounded Context owner:** `BC-005 — Descoberta e Aquisição de Referências`
- **Sprint planejada:** `SPRINT-006`
- **Papel responsável pela implementação:** `Geoprocessamento`
- **Issue principal:** `ISSUE-0056`
- **Dependências:** EPIC-023, EPIC-024, EPIC-052, EPIC-053
- **Release gate:** `G4`
- **Referências arquiteturais:** ADR-044, ADR-050

- ADRs: `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-050`

## Resultado

Máquina de estados de arestas, evidência direta, lineage e sgv independente da imagem dependente.

## Aceitação de produto

- O resultado é observável por interface pública, controle operacional ou artifact verificável.
- Estados de falha são explícitos, persistidos e testáveis.
- Os invariantes de segurança, geoespaciais, científicos e de compatibilidade aplicáveis passam.
- A evidência exigida por `G4` é anexada à issue e ao pull request.

## Restrições de engenharia

- Mudanças de contrato são integradas antes da implementação paralela.
- O Tech Lead decompõe este épico em tarefas limitadas antes da codificação.
- QA e final review são independentes da implementação.

## Rastreabilidade

- Requisitos: REQ-REF-002, REQ-RMV-003
- Issue: `ISSUE-0056`
- Sprint: `SPRINT-006`

## Histórias implementáveis


Este épico possui **7** histórias filhas:

- `STORY-0344` / `ISSUE-0454` / `TASK-0344` — Definir contrato científico e invariantes: máquina de estados de arestas, evidência direta, lineage e SGV independente da imagem dependente
- `STORY-0345` / `ISSUE-0455` / `TASK-0345` — Preparar corpus, fixtures e representação tipada: máquina de estados de arestas, evidência direta, lineage e SGV independente da imagem dependente
- `STORY-0346` / `ISSUE-0456` / `TASK-0346` — Implementar o núcleo algorítmico: máquina de estados de arestas, evidência direta, lineage e SGV independente da imagem dependente
- `STORY-0347` / `ISSUE-0457` / `TASK-0347` — Integrar ao ProcessingPlan e pipeline: máquina de estados de arestas, evidência direta, lineage e SGV independente da imagem dependente
- `STORY-0348` / `ISSUE-0458` / `TASK-0348` — Produzir métricas, diagnóstico e lineage: máquina de estados de arestas, evidência direta, lineage e SGV independente da imagem dependente
- `STORY-0349` / `ISSUE-0459` / `TASK-0349` — Executar benchmark, negativos e regressão científica: máquina de estados de arestas, evidência direta, lineage e SGV independente da imagem dependente
- `STORY-0350` / `ISSUE-0460` / `TASK-0350` — Auditar evidência científica e final: máquina de estados de arestas, evidência direta, lineage e SGV independente da imagem dependente

A ordem efetiva é governada por `STORY_DEPENDENCY_GRAPH.json`; IDs não substituem dependências.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Classificação:** `Supporting`.
- **Modelo interno:** não pode ser importado por outro bounded context.
- **Integrações:** somente pelos contratos e relações do `DDD-040-CONTEXT-MAP.md`.
- **ADRs governantes adicionais:** `ADR-003`, `ADR-004`, `ADR-005`.
- **Resultado:** `PASS`; o épico possui owner semântico único.

## Revisão de ADRs — Fase D

- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-050`
- **Resultado:** `PASS`
