# AGENTS.md — DSGeorref

Leia a issue, [Comece aqui](docs/00-governance/START_HERE.md) e o AGENTS.md mais próximo antes de editar.

- Trabalhe em uma issue por branch ou worktree. Respeite o escopo da issue e os limites de acesso e escrita do ambiente.
- Localize os requisitos, contratos e responsáveis pelo módulo. Pare se faltar uma definição necessária ou houver contradição.
- Integre contratos antes de paralelizar consumidores. Siga o [padrão de arquitetura Python](docs/03-engineering/PYTHON_CODE_ARCHITECTURE_STANDARD.md).
- PostgreSQL é autoritativo para estado. RabbitMQ serve como transporte.
- Preserve imutabilidade, hashes, lineage e semântica de coordenadas. Homografia projetiva é canônica e SGV é fail-closed.
- IA é opcional e se subordina à elegibilidade clássica e ao SGV.
- Execute `make verify` e os testes pertinentes antes do handoff. Nenhum agente aprova o próprio trabalho.
