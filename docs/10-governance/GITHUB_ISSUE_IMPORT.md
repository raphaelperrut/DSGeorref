# Importação controlada das issues do SAR para o GitHub

O script `tools/materialize_github_issues.py` lê o catálogo canônico do SAR e
materializa issues reais no GitHub sem transformar TaskEnvelopes em issues
duplicadas.

## Pré-requisitos

```powershell
gh auth login
gh auth status
```

Quando um GitHub Project for informado:

```powershell
gh auth refresh -s project
```

Execute os comandos na raiz do repositório.

## Segurança operacional

- O script é `dry-run` por padrão.
- Nenhuma escrita ocorre sem `--apply`.
- O mapa `.github/dsgeorref-materialization-map.json` torna a execução retomável.
- Issues existentes com prefixo `[ISSUE-0001]` são detectadas e não são recriadas.
- Épicos devem ser criados antes das histórias.
- Histórias são criadas como sub-issues do épico pai.
- Dependências são aplicadas em uma passagem separada e idempotente.

O mapa de materialização deve ser versionado no repositório. Ele registra apenas
IDs, números e URLs públicas para os colaboradores autorizados do repositório,
sem tokens ou secrets.

## Onda canário recomendada — SPRINT-001

Substitua `OWNER/DSGeorref` pelo repositório real.

### 1. Conferir os épicos sem escrever

```powershell
python tools/materialize_github_issues.py `
  --repo OWNER/DSGeorref `
  --sprint SPRINT-001 `
  --kind epics `
  --project-title "DSGeorref Engineering"
```

### 2. Criar os épicos

```powershell
python tools/materialize_github_issues.py `
  --repo OWNER/DSGeorref `
  --sprint SPRINT-001 `
  --kind epics `
  --project-title "DSGeorref Engineering" `
  --apply
```

### 3. Criar histórias em lotes de 25

```powershell
python tools/materialize_github_issues.py `
  --repo OWNER/DSGeorref `
  --sprint SPRINT-001 `
  --kind stories `
  --max-items 25 `
  --project-title "DSGeorref Engineering" `
  --apply
```

Repita o mesmo comando. A execução seguinte ignora as histórias já criadas e
materializa as próximas 25.

### 4. Aplicar dependências

Depois que todas as issues da sprint estiverem presentes:

```powershell
python tools/materialize_github_issues.py `
  --repo OWNER/DSGeorref `
  --sprint SPRINT-001 `
  --only-links `
  --link-dependencies `
  --apply
```

Dependências cross-sprint permanecem pendentes até a issue predecessora existir.
O comando pode ser repetido depois de cada nova sprint.

## Importar apenas um épico

```powershell
python tools/materialize_github_issues.py `
  --repo OWNER/DSGeorref `
  --epic EPIC-001 `
  --kind all `
  --project-title "DSGeorref Engineering" `
  --apply
```

## Milestone opcional

Para associar o lote a um milestone existente:

```powershell
--milestone "Internal"
```

Não use milestones para representar `SPRINT-001…SPRINT-012`; use o campo
`Planned Sprint` do Project.

## Issue types opcionais

Em uma GitHub Organization que já possua os tipos `Epic` e `Story`:

```powershell
--use-issue-types
```

Em repositório de conta pessoal, omita a flag e use o campo `Work Type` no
Project.

## Commit do mapa de materialização

Após cada onda:

```powershell
git add .github/dsgeorref-materialization-map.json
git commit -m "chore: record GitHub issue materialization"
git push
```

## Limites desta versão

O script:

- cria issues;
- cria a hierarquia épico → história;
- adiciona issues ao Project por título;
- associa milestone opcional;
- materializa dependências `blocked by`;
- preserva idempotência e retomada.

Os campos personalizados do Project (`Stable ID`, `Planned Sprint`, `Gate`,
`Bounded Context`, `Risk Tier` etc.) são preenchidos em uma segunda automação,
porque o GitHub exige IDs internos do Project, dos campos e das opções. Essa
segunda passagem deve ser configurada depois que os campos estiverem criados.
