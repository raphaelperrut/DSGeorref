# ISSUE #160 / TASK-0717 — Slice 2/2

Baseline: `bd90ec86a418254f9b4b55e3b4c78c1e7382ed51` (integra #159).
Branch: `codex/issue-160-hardware-baseline`. Owner: BC-002; executor: Backend.
Autorização do Owner conferida: https://github.com/raphaelperrut/DSGeorref/issues/160#issuecomment-6881890153.

## Escopo e decisão local

O envelope preserva os dois allow_paths de produção e replica nas duas listas somente
as três adições autorizadas. Requisitos, ACs, dependências, deny_paths e flags de banco
permanecem intactos. O arquivo local preexistente `src/frontend/debug.log` é excluído.
Nenhum package de produção contém identificador de ticket. O único módulo novo fica
no adapter autorizado; não há necessidade de duplicar regras na application.

A composição interna `hw-parte-2/runtime.py::build_authorization` aceita somente
`execution_mode="cpu"` (também o default). Delega integralmente ao builder integrado
do Slice 1/2, que valida contrato/digests e reutiliza ResourceAuthorization,
IdentityTransactions, grants, credenciais, memberships e auditoria PostgreSQL.
Não há backend alternativo, seleção automática, capability probe, driver, download,
dependência GPU, framework ou abstração de aceleração.

A política congelada e o contrato deste contexto não declaram uma implementação
acelerada. REQ-HW-001 e `contracts/operations/cost-model.yaml#/gpu_gate` estabelecem CPU
como baseline e aceleração como opcional e governada. Assim GPU, CUDA, auto, valor
inválido ou modo desconhecido falham explicitamente com o erro existente
`Denied("validation_failed")`, antes de importar/compor CPU. Este parâmetro é interno:
nenhuma rota, DTO, permissão, status HTTP ou contrato público foi alterado. Uma futura
implementação acelerada exige sua própria declaração, autorização e evidência; este
slice não a fornece. O modo de execução nunca confere autorização de recurso.

## Banco e rollback

Classificação concreta: banco APPLICABLE por reutilização; **migration_required=false**
para a mudança entregue. O flag histórico true do TaskEnvelope permanece inalterado.
Inspecionados `adapters/local_identity/migrations/schema.sql` e versões integradas:
accounts, sessions, tokens, memberships/revision, requests e observations já atendem
às decisões e à auditoria. Não há nova entidade, coluna, constraint, índice, operação
persistida, enum de estado ou formato de observação. A opção CPU é configuração da
composição, não estado autoritativo novo. Nenhuma migration artificial foi criada.
O teste usa as migrations existentes em PostgreSQL 16 descartável e verifica as
12 decisões persistidas, outcomes COMMITTED/DENIED e policy 1.1.0 sem secret.

Rollback é de código: voltar à composição integrada do Slice 1/2 ou reverter este
adapter. A equivalência entre o serviço antigo, o default e CPU explícito é testada.
Não há downgrade de schema, backfill, cutover ou irreversibilidade nova. Preservar
as observações append-only existentes; nunca apagar auditoria para reverter código.
Reversão operacional deve ser explícita, nunca fallback em resposta a erro de modo.

## Critérios e testes

| Critério | Evidência |
|---|---|
| AC-ISSUE-0827-01 | test_cpu_baseline_gpu_optional_no_silent_fallback; hardware-tests-local.xml |
| AC-ISSUE-0827-02 | validação do envelope e lista/hash dos arquivos em validation.json |
| AC-ISSUE-0827-03 | modos não suportados, contrato ausente, revogação, elegibilidade e banco indisponível; regressões de recursos |
| AC-ISSUE-0827-04 | contratos, classificação de banco, rollback e riscos neste handoff |

`test_hardware.py`: 10 casos PASS, incluindo o teste canônico obrigatório.
A execução compara decisões de conta/projeto/artefato com o serviço integrado,
bloqueia imports de bibliotecas GPU, verifica persistência e revoga credencial.
Oito modos inválidos/não suportados comprovam que a composição CPU não é alcançada.
Contrato, elegibilidade e autoridade indisponíveis continuam falhando sem fallback.
`test_resources.py`: 11 regressões diretamente afetadas PASS; grants por quatro
papéis, isolamento, recurso ausente, política/revisão/credencial corrente,
contrato/digest, auditoria obrigatória e indisponibilidade de autoridade.
Ruff dos dois arquivos novos e `git diff --check`: PASS.

Comando dos testes: `.venv/Scripts/python.exe -X utf8 -m pytest -q -p no:cacheprovider
--import-mode=importlib <test_hardware.py ou test_resources.py> --junitxml=<XML>`.
Ambiente: `PYTHONPATH=src/backend`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`IDENTITY_TEST_DSN=host=127.0.0.1 port=55494 dbname=local_identity_validation user=auth_test`,
`IDENTITY_MIGRATION_DSN=postgresql+psycopg://auth_test@127.0.0.1:55494/local_identity_validation`.
Instância isolada criada para esta execução; não foram usados bancos de produção.
A tentativa restrita (`hardware-tests.xml`) teve 8 PASS e 2 erros de setup por TCP
bloqueado pelo sandbox. A reexecução local autorizada passou todos os 10 casos,
sem alterar assertions, fixtures ou implementação.

## Gate e handoff

Make verify: **FAIL (exit 2), causa ambiental preexistente de CRLF no checkout**.
Python quality, frontend completo, validadores técnicos e os testes anteriores à
stack nativa passaram. Quatro testes de `tests/infra/native_stack/test_native_stack.py`
falharam porque calculam SHA-256 sobre bytes locais CRLF de locks/policy congelados;
15 testes desse arquivo passaram. O target integration-tests não foi alcançado.
`native-gate-diagnosis.json` compara seis arquivos com os blobs do BASELINE_SHA:
os bytes normalizados LF são exatamente os blobs e os digests exigidos; nenhum
arquivo da stack nativa ou teste foi alterado. Corrigir esses paths está fora do
slice autorizado. O gate integral verde permanece pendente em checkout LF/CI;
isto não é declarado como PASS nem como falha do comportamento CPU entregue.
Resultados e logs finais em validation.json e make-verify-local.log.
A tentativa inicial usou Node 24.22.1 incompatível; a seguinte usou Node 24.20.0 e
pnpm 10.26.1 exigidos e encontrou Chromium fora do path do sandbox. A execução local
usa a mesma toolchain e `PLAYWRIGHT_BROWSERS_PATH` explícito para Chromium já instalado.
Os logs preservam todas as tentativas; nenhum check foi enfraquecido.
XML/logs foram normalizados para UTF8/LF sem espaços finais; resultados e
diagnósticos foram preservados. Nenhum código ou assertion mudou após os testes.

Limites: a evidência demonstra somente CPU e fail-closed de modos neste contexto;
não comprova GPU, equivalência científica de aceleração, custo, escala, SLA ou
conformidade de toda release/BC-014. Projeto usa o port sintético já existente nos
testes; persistência, política e auditoria BC-002 são reais. O wiring HTTP permanece
no contrato integrado; a nova opção pertence somente à composição interna.

O candidato é o commit contendo este handoff, os bytes cobertos pelos digests de
validation.json e os resultados XML. SHA informado no retorno ao Owner; este arquivo
não contém autorreferência de hash. QA/Reviewer devem revisar esse mesmo candidato;
nenhuma aprovação independente é declarada pelo implementador. Pronto para avaliação
QA do slice, com pendência explícita do gate global em ambiente LF. Não está aprovado
para merge/release enquanto gate e revisões independentes não forem concluídos.
PR não aberto. PostgreSQL descartável encerrado após os testes.
