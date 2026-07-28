# COMP-009 — Workers duráveis

- **Camada:** Execução e orquestração
- **ADRs owners:** ADR-036
- **Tecnologias principais:** Celery, RabbitMQ

## Responsabilidade

Work units, retry classificado, checkpoints, cancelamento e idempotência.

## Boundaries de contrato

- Produz `ack/redelivery` para `broker`.
- Produz `estado/checkpoints/outbox` para `postgres`.
- Consome `work units` de `domain`.
- Consome `admission/fairness/resources` de `scheduler`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-010`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
