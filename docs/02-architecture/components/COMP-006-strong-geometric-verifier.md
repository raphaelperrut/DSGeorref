# COMP-006 — Strong Geometric Verifier

- **Camada:** Núcleo de domínio e processamento
- **ADRs owners:** ADR-046, ADR-053
- **Tecnologias principais:** SGVProfile, QualityProfile

## Responsabilidade

Aceitação fail-closed, métricas geométricas e Image Deformation Profile.

## Boundaries de contrato

- Consome `submete candidatos` de `geo`.
- Consome `mesma aceitação independente` de `ai`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-007`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
