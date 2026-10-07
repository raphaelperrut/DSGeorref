# ISSUE-0150 / TASK-0040 — Reviewer

Data: 2026-10-05. **Decisão: BLOCKED. EPIC-008 não fechado.**
Candidate SHA: `74244676336ed6770749acbfcba1bf6558d09884`.
Branch exclusiva: `codex/issue-0150-task-0040-review`; um envelope, TASK-0040.
Esta revisão não altera produto nem declara aprovação de QA ou produção.

## Pré-condições e escopo

HEAD inicialmente em main, checkout limpo, uma única worktree local. Ancestry
confirmada por `git merge-base --is-ancestor <commit> HEAD`, exit 0 para todos:

| Dependência integrada | Commit verificado |
| --- | --- |
| STORY-0036 | 42906b8 |
| STORY-0712 | ba0b63d |
| STORY-0713 | 39afd61 |
| STORY-0037 | 3558188 |
| STORY-0038 | 471ec4e |
| STORY-0039 | a2b92a8; merge #1019 no próprio candidate |

Nenhuma colisão local observada: checkout limpo antes da revisão e nenhuma outra
worktree. Única escrita de conteúdo: este relatório, dentro do allow_path efetivo
`evidence/reviews/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/**`.
A referência alternativa do campo evidence não foi usada como autoridade.
Consulta remota `gh issue view 116 --json number,title,state,body,url` retornou
HTTP 401; estado remoto da issue, PRs/lanes e anexos G2 não foram certificados.
A dependência de épico EPIC-004 não foi auditada separadamente após a parada.

## Arquivos/evidências auditados

Paths relativos à raiz do repositório:

- `AGENTS.md`, `evidence/AGENTS.md`, `.codex/roles/ROLE-011-reviewer.md`, `.codex/tasks/TASK-0040.json`.
- `docs/06-delivery/stories/STORY-0040-ISSUE-0150-executar-qa-e-auditoria-final-contas-locais-bootstrap-unico-sessoes-tokens.md`.
- `docs/06-delivery/epics/EPIC-008-contas-locais-bootstrap-unico-sessoes-tokens-e-adapter-oidc.md`.
- `evidence/implementation/epic-008/story-0037/{HANDOFF.md,VALIDATION-REPORT.json}` (E37).
- `evidence/implementation/epic-008/story-0038/{HANDOFF.md,VALIDATION-REPORT.json}` (E38).
- `evidence/implementation/contas-locais-bootstrap-unico-sessoes-tokens-e-ada/auth-impl-dbschema-parte-1/{HANDOFF.md,VALIDATION-REPORT.json}` (E712).
- `evidence/implementation/contas-locais-bootstrap-unico-sessoes-tokens-e-ada/id-parte-2/VALIDATION-REPORT.json` (E713).
- `evidence/security/epic-008/story-0039/{README.md,validation.json}` (E39).

As referências JUnit/runtime nos reports são evidência herdada identificada;
não foram todas abertas/recertificadas após a condição de parada. Nenhum ADR,
spec ou documento global foi relido. Busca literal Git encontrou os dois nomes
obrigatórios somente em metadados; esses matches não são execução de testes.

## Matriz de aceitação

| AC-ISSUE-0150 | Evidência encontrada | Resultado desta revisão |
| --- | --- | --- |
| 01 | E37 integração PostgreSQL; E38 interface real e SDK, browser HTTP 404; E39 aplicação/cripto reais | PARCIAL: observabilidade demonstrada, aceite obrigatório não executável; E38 registra integração HTTP de sucesso indisponível |
| 02 | E37 mapeia 12 requisitos; E39 mapeia REQ-EPIC-076 e REQ-INS-002 | BLOCKED: REQ-AUTH-IMPL-007 explicitamente fora da cobertura de E37; sem evidência objetiva localizada nesta auditoria |
| 03 | E39 quatro testes PASS herdados, rejeições explícitas, nenhum fallback OIDC; E713 failures persistidos | PARCIAL: evidência herdada, sem execução do teste de aceite negativo requerido |
| 04 | Reviewer vinculado ao candidate acima; reports herdados registram revisão independente pendente | BLOCKED: não localizada QA independente vinculada a este mesmo SHA; nenhum PASS de outro papel presumido |

## Requisitos do EPIC-008 → evidência

