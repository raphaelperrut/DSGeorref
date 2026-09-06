# Fundação de licenciamento, citação, contribuição e publicação

Esta fundação materializa o contrato versionado da ISSUE-0141 sem declarar o
repositório pronto para publicação. Ela fornece os textos integrais de licença,
metadados de citação, classificação SPDX/REUSE, notices, inventário direto de
dependências, política DCO e um checkpoint fail-closed do gate de publicação.

## Comando reproduzível

O comando local e o comando de CI são idênticos:

```text
py -3.12 -X utf8 tools/governance/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/foundation_validation.py
```

Para uma faixa de commits de contribuição externa, acrescente
`--commit-range <base>..<head>`. O verificador rejeita qualquer commit sem um
trailer `Signed-off-by` válido.

`--publication-gate` avalia o gate de distribuição. Na fundação 0.0.0 ele retorna
`BLOCKED`, porque SBOM do release candidate, revisão jurídica pré-G6 e os demais
gates compostos ainda não foram fornecidos. Ausência de evidência nunca vira PASS.

## Rastreabilidade dos critérios

- `AC-ISSUE-0142-01`: checkpoint, inventários, artefatos e saída JSON do verificador.
- `AC-ISSUE-0142-02`: requisitos declarados no checkpoint e exercitados pelos testes canônicos.
- `AC-ISSUE-0142-03`: licenças/arquivos desconhecidos, CFF inválido, dependência não inventariada,
  commit externo sem sign-off e evidência de publicação incompleta são rejeitados.
- `AC-ISSUE-0142-04`: `local_command`, `ci_command` e `reproducible_command` são o mesmo comando.

Não há mudança de persistência, migração, API ou runtime de produto. O rollback é
reverter estes artefatos antes de qualquer distribuição pública.
