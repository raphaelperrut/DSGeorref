# SAR-120 — Dependências e entrega

O grafo de histórias é o mecanismo normativo de paralelização. Aresta `A blocks B` significa que B somente inicia após o artifact/contrato de A estar integrado.

- Grafo: `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`.
- Índice: `docs/06-delivery/STORY_INDEX.csv`.
- Ondas topológicas: `docs/06-delivery/STORY_DEPENDENCY_GRAPH.md`.
- Audit: `docs/07-assurance/DEPENDENCY_AUDIT.md`.

Contratos e migrations são serializados; implementações especialistas abrem lanes disjuntas somente após contract freeze. QA e Reviewer atuam sobre o mesmo commit candidato e não aprovam o próprio trabalho.

## SharedPartialDeliveryGate — ADR-006 / BC-001

O grafo de Stories continua somente Story→Story. `TaskEnvelope.dependencies` reflete
literalmente seus predecessores. `delivery_gate_dependencies` acrescenta hard gates
de artifacts parciais; ausência é válida. `delivery_gate_scope` seleciona uma etapa
do owner, sem concluir a Story. A execução sem esse scope usa as dependências integrais.
Stage B de TASK-0738 remove o scope parcial no envelope de execução e mantém STORY-0185.
O gate permanece owned por Task/Story existentes e consumido, independentemente do
scope da execução atual; seu aceite continua ligado ao snapshot histórico da Stage A.

O validator combina nós de conclusão de Stories e nós de entrega de gates: predecessores
Story→Story permanecem; `stage_story_dependencies` liga conclusões ao gate; o gate liga
ao owner (conclusão integral) e aos consumers. Dependências de gates de um task também
precedem seus gates owned. Não se liga a conclusão integral do owner à sua própria
etapa parcial. Ciclos nessa projeção de execução são proibidos, sem editar graph edges.

### Digest e evidência

Definições e envelopes usam SHA-256 do JSON canônico já definido pelo perfil DAA
(UTF-8, normalização NFC, chaves ordenadas, sem whitespace; chaves duplicadas rejeitadas).
Manifests, snapshots, evidências e outputs referenciados usam SHA-256 dos bytes Git.
Alterar qualquer campo da definição invalida evidências anteriores.

Evidence root: `evidence/delivery-gates/<gate_id>/<candidate_sha>/`.
Nomes de transporte do modelo: `acceptance-manifest.json`, `task-envelope.acceptance.json`
e `integration-receipt.json`. Não são outputs frontend nem evidência já produzida.
O manifest liga a definição ao candidate e ao digest canônico do envelope owner de origem
nesse candidate; lista outputs físicos e evidência para cada check. Outputs adicionais
podem concretizar diretórios aprovados, sempre sem glob, únicos e autorizados pelo
envelope de origem; não podem substituir os outputs obrigatórios do registry.

O snapshot aprovado é exatamente o envelope de origem, acrescido somente do digest
dos bytes do manifest em `delivery_gate_scope.acceptance_manifest_sha256`. DAA verifica
esse snapshot no mesmo candidate, selando manifest, outputs e checks sem ciclo de hashes.
O receipt referencia manifest, snapshot, bundles DAA (bindings/attestations) e registro
humano por paths/digests. Um verdict PASS armazenado não substitui revalidação DAA.
Evidência de aprovação pode ser produzida depois do candidate e deve estar commitada
no consumer base; outputs devem ser idênticos no candidate, integração e consumer base.

Integração humana reutiliza o registro `HUMAN_MERGE`, `authority_role=Autoridade Humana`,
`result=PASS`, `reviewed_candidate_commit` e `merged_commit` do protocolo vigente.
Exige merge Git real, candidate na história incorporada por parent não principal e
integration commit na first-parent history de `required_baseline_ref`.
Ancestry obrigatória: candidate → integration commit → consumer base. Receipt/evidências
somente em branch/PR ou cherry-pick isolado não satisfazem o gate. Ref ausente falha fechado.

READY obrigatório: `python tools/validate_repository.py --ready-task TASK-0038 --consumer-base <SHA>`.
Lê definição, schemas, envelopes e evidências dos objetos Git do consumer base;
verifica também disponibilidade das Story dependencies concluídas no índice commitado.
Uma definição divergente do checkout canônico vigente falha fechado. Planejamento
com gate pendente continua válido; não há promoção implícita por Story status.

