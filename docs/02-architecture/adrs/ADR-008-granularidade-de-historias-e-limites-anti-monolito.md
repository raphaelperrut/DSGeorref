# ADR-008 — Granularidade de histórias e limites anti-monólito

- **Status:** `Accepted`
- **Baseline:** `SAR v2.8 — Fase E`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-008`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-001` — Governança de Engenharia e Entrega

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão. Ela substitui agrupamentos amplos da baseline anterior e possui responsabilidade normativa exclusiva sobre o boundary descrito no título.

## Decisão

- Uma história implementável possui no máximo 10 requisitos, um resultado verificável e um write scope principal.
- Contrato, implementação, migração, UI e operação são separados quando verificáveis independentemente.
- Arquivos acima de 400 linhas, funções acima de 60 e classes acima dos limites soft exigem design review; limites hard bloqueiam CI.
- Histórias amplas são decompostas em slices e uma consolidação sem novos requisitos de produto.

## Invariantes

- nenhuma implementação pode criar uma segunda autoridade para este boundary;
- parâmetros quantitativos permanecem em Application Profiles ou Benchmark Profiles;
- detalhes locais e reversíveis pertencem a issues, contratos ou código;
- contradição entre esta ADR e outro artifact interrompe a execução até reconciliação pelo Arquiteto.

## Alternativas consideradas

- manter a decisão agregada em uma ADR ampla: rejeitado por ocultar drivers, trade-offs e owners independentes;
- delegar a escolha à implementação: rejeitado por permitir divergência entre agentes e superfícies;
- transformar parâmetros reversíveis em ADR: rejeitado; profiles e benchmarks continuam sendo os owners desses valores.

## Racional da seleção

A opção selecionada reduz ambiguidade, limita o espaço de inferência dos agentes, permite auditoria independente e mantém um único owner normativo para uma decisão material.

## Consequências e trade-offs

- aumenta o número de ADRs e a disciplina de rastreabilidade;
- reduz o tamanho de cada contexto decisório e o risco de implementações redundantes;
- mudanças futuras precisam identificar exatamente qual boundary será substituído;
- integração entre decisões ocorre somente pelas dependências declaradas abaixo.

## Dependências arquiteturais

`ADR-006`, `ADR-007`

## Gate de mudança

Mudança que altere a autoridade, tecnologia estrutural, formato público, trust boundary, modelo de consistência ou direção de dependências deste boundary exige ADR substituta. Ajustes compatíveis e reversíveis seguem profiles, contratos e issues.

## Verificação de conformidade

- validators devem confirmar referência a IDs existentes e sequência contínua;
- histórias e TaskEnvelopes devem listar esta ADR quando modificarem o boundary;
- contratos, migrations, testes e evidence aplicáveis devem ser versionados no mesmo commit candidato;
- nenhuma decisão aberta pode ser completada por inferência do implementador.

## Rastreabilidade SAR

- **Requisitos owned:** `REQ-ISS-001`, `REQ-ISS-002`, `REQ-ISS-003`, `REQ-ISS-007`, `REQ-ISS-009`, `REQ-SPRINT-001-001`, `REQ-SPRINT-001-002`, `REQ-SPRINT-001-003`, `REQ-SPRINT-001-004`, `REQ-SPRINT-001-006`, `REQ-SPRINT-001-007`, `REQ-SPRINT-001-008`, `REQ-SPRINT-001-009`
- **Épicos relacionados:** `EPIC-001`, `EPIC-002`, `EPIC-005`, `EPIC-086`, `EPIC-091`, `EPIC-110`
- **Matriz canônica:** `docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv`
- **Grafo de decisões:** `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`
- **Revisão:** `docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.md`


## Especificações normativas — Fase E

Este boundary é concretizado por `SPEC-001`, `SPEC-004`. Texto, schemas, exemplos e validadores dessas especificações são obrigatórios. Divergência bloqueia implementação e exige reconciliação pelo Arquiteto.
