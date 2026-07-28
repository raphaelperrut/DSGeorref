# COMP-007 — IA governada

- **Camada:** Núcleo de domínio e processamento
- **ADRs owners:** ADR-051, ADR-053
- **Tecnologias principais:** ModelRunner, ModelPack

## Responsabilidade

Escalonamento opcional, ModelRunner e ModelPacks assinados sem bypass do SGV.

## Boundaries de contrato

- Produz `mesma aceitação independente` para `sgv`.
- Consome `escalona quando elegível` de `geo`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-009`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
