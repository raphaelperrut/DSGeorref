# Boundary HTTP do BC-002

O entrypoint monta somente `DELETE /api/v1/auth/session`. Ele usa o contrato HTTP
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
