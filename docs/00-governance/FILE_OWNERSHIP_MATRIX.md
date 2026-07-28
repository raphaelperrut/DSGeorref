# Matriz de ownership de arquivos

Os escopos machine-readable estão em `.codex/policies/file-scopes.yaml`.

| Papel | Write scope primário | Arquivos compartilhados serializados |
|---|---|---|
| Product Owner | `docs/01-product/**`, seções de produto dos épicos | PRD e índice de épicos |
| Arquiteto | `docs/02-architecture/**`, `contracts/**` | índice de ADR e contratos públicos |
| Tech Lead | `docs/06-delivery/**`, `.codex/tasks/**` | índices de sprint e issue |
| Backend | `src/backend/**`, testes Backend | migrations e OpenAPI |
| Frontend | `src/frontend/**`, testes Frontend | cliente gerado e design tokens |
| IA | `src/ai/**`, fixtures de avaliação | schema de ModelPack |
| Geoprocessamento | `src/geo/**`, testes Geo | profiles científicos e fixtures |
| DevOps | `infra/**`, workflows e tools | locks e release manifests |
| Security | testes/políticas de segurança | contratos de auth e threat model |
| QA | `tests/**`, `evidence/qa/**` | fixtures compartilhados |
| Reviewer | `evidence/reviews/**` | nenhum; restante read-only |
