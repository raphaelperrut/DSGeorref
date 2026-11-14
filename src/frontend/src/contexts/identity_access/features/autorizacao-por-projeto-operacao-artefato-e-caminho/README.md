# Autorização e membros do projeto

Entrypoint público: `mountProjectAccess(container)` / `ProjectAccessSurface`.
Página independente: `/src/contexts/identity_access/features/autorizacao-por-projeto-operacao-artefato-e-caminho/index.html` no servidor Vite do frontend.
O shell compartilhado permanece responsável pelo transporte gerado e pela composição.

Use `pnpm --dir src/frontend dev` na raiz do repositório. Para usar a API real,
reutilize o ambiente HTTPS/proxy de desenvolvimento já documentado na feature
`contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/README.md`.
Sem API configurada, erros ficam visíveis; a página não contém dados de demonstração
nem concede autorização offline. Bootstrap e recuperação de contas continuam na
superfície de identidade existente.

Consome exclusivamente `post_auth_session`, `get_authorization_check`,
`get_projects_projectid_members` e `post_projects_projectid_members` pelo SDK gerado.
O servidor decide permissões, existência de recursos e validade da sessão.
Consultar autorização não desbloqueia comandos nem produz um ticket reutilizável.
Não existe cache de decisão ou persistência no browser.

A política integrada não publica grant de artefato/caminho. A consulta transporta
apenas `action`, `resourceType` e `resourceId`; não acrescenta path, manifest,
endpoint, resolução física ou seletor lógico não publicado no HTTP. Valores
recusados pelo servidor permanecem recusados. A UI não implementa a matriz de papéis.
Listagem parcial é sinalizada; não se inventa parâmetro de paginação.

O vínculo envia `Idempotency-Key` e o CSRF da sessão. Reenvios sem edição preservam
a chave; edição ou sucesso confirmado inicia outra intenção. Persistência,
deduplicação, transação, validação de CSRF/Origin e auditoria pertencem ao servidor.
Sem confirmação, a UI não anuncia vínculo criado. HTTP status permanece visível
mesmo com JSON inválido; Problem Details válido é exibido com redaction de segredos.

Verificação, a partir da raiz:

```powershell
pnpm --dir src/frontend typecheck
pnpm --dir src/frontend exec vitest run src/contexts/identity_access/features/autorizacao-por-projeto-operacao-artefato-e-caminho/surface.test.tsx --environment jsdom
$accessDist = Join-Path $PWD 'node_modules/.cache/project-access-dist'
pnpm --dir src/frontend exec vite build src/contexts/identity_access/features/autorizacao-por-projeto-operacao-artefato-e-caminho --outDir $accessDist
pnpm --dir src/frontend exec playwright test --config src/contexts/identity_access/features/autorizacao-por-projeto-operacao-artefato-e-caminho/playwright.config.ts
```

`test_epic_010_superficie` é o teste obrigatório co-localizado. Os testes usam o
transporte gerado real com respostas HTTP controladas; não demonstram execução de
autorização/idempotência no PostgreSQL. O Chromium testa o bundle construído,
formulários, negativa, Problem Details, reenvio e viewport móvel. A captura fica
no output local do Playwright, fora dos artefatos versionados.
