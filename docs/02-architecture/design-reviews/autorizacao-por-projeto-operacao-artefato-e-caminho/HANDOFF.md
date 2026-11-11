# STORY-0046 — contrato de autorização por recurso

Issue #122 / EPIC-010 / TASK-0046 / BC-002. Baseline remota confirmada:
`737dab68225367eeb5ebf116f54c4511141cd0cf`. Dependência #121 integrada via #1057.
Execução solo: nenhuma aprovação independente de Arquiteto ou Reviewer é declarada.
O próximo gate é revisão humana vinculada ao SHA candidato publicado no PR; sem merge.

## Resultado e autoridade

Contrato de composição `identity-access-resource-authorization` 1.0.0; a política central
continua 1.1.0, sem cópia ou ampliação de concessões. O oracle offline lê a política e
delega os guards e transições ao freeze existente. Hashes SHA-256 normalizados UTF8/LF
fixam as duas dependências no contrato; o teste rejeita drift. Não há implementação runtime.

| Decisão | Autoridade efetiva |
|---|---|
| Concessão explícita, vínculo vigente, matriz de papéis, sem bypass de administrador | Política BC-002 1.1.0 integrada no EPIC-009 |
| Decisão central por papel/projeto/operação/recurso, reavaliada server-side | REQ-ACC-001, REQ-AUTH-IMPL-006, ADR-030 e freeze BC-002 |
| Conta ativa, sessão/PAT vigente, revogação, escopo limitado | ADR-028, ADR-030 e máquinas existentes |
| Throttling como predicado adicional onde já publicado | REQ-AUTH-IMPL-007, ADR-031, política e evidence schema existentes |
| Ownership lógico do artefato | Manifest 2.0.0: project_id e artifacts[].artifact_id; BC-013 é owner do manifest/publicação |
| Caminho relativo como seletor exato, resolução física separada | ArtifactDescriptor 2.0.0, SPEC-005 §15, REQ-ARTLAYOUT-010 |
| Observação sem secrets/caminhos internos | AuthorizationDecision existente e ADR-055 |

REQ-AUTH-IMPL-007 conserva seu significado: throttling com estado e evidência observável.
Não governa concessões. ADR-051 trata de AI Router/classic-first e é não governante para
esta decisão. A referência de owner ADR-043 em REQ-ACC-001 também não transforma a ADR
de stack nativa em autoridade de concessões. O requisito textual, ADR-030, a política
1.1.0 e o freeze fornecem autoridade suficiente e convergente; nenhum ADR foi alterado.
Os vínculos históricos na matriz `ACCEPTANCE_CRITERION_TRACEABILITY.csv`, linhas da
ISSUE-0156, são preservados; esta tabela explicita sua aplicação concreta sem reinterpretação.

## Boundaries, estados e compatibilidade

Permitir exige identidade ativa, credencial vigente, política atual, recurso existente,
concessão vigente, operação/tipo compatíveis e todos os guards publicados. Projeto exige
mesmo sujeito, projeto e revisão autoritativa positiva vigente. PAT restringe a concessão
por permissão exata e projeto; nunca amplia direitos. Campos obrigatórios ausentes e
guards ausentes/não booleanos negam. Autoridade/política/auditoria indisponíveis não têm fallback.

As cinco operações autenticadas conservam a matriz; as três exceções de autenticação
continuam no freeze, sem concessão por papel. `authorization:check` autoriza a consulta
do próprio sujeito, não a ação consultada; seu resultado não é ticket para acesso posterior.
Erros/status/ordem dos guards HTTP permanecem nos contratos publicados dos oito endpoints.
O DTO offline usa somente allowed/policyVersion/reasonCode e negativa genérica sem eco de input.

O manifest publicado fornece o projeto do artefato; um caminho físico não é autoridade.
O vínculo artefato/manifest e o seletor relative_path são testados usando o exemplo real
do manifest, sem I/O ou recursos de filesystem inventados. `artifact_manifest:read` já
existe no catálogo, mas não tem concessão na política 1.1.0: todos os papéis recebem deny.
Esta história não cria concessões de download/manifest nem uma rota de path. O owner BC-013
continua responsável pela integridade e resolução segura após autorização lógica válida.

Concessão de membership reutiliza somente o POST existente, com alvo existente, papel
registrado, unicidade, proveniência e commit. Alteração/revogação de membership não têm
comando publicado neste conjunto: permanecem não suportadas, sem lifecycle inventado.
Conta, sessão, PAT, OIDC link e throttle reutilizam as transições existentes. Transições
inválidas são rejeitadas; mudanças de estado/escopo/política/revisão invalidam a decisão
na próxima avaliação. MembershipChanged só após commit, conforme freeze existente.

## Critérios e evidência executada

