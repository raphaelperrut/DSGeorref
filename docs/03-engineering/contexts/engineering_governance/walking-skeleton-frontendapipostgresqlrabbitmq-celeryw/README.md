# Integração do walking skeleton

O entry point de integração da `ISSUE-0647` compõe os dois controles já
publicados pelos predecessores sem importar nem reimplementar suas regras:

```text
python tools/governance/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/repository_integration.py --repository-root .
```

O processo executa em subprocesso isolado o checkpoint de consolidação da
`STORY-0535` e o validador automatizado em modo `DRY_RUN` da `STORY-0536`.
O relatório JSON determinístico torna observável o fluxo
`FRONTEND → API → POSTGRESQL → RABBITMQ_CELERY → WORKER → DIAGNOSTIC_ARTIFACT`
e vincula os quatro critérios da issue e os 14 requisitos do épico ao teste
`test_epic_086_integracao`.

Falha, timeout, saída malformada, mutação declarada, escrita de output ou drift
do TaskEnvelope produz finding estável e exit code não zero. Não existe
fallback silencioso nem promoção de artefato em caso de erro.

## Limites, persistência e rollback

Esta mudança integra checkpoints versionados e não altera contrato congelado,
frontend, API, schema PostgreSQL, mensagem RabbitMQ/Celery, worker ou estado
persistido. Migration e rollback de dados não se aplicam; o rollback da
integração é a reversão do commit candidato antes de consumo downstream.
PostgreSQL permanece autoritativo para estado e RabbitMQ/Celery permanece
somente transporte. QA e Reviewer independentes ainda devem validar o mesmo
SHA candidato; esta implementação não reivindica aprovação.
