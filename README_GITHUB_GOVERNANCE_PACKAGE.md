# DSGeorref GitHub Governance Package v3.1.0

Pacote de materialização e hardening para o repositório `raphaelperrut/DSGeorref` e o Project central.

## Escopo

Este pacote contém cinco utilitários principais:

1. `sync_project_fields.py` — cria/valida campos personalizados e preenche as issues já materializadas.
2. `sync_labels.py` — cria ou atualiza a taxonomia controlada de labels.
3. `sync_milestones.py` — cria/atualiza milestones e associa issues conforme o mapa sprint → milestone.
4. `configure_project_automations.py` — audita workflows built-in e orienta a configuração manual.
5. `enable_native_fields.py` — audita a visibilidade de `Parent issue` e `Sub-issue progress` por view e gera a ação manual exata.

Também inclui:

- `bootstrap_github_governance.ps1` para executar o fluxo completo;
- templates endurecidos de CODEOWNERS, Issue Forms, PR e Dependabot;
- guia detalhado de hardening do repositório.

## Limites explícitos da API

Dois pontos não podem ser integralmente escritos pela API pública atual do GitHub Projects:

- criação/edição dos workflows built-in do Project;
- alteração dos campos visíveis em cada Project view.

Por isso, os scripts correspondentes fazem auditoria e imprimem o procedimento manual restante. Eles não simulam sucesso remoto inexistente.

## Pré-requisitos

Na raiz do repositório:

```powershell
gh auth login
gh auth refresh -s project -s repo
gh auth status
python --version
```

Use Python 3.12 e uma versão recente do GitHub CLI.

Descubra o número do Project:

```powershell
gh project list --owner raphaelperrut
```

O número é o valor mostrado na coluna `NUMBER` e também aparece na URL do Project.

## Instalação

Extraia o conteúdo deste ZIP na raiz do DSGeorref. Depois confira:

```powershell
Get-ChildItem tools/github
Get-ChildItem config/github
```

Os scripts usam apenas a biblioteca padrão do Python e `gh`.

## 1. Preencher os campos das 166 issues de SPRINT-001 e SPRINT-002

### Dry-run

Substitua `N` pelo número real do Project:

```powershell
python tools/github/sync_project_fields.py `
  --repo raphaelperrut/DSGeorref `
  --owner raphaelperrut `
  --owner-type user `
  --project-number N `
  --sprint SPRINT-001 `
  --sprint SPRINT-002 `
  --create-missing-fields `
  --add-missing-items
```

### Aplicação em lotes de 25

```powershell
python tools/github/sync_project_fields.py `
  --repo raphaelperrut/DSGeorref `
  --owner raphaelperrut `
  --owner-type user `
  --project-number N `
  --sprint SPRINT-001 `
  --sprint SPRINT-002 `
  --create-missing-fields `
  --add-missing-items `
  --max-items 25 `
  --apply
```

Repita até aparecer:

```text
Pending field sync in this batch: 0
```

O script preenche, quando houver fonte canônica:

- Stable ID;
- Work Type;
- Planned Sprint;
- Gate;
- Bounded Context;
- Owner Role;
- Risk Tier;
- ADR IDs;
- TaskEnvelope;
- Status.

`Priority` e `Size` não são inferidos. Preencha-os em:

```text
config/github/project_field_overrides.csv
```

Exemplo:

```csv
issue_id,priority,size
ISSUE-0001,P0,L
ISSUE-0111,P1,M
```

Depois reexecute com `--force --apply` para os itens alterados. Para evitar reescrever todos, você também pode remover somente os IDs afetados de `.github/dsgeorref-project-field-sync.json`.

Quando um épico possui mais de um gate, como `G0/G1`, o campo single-select recebe o maior gate, interpretado como gate de saída.

## 2. Criar ou atualizar labels

Dry-run:

```powershell
python tools/github/sync_labels.py `
  --repo raphaelperrut/DSGeorref
```

Aplicar:

```powershell
python tools/github/sync_labels.py `
  --repo raphaelperrut/DSGeorref `
  --apply
```

A taxonomia fica em `config/github/labels.json`.

## 3. Criar milestones e associar as 166 issues

O pacote associa somente `SPRINT-001` e `SPRINT-002` ao milestone `Internal`. As sprints posteriores não recebem milestone até existir uma decisão explícita de release.

Dry-run:

```powershell
python tools/github/sync_milestones.py `
  --repo raphaelperrut/DSGeorref `
  --sprint SPRINT-001 `
  --sprint SPRINT-002
```

