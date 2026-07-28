# AGENTS.md — DSGeorref

Leia `docs/00-governance/START_HERE.md`, issue, TaskEnvelope e o `AGENTS.md` mais próximo antes de editar.

Regras obrigatórias:

- uma issue e um TaskEnvelope por branch/worktree;
- obedecer allow/deny paths;
- não inventar requisito, contrato, endpoint, tabela, estado, evento, papel, benchmark ou evidência; ausência é condição de parada;
- integrar contratos antes da implementação paralela;
- PostgreSQL é autoritativo para estado; RabbitMQ é somente transporte;
- preservar imutabilidade, hashes, lineage e semântica de coordenadas;
- homografia projetiva é canônica; SGV é fail-closed;
- IA é opcional e não contorna elegibilidade clássica ou SGV;
- código deve seguir `PYTHON_CODE_ARCHITECTURE_STANDARD.md`; paths por épico/issue, imports circulares e módulos gigantes são proibidos;
- nenhum agente aprova o próprio trabalho;
- executar `make verify` antes do handoff.
