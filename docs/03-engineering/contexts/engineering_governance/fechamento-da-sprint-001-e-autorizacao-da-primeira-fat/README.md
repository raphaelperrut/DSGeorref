# Fundação executável do fechamento da SPRINT-001

Esta fundação consome, sem reinterpretar, o contrato congelado de fechamento da
SPRINT-001 e autorização da primeira fatia funcional. O registry liga os requisitos
e critérios da ISSUE-0676 a testes atribuíveis; o checkpoint liga esse control plane
ao comando executável.

## Comando reproduzível

O mesmo comando é executado localmente e pelo `make verify` da CI:

```text
python -X utf8 tools/governance/fechamento-da-sprint-001-e-autorizacao-da-primeira-fat/foundation_validation.py
```

O validador rejeita contrato, registry, checkpoint, teste ou integração de CI
ausente ou divergente. Evidência incompleta, malsucedida, conflitante ou ligada a
outro SHA permanece bloqueante, sem fallback silencioso.

## Limites

O resultado executável confirma que a fundação está pronta para revisão
independente; ele não concede autorização. A transição para
`AUTHORIZED_FOR_FIRST_FUNCTIONAL_SLICE` exige todas as evidências e aprovações
independentes ligadas ao mesmo SHA. Não há mudança de API, persistência, runtime de
produto ou migration. O rollback é reverter o commit antes do consumo downstream
ou publicar uma nova versão compatível do contrato.
