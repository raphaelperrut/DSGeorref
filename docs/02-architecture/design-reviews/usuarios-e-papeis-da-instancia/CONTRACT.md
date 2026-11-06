# Política de usuários e papéis da instância

STORY-0041 / TASK-0041 · BC-002 · versão 1.0.0

A política em `policy.json` complementa o [freeze do BC-002](../../../../contracts/contexts/identity_access/plt/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/contract.json). As chaves de `operations` identificam as operações congeladas. Para cada chave, o freeze fornece método, rota, segurança, parâmetros, schemas de entrada e saída, status de sucesso, erros e ordem das guardas. O [OpenAPI publicado](../../../../contracts/http/openapi.yaml) define os DTOs HTTP. A decisão server-side consome principal, ação, recurso, versão da política, estados da conta e da credencial, escopo e revisão do vínculo, conforme o freeze e a ADR-030.

## Contas, papéis e concessões

A conta local é a identidade interna. O primeiro administrador é criado pelo bootstrap, sob capability de instalação verificada e commit atômico. Administrador da instância é uma responsabilidade administrativa exercida por decisão explícita do servidor. Os valores `owner`, `editor`, `reviewer` e `viewer` identificam vínculos a projetos. Sessões e PATs são credenciais da conta. OIDC opcional autentica somente conta ativa vinculada explicitamente por emissor e sujeito. Claims externos, e-mail, nome, papel informado pelo cliente e posse de credencial não concedem privilégios.

| Operação | Administrador ou outra conta ativa | owner | editor | reviewer | viewer | Condição adicional |
| --- | --- | --- | --- | --- | --- | --- |
| Bootstrap | Capability de instalação | — | — | — | — | Estado autoritativo disponível para bootstrap único |
| Criar sessão | Política de autenticação | — | — | — | — | Credencial válida e conta ativa, sem sessão prévia |
| Callback OIDC | Política de autenticação | — | — | — | — | Transação única validada e vínculo explícito |
| Revogar sessão | Concessão explícita | Condicional | Condicional | Condicional | Condicional | Dono da sessão ou decisão explícita autorizando a revogação |
| Emitir PAT | Concessão explícita | Condicional | Condicional | Condicional | Condicional | Escopos solicitados são subconjunto das permissões vigentes |
| Listar membros | Vínculo obrigatório | Condicional | Condicional | Condicional | Condicional | Concessão de listagem no projeto solicitado |
| Vincular membro | Vínculo obrigatório | Condicional | Condicional | Condicional | Condicional | Concessão de criação, projeto e conta alvo existentes e papel registrado |
| Consultar autorização | Concessão explícita | Condicional | Condicional | Condicional | Condicional | A permissão de consulta é avaliada antes da ação consultada |

Condicional exige concessão da ação pela política versionada para o papel do vínculo corrente entre a conta e o projeto solicitado. Para decisão em âmbito de instância, consulta-se a concessão explícita da conta. O freeze não publica um mapa fixo de concessões por rótulo. A ausência de política ou concessão resulta em negação. Para PAT, a ação e o projeto também devem satisfazer o escopo da credencial. Uma resposta de consulta de autorização não concede acesso a uma chamada posterior.

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
| AC-ISSUE-0151-04 | Matriz de concessões, exceções e guardas server-side verificáveis em contrato. O enforcement real é evidência das histórias executáveis |

Em REQ-AUTH-IMPL-007, PostgreSQL é a autoridade para bucket, revisão, contagem, janela e prazo de bloqueio. Somente `open` pode ser elegível. `limited`, `locked` e indisponibilidade da autoridade falham fechados. A evidência correlaciona operação, decisão e snapshots antes/depois sem segredos ou identificadores brutos. Os testes usam fixtures de contrato. Atomicidade, durabilidade após restart e calibração de produção exigem evidência runtime das histórias responsáveis.

Execute os dois testes desta entrega informando o diretório ao pytest, pois a descoberta padrão do repositório começa em `tests/`.

```sh
python -m pytest -q contracts/contexts/identity_access/plt/usuarios-e-papeis-da-instancia
```
