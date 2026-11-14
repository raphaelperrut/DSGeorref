# ISSUE #124 / STORY-0048 / TASK-0048

Baseline: `061e83daf5f22cd39f2338f83c204a29428c2cc0`.
Branch: `codex/issue-124-authorization-frontend`. Papel: Frontend, BC-002.
O candidato é o commit que contém este handoff e `validation.json`; resolver com
`git log -1 --format=%H -- evidence/implementation/epic-010/story-0048/HANDOFF.md`.
QA, Security, Arquiteto e Reviewer independentes não foram aprovados pelo executor.

## Resultado e autorização

Autorização do Owner confirmada em
https://github.com/raphaelperrut/DSGeorref/issues/124#issuecomment-6883269761.
Antes da sincronização foram corrigidas exclusivamente as duas listas allow_paths
de TASK-0048: produção preservada, evidência e próprio TaskEnvelope adicionados.
`validation.json` compara semanticamente todos os demais campos com o baseline.
Checkout sincronizado por fetch e branch nova no SHA solicitado; sem reset ou
alteração de trabalho preexistente. `src/frontend/debug.log` fica fora da entrega.

A página independente e o componente exportado oferecem sessão local, consulta
de autorização, consulta de membros e vínculo de conta existente. Todos usam
o transporte gerado já integrado. A montagem e os testes permanecem no feature
path autorizado; não foi preciso alterar shell, backend, OpenAPI ou cliente gerado.
Estado de carregamento, vazio, lista parcial, erro e negativa é visível. Formulários
têm labels, fieldsets desabilitados durante pedidos, feedback acessível e layout
móvel sem overflow horizontal. A captura local foi inspecionada visualmente.

## Critérios de aceitação

| AC | Evidência objetiva para revisão |
|---|---|
| AC_01 | `test_epic_010_superficie`: transporte gerado, query exata, allow/deny sem autoridade local, consulta vazia, vínculo confirmado com DTO correspondente e CSRF. Entrypoint utilizável documentado no README da feature. |
| AC_02 | Não há requisito exclusivo da história: DERIVED_CONTROL integra EPIC-010. A rastreabilidade de REQ-ACC/REQ-AUTH-IMPL e REQ-HW permanece nos produtores integrados STORY-0046/0716/0717/0047. Esta entrega demonstra somente consumo frontend, sem alegar revalidação científica, hardware ou calibração do épico. |
| AC_03 | Negativas recebidas permanecem negativas; não há cache de allow. Edição invalida resultado anterior. Testes cobrem respostas malformadas, status/media type inesperados, HTTP 401/403/404/409/412/422/429/500, falha de rede, revogação observada por 401, expiração e resposta tardia descartada, lista de outro projeto e vínculo divergente. |
| AC_04 | GETs sem idempotency key; sessão e vínculo com chave, reenvio sem edição preservado e nova intenção após edição/sucesso. CSRF de sessão no POST protegido. Problem Details com type/title/status/code/detail/instance, redaction de senha e status HTTP preservado mesmo se JSON/Problem for inválido. Nenhuma garantia backend simulada pela aplicação. |

## Contratos e limites reais

Operações consumidas: `post_auth_session` (202), `get_authorization_check` (200),
`get_projects_projectid_members` (200), `post_projects_projectid_members` (201).
Fontes: OpenAPI vigente, operation docs e freeze/resource-authorization de BC-002.
ADRs técnicas consultadas: 010, 011, 014, 016, 028, 031 e 055; ADR-051, citada pela
história, não altera o boundary desta entrega. Governança atual prevalece sobre
gates administrativos históricos. Owner técnico/encaminhamento: BC-002 e CODEOWNERS
`@raphaelperrut`.

Os contratos não publicam concessão de artefato/caminho, campo de path na consulta,
edição/remoção de membership nem paginação de membros por cursor. A UI informa os
limites e permite consultar os parâmetros HTTP existentes; nunca cria uma regra
alternativa, ticket, seletor de path, endpoint ou framework de administração.
Testes de valores de resourceType ilustram transporte e tratamento de negativas
controladas, sem afirmar que tais valores são reconhecidos pelo runtime HTTP.
Erros de validação reais continuam observáveis. Não há import de código backend.

UI e Chromium usam respostas HTTP controladas sobre o cliente gerado real.
Não foi executado novo fluxo contra PostgreSQL ou API de produção; auditoria,
deduplicação persistida, autorização por recurso, path seguro, hashes e lineage
continuam nos produtores existentes, com evidência integrada. O adapter HTTP de
desenvolvimento pode rejeitar tipos não suportados; essa rejeição não é convertida
em sucesso nem corrigida nesta tarefa frontend.

Banco: NOT_APPLICABLE; migration_required=false. Nenhuma migration ou alteração
persistente de aplicação foi criada. Rollback: remover o novo componente/página e
seus testes; não há estado remoto novo a desfazer.

## Validação

- 28 testes da feature e 42 regressões diretas da superfície de identidade: PASS,
  zero skips/falhas; `frontend-tests.xml` e `frontend-tests.log`.
- `test_epic_010_superficie`: PASS, identificado nominalmente no JUnit.
- Chromium sobre build próprio: 1 PASS; `browser-tests.log`. Screenshot em cache.
- TypeScript final: PASS (`typecheck.log`). Build da feature: PASS.
- OpenAPI check/diff contra baseline: PASS. Verificação de escopo e diff: PASS.
- `make verify PYTHON=.venv/Scripts/python.exe PNPM=pnpm.cmd OPENAPI_BASE_SHA=$BASELINE_SHA`:
  FAIL, exit 2, quatro falhas preexistentes na stack nativa (15 casos passaram).
  Qualidade Python, frontend-quality e validadores técnicos anteriores passaram.
  `integration-tests` não foi alcançado. `native-gate-diagnosis.json` demonstra que
  os seis arquivos relevantes são idênticos ao baseline após normalização CRLF/LF;
  os raw digests do checkout divergem. Nenhum deles foi alterado pela #124.
- Primeira tentativa do Chromium foi bloqueada pelo socket do sandbox; repetição
  com execução permitida em loopback passou. Primeira tentativa de make verify
  detectou screenshot sem registro de licença (`make-verify-initial.log`); a captura
  foi movida para cache local e o teste usa o output local do Playwright. Não se
  ampliou o escopo para mudar o catálogo de licenças.

Toolchain existente: Node 24.20.0/pnpm 10.26.1 em workdir/task-0786-toolchain;
Python `.venv/Scripts/python.exe`; Chromium em LOCALAPPDATA/ms-playwright.
Comandos de reprodução estão no README da feature e nos relatórios.

## Riscos residuais e próximo gate

READY_FOR_QA=YES para avaliação do candidato frontend, com limitação explícita do
gate global preexistente. BLOCKER_HIGH=NO no incremento; não há condição material
nova de parada. Isso não é aprovação, merge, liberação de produção ou gate global
verde. QA/Reviewer devem avaliar o mesmo candidato e o tratamento do gate nativo
fora desta issue. Nenhum PR foi aberto e nenhum serviço externo foi modificado.
Lista de arquivos, digests e verificações de escopo estão em `validation.json`.

Nota de representação: BASELINE_SHA corresponde ao baseline da issue declarado acima.
