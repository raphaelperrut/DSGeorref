# COMP-002 — Web UI

- **Camada:** Interfaces e superfícies
- **ADRs owners:** ADR-002, ADR-028, ADR-048
- **Tecnologias principais:** React, TypeScript, Vite, OpenLayers

## Responsabilidade

Experiência guiada, workspace cartográfico, triagem e revisão.

## Boundaries de contrato

- Produz `REST/SSE/polling` para `api`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-016`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
