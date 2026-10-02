# ISSUE-0147 / GitHub #113 — consolidação de STORY-0037

Candidate: o único commit que contém este handoff, teste e relatório. Executor Backend;
QA, Arquiteto e Reviewer independentes devem avaliar esse mesmo SHA. AC-04 é gate
do Reviewer e permanece pendente; este documento não libera dependentes.

## Incremento e baseline

Baseline `39afd61937a2873e4385fc35dbbe2838e32457bc`, com #155/STORY-0712 integrada
por `ba0b63ddbe010a74c7e9ebeeb48f28b18e2864f5` e #156/STORY-0713 integrada
por `39afd61937a2873e4385fc35dbbe2838e32457bc`. Ambas as issues GitHub estão fechadas.
Uma única worktree/branch `codex/issue-0147-slice-consolidation`, TASK-0037.
Nenhum PR aberto ou outra worktree foi encontrado na inspeção de lanes.

O menor incremento é evidência executável de integração. Nenhuma alteração de produção
é necessária: #156 já reutiliza o domínio, serviços, ports e adapter PostgreSQL da #155.
Não há colisão a eliminar nem regra a reimplementar. Foram adicionados somente o teste
obrigatório e evidências; TASK-0037 inclui seus paths exatos e o próprio envelope nas
duas listas allow_paths. Deny paths, dependências, contratos, critérios, database
APPLICABLE e migration_required=false permanecem preservados. A contenção foi
explicitamente autorizada na instrução desta #113, conforme ADR-007.

## Cobertura e autoridades

`VALIDATION-REPORT.json` mapeia os 12 requisitos a owners e evidências herdadas.
O teste compara a matriz canônica, reports/JUnit mergeados e ancestry Git, verifica
owners disjuntos e os digests do source manifest da #156. Também exige ausência de
diff na produção BC-002 em relação ao candidato integrado da #156.

STORY-0712 é owner de REQ-AUTH-IMPL-001/002/003/004/005/006/008/009/010 e
REQ-DBSCHEMA-003. STORY-0713 é owner de REQ-ID-001/002. Nenhum owner/evidência ausente.
REQ-AUTH-IMPL-007 não foi atribuído a estes slices e não é implementado nesta issue.
As evidências mandatory-tests.xml da #155, sua correção H1 (h1-focused-tests.xml),
e focused-tests.xml/runtime-validation.json da #156 são reutilizadas nos SHAs
registrados; não são apresentadas como novas execuções das suítes no candidato.

REQ-ID é aceitação dos mesmos serviços existentes, sem implementação normativa
paralela: LocalAccounts (bootstrap/login), Sessions (ciclo de sessão), Tokens (PAT),
Access/AuthorizationPolicy (autorização), AdministrativeRecovery (recuperação),
Federation/ValidatingOidcProvider (ACL/validação OIDC), PostgresUnitOfWork/Store
(persistência). A #156 adiciona validação de ownership no fluxo existente, com
constraint aditiva já mergeada. Nenhum registry, façade, service/repository novo,
API, tabela, infraestrutura ou segunda autoridade foi introduzido.

Todos esses módulos pertencem a BC-002. O gate de arquitetura confirma direção de
dependências e ausência de ciclos/violações. A inspeção dos imports de produção não
encontrou consumo das entidades/repositories/ORM/state machines por outro contexto.
PostgreSQL continua único estado autoritativo; não há broker neste caminho.

## Validação mínima real

`focused-tests.xml`/`focused-tests.log`: test_story_0037_slice_consolidation PASS,
1 passed, zero skips/falhas. Reutiliza as fixtures já mergeadas, profile sintético
e JWT RS256 realmente assinado, transporte OIDC sintético. Usa apenas PostgreSQL
16.1 local em loopback e Python 3.12.10, PyJWT 2.15.0. Não inicia a stack.

No mesmo estado: bootstrap local -> vínculo OIDC explícito -> sessão federada ->
PAT aceito pelo autorizador -> revogação do PAT -> unlink. Inspeção por novas
conexões demonstra uma conta/admin, bootstrap completed, sessão local active,
sessão federada revoked, PAT revoked, vínculo revoked, transação OIDC consumed,
uma auditoria COMMITTED por mutação. Ambos os segredos revogados são negados e
a sessão local continua válida. Hash do PAT e ownership da transação são conferidos.
`runtime-observed.json` registra contagens e estado, sem segredos ou dados pessoais.

Schema existente `identity_link_binding_v2`: 66 constraints validadas, incluindo
oidc_transaction_session_owner_fk. Só foram aplicadas as migrations já mergeadas
v1/v2 ao banco descartável. Nenhuma migration, alteração de schema ou conversão de
dados desta consolidação é necessária. Banco temporário removido e ausência
confirmada; servidor iniciado para o teste encerrado, bancos anteriores preservados.

Ruff e Python architecture PASS. Resultado do make verify obrigatório está em
VALIDATION-REPORT.json e make-verify.log; não representa aprovação independente.

## Rollback e riscos residuais

Rollback: revert somente deste único incremento (envelope/teste/evidência), sem
downgrade ou alteração de dados. Os commits, serviços e migrations válidos da #155
e #156 permanecem intactos. Não executar downgrade dos slices para reverter #113.
Sem impacto em contratos públicos, DTOs, endpoints, estados, eventos ou ADRs.

Mantêm-se os limites herdados: fixture não promove BP-003, elegibilidade e decisão
administrativa são sintéticas; não há teste de IdP/TLS externo nem claim produtivo
de segurança, capacidade ou SLO. Ambiente local Python 3.12.10/Node 22.14.0 difere
dos pins 3.12.13/24.20.0; validação CI exata permanece gate. Produção continua sujeita
aos controles e reviews já declarados, sem ampliá-los nesta consolidação.

AC-01/02/03 possuem evidência do executor. Próximo passo é QA/Arquiteto/Reviewer no
candidate SHA; somente o Reviewer registra aceitação de riscos e libera dependentes
(AC-04). Não há autoaprovação.
