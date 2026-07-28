# ADR-055 — Audit ledger, privacidade, redaction e support bundles

- **Status:** `Accepted`
- **Baseline:** `SAR v2.8 — Fase E`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-055`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-014` — Operações, Auditoria e Suporte

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão. Ela substitui agrupamentos amplos da baseline anterior e possui responsabilidade normativa exclusiva sobre o boundary descrito no título.

## Decisão

- Audit é append-only, protegido e distinto de logs operacionais.
- Eventos auditáveis registram ator, ação, alvo, resultado, policy e correlação sem secret.
- Redaction usa allowlist estruturada e testes de vazamento.
- Support bundles são locais, sanitizados, allowlisted e produzidos inicialmente em dry-run.

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

`ADR-018`, `ADR-021`, `ADR-028`, `ADR-054`

## Gate de mudança

Mudança que altere a autoridade, tecnologia estrutural, formato público, trust boundary, modelo de consistência ou direção de dependências deste boundary exige ADR substituta. Ajustes compatíveis e reversíveis seguem profiles, contratos e issues.

## Verificação de conformidade

- validators devem confirmar referência a IDs existentes e sequência contínua;
- histórias e TaskEnvelopes devem listar esta ADR quando modificarem o boundary;
- contratos, migrations, testes e evidence aplicáveis devem ser versionados no mesmo commit candidato;
- nenhuma decisão aberta pode ser completada por inferência do implementador.

## Rastreabilidade SAR

- **Requisitos owned:** `REQ-ANC-007`, `REQ-AUD-001`, `REQ-AUTH-IMPL-001`, `REQ-AUTH-IMPL-009`, `REQ-EPIC-021`, `REQ-FS1-005`, `REQ-MCH-001`, `REQ-MSK-003`, `REQ-PRV-001`, `REQ-RUN-009`, `REQ-RUNTIME-009`
- **Épicos relacionados:** `EPIC-002`, `EPIC-004`, `EPIC-005`, `EPIC-008`, `EPIC-009`, `EPIC-010`, `EPIC-011`, `EPIC-012`, `EPIC-013`, `EPIC-014`, `EPIC-020`, `EPIC-021`, `EPIC-022`, `EPIC-023`, `EPIC-024`, `EPIC-026`, `EPIC-031`, `EPIC-032`, `EPIC-039`, `EPIC-041`, `EPIC-045`, `EPIC-050`, `EPIC-075`, `EPIC-076`, `EPIC-100`
- **Matriz canônica:** `docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv`
- **Grafo de decisões:** `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`
- **Revisão:** `docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.md`


## Especificações normativas — Fase E

Este boundary é concretizado por `SPEC-001`, `SPEC-005`. Texto, schemas, exemplos e validadores dessas especificações são obrigatórios. Divergência bloqueia implementação e exige reconciliação pelo Arquiteto.
