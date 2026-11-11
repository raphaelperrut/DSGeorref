# STORY-0045 / TASK-0045 — consolidação de QA do EPIC-009

Issue #121 / ISSUE-0155 · BC-002 · risk tier MEDIUM · 2026-11-11

Baseline funcional auditada `40dbd9dd1a9563c3177c4e05538dbe958cc8d28e`. Os resultados locais abaixo foram obtidos sobre essa árvore funcional com os dois testes de aceite deste diretório. O SHA definitivo que contém estes artefatos será identificado no PR, junto à reexecução dos testes no commit publicado e ao veredito sobre esse candidato. Uma aprovação independente continua pendente.

O levantamento inicial encontrou somente o worktree principal em `codex/issue-120-security`, HEAD `cfe4eb00b3c11c0e0174a49dbc87097ddb888759`, com `src/frontend/debug.log` untracked. Consultas GitHub e refs locais encontraram zero branches/PRs da #121. Esta entrega usa o worktree isolado `issue-121-epic-009-audit` e a branch `codex/issue-121-epic-009-audit`.

## Origem e integridade

Os SHAs de merge abaixo foram confirmados pelo GitHub e por `git merge-base --is-ancestor <merge> 40dbd9dd1a9563c3177c4e05538dbe958cc8d28e`, todos com exit 0. Cada candidato é o segundo pai de seu merge. Os checks exibidos nos PRs de origem terminaram SUCCESS.

