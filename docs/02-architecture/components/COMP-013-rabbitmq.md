# COMP-013 — RabbitMQ

- **Camada:** Persistência e transporte
- **ADRs owners:** ADR-036
- **Tecnologias principais:** RabbitMQ

## Responsabilidade

Transporte de work units; nunca fonte de verdade.

## Boundaries de contrato

- Consome `ack/redelivery` de `workers`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-010`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