| Requisito | Evidência explícita identificada |
| --- | --- |
| REQ-AUTH-IMPL-001 | E37/E712: `test_req_auth_impl_001` |
| REQ-AUTH-IMPL-002 | E37/E712: `test_req_auth_impl_002` |
| REQ-AUTH-IMPL-003 | E37/E712: `test_req_auth_impl_003` |
| REQ-AUTH-IMPL-004 | E37/E712: `test_req_auth_impl_004`, correção H1 |
| REQ-AUTH-IMPL-005 | E37/E712: `test_req_auth_impl_005` |
| REQ-AUTH-IMPL-006 | E37/E712: `test_req_auth_impl_006` |
| REQ-AUTH-IMPL-007 | NÃO DEMONSTRADO; E37 diz que não foi atribuído aos slices |
| REQ-AUTH-IMPL-008 | E37/E712: `test_req_auth_impl_008` |
| REQ-AUTH-IMPL-009 | E37/E712: `test_req_auth_impl_009` |
| REQ-AUTH-IMPL-010 | E37/E712: nome existente `test_req_auth_impl_0010` |
| REQ-DBSCHEMA-003 | E37/E712: `test_req_dbschema_003`, correção H1 |
| REQ-ID-001 | E37/E713: `test_network_authentication_local_oidc` |
| REQ-ID-002 | E37/E713: `test_bootstrap_session_token_recovery` |
| REQ-EPIC-076 | E39: `test_secret_permissions_rotation_redaction_fail_closed` |
| REQ-INS-002 | E39: `test_one_time_bootstrap_no_default_credentials_secret_generation_expiry_and_recovery` |

Isso identifica rastreabilidade herdada, não certifica os 15 requisitos no
candidate nem substitui os testes obrigatórios ou a aprovação independente.

## Dois testes obrigatórios

`test_epic_008_aceite_happy_path`: NOT_EXECUTED / implementação não localizada.
`test_epic_008_aceite_negative_paths`: NOT_EXECUTED / implementação não localizada.

