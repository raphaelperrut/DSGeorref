# Boundary HTTP do BC-002

O entrypoint de produção monta somente `DELETE /api/v1/auth/session`. Ele usa o contrato HTTP
versionado, a política integrada da instância e a unidade de trabalho PostgreSQL
existente. A sessão deve ter sido emitida por uma superfície autorizada.

Instale `requirements.txt` deste diretório e inclua `src/backend` no
`PYTHONPATH`. Configure todas as variáveis antes de iniciar o servidor.

| Variável | Valor obrigatório |
|---|---|
| `DSGEOREF_IDENTITY_DSN` | DSN PostgreSQL com banco explícito e schema de identidade já migrado |
| `DSGEOREF_IDENTITY_POLICY` | Caminho para o `policy.json` da instância com digest reconhecido pelo runtime existente |
| `DSGEOREF_IDENTITY_SECURITY_PROFILE` | Caminho para o JSON do perfil aprovado conforme AP-003 e BP-003, com os campos de `SecurityProfile` e durações expressas em segundos |
| `DSGEOREF_IDENTITY_ORIGIN` | Origem HTTPS exata da aplicação, sem barra final |
| `DSGEOREF_IDENTITY_REPLAY_KEY_HEX` | Segredo estável de pelo menos 32 bytes aleatórios, codificado em hexadecimal |

Execute atrás do proxy TLS de mesma origem, no mesmo host, com o upstream
restrito ao loopback. Preserve os cabeçalhos de proveniência do navegador.

```sh
python -m uvicorn --factory --host 127.0.0.1 --no-proxy-headers --no-access-log \
  dsgeorref.contexts.identity_access.adapters.local_identity.asgi:create_production_app
```

O logout por cookie exige `Origin`, `Sec-Fetch-Site: same-origin`,
`X-CSRF-Token`, `Idempotency-Key` e `If-Match`. Use a revisão da sessão como
ETag forte decimal entre aspas, por exemplo `"1"`. Com PAT autorizado e sem
alvo de sessão autoritativo, o contrato retorna `session_not_found`. O perfil
de benchmark do repositório é insumo de calibração. A implantação exige um
perfil runtime aprovado.

Login, bootstrap, emissão de PAT e consulta de autorização dependem de
elegibilidade persistente e perfil promovido. As operações de membros exigem,
adicionalmente, a autoridade de existência de projeto do BC-003. Bootstrap
também depende da capacidade de instalação verificada pelo servidor. O callback
OIDC requer o início da transação vinculada ao navegador e a configuração
autorizada do provedor. Essas operações ficam fora do roteamento deste entrypoint.

Para rollback, retire o upstream do proxy e pare o processo ASGI. Revogações
confirmadas e a trilha de auditoria permanecem no PostgreSQL.

## Integração de desenvolvimento do Sprint 002

Use um banco PostgreSQL local descartável, com a revisão Alembic
`identity_login_throttle_v3` aplicada pelo controlador existente. Configure as
variáveis comuns da tabela acima e use `DSGEOREF_IDENTITY_MODE=development`.
No JSON de segurança use `approved: false` e uma versão com prefixo
`development-`. A origem HTTPS deve usar loopback e corresponder à porta do
frontend.

- `DSGEOREF_IDENTITY_THROTTLE_PROFILE` aponta para um JSON com `version`
  (prefixo `development-`), `limit_after`, `lock_after`, `window_seconds`,
  `cooldown_seconds` e `lock_seconds`. Use inteiros positivos e configure o
  limiar de limitação abaixo do limiar de bloqueio e o cooldown abaixo da
  duração do bloqueio e da janela.
- `DSGEOREF_IDENTITY_THROTTLE_KEY_HEX` contém um segredo estável com pelo menos
  32 bytes, distinto da chave de replay. Preserve a chave entre reinícios.

```sh
python -m uvicorn --factory --host 127.0.0.1 --no-proxy-headers --no-access-log \
  dsgeorref.contexts.identity_access.adapters.local_identity.asgi:create_development_app
```

Para montar a tela React no Vite, defina `DSGEOREF_IDENTITY_DEV_BACKEND`
como a origem HTTP do upstream em `127.0.0.1` e forneça os arquivos TLS locais
em `DSGEOREF_IDENTITY_DEV_TLS_KEY` e `DSGEOREF_IDENTITY_DEV_TLS_CERT`. Execute
`pnpm --dir src/frontend dev` e abra a origem HTTPS configurada.

O host que compõe o aplicativo fornece a autoridade de existência de projetos
pelo port `project_exists`, a autorização de bootstrap por
`installation_authorized` e o provedor OIDC com resolução do vínculo de
navegador pelo argumento `oidc`. As operações dependentes dessas capacidades
rejeitam a tentativa quando a capacidade está ausente. O teste
`test_epic_009_superficie` usa uma autoridade de projeto de teste e serviços
BC-002 com PostgreSQL real. A suíte também valida React e o SDK contra o
upstream FastAPI pelo proxy HTTPS.

Os parâmetros dessa configuração destinam-se ao desenvolvimento. O gate de
produção da #816 continua pendente. Para rollback da funcionalidade, retire o
upstream de desenvolvimento. A migration recusa downgrade se houver estado
ou evidência de throttling persistidos.
