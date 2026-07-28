# Layout normativo do monorepo greenfield

A partir da Fase C, código é organizado por **bounded context primeiro** e por camada interna depois. Consulte `docs/02-architecture/ddd/DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.

## Regras

- nenhuma pasta global `domain/`, `application/` ou `adapters/` recebe novas capabilities;
- nenhum package usa IDs ou títulos de backlog como boundary;
- o package do context contém `domain`, `application`, `adapters` e `contracts` conforme necessário;
- `geo` e `ai` permanecem distributions separadas, mas também se dividem por contexts;
- frontend, CLI, HTTP e workers são adapters;
- PostgreSQL, filesystem e RabbitMQ são infraestrutura;
- imports cross-context somente por contratos ou ports públicos;
- shared code é exclusivamente técnico e sem linguagem de negócio.

## Layout

Veja o diagrama textual e os packages aprovados em `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