Buscas `rg` em tests/src/evidence e `git grep` no conteúdo versionado não
localizaram implementações. Tentativa mínima, sem suíte global nem novos testes:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
$env:PYTHONPATH='src/backend;tests/backend/identity_access/local_identity'
.venv/Scripts/python.exe -X utf8 -B -m pytest -q -p no:cacheprovider tests/backend/identity_access/local_identity tests/security/contexts/identity_access/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter -k 'test_epic_008_aceite_happy_path or test_epic_008_aceite_negative_paths'
```

Shell exit 1. Coleta abortada em conftest.py:11 → migration.py:5:
`ModuleNotFoundError: No module named 'alembic'`. Nenhum teste executado; não é
falha funcional de assertion. Nenhuma dependência instalada, skip ou substituto
usado. `make verify` não executado conforme instrução explícita desta tarefa.

## Runtime consumido e fail-closed

Nenhum serviço iniciado nem integração repetida. E39 reutiliza resultados do
SHA `57e715789a8a35b69ccebaa161a19ee5bc642233`, ancestral do candidate. Os seis
digests SHA256 UTF8/LF declarados de TaskEnvelope, AP-003, transactions.py,
conftest.py Security, test_security.py e oidc_fixture.py coincidem com os blobs
Git do candidate; não houve releitura semântica desses arquivos. Digest de
transactions.py: `b8bee17af2ce6111001618b667809b1e4b5889b95f0b531ac3667fe57dfbfde1`.
Esse vínculo sustenta reuso dos inputs declarados, sem provar um manifest
completo de toda a implementação/dependências ou revisão independente.

| Origem / ação | Esperado | Observado registrado |
| --- | --- | --- |
| E39: replay_key 0/1/31 bytes | Startup negado | `internal_error` |
| E39: CSPRNG replay_key 32 bytes | Startup aceito | accepted |
| E39: remover grant / rotacionar sessão / inspecionar records | Negar escalada/credencial antiga; redigir segredo | forbidden; rotated + unauthorized; plaintext ausente |
| E39: bootstrap/recovery/reuso/expiry | Um admin; kit único; credenciais terminais negadas | invalid_credentials; um admin; rotated kit; forbidden/conflict/unauthorized; expired |
| E39: bootstrap local → OIDC assinado → PAT → revoke/unlink/logout | Mesma conta; PAT limitado; revogados negados | Mesma conta; autorização true; unauthorized após revogação; login local explícito funciona |
| E39: OIDC/config/redirect/autorizações inválidas | Negação sem vínculo/credencial indevidos ou fallback | Denials publicados; counts inalteradas; state failed e de uso único; redirect negado |
| E37: bootstrap → link OIDC → sessão → PAT → revoke → unlink | Estado/audit persistidos em PostgreSQL | Um admin; bootstrap completed; sessões local active/federada revoked; PAT/link revoked; OIDC consumed; audit COMMITTED |
| E38: POST real via SDK no browser sem identity host | Falha mantém controles protegidos desabilitados | HTTP 404; controles desabilitados |

E37/E713 são observações históricas PostgreSQL, não novas execuções neste HEAD;
E39 usa Store/UnitOfWork e transporte OIDC de teste, JWT/Argon2id reais. E39
registra também CSRF/Origin/Fetch Metadata, scopes, elegibilidade, ownership,
nonce/issuer/audience/signature/outage, replay, HTTPS e redirects negados.
E713 registra FK de ownership, upgrade inválido atômico e restore guard de
downgrade. Essas demonstrações não fecham a falta dos dois testes de aceite.

## Limitações, riscos e gate

- Parada por ausência dos testes de aceite e cobertura objetiva insuficiente;
  nenhum defeito de produto foi corrigido e nenhuma nova Story/Issue criada.
- REQ-AUTH-IMPL-007 sem evidência localizada; não se infere requisito implementado
  nem aprovação por associação com outros testes.
- E38 registra ausência de identity HTTP host autorizado; sucesso HTTP,
  TLS/cookies, transporte CSRF e logout ETag/If-Match continuam não demonstrados.
- QA independente no candidate ausente nas evidências encontradas; aprovação
  do executor e aprovação de outros papéis não foram inferidas.
- Profiles/eligibility/ceremony e IdP sintéticos; sem promoção BP-003, egress/TLS
  externo, durabilidade PostgreSQL por E39, escala/SLO ou prontidão produtiva.
- Runtime anterior diverge dos pins em partes; E38 registra make verify PASS,
  mas isso não constitui novo gate para este SHA. Ambiente atual falta Alembic.
- GitHub indisponível por autenticação; não se declara fechamento remoto,
  anexação G2 ou inexistência de lanes remotas concorrentes.

Migration/rollback = **N/A** para TASK-0040: só evidência append-only, sem alterar
schema, estado persistido, contrato, artifact de produto ou deployment. Não
executar rollback das migrations dos slices para reverter esta revisão.

**FINAL_QA = PENDING / não emitida pelo Reviewer.**
**REVIEW_READY_SHA = 74244676336ed6770749acbfcba1bf6558d09884; decisão BLOCKED.**
Próximo gate depende de evidência dos testes/requisito e QA independente; este
relatório não autoriza correções fora do envelope nem fechamento do épico.

## Adendo — diagnóstico de ownership, sem implementação

Mesmo candidate SHA, 2026-10-05. Este adendo complementa a auditoria acima;
não a reinicia nem emite QA. Corrige a caracterização de REQ-AUTH-IMPL-007:
**existe evidência canônica de contrato; falta implementação funcional do
throttling persistente e sua certificação no candidate.**

### Ausência real dos testes finais

`git grep -l -F <nome> 74244676336ed6770749acbfcba1bf6558d09884` para cada
teste obrigatório retorna somente TASK-0040.json, STORY_INDEX.json, STORY-0040
e as matrizes PHASE-F CSV/JSON. Busca dos dois nomes nos arquivos executáveis
Python/TypeScript/JavaScript do mesmo commit retorna zero matches. Portanto
ambos estão ausentes como testes executáveis versionados; não se trata de erro
de seleção pytest. A falha de import de Alembic é independente dessa ausência.

### Evidência canônica e comportamento de REQ-AUTH-IMPL-007

Leituras adicionais estritamente relacionadas:

- `docs/01-product/requirements/REQ-AUTH-IMPL-007-throttling-possui-estado-e-evidencia-observavel.md`.
- `contracts/contexts/identity_access/plt/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/test_auth_freeze.py`: `test_req_auth_impl_007`, linhas 35–54.
- Nesse mesmo diretório: política `policies.throttling` e máquina `machines.throttle` de contract.json; `_validate_throttle` de conformance.py.
- `docs/02-architecture/design-reviews/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/{DESIGN-REVIEW.md,VALIDATION-REPORT.json,test-results.xml}`.
- Somente os campos de ownership/escopo/requisitos/testes/dependências das seis STORY/TASK integradas indicadas pelo usuário.
- Código diretamente relacionado: transactions.py, port Store em ports.py, trecho de eligibility em conftest.py e teste Security de rejeição de eligibility não booleana.

O requisito exige estado/evidência observável e identifica o teste canônico.
Esse teste **existe**, com testcase PASS herdado em test-results.xml e
mandatory_tests PASS no VALIDATION-REPORT de TASK-0036. Valida schemas,
observações de examples.json, guards e transições do contrato; não instancia
throttling de produção. DESIGN-REVIEW explicita fixtures sintéticas e que
persistência/restart devem ser implementados nas próximas histórias.
Não houve reexecução do teste neste diagnóstico; PASS histórico não certifica
implementação funcional no candidate.

O contrato já integrado exige PostgreSQL autoritativo, bucket digest limitado,
policyVersion/revision/failure count, janela/deadline, estados open/limited/locked,
atualização atômica e audit correlacionado, preservação após restart. Nenhuma
arquitetura nova é necessária para identificar a lacuna.

Em produção BC-002, transactions.py:44–46 só consulta um Callable Eligibility e
nega quando o resultado não é `True`. Busca direta de eligibility, throttle,
rate_limit e call sites encontra esse consumidor e mapeamentos de erro, sem
implementação de autoridade/bucket de throttling. Não há construção de
IdentityTransactions em src; fixtures compõem o serviço. A fixture backend
declara explicitamente upstream falso e injeta `lambda ...: True`; Security
testa rejeição de `1`/negações sintéticas. Isso prova um guard fail-closed,
**não** contador/janela persistentes, atomicidade, transições ou restart.
E712/E713/E37/E39 também negam claims de implementação de REQ-007/throttling.
Conclusão: capacidade funcional ausente/incompleta, não mera falta de evidência.

### Ownership e classificação única por blocker

| Blocker | Classificação | Ownership atual / menor caminho |
| --- | --- | --- |
| Dois testes finais ausentes | SPEC_TASK_INCONSISTENCY | Somente STORY-0040/TASK-0040 os exige; nenhum dos seis predecessores tem esse dever. TASK-0040 é Evidence Only e proíbe tests/contracts/produto. Designar formalmente produtor de testes numa história existente antes de sua execução; não criar testes no Reviewer |
| REQ-AUTH-IMPL-007 funcional incompleto | MISSING_IMPLEMENTATION | STORY-0036/TASK-0036 possui requisito e teste canônico de contrato, mas src é proibido. STORY-0712 exclui 007 de requisitos/testes; 0713 só possui REQ-ID; 0037 consolida slices; 0038 é Frontend; 0039 exige REQ-EPIC-076/REQ-INS-002. Nenhum tem ownership funcional suficiente vigente |
| Alembic ausente | ENVIRONMENT_ONLY | Preparar dependência já existente no ambiente de execução autorizado; isso não produz os testes ausentes nem implementa throttling |
| QA independente ausente | MISSING_EVIDENCE_EXISTING_BEHAVIOR | Executar QA independente após sanar as lacunas; QA e Reviewer precisam vincular o mesmo novo candidate, evidências e riscos. Esta classificação diz respeito ao registro independente, não certifica a completude do produto |

TASK-0040 pode corrigir apenas o diagnóstico/rastreabilidade do relatório.
Não pode resolver os dois blockers técnicos. STORY-0036 já produziu sua
evidência canônica de contrato; reabri-la só para repetir esse teste não produz
throttling de produção. Nenhum predecessor descumpriu dever explícito de
produzir os dois testes finais, porque tal dever não lhes foi atribuído.

**EXISTING_STORY_CAN_FIX = NO com os envelopes vigentes.** O menor candidato
existente para contenção de implementação/testes é reabrir STORY-0712 /
ISSUE-0822 / TASK-0712, pois possui paths de domínio/application/adapters e
tests/backend/identity_access/local_identity. Isso **exige atribuição formal
prévia** de REQ-007 e dos testes finais por autoridade competente; seus paths
amplos não conferem requisito/dever implícito. Não foi feita tal atribuição,
alteração de envelope, reabertura ou implementação nesta sessão.

**NEEDS_PREREQUISITE = YES**: falta autoridade de tarefa para implementação
funcional de REQ-007 e para produção dos testes finais. É um gate de ownership
objetivamente necessário, não criação automática de nova Story/Issue nem a
divergência administrativa do campo evidence. O caminho mínimo é conter a
correção em história existente com autoridade explícita, implementar somente
o contrato já integrado e testes/evidência correspondentes, obter novo SHA e
então QA independente + Reviewer no mesmo SHA. Até lá: **BLOCKED**.

Nenhum teste executado, serviço iniciado ou arquivo de produto/envelope
alterado neste diagnóstico. Migration/rollback deste adendo continuam N/A.
