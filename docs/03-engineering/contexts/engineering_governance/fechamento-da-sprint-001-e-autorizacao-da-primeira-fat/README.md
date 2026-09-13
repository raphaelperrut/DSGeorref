# Fundação executável do fechamento da SPRINT-001

Esta fundação consome, sem reinterpretar, o contrato congelado de fechamento da
SPRINT-001 e autorização da primeira fatia funcional. O registry liga os requisitos
e critérios da ISSUE-0676 a testes atribuíveis; o checkpoint liga esse control plane
ao comando executável.

## Comando reproduzível

O mesmo gate é executado localmente e pelo `make verify` da CI:

```text
python -X utf8 -m pytest -q -p no:cacheprovider tests/fnd/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/test_sprint_001_foundation.py
```

O teste sentinela invoca o CLI com `--candidate-sha` e `--evidence`. O documento
de evidência contém o SHA candidato e um resultado por teste obrigatório. O
validador rejeita contrato, registry, checkpoint ou integração de CI divergente,
assim como evidência ausente, malsucedida, conflitante ou ligada a outro SHA, sem
fallback silencioso.

## Limites

O resultado executável confirma que a fundação está pronta para revisão
independente; ele não concede autorização. A transição para
`AUTHORIZED_FOR_FIRST_FUNCTIONAL_SLICE` exige todas as evidências e aprovações
independentes ligadas ao mesmo SHA. Não há mudança de API, persistência, runtime de
produto ou migration. O rollback é reverter o commit antes do consumo downstream
ou publicar uma nova versão compatível do contrato.
