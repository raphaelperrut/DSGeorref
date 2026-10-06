# Materialização das duas prerequisites de ISSUE-0873

Base administrativa: `3dc47304a66b029cdc9cec9aa5a5a531e8a26743`.
Perfis de execução aprovados: `4b634381328bd969679abe48ee6936aaf8fe4319`.

Foram criadas exatamente duas Stories/Issues/TaskEnvelopes locais:

- STORY-0768 / ISSUE-0875 / TASK-0771 — Arquiteto, decisão do grafo Python.
- STORY-0769 / ISSUE-0876 / TASK-0772 — DevOps, venue do experimento BP-003.

Ambas estão Planned e exigem aprovação independente no mesmo candidate SHA.
A materialização não aprova as decisões, não entrega grafo/constraints aprovados,
não gera uv.lock, não provisiona host e não executa benchmark. A aprovação de
STORY-0767 e os bytes dos perfis/AP-003/BP-003 permanecem preservados.

## Escopos e outputs futuros

TASK-0771 escreve somente quatro documentos em
`docs/02-architecture/design-reviews/python-workspace-dependency-graph/`:
`approved-dependency-graph.yaml`, `constraints.txt`, `rationale.md` e
`devops-handoff.md`; evidência em
`evidence/architecture/python-workspace-dependency-graph/**`.
Arquiteto autor e aprovador técnico devem ser independentes; DevOps verifica o
handoff, QA valida o fechamento e Reviewer verifica escopo/rastreabilidade.

TASK-0772 escreve somente em `infra/benchmarks/bp003-throttling-venue/**` e
`evidence/operations/bp003-throttling-venue/**`. O handoff exige venue identifier,
manifest completo, instruções e evidências reais de todo o hardware profile,
PostgreSQL/backend executáveis e gerador separado, sem workload de calibração.
DevOps executa; Arquiteto, QA e Reviewer validam independentemente o candidato.

Os write scopes são disjuntos e não incluem código de produto, stack nativa,
pyproject.toml/uv.lock, profiles ou parâmetros de throttling. Nenhuma ADR foi criada.
O grafo aprovado é autoridade para uma materialização posterior por DevOps com
scope explícito/serializado; seu handoff não concede escrita na raiz por si só.
Nenhuma terceira prerequisite foi criada. Aprovação de grafo e evidência de host
não substituem uv.lock/frozen install e preflight de runtime/observáveis.

## Cadeia e estado

As duas prerequisites são paralelas, sem aresta ou alcance transitivo entre elas.
Ambas bloqueiam STORY-0762 / ISSUE-0873 / TASK-0769, que permanece Security/ROLE-010
e BLOCKED. Predecessores anteriores STORY-0036 e STORY-0767 foram preservados.
Venue preserva os predecessores de contratos/perfis já aprovados; grafo usa as
autoridades técnicas disponíveis na baseline. STORY-0239 não vira predecessor.
TASK-0712 / ISSUE-0822 e STORY-0040 / ISSUE-0150 continuam bloqueadas.

O commit administrativo registra a decomposição de ISSUE-0873; a execução de cada
nova issue usa sua própria branch/TaskEnvelope. Branches de execução previstas:
`codex/issue-0875-task-0771-python-dependency-graph` e
`codex/issue-0876-task-0772-bp003-execution-venue`. Não há execução das novas lanes
neste passe nem merge na baseline principal.

## Verificação

Checks focados passaram: JSON Schema/referências de TASK-0769/0771/0772,
IDs únicos incluindo envelopes operacionais, índices e predecessores espelhados,
scopes disjuntos, dois predecessores novos para TASK-0769, ausência de ciclo e
de dependência entre as novas prerequisites. Grafo: 765 nós, 1179 arestas,
93 ondas, zero ciclos. Dez critérios novos permanecem BLOCKED.

`make verify` global e QA/review não foram executados, conforme o escopo
administrativo mantido nesta reconciliação; as novas tarefas preservam make verify
obrigatório no handoff de sua execução futura. Não foi investigado EPERM/Vitest.
Os checks da materialização não são aprovações independentes de implementação.
Evidências e arquivos locais preexistentes de outros passes foram preservados.

## Próximo passo

Tech Lead atribui TASK-0771 ao Arquiteto e TASK-0772 a DevOps em lanes separadas,
com revisão independente do candidato de cada entrega. O consumidor permanece
BLOCKED até resolver grafo/lock, venue e preflight completo. Não há autorização de
benchmark ou promoção de política runtime por este handoff.
