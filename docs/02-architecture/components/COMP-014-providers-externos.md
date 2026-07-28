# COMP-014 — Providers externos

- **Camada:** Integrações externas
- **ADRs owners:** ADR-047
- **Tecnologias principais:** STAC / APIs oficiais

## Responsabilidade

Busca e aquisição gratuita, guiada, allowlisted e license-governed.

## Boundaries de contrato

- Consome `gateway governado` de `geo`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-005`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
