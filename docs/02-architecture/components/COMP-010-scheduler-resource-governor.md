# COMP-010 — Scheduler + Resource Governor

- **Camada:** Execução e orquestração
- **ADRs owners:** ADR-039, ADR-054
- **Tecnologias principais:** PostgreSQL leases, Class-aware scheduling

## Responsabilidade

Fairness, backpressure, leases, fencing, quotas e budgets de CPU/RAM/GPU/disco.

## Boundaries de contrato

- Produz `admission/fairness/resources` para `workers`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-010`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
