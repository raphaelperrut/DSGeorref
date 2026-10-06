# STORY-0768 / ISSUE-0875 — Aprovar o grafo Python do workspace para materialização determinística de uv.lock

- **Tipo:** `História implementável — prerequisite técnica`
- **Estado:** `Planned` — execução e review independente pendentes
- **Épico pai:** `EPIC-001`
- **Sprint:** `SPRINT-001`
- **Domínio:** `FND`
- **Bounded Context:** `BC-001 — Governança de Engenharia e Entrega`
- **Owner executor:** `Arquiteto`
- **TaskEnvelope:** `.codex/tasks/TASK-0771.json`
- **Downstream:** `STORY-0762 / ISSUE-0873 / TASK-0769`, Security/ROLE-010

## Resultado e limites

Aprovar o grafo Python direto e a política determinística de fechamento transitivo do backend/workspace atual, reconciliar pins e entregar autoridade versionada e handoff exato para DevOps materializar uv.lock posteriormente.

A decisão é técnica e local às autoridades ADR-001/ADR-009/TECHNOLOGY_BASELINE; não exige uma nova ADR por si só. Inventariar somente o workspace/backend atual, lendo código e manifests como evidência. Não inferir o grafo da máquina do desenvolvedor. O inventário DIRECT_DECLARED_DEPENDENCIES, requirements-validation e requirements do adapter são insumos, não fechamento transitivo aprovado. O lock Conda permanece autoridade da stack nativa e não substitui uv.lock.

Entregar quatro arquivos de decisão: fonte aprovada do grafo com identidade/versão, constraints indispensáveis, rationale de reconciliação e handoff DevOps. A política deve fechar escolhas transitivas de modo reproduzível, com fonte/pins/constraints e bindings necessários; se uma resolução posterior ainda precisar escolher dependências sem aprovação, a decisão não está concluída. Não fabricar lock vazio a partir de dependencies=[].

DevOps materializa o lock posteriormente, após aprovação independente e scope explícito/serializado para pyproject.toml/uv.lock. Essa escrita está fora desta tarefa de decisão; o handoff não concede autorização implícita. Nenhuma terceira Story/Issue/Task é criada nesta decomposição. Aprovar o grafo não atesta um lock materializado ou frozen install: TASK-0769 continua impedida de medir enquanto faltar o lock exigido pelo profile e o preflight real.

Required roles: Arquiteto autor da decisão; Arquiteto independente aprova a escolha técnica; DevOps verifica que o handoff não delega escolhas ad hoc; QA valida inventário/fechamento/reprodução documental; Reviewer verifica escopo e rastreabilidade no mesmo candidate SHA. O executor não aprova a própria entrega. Não resolver venue, criar benchmark, alterar contratos de produto ou promover throttling.

## Allow paths exclusivos de execução

- `docs/02-architecture/design-reviews/python-workspace-dependency-graph/approved-dependency-graph.yaml`
- `docs/02-architecture/design-reviews/python-workspace-dependency-graph/constraints.txt`
- `docs/02-architecture/design-reviews/python-workspace-dependency-graph/rationale.md`
- `docs/02-architecture/design-reviews/python-workspace-dependency-graph/devops-handoff.md`
- `evidence/architecture/python-workspace-dependency-graph/**`

## Deny paths

- `src/**`
- `pyproject.toml`
- `uv.lock`
- `requirements-validation.txt`
- `infra/images/**`
- `.github/**`
- `contracts/**`
- `tests/**`
- `tools/**`
- `**/migrations/**`
- `docs/04-quality/benchmark-profiles/**`
- `docs/03-engineering/application-profiles/AP-003-web-security-runtime-profile.md`
- `.codex/tasks/TASK-0769.json`
- `.codex/tasks/TASK-0712.json`
- `.codex/tasks/TASK-0040.json`
- `infra/**`
- `evidence/operations/bp003-throttling-venue/**`

A criação administrativa de histórias/envelopes/índices foi autorizada separadamente pelo pedido de decomposição de ISSUE-0873. O escopo acima não autoriza sua alteração durante a execução destas prerequisites. Cada execução usa uma issue e TaskEnvelope por branch/worktree; nenhuma execução ocorreu nesta materialização. Não implementar produto, alterar profile, gerar lock ou provisionar host neste passe.

## Dependências e isolamento

Predecessores: nenhum novo predecessor Story; autoridades normativas já disponíveis na baseline.

