# Cobertura do repositório de engenharia

Este relatório descreve o estado atual da baseline, não um registro histórico.

| Entrega solicitada | Evidência ativa | Estado |
|---|---|---|
| Roadmap integralmente processado | `docs/06-delivery/ROADMAP.md`, `SPRINT_INDEX.csv`, 12 arquivos de sprint | Completo |
| Todos os módulos identificados | `docs/02-architecture/MODULE_CATALOG.md`, 18 arquivos `MOD-*` | Completo |
| Requisitos funcionais e não funcionais extraídos | `376` requisitos em `REQUIREMENTS_BASELINE.md` e `requirements/` | Completo |
| PRD profissional | `docs/01-product/PRD.md` | Completo |
| Épicos | 110 arquivos em `docs/06-delivery/epics/` | Completo |
| Histórias de usuário e critérios de aceite | `759` arquivos em `docs/06-delivery/stories/` | Completo |
| Dependências entre histórias | `STORY_DEPENDENCY_GRAPH.json`, `STORY_DEPENDENCY_GRAPH.md`, 88 ondas topológicas | Completo |
| ADRs vigentes e contíguas | `ADR-001` a `ADR-057` | Completo |
| Contratos de API e domínio | `contracts/http/domains/`, OpenAPI e schemas versionados | Completo |
| Tarefas Codex executáveis | `759` TaskEnvelopes validados em `.codex/tasks/` | Completo |
| Prompts permanentes por agente | 11 protocolos em `.codex/roles/` | Completo |
| Backlog sprint a sprint | 12 arquivos em `docs/06-delivery/sprint-backlogs/` | Completo |
| Cobertura requisito → história | 100% na `TRACEABILITY_MATRIX.csv` | Completo |
| Limpeza de material substituído | IDs e artefatos de consolidação ausentes; histórico de mudanças fica no Git | Completo |

## Verificação reproduzível

Execute `make verify` e `sha256sum -c SHA256SUMS.txt` na raiz. A implementação funcional permanece bloqueada até o gate formal da `SPRINT-001`.
