# Modelo operacional do Codex

Codex executa um TaskEnvelope por vez e segue o `AGENTS.md` mais próximo. TaskEnvelope governa write scope; PRD, ADRs, profiles e contratos governam semântica.

Comportamento obrigatório:

- carregar apenas contexto mínimo relevante;
- não inventar requisito, contrato, endpoint ou evidência;
- parar diante de contradição material;
- preservar imutabilidade e invariantes geoespaciais;
- executar checks declarados antes do handoff;
- nunca fazer merge, aprovar o próprio trabalho ou enfraquecer gate;
- emitir handoff estruturado.

Tarefas paralelas seguem `PARALLEL_EXECUTION_PLAN.md` e `.codex/policies/file-scopes.yaml`.
