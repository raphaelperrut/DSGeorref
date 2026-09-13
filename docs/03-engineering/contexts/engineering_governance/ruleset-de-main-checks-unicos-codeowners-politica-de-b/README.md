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

## Integração ao fluxo do repositório

O registry exige os contextos únicos `verify-foundation` e
`validate-main-ruleset-controls`. O segundo é produzido pelo workflow específico
do EPIC-091 e executa tanto a automação fail-closed quanto
`test_epic_091_integracao`. O checkpoint `integration-checkpoint.json` liga os
requisitos e os quatro critérios da ISSUE-0673 a essa prova executável.

## Bypass auditado

O bypass permanece rejeitado por padrão. Para validar um registro, os três
argumentos devem ser fornecidos juntos: `--bypass-record`, `--candidate-sha` e
`--delivery-approval-verdict-ref`. O registro só é aceito quando contém todos os
campos congelados, referencia o ruleset e a branch corretos, está ligado ao SHA
exato e referencia o mesmo veredito da autoridade de aprovação. Evidência ausente,
parcial ou stale termina com código diferente de zero.

## Limites

A fundação não altera persistência, API ou runtime de produto e não substitui a
aprovação independente. A integração versiona o estado desejado e seus produtores,
mas não afirma aplicação remota do ruleset nem enforcement ao vivo. O rollback é a
reversão do commit antes do consumo downstream.
