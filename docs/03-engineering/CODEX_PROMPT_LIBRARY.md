# Biblioteca de prompts do Codex

> Registro histórico. A [governança vigente](../../GOVERNANCE.md) define o fluxo a partir da integração da #1047.

Prompts permanentes ficam em `.codex/roles/`. Prompts reutilizáveis são templates estruturados:

- `.codex/tasks/TASK_ENVELOPE.schema.json`
- `docs/08-templates/AGENT_TASK.md`
- `docs/08-templates/HANDOFF.md`
- `docs/08-templates/DESIGN_REVIEW.md`
- `docs/08-templates/TEST_PLAN.md`

Todo prompt identifica papel, issue, resultado, fontes normativas, paths permitidos/proibidos, critérios, testes, evidência e condições de parada.