## DG-TASK-0738-A — Stage A autorizada

Owner: EPIC-031 / STORY-0738 / ISSUE-0848 / TASK-0738, fundação BC-016, SPRINT-002.
`stage_story_dependencies=[]` vale exclusivamente para essa etapa técnica por Owner
Decision registrada em ADR-006. Stage B permanece no SPRINT-009, dependente de STORY-0185;
STORY-0186 continua consolidando a conclusão integral dos slices. TASK-0038 depende
de STORY-0036 e deste gate, sem adquirir paths compartilhados.

Os outputs físicos obrigatórios são somente os já definidos: `src/frontend/package.json`,
`src/frontend/tsconfig.json`, `src/frontend/vite.config.ts`, `src/frontend/index.html`,
`src/frontend/src/main.tsx` e `src/frontend/openapi-client.config.json`. O layout interno
dos diretórios autorizados será concretizado na Stage A, listado no manifest e verificado
por checks; este registry não inventa arquivos gerados nem entrypoints públicos internos.

<a id="dg-task-0738-a-bootstrap"></a>
### bootstrap
Bootstrap mínimo executável React/TypeScript/Vite, desenvolvimento e build, sem
funcionalidade de produto do SPRINT-009.

<a id="dg-task-0738-a-public-composition"></a>
### public-composition
Ponto público de composição em `src/frontend/src/contexts/operator_experience/contracts/frontend-shell/`,
com implementação no diretório de bootstrap aprovado; consumidores usam exports públicos.

<a id="dg-task-0738-a-deterministic-generation"></a>
### deterministic-generation
Geração determinística exclusivamente de `contracts/http/openapi.yaml` commitado,
versão fixada e configuração canônica. `contracts/http/**` é somente leitura.

<a id="dg-task-0738-a-canonical-scripts"></a>
### canonical-scripts
Scripts em `src/frontend/package.json`: `dev`, `build`, `openapi:generate`,
`openapi:check`, `openapi:diff`, executados via `pnpm --dir src/frontend run <script>`.

<a id="dg-task-0738-a-versioned-artifact"></a>
### versioned-artifact
Artifact versionado em `src/frontend/src/contexts/operator_experience/contracts/openapi/generated/`;
manifest lista seus arquivos e hashes, sem edição manual de DTOs, enums ou wrappers.

<a id="dg-task-0738-a-shared-artifact"></a>
### shared-artifact
Frontend e testes de contrato consomem exatamente o mesmo artifact gerado, provado
por evidência executável e revisão independente.

<a id="dg-task-0738-a-semantic-diff"></a>
### semantic-diff
Diff semântico antes da integração detecta breaking changes; regeneração divergente
do artifact commitado é rejeitada, conforme ADR-013 e controles preservados do EPIC-004.

<a id="dg-task-0738-a-execution-evidence"></a>
### execution-evidence
Evidências versionadas de build, generate, check e diff referenciam o mesmo candidate
e os outputs aceitos. Não bastam configuração declarada ou scripts sem execução.

<a id="dg-task-0738-a-make-verify"></a>
### make-verify
Stage A exige execução real de `make verify` com evidência imutável no candidate.
PASS integral é aceito. Somente o evaluator governado de `DG-TASK-0738-A` pode aceitar
`make-verify` como `NONBLOCKING`, classificação `ENVIRONMENTAL`, exit bruto 2 e reason
`FOUNDATION_INTEGRATION_SERVICES_UNAVAILABLE`, quando o log prova que todos os gates
anteriores passaram e a única parada foi a exigência de `FOUNDATION_INTEGRATION=1`
e dos serviços PostgreSQL/RabbitMQ. Nenhum erro de frontend, OpenAPI, licença,
repositório ou código de Stage A pode ser mascarado. A classificação permanece
NONBLOCKING/ENVIRONMENTAL e nunca é convertida em PASS bruto.

<a id="dg-task-0738-a-independent-approval"></a>
### independent-approval
QA e Reviewer independentes no mesmo candidate, com approval DAA vigente verificado
pelo verifier existente e integração humana canônica; nunca autoaprovação.
