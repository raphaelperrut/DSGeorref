# Fundação executável de Issue Forms

Esta fundação materializa o contrato congelado da `STORY-0555` como quatro
GitHub Issue Forms: `BUG`, `SPIKE`, `STORY` e `TASK`. O registry versionado liga
cada campo lógico do contrato ao `id` correspondente no form sem alterar o
contrato público nem criar estado de produto.

O mesmo comando offline é usado localmente e no workflow de CI:

```text
python tools/governance/issue-forms-templates-e-taxonomia-de-tipos-com-validac/validate_issue_forms.py --repository-root .
```

O validador é read-only e emite JSON determinístico. Form desconhecido, drift
da taxonomia, campo obrigatório ausente, `validations.required` diferente de
`true`, issue em branco habilitada, rota privada de segurança ausente ou
TaskEnvelope divergente geram findings estáveis e exit code não zero, sem
fallback silencioso.

## Integração no repositório

O ponto de integração da `ISSUE-0668` compõe a fundação e a automação já
versionadas sem importar ou duplicar suas regras:

```text
python tools/governance/issue-forms-templates-e-taxonomia-de-tipos-com-validac/repository_integration.py --repository-root .
```

O runner executa ambos os predecessores em subprocessos read-only, exige seus
relatórios JSON completos e falha fechado diante de erro, timeout, saída
malformada, modo permissivo ou drift do `TASK-0558`. O teste canônico é
`test_epic_090_integracao`.

## Limites, migração e rollback

- A autoridade permanece no contrato e nos arquivos versionados; a UI do
  GitHub é apenas uma projeção derivada.
- Não há endpoint, persistência, broker ou alteração de runtime do produto.
- Migração de dados não se aplica. Rollback é a reversão do commit candidato
  antes de consumo downstream.
- A integração não assume ownership das regras de taxonomia ou automação; os
  validadores das `ISSUE-0666` e `ISSUE-0667` continuam autoritativos.
- QA e Reviewer independentes ainda devem validar o mesmo SHA candidato.
