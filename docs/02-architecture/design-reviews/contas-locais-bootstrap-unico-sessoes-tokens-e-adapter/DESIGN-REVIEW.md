# BC-002 — contract freeze de autenticação local v1.0.0

TASK-0036 / STORY-0036 / ISSUE-0146 / EPIC-008 / SPRINT-002.
Este candidato publica o contrato, schemas, fixtures sintéticas e testes offline.
Não implementa backend, banco, adapter de provider, UI ou infraestrutura.

A autoridade local legível por máquina é
`contracts/contexts/identity_access/plt/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/contract.json`.
`contract.schema.json` verifica estrutura e invariantes; `conformance.py` interpreta
as tabelas para evidência executável. Não é um serviço de autorização reutilizável
em produção e não realiza autenticação, criptografia ou persistência.

## Fontes e evolução

Owner: BC-002. ADR-028 governa contas/sessões; ADR-029, OIDC; ADR-030, PATs e
política central; ADR-031, proteção Web e throttling. ADR-018 e ADR-016 continuam
regendo autoridade e transações. STORY-0036 autoriza congelar os detalhes locais;
nenhum endpoint, papel, erro HTTP, tabela ou evento de domínio novo é publicado.
Os estados e guardas são especificações do owner para esta capacidade, não
novos campos dos DTOs HTTP compartilhados.

As oito operações existentes estão pinadas por método/path, permissão, segurança,
parâmetros, schemas, códigos/statuses e idempotência. Os digests das fontes
normativas usam SHA-256 de UTF-8 com newlines LF; não dependem do checkout Windows
ou Linux. Alteração incompatível requer versão explícita e o gate de ADR-010;
este freeze não autoriza editar contrato compartilhado ou ADR.

Baseline main: `9bc6b5497938202581d599fa95ac459e00283616`, com #1007 / PR #1008
integrada. `get_projects_projectid_members` não exige application-level
Idempotency-Key. O histórico `b2e06a94...` é diagnóstico anterior preservado na
branch original; não integra este candidato nem é sua evidência final.

## Estados e ações

| Modelo | Estados | Transições e limites |
|---|---|---|
| Account | absent, active, inactive, locked | criação elegível e autorizada; ativar/desativar por decisão administrativa registrada; lock/unlock server-owned; inactive/locked não autenticam |
| Bootstrap | available, completed | um BootstrapAdmin atômico; completed terminal para sempre, inclusive após recuperação ou exclusão de conta |
| Session | absent, active, revoked, expired, rotated | criar, revogar, expirar e rotacionar; identidades antigas terminais; substituição tem identidade e CSRF novos |
| PAT | absent, active, revoked, expired | emissão escopada, revogação e expiração; sem reativação ou emissão silenciosa em replay |
| OIDC link | unlinked, linked, revoked | linking explícito por issuer+subject para Account existente; vínculo revogado não é relink automático |
| OIDC callback | pending, consumed, failed | estado one-time; sucesso consome com sessão; falha nunca autentica |
| OIDC adapter | disabled, ready, unavailable | configuração explícita; indisponibilidade só retorna a ready após revalidação; nenhuma troca implícita para login local |
| Throttle | open, limited, locked | limite/lock por profile autorizado; liberação server-owned somente após janela/deadline; autoridade persiste após restart |

O grafo fechado em `machines` define todas as transições admissíveis. Estado,
evento, ação, permissão ou guarda não reconhecidos negam. Toda transição exige
autoridade, política, auditoria, ausência de fallback, decisão server-side e commit.
A expiração/revogação é irreversível para a mesma identidade. Uma nova sessão/PAT
é outra identidade, sujeita novamente às guardas.

Account cria-se ativa apenas após senha elegível e profile válido. O primeiro
administrador é criado pelo bootstrap. Criação/ativação/desativação administrativa
fora dele é somente uma capability interna sob ação e grant já registrados na
política central; estas oito operações não introduzem um endpoint de gestão de
contas. Na ausência dessa decisão registrada, a capability nega. Nenhum grant é
inferido dos nomes owner/editor/reviewer/viewer ou de claims do IdP.

## Bootstrap e atomicidade

Disponibilidade vem de PostgreSQL: bootstrap disponível e primeiro administrador
não criado. O commit único contém administrador ativo, hash Argon2id, sessão,
marcador definitivo completed, resultado idempotente e audit. Dois concorrentes
precisam disputar a mesma transação/lock/CAS; um vence e o perdedor observa
completed, retornando `bootstrap_already_completed` (409). Antes do commit,
qualquer falha preserva available e não entrega conta/sessão parcial.

Uma tentativa distinta após completed recebe 409. Replay exato do resultado
idempotente registrado pode retornar o BootstrapStatus original, sem criar nada;
uso de cookie continua condicionado à validade da sessão. Sem autoridade para
replay, nega. Recuperação usa o kit offline e cerimônia auditada de ADR-028, sem
senha padrão, backdoor ou reabertura de bootstrap.

O cenário offline de concorrência representa duas tentativas sobre o mesmo
estado autoritativo: após o primeiro completed não existe segunda aresta válida.
Isso prova a exigência contratual de um único vencedor; não é teste de lock/CAS
real em PostgreSQL. Essa integração pertence às próximas histórias.

## Guardas server-side e HTTP

`operations.*.guards` é ordenada: a primeira guarda negada determina um código
publicado. Facts faltantes, extras ou não booleanas falham fechado. Facts do
intérprete representam resultados de ports confiáveis, nunca flags de request,
UI, CLI, broker ou claims de provider.

- `permission_granted`: decisão da política BC-002 por principal, ação, recurso,
  versão e estados atuais. Não basta posse de cookie/PAT, membership ou role.
