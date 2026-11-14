# ISSUE #125 / STORY-0049 / TASK-0049

Papel: Security. BC-002. Branch: `codex/issue-125-security`.
Baseline: `bb2b2795ec414a7656c3f93aee32085f96b953bf`.
O candidato é o commit que contém este handoff e os digests LF de validation.json.
Resolver com `git log -1 --format=%H -- evidence/security/epic-010/story-0049/HANDOFF.md`.
QA e Reviewer independentes permanecem pendentes no mesmo candidato.

## Resultado e escopo

O incremento contém exclusivamente testes adversariais do builder e serviço central
já integrados, evidências e a correção administrativa do envelope. Criar adapter
novo duplicaria uma composição existente. Não há código de produção novo,
autorização paralela, cache de allow, endpoint, contrato ou expansão do BC-002.
Owner técnico: BC-002; CODEOWNERS encaminha a revisão a @raphaelperrut.

Autorização do Owner consultada:
https://github.com/raphaelperrut/DSGeorref/issues/125#issuecomment-6884641931.
Somente allow_paths e phase_f_review.files.allow_paths receberam os dois paths
autorizados. Os dois paths anteriores e todos os demais campos foram preservados;
record_evidence.py verifica igualdade semântica com a baseline. A correção foi feita
antes do fetch/switch. O arquivo preexistente src/frontend/debug.log fica excluído.

#123 e #124 estão fechadas como completed no GitHub e seus merges #1061 e #1062
estão na baseline. validation.json comprova ancestralidade e igualdade de todos os
outputs dos commits de implementação com os blobs da baseline. Não foi alterada
nenhuma dependência ou atribuição de requisito.

## Critérios e controles derivados

| Critério | Evidência executável |
|---|---|
| AC_01 | test_epic_010_seguranca_happy_path verifica builder integrado, mesma IdentityTransactions, DTO exato, ator/alvo/policy/correlação e decisão durável no PostgreSQL. |
| AC_02 | Esta matriz, nomes dos testes e digests LF em validation.json vinculam explicitamente os controles ao conteúdo do candidato. A história é DERIVED_CONTROL, sem requisito exclusivo. |
| AC_03 | Negativas exatas, ação desconhecida, tipo ausente/inesperado, existência de projeto com respostas inválidas, elegibilidade não True, membership/conta/credencial/policy alteradas; regressões incluem contrato ausente/drift, auditoria obrigatória e banco indisponível. Nunca retornam allow como fallback. |
| AC_04 | Matriz de aplicabilidade abaixo; somente superfícies já existentes são exercitadas. |

| Controle | Classificação | Demonstração e limite |
|---|---|---|
| Abuso | APPLICABLE + TESTED | test_abuse_eligibility_is_conjunctive: False, None, string e inteiro não habilitam consulta; rate_limited e auditoria DENIED. REQ-AUTH-IMPL-007 somente no ponto de composição; calibração/limiares são de STORY-0762, sem claim de produção. |
| Autorização | APPLICABLE + TESTED | Obrigatórios, previous_allow e query_permission: isolamento de projeto e conta, menor privilégio, PAT sem ampliação de scope, releitura de membership, conta inativa, credencial expirada/revogada e policy divergente. ADR-030, REQ-ACC-001 e REQ-AUTH-IMPL-001/004/006/008. |
| Secrets | APPLICABLE + TESTED | persisted_secret_minimization verifica hash da sessão e ausência de credencial, CSRF, recovery e hashes em saída/auditoria; credencial inválida é rejeitada. ADR-032, REQ-LOG-001 no boundary de observação. Nenhum segredo real é utilizado ou publicado. |
| Path/egress | APPLICABLE + TESTED | Caminhos e URL como resource_id, artifact/artifact_path/physical_path não recebem grant. O DTO não ecoa inputs. Rejeição central conforme contrato, sem resolução de filesystem. Egress externo/SSRF: NOT_APPLICABLE, este fluxo não possui cliente HTTP/URL fetch ou port de saída externo. PostgreSQL local é a autoridade interna. |
| Redaction | APPLICABLE + TESTED | persisted_secret_minimization e mandatory_negative verificam allowlist exata de colunas de auditoria, códigos limitados e ausência de inputs sensíveis em auditoria, exceção e saída capturada. ADR-055. Não se afirma implementação de support bundle/ledger BC-014. |

