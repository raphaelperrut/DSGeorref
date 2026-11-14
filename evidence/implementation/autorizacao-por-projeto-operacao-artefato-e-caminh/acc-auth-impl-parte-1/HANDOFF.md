# STORY-0716 / ISSUE #159 — Slice 1/2

Baseline: `86d8798ca81cd0fee64d260c8895b49481958618`, merge #1058 da
dependência #122 / STORY-0046. Branch: `codex/issue-159-resource-authorization`.
Owner: BC-002; executor Backend. Nenhuma aprovação independente é declarada.

## Escopo e autorização

Autorização administrativa conferida em
https://github.com/raphaelperrut/DSGeorref/issues/159#issuecomment-6880844877.
TASK-0716 preserva integralmente os dois allow_paths de produção, requisitos,
ACs, deny_paths e dependências. Somente allow_paths e seu espelho em
phase_f_review.files foram acrescidos de:

- path de evidência já declarado, preservando a grafia `caminh`;
- `tests/backend/identity_access/resource_authorization/**`;
- `.codex/tasks/TASK-0716.json`.

O arquivo preexistente `src/frontend/debug.log` permanece fora da entrega.
Não há alteração em ADR, contrato congelado, outros slices ou consumidores.

## Implementação e persistência

ResourceAuthorization compõe a consulta do próprio sujeito com Access/InstanceAccess
e IdentityTransactions existentes. A aplicação carrega conta e credencial vigentes
no PostgreSQL a cada uso, aplica a permissão de consulta, a elegibilidade existente,
a concessão corrente e a identidade do recurso. Projeto exige vínculo corrente e
existência confirmada por port autoritativo de servidor, na mesma UoW. Não há cache
de allow, role de cliente, bypass administrativo, tabela de grants duplicada ou oracle
contratual executado como serviço de produção.

O adapter confere SHA-256 UTF8/LF do contrato 1.0.0 e de suas dependências antes
de compor o serviço. Ações e tipos vêm do contrato e da política 1.1.0 existentes.
Conta só admite o próprio account_id; ação/tipo incompatíveis negam. Ações de
autenticação conhecidas não viram concessões de projeto. Ação desconhecida produz
validation_failed. Negativas de recurso usam somente access_denied no DTO existente.

Artefatos, artifact_path e caminhos físicos não recebem concessão: a política 1.1.0
não contém artifact_manifest:read para nenhum papel. A negativa precede qualquer
manifest/locator/filesystem I/O. Não há nova rota ou resolução física; BC-013 continua
owner da publicação, integridade, hashes, lineage e resolução segura. Como não existe
allow para artefatos, não se introduz port redundante de manifest para justificar deny.

Consulta não executa a ação consultada nem fornece ticket reutilizável. Sessões,
tokens, OIDC, recovery, membership e seus guards de execução permanecem nos serviços
BC-002 integrados, incluindo CSRF, idempotência, transação e elegibilidade. Não há
novo endpoint ou alteração de wiring HTTP nesta entrega de domínio/application.

Decisões são persistidas em identity.observations com ator, ação, alvo UUID,
resultado, versão e correlação. Um allow só é devolvido depois do commit da UoW;
indisponibilidade de banco, auditoria, política, elegibilidade ou existência autoritativa
nunca produz allow. Senhas, secrets, claims e caminhos internos não são gravados.

Migration nova: **não necessária**. O schema integrado já contém contas, sessões,
PATs, memberships com revisão e observações necessárias. Nenhuma coluna, constraint
ou estado persistido novo foi adicionado. Os flags históricos migration_required e
rollback_required do TaskEnvelope não foram modificados; esta análise concreta
aplica a instrução do Owner de migrar somente quando necessário à persistência entregue.

Rollback: reverter os dois módulos novos e a sua composição; não remover observações
históricas nem reverter o schema compartilhado de identidade. A correção administrativa
pode ser revertida separadamente. Não existe backfill, cutover ou fase contract nova.
As regressões confirmaram que o rollback existente recusa apagar banco populado e
permite downgrade/reapply do schema vazio descartável.

## ACs e requisitos

| Critério | Evidência |
|---|---|
| AC-ISSUE-0826-01 | Dez testes canônicos executados; tabela abaixo e XML |
| AC-ISSUE-0826-02 | Escopo administrativo autorizado; produção nos dois paths originais; sem ticket em package |
| AC-ISSUE-0826-03 | Negativas de vínculo, tipo, projeto, artefato, estado, contrato, elegibilidade, banco e auditoria testadas |
| AC-ISSUE-0826-04 | Este handoff registra contratos preservados, persistência reutilizada, riscos e rollback |

