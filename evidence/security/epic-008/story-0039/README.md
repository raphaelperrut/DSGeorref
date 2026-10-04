# ISSUE-0149 / TASK-0039 — candidato Security

Base: `471ec4e1d3a2a376b080973f5395dc8634a04918`.
Branch: `codex/issue-0149-task-0039`. Revisão independente pendente.

A decisão explícita do Project Owner foi materializada no AP-003: a chave do
fingerprint HMAC-SHA-256 exige pelo menos 32 bytes, geração CSPRNG pelo sistema
e startup fail-closed abaixo do piso. Não há estimativa estatística de entropia.
`IdentityTransactions` aplica a invariante no consumidor existente, sem wrapper,
nova API ou mudança de contrato. Configuração fora do tipo `bytes` também é negada
com o erro existente `internal_error`.

## Rastreabilidade

| AC / requisito | Evidência nos quatro testes obrigatórios |
|---|---|
| AC-ISSUE-0149-01 | `test_epic_008_seguranca_happy_path`: bootstrap, assinatura RS256 real, vínculo explícito, login OIDC, PAT, autorização, revoke, unlink, logout e login local explícito. |
| AC-ISSUE-0149-02 / REQ-EPIC-076 | `test_secret_permissions_rotation_redaction_fail_closed`: piso no construtor real; chave `secrets.token_bytes(32)` aceita; `opaque()` usa `secrets.token_urlsafe(32)` existente; concessões atuais, rotação sem grace e ausência de plaintext em records/audits/repr. |
| AC-ISSUE-0149-02 / REQ-INS-002 | `test_one_time_bootstrap_no_default_credentials_secret_generation_expiry_and_recovery`: zero contas iniciais, defaults negados, um administrador, replay sem segredo, Argon2id real, kit opaco hasheado, recovery autorizado e de uso único, credenciais antigas negadas e expiry. |
| AC-ISSUE-0149-03 | Os quatro testes: chave insuficiente, profile não aprovado, indisponibilidade de commit injetada, credencial ambígua/inválida, autorização ausente, estados terminais/inválidos e OIDC inválido falham fechados. |
| AC-ISSUE-0149-04 | `test_epic_008_seguranca_negative_paths`: elegibilidade falsa/não booleana, CSRF/Origin/Fetch Metadata, scopes vazios/duplicados/desconhecidos, recurso alheio, dono diferente, grants removidos, replay PAT, expiry, OIDC desabilitado/issuer/audience/subject/nonce/browser/signature/outage/expiry de state e JWT, reuso de state, HTTPS/config e redirect. Redaction no primeiro, segundo e terceiro testes. |

`validation.json` contém nomes/resultados dos quatro testes, digests dos inputs,
checks focados e somente AÇÃO → ESPERADO → OBSERVADO para as demonstrações.
Esses quatro testes executam a implementação real e constituem a menor evidência
executável deste passe. Não foi criado harness adicional nem matriz de testes.

## Reprodução

Em PowerShell, na raiz do repositório, com as dependências de identidade existentes
(`cryptography` e `PyJWT` fixados em `adapters/local_identity/requirements.txt`):

```powershell
$env:PYTHONPATH = 'src/backend;tests/backend/identity_access/local_identity'
.venv/Scripts/python.exe -X utf8 -B -m pytest -q -s -p no:cacheprovider tests/security/contexts/identity_access/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/test_security.py
.venv/Scripts/python.exe -m ruff check src/backend/dsgeorref/contexts/identity_access/application/local_identity/transactions.py tests/security/contexts/identity_access/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter
$env:MYPYPATH = 'src/backend'
.venv/Scripts/python.exe -m mypy --no-incremental --cache-dir=.venv/mypy-issue-0149 src/backend/dsgeorref/contexts/identity_access/application/local_identity/transactions.py
git diff --check
```

## Escopo e limites

- TaskEnvelope corrigido com autorização explícita: arquivo exato de application,
  diretório de evidence já obrigatório e arquivo exato AP-003, sem ampliar globs
  de código ou alterar deny_paths; ambas as listas allow_paths sincronizadas.
- Serviços de application/domain, Argon2id, CSPRNG, HMAC e validação JWT são reais.
  `TransactionalRecords` é uma fixture do port privado Store/UnitOfWork; o port
  upstream de eligibility usa decisões sintéticas. O transporte OIDC reutiliza
  `tests/backend/identity_access/local_identity/oidc_fixture.py` de STORY-0037;
  chaves RSA e JWTs são gerados e verificados por bibliotecas reais.
- A fixture não prova constraints SQL, locks, concorrência, restart, backup ou
  durabilidade PostgreSQL. Não é uma segunda autoridade de produção. Não se
  afirma implementação de throttling persistente ou aprovação BP-003; os valores
  Argon2id/TTL da fixture são sintéticos. QA deve avaliar esses limites.
- A chave de replay é injetada pelo caller; não existe loader/filesystem de secrets
  nesta capacidade. ACLs de arquivo, vault, rotação operacional dessa chave e
  suporte/backup não são superfícies implementadas nem claims desta evidência.
  Rotação/expiry/recovery aplicáveis a sessões, PATs e kits foram exercitados;
  o kit offline é de uso único, sem inventar TTL ausente do contrato.
- Egress real é o transporte OIDC configurado: validação de HTTPS e rejeição de
  redirects são exercitadas diretamente. Nenhuma conexão a IdP, DNS/rebinding,
  proxy, TLS em rede ou limite de payload remoto foi validado neste passe. Não há
  entrada de path/filesystem nos serviços testados, portanto path traversal é N/A.
- Banco/API/frontend/geo: NOT_APPLICABLE em TASK-0039; nenhum servidor ou stack
  iniciado. A superfície/experimento removido da ISSUE-0148 não foi recriado.
- Migration/rollback: NOT_APPLICABLE; nenhum schema/estado persistido/deployment
  foi alterado. Contratos públicos intactos. Piso operacional pode ser revertido
  por decisão normativa versionada; não exige nova arquitetura.
- `make verify` não executado: instrução explícita deste passe limita a validação
  a lint/typecheck/testes focados; esse target também executa frontend e gates
  alheios. Nenhum gate global, Sentinel QA ou aprovação independente é declarado.
