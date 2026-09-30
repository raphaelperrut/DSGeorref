# Handoff — ISSUE-0796 / integração do EPIC-110

## Baseline e incremento

`STORY-0684` está presente pelo commit candidato de consolidação
`a409ef45232d04283ac4cf5a7d71c6f4606342e5`. `STORY-0685` está presente pelo
commit de hardening `c1f46422db4ab430adcac7faaf870f6f18af76e6`, integrado pelo merge da PR
#1000. Ambos são ancestrais do `HEAD` candidato.

O incremento adiciona somente o sentinela executável `test_epic_110_integracao`.
Ele chama a consolidação existente da `STORY-0684` e o validador read-only da
`STORY-0685`; nenhuma regra normativa é copiada. O control plane permanece em
`tools/governance` e `tools/quality`, sem import ou alteração em runtime de
produto.

## Critérios de aceitação

- `AC-ISSUE-0796-01`: o teste obrigatório observa, no mesmo checkout, ancestry,
  consolidação e o relatório `PASS` do validador.
- `AC-ISSUE-0796-02`: a evidence versionada vincula os quatro ACs ao teste, aos
  commits predecessores e aos arquivos do candidato.
- `AC-ISSUE-0796-03`: o sentinela valida `FAIL_CLOSED`, `READ_ONLY`, ausência de
  ações destrutivas e rejeição determinística de repository root sem inputs, sem
  fallback silencioso ou escrita.
- `AC-ISSUE-0796-04`: a regra continua nos predecessores; o incremento somente os
  orquestra. Como nenhum módulo de produção ou import entre os dois packages foi
  criado, o diff não introduz dependência cíclica relevante.

## Contratos, migration e rollback

Impacto contratual: `NONE`. O contrato congelado e os manifests existentes são
somente lidos; não há mudança de ADR, schema, API, evento, estado ou regra de
produto.

Migration/rollback: `NOT_APPLICABLE`. Não há estado persistido, artifact de
runtime ou deployment alterado. Antes de consumo, rollback é o revert normal do
commit candidato, sem ação de dados.

## Limitações e riscos residuais

- O sentinela cobre o control plane versionado e não executa mutação remota no
  GitHub nem operação runtime.
- QA e Reviewer independentes ainda devem validar o mesmo SHA candidato; este
  handoff não declara autoaprovação.
- Nenhum prerequisite novo foi criado e nenhuma stop condition permanece aberta.
