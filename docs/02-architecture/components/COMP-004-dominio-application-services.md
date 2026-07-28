# COMP-004 — Domínio + Application Services

- **Camada:** Núcleo de domínio e processamento
- **ADRs owners:** ADR-002, ADR-026
- **Tecnologias principais:** Python 3.12+, Monólito modular

## Responsabilidade

Regras de negócio únicas, ports, UoW, ProcessingPlan e erros tipados.

## Boundaries de contrato

- Produz `orquestra ProcessingPlan` para `geo`.
- Produz `execução síncrona` para `direct`.
- Produz `work units` para `workers`.
- Produz `UoW/system of record` para `postgres`.
- Produz `ArtifactSets/inputs` para `filesystem`.
- Consome `invoca` de `cli`.
- Consome `adapta contratos` de `api`.

## Regras de implementação

- Entradas e saídas públicas devem possuir contratos versionados.
- Regras de domínio devem permanecer no núcleo compartilhado da aplicação.
- Mudanças exigem testes do componente e os gates vinculados às ADRs owners.
- A issue e o TaskEnvelope atribuídos definem os paths graváveis exatos.

## Domain-Driven Design — Fase C

- Este é um componente técnico, não uma fronteira semântica.
- **Contexts servidos:** `BC-002`, `BC-003`, `BC-004`, `BC-010`, `BC-011`, `BC-012`, `BC-013`.
- Nenhum aggregate ou state machine é compartilhado por este componente.
