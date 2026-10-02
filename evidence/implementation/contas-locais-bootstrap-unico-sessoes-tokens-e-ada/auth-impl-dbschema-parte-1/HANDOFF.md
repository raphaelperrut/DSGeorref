# Handoff — ISSUE-0822 / GitHub #155

TASK-0712 / STORY-0712, Slice 1/2 do EPIC-008, owner BC-002.
O commit candidato é o commit que contém este handoff; seu SHA é informado no retorno final.
Evidência do executor, sem aprovação própria ou claim de aprovação por outro papel.

## Resultado e escopo

Implementados domínio, application services e adapters privados para bootstrap atômico,
login local, sessões opacas com idle/absolute timeout, rotação, logout, PATs hash-only,
autorização central com membership atual, recuperação offline e OIDC opcional com
vínculo explícito. Não foi criado endpoint, UI, papel público ou contrato externo.
Não há código do Slice 2/2 nem package por ticket. PostgreSQL permanece autoritativo.

STORY-0036 está integrada pelo PR #1009, merge
`42906b8de172fb1dd487e821575e5bc21ec093d3`, também base limpa desta branch.
`origin/main` e o HEAD inicial coincidiam; a consulta remota de main confirmou o SHA.
Na inspeção inicial, nenhum PR aberto e nenhuma worktree de implementação concorrente
foi encontrado. A outra worktree estava detached nesse merge e tinha escopo de contratos,
disjunto dos packages de implementação. Não há registry de lanes ativas no repositório.

O usuário autorizou corrigir omissões administrativas no TaskEnvelope. Conforme
ADR-005/007 e PYTHON_CODE_ARCHITECTURE_STANDARD, os slugs gerados não importáveis foram
substituídos pelos packages estáveis `domain/local_identity`, `application/local_identity`
e `adapters/local_identity`, dentro de `contexts/identity_access`. Foram incluídos testes,
o diretório de evidência já declarado e o próprio envelope. As duas listas allow_paths
do envelope são iguais; os deny_paths permanecem intactos. Migrations Alembic e manifest
de dependências pertencem ao adapter. Lista e hashes dos arquivos: VALIDATION-REPORT.json.

## Evidências e requisitos

Os dez entrypoints canônicos estão em `tests/backend/identity_access/local_identity/test_requirements.py`.
`mandatory-tests.xml` contém o resultado final. Não houve skip ou mudança das assertivas
para aceitar falhas de implementação.

| Requisito | Evidência principal |
|---|---|
| REQ-AUTH-IMPL-001 | Estado server-side, revogação, auditoria append-only e indisponibilidade real do banco negada |
| REQ-AUTH-IMPL-002 | Argon2id PHC com salt distinto; profile BP-003 obrigatório, parâmetros inválidos/ausentes e budget ocupado negam |
| REQ-AUTH-IMPL-003 | Origin/Fetch Metadata e CSRF ligado à sessão; credenciais ambíguas negam, sem downgrade para PAT |
| REQ-AUTH-IMPL-004 | Escopos atuais, projeto, prazo finito, hash-only, replay sem reemissão e revogação persistente |
| REQ-AUTH-IMPL-005 | JWT RS256 realmente assinado; issuer/audience/nonce/signature; state browser-bound e single-use; vínculo explícito e unlink |
| REQ-AUTH-IMPL-006 | Política versionada em BC-002, estado da conta e grant/membership atual em cada uso; redução de grant nega |
| REQ-AUTH-IMPL-008 | Rotação atômica, revisão, logout com alvo explícito para PAT, replay sem segredo e expiração terminal |
| REQ-AUTH-IMPL-009 | Kit offline one-time, decisão administrativa confiável obrigatória, cerimônia auditada, invalidação de sessões/PATs |
| REQ-AUTH-IMPL-010 | Same-origin, allowlist CORS explícita, HTTPS, cookie Secure/HttpOnly/SameSite, CSP e headers restritivos |
| REQ-DBSCHEMA-003 | PK/FK composto projeto/conta, unicidade de membership, scopes imutáveis e autorização com lock de membership |