| História | PR | Candidato integrado | Merge em main |
| --- | --- | --- | --- |
| STORY-0041 | [#1041](https://github.com/raphaelperrut/DSGeorref/pull/1041) | 8d7396421d225c7ec156e8f7c33f111118130bda | f33429b91194177aad3cbd75c3966b1a8c58ea09 |
| STORY-0714 | [#1042](https://github.com/raphaelperrut/DSGeorref/pull/1042) | bec6c76a20d32f0372bb67eeff7d772f4292c551 | 440df33913dfa74105d4ab69e0692c9b2c5c1d2f |
| STORY-0715 | [#1052](https://github.com/raphaelperrut/DSGeorref/pull/1052) | 19029f4df2dc54c734f335d1513fee65fa64f72b | f8f7451897b2963a1b6d9e571873cec6cd3d51cb |
| STORY-0042 | [#1053](https://github.com/raphaelperrut/DSGeorref/pull/1053) | 827504e67d73a1ca9fd77a026efe20870f07b3cf | 1d8d130480e390a1ae164740f06f8b995bc011a1 |
| STORY-0043, boundary logout | [#1054](https://github.com/raphaelperrut/DSGeorref/pull/1054) | 0b62669853f2069444af7ac65060b090f74cb1d2 | ed3821c2be6a16e7b8fdb9a8bd6ffa85bf880153 |
| STORY-0043, desenvolvimento | [#1055](https://github.com/raphaelperrut/DSGeorref/pull/1055) | d6f6e0f95da1fee3948454bec4065101421ed8fc | 64dc605697d29e557df282bd8711a607b12a329a |
| STORY-0044 | [#1056](https://github.com/raphaelperrut/DSGeorref/pull/1056) | cfe4eb00b3c11c0e0174a49dbc87097ddb888759 | 40dbd9dd1a9563c3177c4e05538dbe958cc8d28e |

A política de usuários e papéis tem versão 1.1.0. Complementa o freeze de autenticação, cujo `contract_version` é 1.0.0. `git diff --exit-code f33429b 40dbd9d -- contracts/contexts/identity_access/plt` retornou 0. Os testes de conformidade e os testes HTTP/runtime usam esses contratos integrados. A factory de produção publica logout. A superfície ampliada de desenvolvimento exige configuração explícita e loopback.

A CI pós-merge da baseline executou `make verify`, 86 testes de identidade/HTTP/segurança e a consolidação STORY-0042 em separado, todos com sucesso. Inclui os 27 casos da STORY-0044. Sua revisão COMMENTED registra QA e Reviewer em duas passagens solo e o finding LOW de credenciais ambíguas descrito adiante. Essa revisão permanece vinculada a cfe4eb0. [Run da baseline](https://github.com/raphaelperrut/DSGeorref/actions/runs/42933658707)

## Critérios da #121

| Critério | Avaliação desta consolidação | Evidência |
| --- | --- | --- |
| AC-ISSUE-0155-01 | PASS, desenvolvimento | Happy path executa HTTP real, decisão por papel/projeto, bootstrap, sessão, PAT, OIDC e PostgreSQL. Quatro casos canônicos exercitam owner/editor/reviewer/viewer. |
| AC-ISSUE-0155-02 | PASS com lacunas históricas explícitas | Matriz dos 12 requisitos abaixo, SHAs de origem e classificação das obrigações históricas. A cobertura integral do pacote histórico permanece sem demonstração. |
| AC-ISSUE-0155-03 | PASS | Dez casos selecionados de rejeição, isolamento, revogação, autoridade ausente, IdP indisponível, throttle persistido e rollback de escrita. Zero skips. |
| AC-ISSUE-0155-04 | PENDING_REVIEW | QA executável, relatório e revisão final devem usar o SHA definitivo publicado no PR. A avaliação independente do candidato da #121 ainda precisa ocorrer. Para o relatório binário de fechamento, FAIL enquanto pendente. |

Veredito desta auditoria sobre a baseline funcional acima é tecnicamente apta à revisão da entrega de desenvolvimento. Nenhum BLOCKER/HIGH funcional foi demonstrado. O encerramento do aceite e a decisão humana de integração dependem da revisão do candidato final. O EPIC-009 conserva limites de produção e de comprovação histórica.

## Requisitos atuais

Prefixo I significa `tests/backend/identity_access/local_identity/`. Prefixo S significa `tests/security/contexts/identity_access/usuarios-e-papeis-da-instancia/test_instance_security.py`. Prefixo A significa `src/backend/dsgeorref/contexts/identity_access/adapters/usuarios-e-papeis-da-instancia/acc-auth-impl-parte-1/tests/`. Os seletores exatos dos 16 casos estão em `test_acceptance.py`.

| Requisito | Evidência identificável | Classificação e limite |
| --- | --- | --- |
| REQ-ACC-001 | A/test_canonical.py::test_role_project_operation_access, quatro papéis, S happy path e negativas de escalada/projeto/autoridade | Demonstrado em desenvolvimento com existência de projeto fornecida por fixture. |
| REQ-AUTH-IMPL-001 | I/test_requirements.py::test_req_auth_impl_001, logout HTTP e negativa de sessão revogada | Demonstrado em PostgreSQL. |
| REQ-AUTH-IMPL-002 | I/test_requirements.py::test_req_auth_impl_002 | Demonstrado com profile Argon2id sintético. Calibração BP-003/AP-003 de produção permanece na #816. |
| REQ-AUTH-IMPL-003 | I/test_requirements.py::test_req_auth_impl_003 e S invalid-csrf | Demonstrado, proveniência/CSRF e rejeição de credenciais ambíguas. Limite LOW específico abaixo. |
| REQ-AUTH-IMPL-004 | I/test_requirements.py::test_req_auth_impl_004, S happy path e PAT revogado | Demonstrado, escopo/projeto/hash-only/revogação. |
| REQ-AUTH-IMPL-005 | I/test_requirements.py::test_req_auth_impl_005 e I/test_development_surface.py::test_oidc_callback_uses_browser_bound_transaction | Demonstrado, JWT assinado e transação vinculada ao navegador. Provedor externo é fixture. |
| REQ-AUTH-IMPL-006 | I/test_requirements.py::test_req_auth_impl_006 e quatro papéis de A/test_canonical.py | Demonstrado, política central e concessões vigentes. |
| REQ-AUTH-IMPL-007 | test_req_auth_impl_007 nos dois packages contratuais e S::test_epic_009_seguranca_negative_paths_abuse | Contrato demonstrado. Evidência runtime atual identificável demonstra bucket, failure_count, estado limited, decisão persistida, correlação de auditoria e negação 429 entre instâncias da aplicação. A ausência no relatório STORY-0712 permanece lacuna histórica. |
| REQ-AUTH-IMPL-008 | I/test_requirements.py::test_req_auth_impl_008, logout HTTP e S sessão revogada | Demonstrado, ciclo/rotação/revogação. |
| REQ-AUTH-IMPL-009 | I/test_requirements.py::test_req_auth_impl_009 e I/test_identity_requirements.py::test_bootstrap_session_token_recovery | Demonstrado com decisão do operador/custódia sintéticas e cerimônia offline. |
| REQ-AUTH-IMPL-010 | I/test_requirements.py::test_req_auth_impl_0010 e S happy path | Demonstrado, cookies/headers/proveniência. O nome canônico histórico usa 0010. |
| REQ-ID-002 | I/test_identity_requirements.py::test_bootstrap_session_token_recovery, S happy path/abuse e A/test_slice_consolidation.py::test_story_0042_slice_consolidation | Demonstrado, bootstrap único, sessão/PAT e recuperação. |

A matriz canônica `ACCEPTANCE_CRITERION_TRACEABILITY.csv`, AC-ISSUE-0824-01, atribui dez requisitos à STORY-0714, excluindo 007. AC-ISSUE-0825-01 atribui REQ-ID-002 à STORY-0715. A linha da STORY-0712 qualifica 007 como PASS_STRUCTURAL_ONLY, com runtime histórico NOT_IMPLEMENTED_FINAL e benchmark NOT_EXECUTED. A lista de requisitos do EPIC-009 também inclui 007, por isso esta auditoria combina seu contrato com a evidência runtime posterior da STORY-0043/#1055 e STORY-0044/#1056. O resultado atual preserva a classificação histórica e o gate de produção.

## Obrigações históricas

Foram inspecionados os handoffs integrados, AC04-RECONSTRUCTION-v1.md, CONTRACT.md e HANDOFF.md da STORY-0041, as matrizes canônicas, o relatório e JUnit da STORY-0712 referenciados por seu teste de consolidação, e os atos Owner da #117. `git ls-files` também confirmou ausência dos três nomes originais na árvore auditada. A reconstrução parcial aprovada declara que os originais permaneceram ausentes após busca histórica anterior.

O ato 6098913884 distribui responsabilidades, preserva 36 obrigações, 20 vínculos G2 Access, dois vínculos Identity e oito testes pendentes. O ato 6099017507 fixa três digests originais. O ato 6709165678 aprova a reconstrução parcial e mantém a reconciliação individual pendente. [Ato de responsabilidade](https://github.com/raphaelperrut/DSGeorref/issues/117#issuecomment-6098913884) · [Identidade original](https://github.com/raphaelperrut/DSGeorref/issues/117#issuecomment-6099017507) · [Aceite parcial](https://github.com/raphaelperrut/DSGeorref/issues/117#issuecomment-6709165678)

| Obrigação recuperável | Situação verificada |
| --- | --- |
| Política versionada, papéis, permissões, transições, exceções e erros | Demonstrada pelo package policy 1.1.0, CONTRACT.md, freeze e 320 testes contratuais executados. |
| Throttling com estado e evidência observável | Demonstrado em desenvolvimento pelo teste S abuse, que consulta buckets/decisões/observações em PostgreSQL após recriar a aplicação. O escopo da correspondência é este comportamento recuperável. |
| Identidade administrativa | Demonstrada pelo teste canônico de REQ-ID-002 e integração STORY-0042 executados. |
| Integração, superfície e segurança | Demonstradas pelos testes atuais selecionados e pelo run integrado da baseline com 86 + 1 passes. |
| Verificação final | Dois testes obrigatórios criados e executados neste diretório. Revisão final do candidato permanece pendente. |
| Identidade dos três originais e 36 obrigações individuais | Lacuna histórica preexistente. Conteúdo/IDs individuais indisponíveis impedem correspondência técnica completa e reprodução dos digests. NÃO DEMONSTRADA a cobertura de 36/36. |
| 20 vínculos G2 Access | Lacuna histórica preexistente. Contagem recuperada do ato, destinos individuais ausentes. 0/20 vínculos individuais reconciliados por esta auditoria. |
| Dois vínculos Identity | Lacuna histórica preexistente. Destinos individuais ausentes. 0/2 reconciliados por esta auditoria. |
| Oito testes históricos | Lacuna histórica preexistente. Nomes/asserções originais ausentes. 0/8 correspondências individuais demonstradas. Os testes atuais têm identidade própria. |
| Produção BP-003/AP-003 e autoridade operacional BC-003 | Não aplicáveis ao aceite de desenvolvimento solicitado. Permanecem com os responsáveis existentes e seus gates próprios. |
| Path traversal no HTTP de projetos | Não aplicável. A superfície usa UUID e não resolve paths de filesystem fornecidos pelo cliente. |

Os grupos recuperáveis acima têm evidência equivalente identificável quanto aos comportamentos expressos na reconstrução parcial. A ausência da matriz original impede atribuir esses grupos a itens específicos das 36 obrigações ou aos vínculos/testes contados. A auditoria registra cobertura dos requisitos atuais, sem afirmar equivalência histórica integral.

A ausência de REQ-AUTH-IMPL-007 no VALIDATION-REPORT.json da STORY-0712 foi reproduzida com `test_story_0037_slice_consolidation`, FAIL/KeyError antes do fluxo de identidade. O relatório tem último commit `85225ba9b698259c8a36620c194494268c5e7910`. A STORY-0042 e a verificação atual do throttling passam. O efeito sobre esta história é uma limitação de rastreabilidade histórica. A evidência runtime atual permite o aceite de desenvolvimento de 007 nos limites acima. Recuperar os três originais e verificar seus digests é a menor ação para completar a reconciliação individual histórica.

## Execução e reprodução

CPython 3.12.10 da venv existente, pytest 9.1.1, PostgreSQL 18.4 em container descartável `dsgeorref-issue-121-pg`, porta loopback 55482 e base `local_identity_validation`. Configure `PYTHONPATH=src/backend` e instale as dependências de `src/backend/dsgeorref/contexts/identity_access/adapters/local_identity/requirements.txt` conforme o workflow integrado. Configure IDENTITY_TEST_DSN e IDENTITY_MIGRATION_DSN para a mesma base privada descartável. A fixture valida o nome e trunca suas tabelas. Execute em série.

| Comando executado | Resultado real |
| --- | --- |
| `python -m pytest -s -q -p no:cacheprovider evidence/reviews/usuarios-e-papeis-da-instancia/test_acceptance.py` | PASS, 2 testes externos em 17.00s. Happy 6/6 em 4.29s. Negative 10/10 em 9.76s. Zero skips/falhas/erros nos relatórios JUnit internos. |
| `python -m pytest -q -p no:cacheprovider contracts/contexts/identity_access/plt/usuarios-e-papeis-da-instancia contracts/contexts/identity_access/plt/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter` | PASS, 320 em 2.56s. |
| `python -m pytest -q -p no:cacheprovider --import-mode=importlib I/test_requirements.py I/test_identity_requirements.py::test_bootstrap_session_token_recovery I/test_http.py::test_logout_revokes_once_and_clears_cookie A/test_slice_consolidation.py::test_story_0042_slice_consolidation` | PASS, 13 em 15.03s. Expandir I e A conforme os prefixos acima. |
| `python -m pytest -q -p no:cacheprovider I/test_slice_consolidation.py::test_story_0037_slice_consolidation --tb=short` | FAIL, KeyError REQ-AUTH-IMPL-007, 0.37s. |
| Tentativa anterior do mesmo teste com `--import-mode=importlib` | Erro de coleta por import legado de conftest. A reexecução no modo próprio acima demonstrou o KeyError. |
| `make verify`, venv Python no PATH, OPENAPI_BASE_SHA=40dbd9d | FAIL de ambiente em frontend openapi:check. Ruff, mypy e arquitetura Python passaram. Node 24.22.1/pnpm 11.25.0 disponíveis divergem dos pins 24.20.0/10.26.1. |
| `python -m ruff check --no-cache evidence/reviews/usuarios-e-papeis-da-instancia/test_acceptance.py` | PASS. |
| `python -m ruff format --check --no-cache evidence/reviews/usuarios-e-papeis-da-instancia/test_acceptance.py` | PASS. |
| `git diff --check` | PASS. A conferência staged e a conferência do commit serão registradas no PR. |

O helper executa os seletores existentes em subprocesso e exige exit 0, contagem exata e zero skips/erros/falhas em JUnit. A descoberta padrão começa em tests/, por isso o diretório desta história precisa ser informado explicitamente. O CI vigente executa os 27 casos de segurança, o callback OIDC de desenvolvimento e a consolidação STORY-0042. Os quatro casos canônicos de papel também foram executados localmente nesta auditoria. O resultado dos wrappers no SHA definitivo será registrado no PR. Os checks obrigatórios do ruleset main 19942009 são `verify-foundation` e `verify-technical-security`, estritos, com resolução de conversas. A situação final será consultada após abrir o PR.

## Riscos e handoff

| Impacto | Risco/limitação | Destino |
| --- | --- | --- |
| MEDIUM, rastreabilidade | Pacote original ausente impede comprovação individual 36/20/2/8 e seus digests. | Consolidação histórica explicitada acima. Owner recebe o limite para sua decisão sobre desenvolvimento. |
| MEDIUM, produção | Profiles quantitativos e autoridade operacional de projetos ainda dependem de homologação/integração. | #816/BP-003/AP-003 e BC-003, responsáveis existentes. |
| MEDIUM, rollback operacional | Binário anterior à reserva durável de tentativa OIDC pode reabrir replay de estados pending. | Procedimento do #1042 deve preservar mitigação ou drenar/inutilizar transações antes do rollback. |
| LOW, teste | Caso de credenciais ambíguas da STORY-0044 combina sessão válida com PAT inexistente, limitando seu poder de discriminar precedência Bearer. | Finding histórico do #1056 preservado. O parser integrado rejeita ambiguidade. |
| LOW, ambiente | Fixtures de existência de projeto, custódia, decisão do operador e transporte IdP, banco compartilhado serial e limites quantitativos sintéticos. | Evidência de desenvolvimento delimitada. Não usar execução paralela na mesma base. |
| LOW, execução local | Node/pnpm fora dos pins impedem make verify local completo. | CI do candidato com toolchain de referência. |

Escrita limitada a dois arquivos deste diretório, `REVIEW.md` e `test_acceptance.py`. A divergência entre `evidence/reviews/epic-009/story-0045/` citado no TaskEnvelope e seu allow_paths foi resolvida usando o allow_paths efetivo autorizado. Contratos e schema têm impacto NONE. Migrations NOT_APPLICABLE. Reversão desta entrega remove somente seus artefatos de revisão pelo revert do commit.

QA executável PASS sobre a baseline funcional identificada. REVIEWER_VERDICT = READY_FOR_INDEPENDENT_REVIEW, com a revisão final vinculada ao SHA definitivo no PR. AC-04 permanece pendente até essa avaliação. Nenhum agente aprova o próprio trabalho. A governança vigente após #1047 usa issue, PR, evidência, checks técnicos e revisão proporcional ao risco. Autoridade de merge permanece com o Owner.
