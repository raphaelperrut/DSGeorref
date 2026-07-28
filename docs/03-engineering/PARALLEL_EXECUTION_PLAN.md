# Plano de execução paralela para Codex

## Pré-condições

1. História está Product Ready.
2. Arquiteto aprovou boundary e impacto contratual.
3. Mudanças de contrato foram integradas primeiro.
4. Tech Lead criou TaskEnvelopes com write scopes disjuntos.
5. Cada lane usa branch e worktree próprios.

## Lanes

- **Contratos:** ADR, OpenAPI, JSON Schema, eventos e fonte do cliente gerado; sempre serializada.
- **Backend:** domínio, application, API, persistência e workers.
- **Frontend:** UI contra o cliente gerado já integrado.
- **Geo:** raster, vetor, CRS, matching, SGV e mosaico.
- **IA:** ModelRunners e escalonamento governado atrás de contratos existentes.
- **Operações/Security:** infraestrutura, controles e evidências.
- **QA:** inicia em commits candidatos imutáveis e não corrige implementação.
- **Reviewer:** inicia após QA e é read-only, exceto pelo relatório de review.

## Ordem de integração

`contratos → migrations/core → adapters → frontend/CLI → testes de integração → evidência de QA → final review → merge humano`

## Controle de colisão

TaskEnvelope lista paths permitidos e proibidos. Duas tarefas ativas não podem gravar o mesmo path. Dependência nova em arquivo compartilhado interrompe as lanes; o Tech Lead cria tarefa serializada de integração.

## Branches e worktrees

Use `issue/ISSUE-0001-slug-curto` e worktree dedicado. Uma branch atende uma issue. Arquivos gerados são commitados no mesmo PR da fonte do contrato.

## Handoff

Cada lane entrega commit, arquivos alterados, versão/digest do contrato, testes, evidências, limitações e próxima dependência. Correção posterior gera nova revisão de handoff.