Aplicar em lotes:

```powershell
python tools/github/sync_milestones.py `
  --repo raphaelperrut/DSGeorref `
  --sprint SPRINT-001 `
  --sprint SPRINT-002 `
  --max-items 25 `
  --apply
```

Repita até `Pending milestone associations: 0`.

Para ampliar a estratégia, edite `config/github/milestones.json` antes de importar sprints posteriores.

## 4. Auditar automações nativas do Project

Dry-run:

```powershell
python tools/github/configure_project_automations.py `
  --owner raphaelperrut `
  --owner-type user `
  --project-number N
```

Aplicar:

```powershell
python tools/github/configure_project_automations.py `
  --owner raphaelperrut `
  --owner-type user `
  --project-number N `
  --apply
```

Com `--apply`, o utilitário persiste somente o relatório
`evidence/github/project-workflows-audit.json`. Ele não altera workflows nem
repository variables.

### Workflows built-in ainda manuais

No Project:

```text
Project → … → Workflows
```

Ative e configure:

1. Item added to project → `Status = Backlog`.
2. Issue closed → `Status = Done`.
3. Issue reopened → `Status = Backlog`.
4. Status changed to Done → close issue.
5. Auto-add para novas issues do repositório `raphaelperrut/DSGeorref`.
6. Auto-archive para itens concluídos após o período de retenção escolhido.

Evite configurar dois workflows built-in para executar exatamente a mesma transição.

## 5. Auditar e habilitar campos nativos por view

```powershell
python tools/github/enable_native_fields.py `
  --owner raphaelperrut `
  --owner-type user `
  --project-number N `
  --apply
```

O script grava:

```text
evidence/github/native-fields-audit.json
```

Para cada view marcada como incompleta:

1. abra a view em formato `Table`;
2. clique no `+` da última coluna;
3. abra `Hidden fields`;
4. marque `Parent issue` e `Sub-issue progress`;
5. salve a view.

## Execução agregada

Dry-run completo:

```powershell
powershell -ExecutionPolicy Bypass -File tools/github/bootstrap_github_governance.ps1 `
  -ProjectNumber N
```

Aplicação completa:

```powershell
powershell -ExecutionPolicy Bypass -File tools/github/bootstrap_github_governance.ps1 `
  -ProjectNumber N `
  -Apply
```

O bootstrap não executa os cliques manuais do Project.

## Instalar os templates de governança

Revise primeiro:

```powershell
Get-Content templates/.github/CODEOWNERS
Get-Content templates/.github/dependabot.yml
Get-Content templates/.github/pull_request_template.md
```

Depois copie:

```powershell
Copy-Item templates/.github/CODEOWNERS .github/CODEOWNERS -Force
Copy-Item templates/.github/dependabot.yml .github/dependabot.yml -Force
Copy-Item templates/.github/pull_request_template.md .github/pull_request_template.md -Force
Copy-Item templates/.github/ISSUE_TEMPLATE/* .github/ISSUE_TEMPLATE/ -Force
```

O CODEOWNERS inicial usa somente `@raphaelperrut`. Não habilite aprovação obrigatória de Code Owner sem um segundo revisor ou um bypass de emergência documentado, pois o autor não pode aprovar o próprio pull request.

## Arquivos de checkpoint que devem ser versionados

Após aplicar as sincronizações, inclua no Git:

```text
.github/dsgeorref-materialization-map.json
.github/dsgeorref-project-field-sync.json
.github/dsgeorref-milestone-sync.json
```

Também podem ser versionados:

```text
evidence/github/project-workflows-audit.json
evidence/github/native-fields-audit.json
```

Esses arquivos não contêm tokens. Eles registram o estado materializado, permitem retomada e impedem reprocessamento desnecessário.

```powershell
git add tools/github config/github docs/10-governance templates `
  .github/dsgeorref-materialization-map.json `
  .github/dsgeorref-project-field-sync.json `
  .github/dsgeorref-milestone-sync.json `
  evidence/github

git commit -m "chore: configure GitHub governance and project synchronization"
git push
```

## Hardening do repositório

Siga o documento:

```text
docs/10-governance/GITHUB_REPOSITORY_HARDENING_GUIDE.md
```
