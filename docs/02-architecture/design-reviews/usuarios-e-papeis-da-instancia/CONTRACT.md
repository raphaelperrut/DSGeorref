# Política de usuários e papéis da instância

STORY-0041 / TASK-0041 · BC-002 · versão 1.1.0

Matriz e aceite parcial aprovados pelo [ato Owner 6709165678](https://github.com/raphaelperrut/DSGeorref/issues/117#issuecomment-6709165678), sobre o candidato de referência 0c325f1453be003ab3f6d39e9abe3cbcaa00a617.

A política em `policy.json` complementa o [freeze do BC-002](../../../../contracts/contexts/identity_access/plt/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/contract.json). As chaves de `operations` identificam as operações congeladas. Para cada chave, o freeze fornece método, rota, segurança, parâmetros, schemas de entrada e saída, status de sucesso, erros e ordem das guardas. O [OpenAPI publicado](../../../../contracts/http/openapi.yaml) define os DTOs HTTP. A decisão server-side consome principal, ação, recurso, versão da política, estados da conta e da credencial, escopo e revisão do vínculo, conforme o freeze e a ADR-030.

## Contas, papéis e concessões

A conta local é a identidade interna. O primeiro administrador é criado pelo bootstrap, sob capability de instalação verificada e commit atômico. Administrador da instância é uma responsabilidade administrativa exercida por decisão explícita do servidor. Os valores `owner`, `editor`, `reviewer` e `viewer` identificam vínculos a projetos. Sessões e PATs são credenciais da conta. OIDC opcional autentica somente conta ativa vinculada explicitamente por emissor e sujeito. Claims externos, e-mail, nome, papel informado pelo cliente e posse de credencial não concedem privilégios.

| Operação | Administrador da instância | owner | editor | reviewer | viewer | Condição adicional |
| --- | --- | --- | --- | --- | --- | --- |
| Bootstrap | Capability de instalação | — | — | — | — | Estado autoritativo disponível para bootstrap único |
| Criar sessão | Política de autenticação | — | — | — | — | Credencial válida e conta ativa, sem sessão prévia |
| Callback OIDC | Política de autenticação | — | — | — | — | Transação única validada e vínculo explícito |
| Revogar sessão | Própria sessão | Própria sessão | Própria sessão | Própria sessão | Própria sessão | Conta ativa, credencial elegível e concessão explícita vigente |
| Emitir PAT | Próprio PAT | Próprio PAT | Próprio PAT | Próprio PAT | Próprio PAT | Validade elegível e escopos solicitados contidos nas permissões vigentes |
| Listar membros | Conforme vínculo e papel do projeto | Permitido no próprio projeto | Permitido no próprio projeto | Permitido no próprio projeto | Permitido no próprio projeto | Vínculo vigente da conta ao projeto solicitado e concessão vigente |
| Vincular membro | Conforme vínculo e papel do projeto | Permitido no próprio projeto | Negado | Negado | Negado | Conta alvo existente, papel entre owner/editor/reviewer/viewer e todas as guardas da operação |
| Consultar autorização | Próprio principal | Próprio principal | Próprio principal | Próprio principal | Próprio principal | A permissão de consulta é avaliada antes da ação consultada |

A matriz é o mapa concreto aprovado para a política versionada desta entrega. O autosserviço é concedido explicitamente à própria conta ativa e restringe o alvo à conta autenticada. Os papéis de projeto concedem somente as ações de `project_role_grants`, mediante vínculo server-side da mesma conta ao mesmo projeto. Rótulos enviados pelo cliente e a responsabilidade de administrador não substituem vínculo ou concessão. Ausência, revogação ou incompatibilidade de concessão, conta, credencial ou vínculo resulta em negação. Para PAT, ação e projeto também devem satisfazer o escopo da credencial. A consulta descreve somente a autorização do próprio principal e não concede acesso a uma chamada posterior.

Bootstrap depende de capability de instalação e estado único, criação de sessão depende de credenciais válidas e callback OIDC depende de transação validada. Essas operações não pertencem ao mapa de concessões por papel. O administrador recebe o mesmo autosserviço e segue o papel efetivo em cada projeto. Nenhuma das oito operações desta política concede acesso a sessões ou credenciais de terceiros.

`VincularMembro` usa a operação POST existente, com idempotência obrigatória. Um vínculo duplicado segue o erro publicado e o replay válido segue a política congelada. `MembershipChanged` só pode ser publicado após o commit. O POST não edita nem revoga vínculos existentes. Quando a autoridade remove um vínculo ou concessão, a próxima decisão deve avaliar o estado e revisão atuais. Conta inativa ou credencial revogada perde elegibilidade nos usos subsequentes. O freeze não publica operações HTTP de administração de papéis globais, remoção de membro ou revogação de PAT.

## Estados e transições

| Origem | Evento | Destino | Condição específica do freeze |
| --- | --- | --- | --- |
| absent | create | active | Criação autorizada, senha elegível e profile válido |
| active | deactivate | inactive | Decisão administrativa |
| locked | deactivate | inactive | Decisão administrativa |
| inactive | activate | active | Decisão administrativa, senha elegível e profile válido |
| active | lock | locked | Lockout devido |
| locked | unlock | active | Desbloqueio devido e profile válido |

As seis transições da máquina `account` exigem as guardas completas do freeze, incluindo autoridade, política, auditoria, permissão e commit. Todo par estado/evento fora da máquina é negado. A cerimônia auditada de recuperação offline da ADR-028 não reabre bootstrap nem concede exceção às guardas. Sessões, PATs, vínculos OIDC e throttling mantêm suas máquinas congeladas.

## Falhas e rastreabilidade

A avaliação usa somente fatos server-side e o primeiro erro aplicável na ordem congelada. Estado desconhecido, autoridade ou revisão indisponível, credenciais ambíguas, escopo insuficiente, vínculo incorreto e falha de commit impedem sucesso. Mutações Web com cookie obedecem às guardas de proveniência e CSRF aplicáveis. Erros de transporte usam os códigos da operação e `application/problem+json`. Por exemplo, a listagem responde `forbidden` (403) por falta de concessão e `rate_limited` (429) se o throttle estiver fechado. A proteção de bootstrap e callback usa, respectivamente, `internal_error` e `oidc_exchange_failed` segundo o freeze. A falha não pode emitir credencial, vínculo, evento de sucesso ou concessão.

| Critério | Evidência contratual |
| --- | --- |
| AC-ISSUE-0151-01 | Política versionada, oito referências HTTP e `test_epic_009_politica` |
| AC-ISSUE-0151-02 | `REQ-AUTH-IMPL-007`, máquina `throttle`, schema de evidência e `test_req_auth_impl_007` |
| AC-ISSUE-0151-03 | Matriz de falhas por guarda e transição, incluindo negação sem efeito de sucesso |
| AC-ISSUE-0151-04 | Matriz concreta aprovada, cenários positivos e negativos por papel, alvo, projeto e concessão em test_instance_policy.py. O enforcement real é evidência das histórias executáveis |

Em REQ-AUTH-IMPL-007, PostgreSQL é a autoridade para bucket, revisão, contagem, janela e prazo de bloqueio. Somente `open` pode ser elegível. `limited`, `locked` e indisponibilidade da autoridade falham fechados. A evidência correlaciona operação, decisão e snapshots antes/depois sem segredos ou identificadores brutos. Os testes usam fixtures de contrato. Atomicidade, durabilidade após restart e calibração de produção exigem evidência runtime das histórias responsáveis.

## Aceite parcial AC-04

O ato Owner aprova AC04-RECONSTRUCTION-v1.md no SHA de referência como nova referência parcial das obrigações comprováveis. O aceite contratual da STORY-0041 exige os quatro critérios acima, a matriz concreta e seus testes. Os três originais continuam ausentes. Identidade histórica e reprodução dos digests originais permanecem sem comprovação.

A reconciliação individual das 36 obrigações, 20 vínculos G2 Access, dois vínculos Identity e oito testes históricos continua atribuída às histórias responsáveis e à consolidação da STORY-0045. Uma lacuna contratual necessária a uma história executável deve ser resolvida antes de seu consumo. Os gates de segurança, integração e produção mantêm suas exigências.

Execute os dois testes desta entrega informando o diretório ao pytest, pois a descoberta padrão do repositório começa em `tests/`.

```sh
python -m pytest -q contracts/contexts/identity_access/plt/usuarios-e-papeis-da-instancia
```
