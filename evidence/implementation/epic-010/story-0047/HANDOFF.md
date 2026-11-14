# ISSUE #123 / STORY-0047 / TASK-0047

Baseline: `0c7b85dfe6dbb041e64852280c393d00dbab05b9`.
Branch: `codex/issue-123-slice-consolidation`. Executor: Backend, BC-002.
O candidato é o commit que contém este handoff e os digests de validation.json;
obter seu SHA com `git rev-parse HEAD`. Nenhuma aprovação independente é declarada.

## Resultado e escopo

A consolidação reutiliza integralmente os dois slices integrados. O incremento
necessário é o teste de composição e a evidência de compatibilidade; não há mudança
de produção, contrato, migration, dependência ou responsabilidade de BC-002.
O adapter CPU do Slice 2 já delega ao builder do Slice 1. Criar outro wrapper
ou serviço de consolidação seria redundante.

Autorização administrativa:
https://github.com/raphaelperrut/DSGeorref/issues/123#issuecomment-6882299351.
Somente as duas listas allow_paths de TASK-0047 foram acrescidas dos três paths
autorizados. Os dois paths de produção, deny_paths, requisitos, ACs e dependências
permanecem iguais à baseline, verificação por comparação semântica registrada em
consolidation.json. O checkout foi sincronizado após a correção administrativa.
`src/frontend/debug.log` já existia e está excluído da entrega.

## Critérios de aceitação

| AC | Demonstração e estado |
|---|---|
| AC_01 | #159 e #160 fechadas como completed, merges #1059/#1060 na baseline. Commits 1e0625d e f5f5c46 são ancestrais; todos os outputs de produção/testes/evidência desses commits conferidos contra blobs da baseline em consolidation.json. Demonstrado para revisão. |
| AC_02 | Matriz canônica preservada: dez requisitos do Slice 1, REQ-HW-001 no Slice 2, interseção vazia e nenhum requisito próprio na consolidação. Teste de ownership e linhas canônicas em consolidation.json. Demonstrado para revisão. |
| AC_03 | Teste obrigatório instancia os builders original, default CPU e CPU explícito; todos retornam o mesmo tipo de serviço com a mesma IdentityTransactions. Compara DTOs, releitura de membership alterada no PostgreSQL, isolamento, negativa de artefato/caminho, revogação e 21 decisões duráveis. Regressões cobrem digests, falhas de autoridade/auditoria/elegibilidade e rejeição de modo sem fallback. Demonstrado para revisão. |
| AC_04 | Riscos, limites e condições de liberação abaixo. Handoff preparado; registro e liberação pelo Reviewer independente continuam PENDENTES. Não há autoaprovação nem liberação efetiva downstream. |

## Rastreabilidade e autoridade única

STORY-0716 mantém REQ-ACC-001 e REQ-AUTH-IMPL-001/002/003/004/005/006/008/009/010.
Os testes canônicos e sua evidência integrada são reutilizados, não reimplementados
nem repetidos nesta tarefa sem necessidade de compatibilidade. STORY-0717 mantém
REQ-HW-001. A cobertura do épico não é reduzida: REQ-AUTH-IMPL-007 permanece
na história explícita de calibração STORY-0762 e não é transferido aos slices.
Isso não declara calibração de produção concluída nem cobertura integral da release.

Contrato resource-authorization 1.0.0, política 1.1.0 e freeze de identidade
mantêm seus digests UTF8/LF pinados. O campo histórico runtime_implemented=false
do contrato é o snapshot de definição; a execução está nos outputs integrados.
PostgreSQL mantém identidade, grants e auditoria autoritativos. O modo CPU não
confere permissões. Artefatos e caminhos continuam sem grant na política 1.1.0;
BC-013 mantém publicação, manifest, resolução, hashes e lineage. Não há nova rota,
autoridade concorrente, cache de allow, regra duplicada ou import entre contexts.
ADR-051 foi consultada por referência da história: seu boundary IA/SGV não é
modificado nem usado para ampliar BC-002.

## Testes e reprodução

Python `.venv/Scripts/python.exe`, PYTHONPATH=src/backend,
PYTHONDONTWRITEBYTECODE=1, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1.
PostgreSQL 16.14 descartável em loopback 55495, criado em `.runtime/pg`;
base privada local_identity_validation e usuário auth_test, trust apenas local.
IDENTITY_TEST_DSN: `host=127.0.0.1 port=55495 dbname=local_identity_validation user=auth_test`.
IDENTITY_MIGRATION_DSN: `postgresql+psycopg://auth_test@127.0.0.1:55495/local_identity_validation`.
As fixtures aplicam somente migrations já integradas e truncam apenas essa base.

Comando: `python -X utf8 -m pytest -q -p no:cacheprovider --import-mode=importlib`
seguido de `tests/backend/identity_access/resource_authorization/test_consolidation.py`,
`test_hardware.py` e `test_resources.py` no mesmo diretório, com
`--basetemp evidence/implementation/epic-010/story-0047/.runtime/pytest`
e `--junitxml=evidence/implementation/epic-010/story-0047/tests.xml`.

Resultado: **23 passed, zero skips/falhas/erros** em tests.xml:
2 testes novos, 10 casos CPU e 11 casos de autorização de recursos.
`test_story_0047_slice_consolidation`: PASS.
Ruff check e format --check do arquivo novo: PASS. git diff --check: PASS.

`make verify PYTHON=.venv/Scripts/python.exe PNPM=pnpm.cmd`: **FAIL, exit 2**.
Toolchain local existente workdir/task-0786-toolchain: Node 24.20.0, pnpm 10.26.1;
PLAYWRIGHT_BROWSERS_PATH=C:/Users/DGEO2CGEO/AppData/Local/ms-playwright.
Qualidade Python, frontend completo e validadores técnicos passaram. O gate falha
em quatro testes da stack nativa (15 passed): digests raw CRLF divergem dos locks
e política LF. native-gate-diagnosis.json confirma que seis arquivos normalizados
são idênticos aos blobs da baseline. Falha ambiental preexistente já registrada
no Slice 2, sem correção fora do escopo. Target integration-tests não alcançado.

## Banco, riscos e próximo gate

Migration_required=false preservado. Não há mudança de schema, estado persistido,
backfill ou cutover. As únicas escritas novas são testes/evidência e a correção do
envelope. Rollback: reverter esse incremento; preservar schema e auditoria integrada.

Limites: port de existência de projeto e profile de segurança são sintéticos nos
testes; PostgreSQL, política, releitura e auditoria são reais. Não há claim sobre
BC-003/BC-013 reais, HTTP novo, GPU, desempenho, calibração, segurança de release
ou aptidão de produção. A cobertura normativa preservada não quita esses gates.

Handoff pronto para QA/Arquiteto/Reviewer no mesmo candidato. O Reviewer deve
registrar riscos e decidir a liberação da aresta STORY-0047 → STORY-0049, respeitando
também STORY-0048 → STORY-0049; STORY-0050 depende de STORY-0049. Nenhuma dessas
dependências foi alterada ou marcada como liberada pelo implementador. Exigir gate
global em checkout LF/CI e revisões independentes antes de merge/liberação.
Não há bloqueio material de implementação; há pendência explícita do gate global
e da decisão independente de AC_04. PR não aberto nesta execução.
