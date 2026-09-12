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

## Limites, migração e rollback

- A autoridade permanece no contrato e nos arquivos versionados; a UI do
  GitHub é apenas uma projeção derivada.
- Não há endpoint, persistência, broker ou alteração de runtime do produto.
- Migração de dados não se aplica. Rollback é a reversão do commit candidato
  antes de consumo downstream.
- QA e Reviewer independentes ainda devem validar o mesmo SHA candidato.
