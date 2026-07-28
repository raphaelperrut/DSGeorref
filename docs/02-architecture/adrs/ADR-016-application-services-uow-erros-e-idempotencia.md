# ADR-016 — Application services, Unit of Work, erros e idempotência

- **Status:** `Accepted`
- **Baseline:** `SAR v2.8 — Fase E`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-016`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-004` — Plano de Processamento e Workflow

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão. Ela substitui agrupamentos amplos da baseline anterior e possui responsabilidade normativa exclusiva sobre o boundary descrito no título.

## Decisão

- Comandos são coordenados por application services com Unit of Work explícita.
- Erros de domínio são tipados e mapeados para Problem Details versionado.
- Mutações repetíveis usam idempotency key persistida; concorrência usa revision precondition ou lock explícito.
- Transação de banco termina antes de efeitos externos, que são coordenados pelo outbox.

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

`ADR-005`, `ADR-018`, `ADR-020`

## Gate de mudança

Mudança que altere a autoridade, tecnologia estrutural, formato público, trust boundary, modelo de consistência ou direção de dependências deste boundary exige ADR substituta. Ajustes compatíveis e reversíveis seguem profiles, contratos e issues.

## Verificação de conformidade

- validators devem confirmar referência a IDs existentes e sequência contínua;
- histórias e TaskEnvelopes devem listar esta ADR quando modificarem o boundary;
- contratos, migrations, testes e evidence aplicáveis devem ser versionados no mesmo commit candidato;
- nenhuma decisão aberta pode ser completada por inferência do implementador.

## Rastreabilidade SAR

- **Requisitos owned:** `REQ-EPIC-014`, `REQ-GC-001`, `REQ-INS-001`, `REQ-ISM-006`, `REQ-ISS-006`, `REQ-PLN-001`, `REQ-PLN-003`, `REQ-PLN-004`, `REQ-PLN-006`, `REQ-PLN-007`, `REQ-PLN-008`, `REQ-PLN-010`, `REQ-PRM-006`
- **Épicos relacionados:** `EPIC-002`, `EPIC-014`, `EPIC-016`, `EPIC-073`, `EPIC-074`, `EPIC-081`, `EPIC-091`, `EPIC-108`, `EPIC-110`
- **Matriz canônica:** `docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv`
- **Grafo de decisões:** `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`
- **Revisão:** `docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.md`