`runtime-evidence.json` registra rehearsal diretamente pelas application services:
falha diferida no commit sem efeitos parciais; dois bootstraps concorrentes com um
vencedor; sobrevivência a restart; escopo, expiração, revogação, rotação e logout;
inspeção de todos os registros e dump sem senha, kit, cookie, CSRF ou PAT em claro;
rollback protegido, downgrade vazio, reapply e restore com mesmo digest dos dados.
`schema-constraints.json` contém as constraints inspecionadas no banco real.

As observações são registros privados de BC-002, persistidos junto aos efeitos ou,
para negações, em transação separada depois do rollback. Não são uma implementação
do ledger de BC-014 e não publicam evento antes do commit. Nenhum repository, entidade,
ORM ou state machine é importado por outro contexto. O provider devolve somente
identidade externa validada; tokens/SDK models não chegam à ACL nem à auditoria.

## Validação e limites

Ruff, mypy strict e gate de arquitetura passaram. O report registra versões realmente
usadas. O rehearsal usa Python 3.12 e PostgreSQL 16.1 instalado, isolado em loopback,
com dados sintéticos; não certifica a imagem nativa pinada nem readiness produtiva.

`make verify` foi executado. Todos os seus checks têm resultado aprovado: frontend,
qualidade, repository/SAR/requisitos/DDD/ADRs/specifications/sprint/arquitetura,
licenças, implementação/completion, decisões 09/10, ruleset e fechamento da fundação.
Após o usuário iniciar Docker, a integração real da fundação passou com PostgreSQL
18.4, RabbitMQ 4.3.4 e seus processos API/Celery worker. O fluxo persistiu COMPLETED,
a sequência esperada e o checksum do artefato. Não foi criada API de autenticação.
Os logs preservam a falha inicial de ambiente e as interrupções posteriores.

Não houve uma invocação única de make com saída zero: sob pressão de memória do
Windows e fixtures Git lentos, os comandos pendentes foram retomados exatamente,
reutilizando apenas checks aprovados sem mudanças. O registro consolidado está em
`make-verify-completion.log`; decisões 09/10: 2 passed; ruleset: 5 passed;
fechamento da fundação: 2 passed. Nenhum teste foi desabilitado ou substituído.
A tentativa auxiliar Linux não produziu validação; não há claim de execução Linux.
Ruff/mypy e arquitetura específicos da capacidade cobrem 21 módulos de produção.

Os números da fixture são sintéticos, não uma promoção de BP-003. Produção exige
profile bounded aprovado/calibrado, política e capabilities confiáveis de instalação,
eligibilidade e cerimônia. O port obrigatório de elegibilidade integra o controle
publicado, sem default ALLOW; não implementa REQ-AUTH-IMPL-007 fora deste slice.
Profile ausente/inválido e ausência de decisão administrativa falham fechado.
Mudança de parâmetros Argon2 exige plano aprovado para hashes já existentes;
parâmetros divergentes são negados, sem recalibração silenciosa.
OIDC foi validado com transporte isolado e JWTs reais, sem IdP externo ou handshake
TLS real nesta evidência. Não há claim de latência, custo, capacidade ou segurança
produtiva calibrada. QA, Arquiteto e Reviewer independentes no mesmo SHA estão pendentes.

## Migration, impacto e rollback

`local_identity_v1` é a primeira migration aditiva de BC-002. O executor usa Alembic,
lock transacional exclusivo, lock_timeout/statement_timeout e DDL transacional.
Não há reader anterior de identidade, backfill ou fase contract destrutiva neste slice.
O preflight exige schema novo ou revisão Alembic conhecida, espaço para as tabelas,
janela de locks e escritores parados para downgrade. A revisão Alembic é o checkpoint;
repetir upgrade em head não recria tabelas. Schema ou revisão incompatível falha,
sem adoção silenciosa. O teste valida constraints e persistência antes de handoff.

Nenhum contrato congelado, OpenAPI, ADR, requirement ou tabela de outro contexto foi
alterado. Impacto físico: schema `identity`, aggregates de BC-002, bootstrap, replay,
transações OIDC, cerimônias e observações privadas, mais metadata Alembic.

