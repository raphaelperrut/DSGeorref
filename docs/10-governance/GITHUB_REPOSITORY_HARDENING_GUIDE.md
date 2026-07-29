# GitHub Repository Hardening Guide — DSGeorref

## Objetivo

Configurar o repositório privado `raphaelperrut/DSGeorref` para impedir mudanças não revisadas, exigir CI, limitar permissões, proteger segredos e preparar releases/deployments sem bloquear indevidamente um mantenedor solo.

## 0. Pré-checagens

1. Confirme que `main` é a default branch.
2. Abra pelo menos um pull request de teste para que os checks de CI apareçam na seleção do ruleset.
3. Confirme que os workflows abaixo passaram ao menos uma vez:
   - `foundation-ci`, job `verify-foundation`;
   - `foundation-security`, job `secret-pattern-review`.
4. Verifique o plano da conta. Alguns controles em repositório privado, especialmente rulesets avançados, ambientes protegidos, secret scanning e push protection, dependem do plano disponível.

## 1. Ruleset recomendado para `main`

Caminho:

```text
Repository → Settings → Rules → Rulesets → New ruleset → New branch ruleset
```

Configure:

```text
Name: main-protection
Enforcement status: Active
Target branches: Default branch
```

### Regras obrigatórias

Ative:

- Restrict deletions;
- Require a pull request before merging;
- Require status checks to pass;
- Require conversation resolution before merging;
- Block force pushes;
- Require linear history, somente se o repositório usar squash/rebase e não merge commits.

Não habilite criação restrita da branch se isso interferir no bootstrap inicial. Depois que `main` existir e estiver estabilizada, a criação deixa de ser relevante.

### Configuração solo versus equipe

#### Modo solo inicial

Use:

```text
Required approvals: 0
Require pull request: enabled
Require conversation resolution: enabled
Required status checks: enabled
```

Isso ainda impede push direto e exige PR + CI, mas evita deadlock: o autor não pode aprovar o próprio PR.

#### Modo com segundo revisor

Quando houver colaborador/revisor real:

```text
Required approvals: 1
Dismiss stale pull request approvals: enabled
Require review from Code Owners: enabled
Require approval of the most recent reviewable push: enabled
```

Não habilite `Require review from Code Owners` com CODEOWNERS apontando somente para o próprio autor sem bypass, pois nenhum PR poderá satisfazer a aprovação.

### Status checks obrigatórios

Depois de um PR executar a CI, selecione os checks exatamente como aparecem na interface. Para a baseline atual, procure os jobs:

```text
verify-foundation
secret-pattern-review
```

Recomendação inicial:

- habilitar `Require branches to be up to date before merging` enquanto o volume de PRs for baixo;
- reavaliar quando o custo de reexecução da CI ficar alto;
- não tornar a automação de Project um check obrigatório de merge, pois ela não valida código.

### Bypass

Preferência:

```text
Bypass list: empty
```

Se o fluxo solo exigir recuperação emergencial, adicione somente o owner com bypass restrito e documente cada uso. Bypass não deve ser o caminho normal de merge.

## 2. Alternativa: branch protection clássica

Se `Rulesets` não estiver disponível no plano:

```text
Repository → Settings → Branches → Add branch protection rule
```

Branch name pattern:

```text
main
```

Ative os equivalentes:

- Require a pull request before merging;
- Require status checks to pass before merging;
- Require branches to be up to date before merging;
- Require conversation resolution before merging;
- Do not allow bypassing the above settings, somente quando houver processo viável;
- Allow force pushes: disabled;
- Allow deletions: disabled.

Use ruleset ou proteção clássica como autoridade principal; evite duas configurações contraditórias.

## 3. Revisão obrigatória antes de merge

A revisão obrigatória é parte da regra de PR.

Para trabalho solo:

- PR obrigatório;
- aprovação numérica igual a zero;
- CI obrigatória;
- conversas resolvidas;
- checklist do PR preenchido;
- evidência persistida.

Para equipe:

- uma aprovação mínima;
- aprovação de Code Owner nos caminhos críticos;
- invalidar aprovação quando novos commits forem enviados;
- exigir aprovação do commit mais recente por alguém diferente do autor.

