# Fundação executável do ruleset de `main`

Esta fundação materializa o contrato congelado do EPIC-091 como control plane
versionado. O ruleset desejado, o registry de checks e o checkpoint permanecem
separados do runtime de produto e não declaram que a configuração já foi aplicada
no GitHub.

## Comando reproduzível

O comando local e o comando chamado por `make verify` em CI são idênticos:

```text
python -X utf8 tools/governance/ruleset-de-main-checks-unicos-codeowners-politica-de-b/foundation_validation.py
```

O validador rejeita contrato, ruleset, registry ou CODEOWNERS ausente ou divergente.
Um contexto obrigatório deve ter um único produtor em `.github/workflows`.

## Bypass auditado

O bypass permanece rejeitado por padrão. Para validar um registro, os três
argumentos devem ser fornecidos juntos: `--bypass-record`, `--candidate-sha` e
`--delivery-approval-verdict-ref`. O registro só é aceito quando contém todos os
campos congelados, referencia o ruleset e a branch corretos, está ligado ao SHA
exato e referencia o mesmo veredito da autoridade de aprovação. Evidência ausente,
parcial ou stale termina com código diferente de zero.

## Limites

A fundação não altera persistência, API ou runtime de produto e não substitui a
aprovação independente. A aplicação remota do ruleset e a observação de enforcement
ao vivo não são afirmadas por esta história. O rollback é a reversão do commit antes
do consumo downstream.