- `principal_valid`/`account_active`: credencial atual, não revogada/rotacionada,
  não expirada, Account active e resolução autoritativa; nenhuma tentativa de
  outra credencial após falha ou combinação ambígua de credenciais.
- `request_valid`: schema específico publicado e parâmetros correspondentes;
  `revision_matches`: If-Match autoritativo quando publicado.
- `profile_ready`, `expiry_valid`, `scope_subset`, `throttle_open`: parâmetros
  bounded aprovados, prazo futuro finito, escopos dentro do grant atual e bucket
  elegível. Não há TTL, limite, custo Argon2 ou prefixo numérico inventado.
- `provenance_valid`: CSRF ligado à sessão, Origin/Fetch Metadata nas mutações
  cookie aplicáveis; fluxos pré-sessão validam provenance aplicável sem inventar
  token de sessão no request publicado. Cookies/CORS/headers/TLS seguem ADR-031.
- `commit_ready`: resultado da fronteira transacional autoritativa; não uma
  declaração do cliente de que a gravação funcionou.

Bootstrap usa a capability confiável de instalação para instance:bootstrap;
login usa credenciais elegíveis para session:create sem exigir sessão anterior;
callback usa transação OIDC validada para oidc:callback. São exceções ao principal
pré-autenticado, não exceções à política central.

`get_authorization_check` protege o próprio caller; seu allowed descreve a ação
consultada. Para ação conhecida negada, retorna allowed=false com policyVersion e
reasonCode. Isso não autoriza a próxima operação; ela deve reavaliar a decisão.
Membership exige projeto alvo, usuário existente e role publicada; grants não
atravessam projetos. Não se expõe entidade/ORM/repository para outro contexto.

Erros permanecem `application/problem+json` com Problem e códigos existentes.
Quando a operação não publica erro dedicado, o motivo interno é registrado e
mapeado para um código já permitido: provenance/permission de bootstrap para
validation_failed; permission no login para invalid_credentials; no logout para
unauthorized; revision mismatch do logout para internal_error; throttling de
bootstrap para internal_error e de callback para oidc_exchange_failed. Não são
adicionados 403/412/429 onde a operação não os declara. Nunca responder sucesso
para contornar a limitação do catálogo de erros.

## Sessões, PATs e OIDC

Sessões são opacas, persistidas e verificadas em cada uso com prazo, revisão e
Account. Rotação revoga a identidade anterior e cria a substituta atomicamente.
Logout segue a operação publicada, incluindo If-Match e os dois schemes; um PAT
válido não determina implicitamente a sessão alvo, e a ausência de alvo resolvido
produz session_not_found. Replay não ressuscita sessão expirada/revogada.

PAT armazena somente hash e metadata. Plaintext é entregue uma única vez na
emissão inicial, nunca em audit ou recuperação. Replay idempotente após entrega
retorna conflict, sem guardar plaintext nem emitir novo PAT. Expiry omitida/null
no request recebe prazo finito definido pelo profile aprovado; sem profile nega,
sem fallback ilimitado. A revogação e o uso são capabilities do owner; nenhum
endpoint de revogação novo é introduzido. Escopos são reconhecidos e contidos nos
grants atuais; redução de grant ou desativação da conta vale no próximo uso.

OIDC permanece opcional, com configuração explícita. O adapter valida provider,
issuer, audience, assinatura, nonce, state browser-bound e prazo antes de devolver
o DTO externo definido em `boundary-evidence.schema.json#/$defs/oidc`. A ACL do
application boundary resolve issuer+subject por vínculo explicitamente autorizado
para Account existente/ativa; email não faz linking e o IdP não concede roles.
State consumido/falhado não volta a pending; sessão só existe depois do commit.
Provider ausente, configuração/resultado inválido ou outage recebe erro publicado,
sem autenticação implícita de conta local. Configuração disabled não apaga contas
locais; entrar explicitamente pelo login local é outro fluxo sujeito às guardas.
O campo HTTP linked informa se este callback criou o vínculo; um vínculo explícito
preexistente retorna false. As provas booleanas da fixture representam validação
do adapter confiável; a suíte não alega verificar assinatura/handshake OIDC real.

## REQ-AUTH-IMPL-007 e evidência observável

Bucket autoritativo possui estado, revision, failureCount, janela e blockedUntil;
keyDigest pseudonimiza a chave. A observação contém operação, correlationId,
policyVersion, server observedAt, snapshots antes/depois, decisão e motivo.
Limited/locked exigem deadline observável e negam; mudança exige nova revisão.
Contador não reseta na mesma janela, restart não limpa estado e liberação não
precede deadline. Profile/autoridade/evidência necessários indisponíveis negam.

`examples.json` oferece observações sintéticas de elegibilidade, limite, lockout e
falha da autoridade, validadas por schema e invariantes sem parâmetros produtivos.
Digest/correlation ficam no audit; labels de métricas são somente operação,
estado e decisão, sem cardinalidade por identidade. Nenhum segredo ou identidade
bruta cabe no DTO fechado. `audit` valida que AdminBootstrapped e os eventos
canônicos só representam sucesso após commit; negação não publica sucesso.

## Execução e limites de evidência

Executar apenas o arquivo deste bundle com pytest, ou selecionar os entrypoints
obrigatórios test_req_auth_impl_007 e test_epic_008_politica. Detalhes e resultados
estão no relatório e JUnit adjacentes. Não há suíte global nem make verify nesta
execução: a instrução atual restringe explicitamente os validadores proporcionais.

Esta evidência prova o contract freeze e casos de conformidade/falha, não runtime,
força criptográfica, performance, persistência após restart ou concorrência física.
Essas verificações exigem implementação nas próximas histórias. O valor de um
profile ausente nunca é substituído por um número de fixture. QA e Reviewer
independentes no mesmo candidate commit permanecem como próximo gate.
