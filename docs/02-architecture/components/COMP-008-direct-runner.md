# COMP-008 — Direct Runner

- **Camada:** Execução e orquestração
- **ADRs owners:** ADR-002, ADR-036
- **Tecnologias principais:** Python process

## Responsabilidade

Execução síncrona sobre o mesmo núcleo.

## Boundaries de contrato

- Consome `execução síncrona` de `domain`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-010`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