Antes de qualquer conta existir, parar escritores e executar `migrate(dsn, "downgrade")`
remove as tabelas da capacidade em uma transação, preservando metadata Alembic em base.
Depois de bootstrap, o downgrade recusa apagar identidade e reabrir bootstrap.
Para instalação inicializada, preferir forward fix; rollback de dados exige backup e
restore coordenados, com escritores parados e compatibilidade dos readers verificada.
O rehearsal fez backup, comprovou a recusa com digest intacto, limpou somente o banco
descartável, executou downgrade/reapply e restaurou o backup com digest idêntico.
O estado validado foi preservado no cluster temporário, encerrado normalmente,
e no backup `workdir/identity-validation-backup.sql`; nenhum deployment foi realizado.
O digest restaurado é `ade917c416df69f08cafdd609679cdad9c88f58fadf6c6b77f4cfbcf361de04f`.
API/worker são encerrados pela fixture. As portas dos serviços descartáveis estavam
fechadas na inspeção final. Docker Desktop ficou indisponível após a integração
aprovada; a remoção final dos containers `dsgeorref-auth-validation-postgres` e
`dsgeorref-auth-validation-rabbitmq` e da rede `dsgeorref-auth-validation` não foi
confirmada. Somente recursos desta tarefa devem ser removidos após recuperar o daemon;
nenhuma imagem, cache ou aplicação do usuário foi removida.

## Próximo gate

Revisão independente de Arquiteto, QA e Reviewer no SHA candidato; promover BP-003
aprovado e integrar as capabilities confiáveis antes de produção. Os checks globais
foram completados nas execuções retomadas registradas, com a limitação operacional acima.
Riscos residuais e ausência de aprovação não são apresentados como gates aprovados.

## Correção H1 — revisão do candidato anterior

Base revisada: `a61be06e765f6af360487d36f122b462aa8eef2e`. A correção pertence ao
novo commit que contém este adendo. Somente H1 foi tratado; nenhuma aprovação
independente é atribuída ao executor.

A revogação autenticava e verificava ownership, mas não exigia permission_granted
para a ação sobre o alvo. `Tokens.revoke` agora chama `Access.enforce` com a permissão
registrada `token:create` e o `project_id` da linha persistida do token alvo, sob os
locks e a transação existentes, antes da mutação. Ownership continua obrigatório.
Não foi criada ação, política, contrato, endpoint ou capacidade de outro slice.

`h1-focused-tests.xml`: PASS, quatro testes — canônicos REQ-AUTH-IMPL-004/006,
REQ-DBSCHEMA-003 e regressão de autorização da revogação. Setup usa schema já aprovado
copiado em `local_identity_h1_validation`; sujeitos/sessões são dados sintéticos,
sem bootstrap, migration, rollback ou OIDC. Ruff dos três arquivos e mypy strict
do módulo alterado passaram. A propriedade de runtime no JUnit gera um warning
de compatibilidade xunit2; os resultados e seu conteúdo são preservados também
em `h1-runtime-evidence.json`.

A integração real comprovou quatro negações com a linha completa do alvo intacta
e nenhuma revogação confirmada: PAT A list-only para B com permissão central negada;
sessão proprietária sem permissão B; PAT A token:create para B mesmo com grant B;
PAT B list-only sem a ação exigida. PAT B token:create autorizado revoga o alvo B,
incrementa revisão, registra uma única revogação e nega usos posteriores.

Evidências de migration/rollback, contratos e capacidades não alteradas permanecem
vinculadas ao SHA revisado anterior. Os resultados de revogação e AC-01/AC-03 são
supersedidos pela evidência H1. Nenhum gate global foi repetido ou apresentado como
novo resultado neste SHA. Mudança de produção: uma chamada ao autorizador existente.
Rollback da correção por revert reintroduziria H1 e exige decisão consciente; não
há alteração de schema/dados ou procedimento novo de migration/rollback.

Próximo gate: Reviewer independente confirmar o fechamento de H1 no novo SHA.
Permanecem os limites produtivos e de aprovação registrados no handoff original.