| Critério | Resultado contratual e evidência |
|---|---|
| AC-ISSUE-0156-01 | PASS: contrato 1.0.0 e oracle com decisões positivas/negativas executáveis |
| AC-ISSUE-0156-02 | PASS: test_req_auth_impl_007 reutiliza prova existente de estados/evidência e testa composição com concessões |
| AC-ISSUE-0156-03 | PASS: ausência de vínculo/concessão, projeto/recurso/escopo divergentes, credencial revogada, autoridade ausente, transição inválida e ausência de fallback |
| AC-ISSUE-0156-04 | PASS contratual: permissões, exceções, transições e obrigações server-side explícitas; enforcement novo não implementado |

Comandos executados na raiz; `P=.venv/Scripts/python`, `I=workdir/identity-env/Scripts/python`,
`C=contracts/contexts/identity_access/plt/autorizacao-por-projeto-operacao-artefato-e-caminho`.
Essas abreviações são apenas para reprodução dos comandos abaixo.

| Comando | Resultado |
|---|---|
| `P -X utf8 -m pytest -q -p no:cacheprovider --import-mode=importlib C -k 'test_req_auth_impl_007 or test_epic_010_politica'` | 6 passed, 119 deselected |
| `P -X utf8 -m pytest -q -p no:cacheprovider --import-mode=importlib contracts/contexts/identity_access` | 445 passed: 125 novos + 320 anteriores |
| `P -m ruff check --no-cache C` e `P -m ruff format --check --no-cache C` | PASS |
| `I -X utf8 -m pytest -s -q -p no:cacheprovider evidence/reviews/usuarios-e-papeis-da-instancia/test_acceptance.py --tb=short` | 2 passed; internamente 6 happy + 10 negative, sem skips |
| `I -X utf8 -m pytest -q -p no:cacheprovider --import-mode=importlib tests/backend/identity_access/local_identity/test_requirements.py tests/backend/identity_access/local_identity/test_identity_requirements.py::test_bootstrap_session_token_recovery tests/backend/identity_access/local_identity/test_http.py::test_logout_revokes_once_and_clears_cookie src/backend/dsgeorref/contexts/identity_access/adapters/usuarios-e-papeis-da-instancia/acc-auth-impl-parte-1/tests/test_slice_consolidation.py::test_story_0042_slice_consolidation --tb=short` | 13 passed |
| `git diff --check` | PASS; conferência staged/commit registrada no PR |
| `make verify PYTHON=.venv/Scripts/python` | Python quality PASS; frontend bloqueado por Node 24.22.1/pnpm 11.25.0 versus pins 24.20.0/10.26.1 |
| `make technical-tests PYTHON=.venv/Scripts/python` | Validadores PASS; 50 + 1 + 26 passed (3 deselected); native-stack: 15 passed, 4 failed por CRLF nos bytes pinados |

Regressão executada em série com PYTHONPATH=src/backend, PostgreSQL 18.4 descartável
`dsgeorref-issue-122-pg`, porta loopback 55482, base privada `local_identity_validation`.
IDENTITY_TEST_DSN e IDENTITY_MIGRATION_DSN apontam para essa mesma base com usuário de teste.
O primeiro ensaio no sandbox foi impedido por bloqueio TCP (10013); a reexecução autorizada
fora do sandbox passou. O Python global não tinha pytest/ruff; as venvs existentes foram usadas.

Diagnóstico dos quatro erros native-stack: normalizar CRLF para LF, apenas em memória,
reproduz exatamente os digests esperados 16970dba… (source lock), dafb10f3… (conda lock)
e 756dd9e6… (policy). Nenhum desses arquivos foi alterado. São limitações ambientais,
não defeitos introduzidos. A CI com pins e checkout Linux é acompanhada no PR candidato;
esta entrega não altera gates para incluir os novos testes, executados explicitamente acima.

## Escopo, riscos e reversão

Quatro arquivos novos: contract.json, conformance.py e test_resource_authorization.py
no diretório contratual permitido; este HANDOFF.md no diretório de design review permitido.
Conferência contra os dois allow_paths do TASK-0046; nenhum arquivo de evidence foi criado.
Branch anterior `codex/issue-120-security` e untracked `src/frontend/debug.log` preservados;
nenhum trabalho existente da #122 foi localizado localmente, no remoto ou em PR aberto.

Impacto: composição aditiva 1.0.0; política 1.1.0, oito endpoints, schemas globais e src
inalterados. Migrations: nenhuma, pois não há schema persistido alterado. Rollback:
reverter os quatro arquivos sem efeito em dados/runtime. Nenhum bloqueio material de definição.

Riscos residuais: fixtures são sintéticas; não atestam produção, calibração BP-003, provedor
externo ou enforcement novo. As limitações históricas documentadas na #121 permanecem;
não são sanadas por esta história. Consumidores deverão aplicar os predicados no serviço
central, validar ownership por port autoritativo e manter resolução física no owner.
Concessões futuras de artefato exigirão autoridade explícita; acesso continua negado até lá.
Revisão independente e resultado obrigatório da CI devem referenciar o SHA publicado no PR.