## 4. CI obrigatória

Os workflows existentes são:

```text
.github/workflows/ci.yml
.github/workflows/security.yml
```

Antes de torná-los obrigatórios:

1. abra um PR de teste;
2. aguarde os dois jobs aparecerem e passarem;
3. volte ao ruleset;
4. adicione `verify-foundation` e `secret-pattern-review` aos checks exigidos;
5. salve;
6. confirme que o botão de merge fica bloqueado quando qualquer check falha.

Mantenha nomes de jobs estáveis. Renomear um job pode deixar o ruleset apontando para um check que não será mais produzido.

## 5. Bloqueio de force push e exclusão de `main`

No ruleset:

```text
Block force pushes: enabled
Restrict deletions: enabled
```

Na proteção clássica:

```text
Allow force pushes: disabled
Allow deletions: disabled
```

Teste com uma branch descartável; não tente validar force push diretamente contra `main` com trabalho não publicado.

## 6. Exclusão automática de branches após merge

Caminho:

```text
Repository → Settings → General → Pull Requests
```

Ative:

```text
Automatically delete head branches
```

Isso remove branches de feature após merge, sem excluir a default branch nem branches protegidas.

## 7. CODEOWNERS

Arquivo recomendado:

```text
.github/CODEOWNERS
```

O pacote inclui um modelo em:

```text
templates/.github/CODEOWNERS
```

Instalação:

```powershell
Copy-Item templates/.github/CODEOWNERS .github/CODEOWNERS -Force
```

O modelo atribui inicialmente todos os caminhos a `@raphaelperrut`. Quando existirem revisores, distribua ownership por domínio, por exemplo:

```text
/src/geo/ @geo-reviewer
/src/ai/ @ai-reviewer
/.github/ @platform-reviewer
/contracts/ @architecture-reviewer
```

Após adicionar revisores reais, habilite `Require review from Code Owners` no ruleset.

## 8. Templates de issue

Arquivos:

```text
.github/ISSUE_TEMPLATE/config.yml
.github/ISSUE_TEMPLATE/bug.yml
.github/ISSUE_TEMPLATE/story.yml
.github/ISSUE_TEMPLATE/spike.yml
.github/ISSUE_TEMPLATE/task.yml
```

O pacote fornece versões endurecidas em `templates/.github/ISSUE_TEMPLATE/`.

Copie após revisar:

```powershell
Copy-Item templates/.github/ISSUE_TEMPLATE/* .github/ISSUE_TEMPLATE/ -Force
```

Validação:

1. faça commit em uma branch;
2. abra `Issues → New issue`;
3. confirme que aparecem somente os formulários esperados;
4. confirme que blank issues estão desabilitadas;
5. confirme que o link de vulnerabilidade aponta para Security Advisories.

Não use labels para duplicar `Planned Sprint`, `Gate`, `Priority`, `Risk Tier` ou `Bounded Context`; esses dados pertencem aos campos estruturados do Project.

## 9. Template de pull request

Arquivo:

```text
.github/pull_request_template.md
```

Instale o modelo do pacote:

```powershell
Copy-Item templates/.github/pull_request_template.md .github/pull_request_template.md -Force
```

O template exige:

- Stable IDs e vínculo com issue/épico;
- objetivo e escopo;
- comandos de validação;
- evidências;
- análise de segurança, privacidade e compatibilidade;
- risco e rollback.

Abra um PR de teste e confirme que o corpo é carregado automaticamente.

## 10. Dependabot

Instale:

```powershell
Copy-Item templates/.github/dependabot.yml .github/dependabot.yml -Force
```

A configuração atual monitora:

- dependências Python no diretório raiz;
- versões de GitHub Actions.

Quando surgirem manifests adicionais, acrescente ecossistemas somente depois de o arquivo correspondente existir, por exemplo npm, Docker, Terraform ou Docker Compose.

Na interface:

```text
Repository → Settings → Security → Code security and analysis
```

Ative, quando disponíveis:

- Dependency graph;
- Dependabot alerts;
- Dependabot security updates.

