# ADR-040 — Progresso, event ledger, replay e ETA

- **Status:** `Accepted`
- **Baseline:** `SAR v2.8 — Fase E`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-040`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-010` — Orquestração de Jobs e Recursos, `BC-014` — Operações, Auditoria e Suporte

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão. Ela substitui agrupamentos amplos da baseline anterior e possui responsabilidade normativa exclusiva sobre o boundary descrito no título.

## Decisão

- Progresso é persistido por work units, tipado e monotônico.
- ETA é apresentada com confiança e pode ser desconhecida sem inventar precisão.
- Event ledger permite replay offline e comparação por invariantes.
- Telemetria do Celery é derivada e não substitui o estado do produto.

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

`ADR-036`, `ADR-039`

## Gate de mudança

Mudança que altere a autoridade, tecnologia estrutural, formato público, trust boundary, modelo de consistência ou direção de dependências deste boundary exige ADR substituta. Ajustes compatíveis e reversíveis seguem profiles, contratos e issues.

## Verificação de conformidade

- validators devem confirmar referência a IDs existentes e sequência contínua;
- histórias e TaskEnvelopes devem listar esta ADR quando modificarem o boundary;
- contratos, migrations, testes e evidence aplicáveis devem ser versionados no mesmo commit candidato;
- nenhuma decisão aberta pode ser completada por inferência do implementador.

## Rastreabilidade SAR

- **Requisitos owned:** `REQ-ARTLAYOUT-006`, `REQ-BEX-009`, `REQ-FS1-003`, `REQ-GOV-ADR-003`, `REQ-ISM-001`, `REQ-ISS-004`, `REQ-MOS-002`, `REQ-MSK-002`, `REQ-MTD-001`, `REQ-NFR-001`, `REQ-RAS-005`, `REQ-REF-001`, `REQ-REF-002`, `REQ-RUN-002`, `REQ-RUN-004`, `REQ-RUN-006`, `REQ-RUN-007`, `REQ-SMO-002`
- **Épicos relacionados:** `EPIC-001`, `EPIC-002`, `EPIC-004`, `EPIC-005`, `EPIC-012`, `EPIC-014`, `EPIC-018`, `EPIC-019`, `EPIC-020`, `EPIC-021`, `EPIC-022`, `EPIC-023`, `EPIC-024`, `EPIC-026`, `EPIC-031`, `EPIC-032`, `EPIC-034`, `EPIC-037`, `EPIC-040`, `EPIC-045`, `EPIC-046`, `EPIC-048`, `EPIC-053`, `EPIC-055`, `EPIC-056`, `EPIC-065`, `EPIC-066`, `EPIC-067`, `EPIC-068`, `EPIC-069`, `EPIC-078`, `EPIC-097`, `EPIC-098`, `EPIC-110`
- **Matriz canônica:** `docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv`
- **Grafo de decisões:** `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`
- **Revisão:** `docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.md`