STORY-0768 / ISSUE-0875 / TASK-0771 e STORY-0769 / ISSUE-0876 / TASK-0772 são paralelas: nenhuma depende da outra e seus write scopes são disjuntos. Ambas bloqueiam STORY-0762 / ISSUE-0873 / TASK-0769, que bloqueia STORY-0712 / ISSUE-0822 e depois STORY-0040 / ISSUE-0150. STORY-0239 não vira predecessor; seu caminho já é downstream e produziria ciclo. STORY-0767 aprovada permanece satisfeita; não se altera a semântica ou o conteúdo do benchmark.

## Requisitos e ADRs

REQ-TOOL-002; downstream REQ-AUTH-IMPL-007.
ADRs: ADR-001, ADR-006, ADR-007, ADR-008, ADR-009, ADR-033. Sem nova ADR nesta decomposição.

## Critérios de aceitação

- [ ] AC-ISSUE-0875-01: Inventário versionado e rastreável somente das dependências Python realmente requeridas pelo backend/workspace atual, com origem em imports/manifests/uso, classificação runtime/validação e fronteiras de workspace; reconciliar dependencies=[] e inventários parciais sem adições por oportunidade.
- [ ] AC-ISSUE-0875-02: Grafo direto e pins/constraints necessários aprovados por autoridade técnica independente da autoria; divergências de versão, inclusive psycopg, resolvidas com rationale de compatibilidade/ABI e fontes, sem alterar stack nativa ou fazer upgrades dispensáveis.
- [ ] AC-ISSUE-0875-03: Política de resolução transitiva aprovada fixa escopo, Python/plataforma, fontes, versão/digest do resolver, markers/extras e constraints ou snapshot/fechamento suficiente para reprodução; nenhuma escolha transitiva ad hoc ou dependência sem autoridade pode restar para DevOps.
- [ ] AC-ISSUE-0875-04: Fonte approved-dependency-graph.yaml e constraints versionadas, digests e candidate SHA vinculados a aprovação arquitetural independente, validação QA e final review; ausência de aprovação ou ambiguidade de fechamento mantém TASK-0769 bloqueada.
- [ ] AC-ISSUE-0875-05: Handoff exato para DevOps identifica fontes, versões/SHA-256, transformações para pyproject/workspace, procedimento determinístico de lock/frozen install, validações e scope compartilhado que Tech Lead deverá autorizar e serializar; não gera uv.lock, não modifica pyproject, produto, stack nativa ou semântica BP-003 nesta tarefa.

## Validações e evidência

- Conferir rastreabilidade imports/uso -> inventário -> grafo direto -> pins/constraints, excluindo dependências não requeridas e distinguindo runtime/tooling/native.
- Conferir fundamento de cada divergência e coerência Python/plataforma/ABI; demonstrar documentalmente que a política transitiva é determinística e rejeita fontes/pins ausentes.
- Verificar YAML/constraints, versionamento/SHA-256/candidate e handoff DevOps por revisão independente; não gerar lock nem instalar/atualizar dependências nesta tarefa.
- Verificar diff limitado aos outputs declarados e ausência de mudanças em pyproject/uv.lock, stack nativa, código de produto e BP-003/profiles; make verify antes do handoff.

Evidência: `evidence/architecture/python-workspace-dependency-graph/`. Required roles: Arquiteto, DevOps, QA, Reviewer. Aprovações independentes no mesmo candidate SHA, com identidade/role/evidência atribuíveis; não basta autoemitir PASS ou reutilizar review de outro candidato. Perfis existentes são lidos por digest; evidências revisadas são append-only.

## Handoff, rollback e parada

Handoff identifica outputs exatos, versões/SHA-256/candidate SHA, limites e comandos de reprodução; o consumidor mantém BLOCKED se faltar lock, venue ou runtime/observáveis exigidos. Sem migration ou mudança de contrato de produto. Rejeição invalida o handoff e preserva o blocker, sem defaults silenciosos. Parar por autoridade contraditória, necessidade de ampliar escopo, entrada operacional ausente ou aprovação independente faltante.

## Planejamento e prompt

Leia AGENTS.md, papel, esta história, TaskEnvelope e referências aplicáveis. Execute somente o recorte autorizado após liberação do Tech Lead. Campos PASS constantes exigidos pelo schema descrevem a baseline estrutural; não comprovam execução ou aprovação. Estado Planned e review BLOCKED até evidência independente. A criação destes documentos não libera TASK-0769 nem conclui ISSUE-0873/0822/0150.
