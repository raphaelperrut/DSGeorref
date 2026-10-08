# STORY-0768 / ISSUE-0875 — Aprovar o grafo Python do workspace para materialização determinística de uv.lock

- **Tipo:** `História implementável — prerequisite técnica`
- **Estado:** `CLOSED_AS_DEFERRED` — obrigação consumida pela SPRINT-012; sem PASS de execução pendente
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

## Reconciliação administrativa — materialização DevOps (2026-10-07)

Autoridade humana desta reconciliação: `APPROVED_GRAPH_SHA = cb198c9e8340e0675c36679de426abf922e1c569`. Architect Review, QA e Final Review = PASS no mesmo SHA; BLOCKER/HIGH = NONE e MATERIAL_DECISION_OPEN = NONE, conforme aprovação final informada pelo usuário. Essa informação encerra o objetivo arquitetural do TASK-0771 e supera seus estados históricos Planned/review pendente para o dependency graph, sem alterar nenhum artifact aprovado ou atribuir aprovação à execução DevOps futura.

Foi verificada ausência de task DevOps filha com escopo suficiente. Existe somente TASK-0771 para esta Story/Issue, sem autorização de pyproject.toml/uv.lock. Cria-se UMA task operacional filha, preservando o TaskEnvelope arquitetural e os índices canônicos de Story/Issue:

- **Task:** `TASK-0773` — `.codex/tasks/operations/TASK-0773.json`.
- **Owner:** DevOps / ROLE-009.
- **Outcome:** materializar deterministicamente o dependency graph aprovado e gerar uv.lock sem qualquer nova escolha técnica.
- **Autoridade imutável:** os quatro artifacts approved-dependency-graph.yaml, constraints.txt, rationale.md e devops-handoff.md, com seus inputs/digests/evidência, no SHA acima. Consumir os blobs desse commit, não regenerar ou editar o graph/snapshot/handoff.
- **Allow paths de execução:** `pyproject.toml` exclusivamente pela transformação do handoff aprovado; `uv.lock`; `evidence/operations/python-workspace-lock/**`. O envelope é criado por esta autorização administrativa e permanece read-only durante execução DevOps; não há necessidade de conceder autoedição.
- **Serialização:** uma branch/worktree exclusiva de TASK-0773/ISSUE-0875; pyproject.toml e uv.lock reservados apenas para esta execução, sem colisão com outra lane. Não descartar trabalho alheio, transportar evidência da ISSUE-0876 ou ampliar scope.
- **Estado da execução:** não realizada; lock ausente; QA/Reviewer do candidate de execução pendentes. O PASS arquitetural não atesta lock/frozen install.

A tarefa fica em `.codex/tasks/operations/` conforme o padrão existente de envelopes operacionais filhos; não substitui o task_id arquitetural canônico da Story, não cria nova Story/Issue nem modifica o grafo de dependências entre histórias. A proibição original de criar terceira task descreve a decomposição/escopo anteriores; esta autorização humana posterior permite apenas essa única tarefa filha de materialização, dentro da mesma Story/Issue.

### Aceite da task operacional

Os IDs abaixo são critérios da tarefa filha autorizados neste pedido, não novos requisitos nem decisões de versão; os cinco critérios arquiteturais originais permanecem preservados.

