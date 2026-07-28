# TaskEnvelopes Codex

Esta pasta contém **687 tarefas executáveis**, uma para cada história implementável.

- Schema: `TASK_ENVELOPE.schema.json`
- Tarefas: `TASK-0001.json` a `TASK-0687.json`
- Índice: `docs/06-delivery/STORY_INDEX.csv`
- Dependências: `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`
- Ondas: `docs/03-engineering/PARALLELIZATION_WAVES.md`

O agente deve carregar apenas o TaskEnvelope, a história, o épico, os requisitos e contratos referenciados. Paths não listados em `allow_paths` são read-only.
