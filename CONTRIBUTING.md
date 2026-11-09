# Contribuição

Siga a [governança](GOVERNANCE.md) e vincule o PR à issue. Commits devem ser claros e rastreáveis. Conventional Commits é recomendado.

## Certificação de origem (DCO 1.1)

O mecanismo aprovado é o [Developer Certificate of Origin 1.1](https://developercertificate.org/).
Cada contribuição externa deve conter, em todos os commits, um trailer no formato:

```text
Signed-off-by: Nome do Contribuidor <email@example.com>
```

Use `git commit -s` para acrescentar o trailer. O sign-off certifica a origem nos
termos do DCO 1.1; não é apenas uma identificação do autor. Commits externos sem
sign-off válido são rejeitados, inclusive quando produzidos por automação.

O projeto adota `inbound=outbound`: a contribuição entra sob a mesma licença que
governa a classe de arquivo declarada em `.reuse/dep5`. CLA não é exigido na
baseline inicial. Introduzir CLA exige decisão jurídica específica e não pode ser
usado como fallback para DCO ausente.

O repositório privado permanece fechado a contribuições externas até o gate de
publicação. Quando uma faixa de commits externa estiver sob avaliação, o mesmo
comando reproduzível deve ser usado localmente e em CI:

```text
python -X utf8 tools/governance/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/foundation_validation.py --technical --commit-range <base>..<head>
```

## Após a publicação

Quando o repositório for aberto, pull requests externos exigirão `Signed-off-by` conforme DCO 1.1, `inbound=outbound`, SPDX/REUSE e provenance verificável. Durante a incubação privada, contribuições externas permanecem fechadas pelo gate de publicação.
