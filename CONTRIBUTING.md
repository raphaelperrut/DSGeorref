# Contribuição

## Durante a incubação privada

O desenvolvimento é conduzido pelo mantenedor único. O fluxo de trabalho permanece rastreável mesmo sem equipe:

1. selecionar uma issue ou épico;
2. criar branch curta vinculada ao identificador;
3. registrar plano, riscos, testes e rollback;
4. implementar a menor mudança coerente;
5. executar checks e anexar evidências;
6. revisar o diff com Codex e, para mudanças críticas, buscar revisão humana externa quando disponível;
7. integrar somente após critérios de aceite satisfeitos.

Commits devem ser claros e vinculados à issue. Conventional Commits é recomendado, não substitui rastreabilidade.

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
python -X utf8 tools/governance/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/foundation_validation.py --commit-range <base>..<head>
```

## Após a publicação

Quando o repositório for aberto, pull requests externos exigirão `Signed-off-by` conforme DCO 1.1, `inbound=outbound`, SPDX/REUSE e provenance verificável. Durante a incubação privada, contribuições externas permanecem fechadas pelo gate de publicação.