| Requisito | Teste / cobertura |
|---|---|
| REQ-ACC-001 | test_role_project_operation_access: owner/editor/reviewer/viewer, isolamento e binding de recurso |
| REQ-AUTH-IMPL-001 | test_req_auth_impl_001: sessão server-side, revogação, auditoria e banco indisponível |
| REQ-AUTH-IMPL-002 | test_req_auth_impl_002: Argon2id real, profile BP-003 bounded, calibração inválida nega |
| REQ-AUTH-IMPL-003 | test_req_auth_impl_003: CSRF, Origin, Fetch Metadata, sem downgrade de credencial |
| REQ-AUTH-IMPL-004 | test_req_auth_impl_004: hash-only, escopo, unicidade/replay e revogação |
| REQ-AUTH-IMPL-005 | test_req_auth_impl_005: linking explícito e negativas de issuer/subject/nonce/audience/assinatura/replay |
| REQ-AUTH-IMPL-006 | test_req_auth_impl_006 e testes novos: autorização central e releitura de papel, estado e versão |
| REQ-AUTH-IMPL-008 | test_req_auth_impl_008: rotação, logout, expiração e bootstrap terminal |
| REQ-AUTH-IMPL-009 | test_req_auth_impl_009: cerimônia/kit, auditoria e invalidação de credenciais |
| REQ-AUTH-IMPL-010 | test_req_auth_impl_0010: CORS, headers, cookies Secure/HttpOnly/SameSite e rejeição de configuração insegura |

Os nove testes AUTH são as próprias funções canônicas existentes, importadas sem
alteração de asserções e executadas com a composição aprovada da política 1.1.0.
Não constituem nova implementação de identidade. Perfis, provedor OIDC e existência
de projetos são fixtures sintéticas identificadas; não atestam calibração de produção,
IdP externo, owner BC-003/BC-013 ou ambiente de produção.

## Execução reproduzível

Na raiz, Python: `workdir/identity-env/Scripts/python.exe`; PYTHONPATH=src/backend;
PYTHONDONTWRITEBYTECODE=1. PostgreSQL 16.14 local descartável, loopback 127.0.0.1:55493,
base privada local_identity_validation, usuário auth_test; autenticação trust somente
no cluster descartável de teste. IDENTITY_TEST_DSN usa libpq e IDENTITY_MIGRATION_DSN
usa postgresql+psycopg para essa mesma base. Não usar fixtures destrutivas em outra base.
Runtime temporário e basetemp estão em `.runtime/`, ignorado neste diretório.

| Comando / seleção | Resultado |
|---|---|
| pytest -q -p no:cacheprovider --import-mode=importlib tests/backend/identity_access/resource_authorization --basetemp E/.runtime/pytest-final --junitxml E/mandatory-and-resource-tests.xml | 20 passed; 10 nomes obrigatórios, 4 papéis e casos negativos adicionais; sem skips |
| pytest -q -p no:cacheprovider --import-mode=prepend: seleção abaixo, --basetemp E/.runtime/regression2 --junitxml E/regression-tests.xml | 134 passed; sem skips |
| ruff check --no-cache e ruff format --check --no-cache nos dois packages novos e testes novos | PASS |
| .venv/Scripts/python -X utf8 tools/check_python_architecture.py | PASS |
| git diff --check | PASS |
| make verify PYTHON=.venv/Scripts/python | Qualidade Python PASS; frontend interrompido por engines Node/pnpm; ver make-verify.log |

E representa este diretório de evidência. Seleção de regressão no package existente
adapters/usuarios-e-papeis-da-instancia/acc-auth-impl-parte-1/tests:
test_canonical.py::test_role_project_operation_access;
test_safety.py::test_scope_revision_and_account_state_are_reread;
test_safety.py::test_unavailable_throttle_or_project_authority_fails_closed;
test_persistence.py::test_membership_commit_failure_rolls_back_idempotency_and_event;
test_persistence.py::test_existing_schema_populated_rollback_refuses_data_loss;
test_persistence.py::test_empty_schema_downgrade_and_reapply;
mais o contrato contracts/contexts/identity_access/plt/autorizacao-por-projeto-operacao-artefato-e-caminho.

Tentativas iniciais: import do conftest novo foi corrigido para relativo; TCP no
sandbox foi bloqueado com 10013, e a execução fora do sandbox passou. A seleção
legada requer prepend, pois importa conftest/test_canonical por nome simples.
Nenhum teste legado foi alterado. RUFF_NO_CACHE precisa ser true, não 1.

## Limitações e próximo gate

make verify não passou integralmente: ambiente possui Node 24.22.1 e pnpm 11.25.0,
enquanto o repositório exige 24.20.0 / 10.26.1. A falha ocorre antes das etapas
posteriores do Makefile; não se declara que elas passaram. Não foram alterados pins,
frontend ou gates para contornar a falha. Deve ser reexecutado no ambiente pinado
antes de integração. Não é falha funcional observada neste slice.

Próximo gate: QA e revisão independentes no commit candidato, incluindo adequação
dos ports reais de composição dos consumidores. Nenhuma aprovação própria, claim de
produção ou implementação do Slice 2 é declarada. Nenhum PR ou merge foi realizado.
O SHA candidato acompanha o handoff externo; digests fixam os bytes testados.