- AC-1 / AC-ISSUE-0875-06: workspace materializado exatamente conforme approved-dependency-graph.yaml no SHA cb198c9e8340e0675c36679de426abf922e1c569; pyproject.toml deve corresponder aos bytes de pyproject-proposed.toml desse SHA. Somente os dois arquivos raiz pyproject.toml e uv.lock podem ser alterados fora da evidência própria; nenhum manifest filho ou package novo.
- AC-2 / AC-ISSUE-0875-07: uv.lock gerado com CPython 3.12.13/Linux amd64, uv 0.12.19 e seu digest oficial, índice local canônico, metadados, markers/extras e política transitiva do handoff aprovado no SHA cb198c9e8340e0675c36679de426abf922e1c569; não regenerar snapshot nem consultar outro índice.
- AC-3 / AC-ISSUE-0875-08: nenhuma dependência, versão, constraint, extra, origem ou parâmetro de resolução escolhido manualmente pelo DevOps; sem upgrade/downgrade, override, fallback ou atualização por conveniência; preservar todos os inputs aprovados.
- AC-4 / AC-ISSUE-0875-09: uv lock --check equivalente PASS, com o resolver/config/intérprete aprovados, e check-structure.py --verify-digests --check-lock uv.lock PASS; registrar resultados reais.
- AC-5 / AC-ISSUE-0875-10: sync --frozen reproduzível PASS no ambiente aplicável do graph, para runtime e dev/test conforme handoff; segunda geração independente em checkout limpa produz o mesmo SHA-256 de uv.lock, sem usar o primeiro lock como preferência; repetir frozen sync offline com cache completo verificado. Não depender do venue BP-003/ISSUE-0876.
- AC-6 / AC-ISSUE-0875-11: registrar em evidence/operations/python-workspace-lock/** os comandos e saídas reais, identidade/digest do CPython e uv, plataforma, APPROVED_GRAPH_SHA=cb198c9e8340e0675c36679de426abf922e1c569, SHA-256 dos quatro artifacts e de todos os inputs consumidos, pyproject.toml, uv.lock, duas reproduções e frozen installs; sem secrets nem PASS presumido.
- AC-7 / AC-ISSUE-0875-12: diff e inventário efetivamente materializados correspondem à autoridade aprovada: mesmos grupos/direct pins, 43 distribuições, 31 constraints, markers/extras e URLs/hashes admitidos. Comparação explícita graph -> pyproject -> uv.lock -> instalação; nenhum diff no graph aprovado, sua evidência, código, manifests históricos ou Conda/native. QA e Reviewer independentes validam o mesmo candidate SHA de execução.

### Paralelismo e bloqueio downstream

TASK-0773 consome somente o TASK-0771 concluído e a autoridade imutável aprovada. ISSUE-0876 / TASK-0772 não é sua dependência; ambas as lanes continuam paralelas. Lock/frozen install deve usar o ambiente aplicável do graph e não aguardar ou substituir o venue BP-003. A task operacional não autoriza mudanças de código, manifests históricos, graph, Conda/native, upgrades/downgrades, choices por conveniência ou execução de benchmark.

TASK-0769 permanece BLOCKED por dois fatos independentes: uv.lock ainda não materializado e venue ISSUE-0876 ainda indisponível. Criar este envelope não satisfaz nenhum desses blockers, não libera execução de benchmark e não conclui ISSUE-0873/0822/0150. Próxima ação: DevOps executar TASK-0773 sob o escopo reservado, produzir lock/reprodução/frozen install e submetê-los a QA/Reviewer independentes no mesmo candidate SHA.

TASK-0771: grafo aprovado independentemente em cb198c9e8340e0675c36679de426abf922e1c569, preservado e não reaberto. TASK-0773: DEFERRED_TO_SPRINT_012; uv 0.12.19 e inputs validados, CPython externo ao Conda EXTERNAL_INPUT_MISSING; lock e frozen install não executados.

## Disposição administrativa vigente — 2026-10-07

CLOSED_AS_DEFERRED / DEFERRED_TO_SPRINT_012, por decisão explícita do usuário.
[Obrigação canônica que absorve o trabalho pendente](../../07-assurance/PHASE-G-CTO-REVIEW-REPORT.md#epic-008-req-auth-impl-007-production-readiness):
EPIC-008-REQ-AUTH-IMPL-007-PRODUCTION-READINESS. Este item deixa de bloquear o
 desenvolvimento corrente; suas instruções de execução anteriores descrevem o
escopo técnico futuro e não autorizam retomar infraestrutura nesta fase.
Não há PASS de execução/produção. Evidências anteriores permanecem imutáveis.
Retomada na fase de readiness exige autoridade operacional e gates existentes.

## Revisão SAR

Reconciliação estrutural de 2026-10-07, conforme os charters das Fases B e F. Aprovação humana explícita de 2026-10-08: os campos PASS de B/F neste recorte significam PASS_STRUCTURAL_ONLY; não certificam execução.
B revisa definição, conflitos, critérios/ADRs, requisitos e dependências.
F revisa planejamento por dimensão e não concede autorização de implementação.
Neste passe: IDs, JSON Schema, owner Story/Issue, paths, referências, DAG e
predecessores declarados conferidos; PASS estrutural não é execução técnica.

- **Definição/requisitos:** PASS estrutural; critérios e requisito preservados.
- **Dependências:** PASS estrutural do DAG e da ordem declarada, sem quitação operacional.
- **Review:** PASS estrutural dos papéis requeridos e obrigação de mesmo candidato, sem presumir review de execução.
- **Estado real:** Dependency graph aprovado: Architect Review, QA e Reviewer PASS no SHA cb198c9e8340e0675c36679de426abf922e1c569, conforme reconciliação existente. TASK-0773 DEFERRED_TO_SPRINT_012; uv.lock NÃO GERADO, frozen install não concluído e CPython input EXTERNAL_INPUT_MISSING.
- **DEFERRED_ID preservado:** EPIC-008-REQ-AUTH-IMPL-007-PRODUCTION-READINESS.
- **Gate:** EPIC-108 / GitHub #816 / SPRINT-012 permanece fail-closed.
- **Ownership:** Backend / identity_access funcional; benchmark Security; BC-015 consome/enforce release gate.

## Domain-Driven Design — Fase C

- **Contexto owner:** BC-001, conforme TaskEnvelope e STORY_INDEX existentes.
- **Impacto no modelo:** NONE; nenhum modelo/código de produto alterado.
- **Regra:** boundaries e contratos publicados preservados; sem transferir ownership funcional.
- **Resultado:** PASS estrutural de definição/ownership; não atesta execução ou produção.