Depois do commit de `.github/dependabot.yml`, confira:

```text
Insights → Dependency graph → Dependabot
```

Corrija qualquer erro de configuração antes de considerar o controle ativo.

## 11. Secret scanning e push protection

Caminho típico:

```text
Repository → Settings → Security → Code security and analysis
```

Quando o plano oferecer os recursos, ative:

- Secret scanning;
- Push protection.

Push protection deve bloquear o push quando detectar credenciais conhecidas. Um bypass, quando permitido, deve exigir justificativa e ser excepcional.

Controles complementares já existentes:

- `.gitignore` para arquivos locais;
- `.env.example` sem credenciais reais;
- workflow `foundation-security`;
- revisão de arquivos rastreados.

Nunca faça teste com uma credencial real. Use apenas padrões de teste oficialmente documentados ou valide o controle pela interface.

## 12. Environments de deployment

Não crie ambientes apenas para preencher a interface. Crie-os quando existir workflow real de deployment.

Sequência sugerida:

```text
internal
alpha
beta
production
```

Caminho:

```text
Repository → Settings → Environments → New environment
```

Para `internal`:

- branches permitidas: `main` ou tags internas conforme o workflow;
- secrets específicos do ambiente;
- sem aprovação obrigatória enquanto não houver segundo revisor, se isso bloquear o fluxo.

Para `production`:

- required reviewers reais;
- deployment branches/tags restritas;
- prevent self-review, quando houver equipe;
- secrets somente do ambiente;
- tempo de espera opcional;
- regras de proteção consistentes com a estratégia de release.

Não reutilize um único secret global para todos os ambientes quando os privilégios puderem ser separados.

## 13. Permissões do GitHub Actions

Caminho:

```text
Repository → Settings → Actions → General
```

### Actions permitidas

Use uma política restritiva compatível com os workflows atuais:

- permitir actions criadas pelo GitHub;
- permitir actions verificadas necessárias;
- adicionar explicitamente actions externas quando forem introduzidas;
- evitar `Allow all actions` sem necessidade.

A baseline usa:

```text
actions/checkout
actions/setup-python
```

### Workflow permissions

Defina:

```text
Read repository contents and packages permissions
```

Mantenha desabilitado:

```text
Allow GitHub Actions to create and approve pull requests
```

Ative essa permissão somente quando existir um workflow explicitamente aprovado que necessite abrir ou aprovar PRs.

Dentro de cada workflow, declare `permissions` mínimas. Para validação:

```yaml
permissions:
  contents: read
```

Para a automação do Project, o workflow usa um PAT guardado em `DSGEO_PROJECT_TOKEN`; o `GITHUB_TOKEN` permanece somente leitura para conteúdo e issues.

### Fork pull request workflows

Se o repositório se tornar público, exija aprovação para workflows originados de forks e nunca exponha secrets a código não confiável.

## 14. Validação final

Crie uma branch de teste:

```powershell
git switch -c chore/validate-github-governance
```

Faça uma alteração documental, commit e push. Abra um PR e confirme:

- push direto em `main` não é necessário nem permitido pelo fluxo;
- template do PR aparece;
- CI e security jobs executam;
- merge fica bloqueado enquanto checks falham;
- conversas não resolvidas bloqueiam merge;
- após merge, a branch é excluída automaticamente;
- a issue vinculada recebe `Done`;
- a issue aparece no Project;
- os campos canônicos estão preenchidos;
- nenhuma credencial apareceu em logs ou arquivos.

## 15. Evidência e versionamento

Versione as configurações declarativas:

```text
.github/CODEOWNERS
.github/dependabot.yml
.github/ISSUE_TEMPLATE/*
.github/pull_request_template.md
.github/workflows/*
config/github/*
tools/github/*
```

Versione também os checkpoints sem segredo:

```text
.github/dsgeorref-materialization-map.json
.github/dsgeorref-project-field-sync.json
.github/dsgeorref-milestone-sync.json
```

Não versione:

- PATs;
- arquivos `.env` reais;
- exports de secrets;
- logs contendo headers de autenticação;
- cópias locais de credenciais de deployment.