ADR-031: elegibilidade no boundary é aplicável e testada. CSRF, CORS, cookies,
headers e exposição TLS não são alterados nem reimplementados: API e frontend
são NOT_APPLICABLE nesta entrega. Nenhuma afirmação nova sobre proteção HTTP.
ADR-032: ingress, rotação externa e TLS de deployment são NOT_APPLICABLE;
não há rede publicada ou credencial de implantação nova.
REQ-AUTH-IMPL-002/003/005/009/010 e REQ-HW-001 mantêm os produtores e evidências
integrados de STORY-0716/0717/0047/0048; não são certificados novamente aqui.
Preservados contratos resource-authorization 1.0.0, policy 1.1.0 e freeze existente.
O campo histórico runtime_implemented=false é snapshot de definição, conforme
handoff integrado da #123; o teste executa a capacidade já implementada.

Artefatos não têm grant na policy 1.1.0, para qualquer role. Publicação, hashes,
lineage, ownership de manifest e resolução segura continuam sob BC-013/SPEC-005.
Não se inventou leitura de path, ameaça de downloader ou política de egress nova.
Nenhum custo, escala, latência, RPO/RTO, conformidade LGPD ou gate de release é
declarado; não há dependência externa, estado de produto ou deployment alterado.

## Validação e reprodução

38 casos passaram, zero falhas/erros/skips: 27 novos e 11 regressões diretamente
relacionadas em test_resources.py. Ambos os testes obrigatórios estão nomeados
no JUnit security-tests.xml; negative_paths possui 10 cenários. Ruff check,
format --check e git diff --check passaram nos arquivos de testes.

Python: `.venv/Scripts/python.exe`, PYTHONPATH=src/backend,
PYTHONDONTWRITEBYTECODE=1, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1.
PostgreSQL 16.14 descartável em loopback 55496, .runtime/pg-ready, usuário auth_test,
base local_identity_validation, autenticação trust somente nesse loopback local.
IDENTITY_TEST_DSN: `host=127.0.0.1 port=55496 dbname=local_identity_validation user=auth_test`.
IDENTITY_MIGRATION_DSN: `postgresql+psycopg://auth_test@127.0.0.1:55496/local_identity_validation`.
As fixtures reutilizam apenas migrations integradas na base privada e fazem sua
limpeza; não há mudança de banco da aplicação ou migration nova.

Comando: `python -X utf8 -m pytest -q -p no:cacheprovider --import-mode=importlib`
com `tests/security/contexts/identity_access/autorizacao-por-projeto-operacao-artefato-e-caminho`
e `tests/backend/identity_access/resource_authorization/test_resources.py`,
`--basetemp evidence/security/epic-010/story-0049/.runtime/pytest-final`
e `--junitxml=evidence/security/epic-010/story-0049/security-tests.xml`.
O profile e ports de projeto/elegibilidade são sintéticos; persistência, política,
credenciais e auditoria são reais. Expiração avança o relógio do store por fixture;
não modifica o prazo imutável de uma credencial. Nada serializa os tokens gerados.
A primeira tentativa foi bloqueada pelo socket do sandbox; repetição autorizada
passou. Duas preparações iniciais de teste infringiam a imutabilidade/revisão de
credencial; foram corrigidas sem enfraquecer os invariantes ou assertions.

`make verify PYTHON=.venv/Scripts/python.exe PNPM=pnpm.cmd OPENAPI_BASE_SHA=$BASELINE_SHA`:
FAIL, exit 2. Qualidade Python, frontend-quality e validadores técnicos anteriores
passaram. Quatro falhas na stack nativa, 15 casos passaram, por digests raw CRLF
divergentes dos locks LF. validation.json compara os seis arquivos envolvidos com
os blobs da baseline: idênticos após normalização. É falha ambiental preexistente,
já registrada nas dependências, sem alteração fora de escopo. integration-tests
não foi alcançado. O target frontend faz parte do gate obrigatório global.
Toolchain existente: Node 24.20.0/pnpm 10.26.1 em workdir/task-0786-toolchain;
Chromium LOCALAPPDATA/ms-playwright.

Gitleaks local 8.24.3 usa .github/gitleaks.toml com defaults e redaction, sem
exceção nova ou supressão. Relatórios locais gitleaks.json/gitleaks.log registram
a varredura dos arquivos desta entrega. Digests novos são scanner-safe desde a
geração: sha256 seguido de oito grupos hex separados por dois-pontos, reversível
removendo o prefixo e separadores; jamais usado como credencial.

## Handoff e riscos residuais

database=NOT_APPLICABLE; migration_required=false; API=NOT_APPLICABLE;
frontend=NOT_APPLICABLE. Backend domain e contratos não mudaram.
Rollback: reverter testes/evidência/correção administrativa, sem backfill ou cutover.
Evidências são do executor, não aprovação de QA/Reviewer. READY_FOR_QA=YES para
avaliação do mesmo candidato com a limitação do gate global explicitada.
BLOCKER_HIGH=NO no incremento; STOP_CONDITION=NONE. Gate global verde e aprovação
independente continuam necessários antes de integração. Nenhum PR foi aberto.
